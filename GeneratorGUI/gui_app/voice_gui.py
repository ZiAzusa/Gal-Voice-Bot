import sys
import os
import signal
import asyncio
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QHBoxLayout, QLabel, QComboBox, QTextEdit, QPushButton,
                           QFileDialog, QLineEdit, QRadioButton, QButtonGroup,
                           QMessageBox, QCheckBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from VITS import Trans, Trans2
from VITS_GENSHIN import Trans_GS
from .katakana import chinese_to_katakana

class BotConnection():
    host = "127.0.0.1"
    port = 5700

    def _call_api(self, route, data=None, method='GET'):
        url = f"http://{self.host}:{self.port}/{route}"
        headers = {'Content-Type': 'application/json'}
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=data)
            else:
                response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            print(f"Called: {url} - {data} - {response.json()}")
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"API调用失败: {str(e)}")

    def _check_record(self, ):
        res = self._call_api('can_send_record')['data']['yes']
        return res

    def send_private_msg(self, user_id, message):
        if not self._check_record():
            raise RuntimeError("无法发送语音消息，可能是API限制或其他原因。")
        data = {
            'user_id': user_id,
            'message': message
        }
        res = self._call_api('send_private_msg', data)
        return res
    
    def send_group_msg(self, group_id, message):
        if not self._check_record():
            raise RuntimeError("无法发送语音消息，可能是API限制或其他原因。")
        data = {
            'group_id': group_id,
            'message': message
        }
        res = self._call_api('send_group_msg', data)
        return res


class SendMessageThread(QThread):
    finished = pyqtSignal(bool, str)

    def __init__(self, target_type, target_id, message):
        super().__init__()
        self.target_type = target_type
        self.target_id = target_id
        self.message = message

    def run(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._send_message())
        except Exception as e:
            self.finished.emit(False, f"发送失败: {str(e)}")

    async def _send_message(self):
        try:
            bot = BotConnection()
            if self.target_type == "private":
                res = bot.send_private_msg(user_id=self.target_id, message=self.message)
            else:
                res = bot.send_group_msg(group_id=self.target_id, message=self.message)
            if res['status'] != 'ok':
                raise RuntimeError(f"发送失败: {res.get('message', '未知错误')}")
            self.finished.emit(True, "发送成功")
        except Exception as e:
            self.finished.emit(False, f"发送失败: {str(e)}")

class VoiceGeneratorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gal Voice Generator")
        self.setGeometry(100, 100, 800, 600)
        
        # 设置关闭窗口时的处理
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        
        # 创建中心部件和主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 创建角色选择区域
        char_layout = QHBoxLayout()
        
        # 创建角色类型选择
        type_label = QLabel("角色类型:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["亚托莉（日语）", "柚子社（日语）", "原神（汉语）"])
        self.type_combo.currentTextChanged.connect(self.on_type_changed)
        
        # 创建具体角色选择
        char_label = QLabel("选择角色:")
        self.char_combo = QComboBox()
        
        char_layout.addWidget(type_label)
        char_layout.addWidget(self.type_combo)
        char_layout.addWidget(char_label)
        char_layout.addWidget(self.char_combo)
        layout.addLayout(char_layout)
        
        # 初始化角色列表
        self.update_character_list("亚托莉（日语）")
        
        # 创建文本输入区域
        text_label = QLabel("输入文本:")
        self.text_edit = QTextEdit()
        layout.addWidget(text_label)
        layout.addWidget(self.text_edit)
        
        # 添加片假名转换选项
        self.katakana_check = QCheckBox("中文转换为片假名（使用日语角色发送中文请勾选这个）")
        layout.addWidget(self.katakana_check)
        
        # 创建发送目标选择区域
        target_group = QWidget()
        target_layout = QVBoxLayout(target_group)
        
        # 创建单选按钮
        self.target_type_group = QButtonGroup()
        self.private_radio = QRadioButton("私聊")
        self.group_radio = QRadioButton("群聊")
        self.target_type_group.addButton(self.private_radio)
        self.target_type_group.addButton(self.group_radio)
        
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.private_radio)
        radio_layout.addWidget(self.group_radio)
        target_layout.addLayout(radio_layout)
        
        # 创建目标ID输入框
        target_id_layout = QHBoxLayout()
        self.target_id_label = QLabel("目标QQ号/群号:")
        self.target_id_input = QLineEdit()
        target_id_layout.addWidget(self.target_id_label)
        target_id_layout.addWidget(self.target_id_input)
        target_layout.addLayout(target_id_layout)
        
        layout.addWidget(target_group)
        
        # 创建按钮区域
        button_layout = QHBoxLayout()
        self.generate_btn = QPushButton("生成语音")
        self.generate_btn.clicked.connect(self.generate_voice)
        self.play_btn = QPushButton("播放")
        self.play_btn.clicked.connect(self.play_voice)
        self.send_btn = QPushButton("发送")
        self.send_btn.clicked.connect(self.send_voice)
        self.save_btn = QPushButton("保存")
        self.save_btn.clicked.connect(self.save_voice)
        
        button_layout.addWidget(self.generate_btn)
        button_layout.addWidget(self.play_btn)
        button_layout.addWidget(self.send_btn)
        button_layout.addWidget(self.save_btn)
        layout.addLayout(button_layout)
        
        # 状态标签
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)
        
        # 初始化时禁用相关按钮
        self.play_btn.setEnabled(False)
        self.send_btn.setEnabled(False)
        self.save_btn.setEnabled(False)
        
        # 设置默认选择
        self.private_radio.setChecked(True)
    
    def get_yozo_characters(self):
        return {"宁宁": 0, "爱瑠": 1, "芳乃": 2, "茉子": 3, "丛雨": 4, "小春": 5, "七海": 6}
    
    def get_genshin_characters(self):
        return {
            "派蒙": 0, "凯亚": 1, "安柏": 2, "丽莎": 3, "琴": 4, "香菱": 5, "枫原万叶": 6,
            "迪卢克": 7, "温迪": 8, "可莉": 9, "早柚": 10, "托马": 11, "芭芭拉": 12,
            "优菈": 13, "云堇": 14, "钟离": 15, "魈": 16, "凝光": 17, "雷电将军": 18,
            "北斗": 19, "甘雨": 20, "七七": 21, "刻晴": 22, "神里绫华": 23,
            "戴因斯雷布": 24, "雷泽": 25, "神里绫人": 26, "罗莎莉亚": 27, "阿贝多": 28,
            "八重神子": 29, "宵宫": 30, "荒泷一斗": 31, "九条裟罗": 32, "夜兰": 33,
            "珊瑚宫心海": 34, "五郎": 35, "散兵": 36, "女士": 37, "达达利亚": 38,
            "莫娜": 39, "班尼特": 40, "申鹤": 41, "行秋": 42, "烟绯": 43, "久岐忍": 44,
            "辛焱": 45, "砂糖": 46, "胡桃": 47, "重云": 48, "菲谢尔": 49, "诺艾尔": 50,
            "迪奥娜": 51, "鹿野院平藏": 52
        }
    
    def on_type_changed(self, type_name):
        self.update_character_list(type_name)
    
    def update_character_list(self, type_name):
        self.char_combo.clear()
        if type_name == "亚托莉（日语）":
            self.char_combo.addItem("亚托莉")
        elif type_name == "柚子社（日语）":
            self.char_combo.addItems(self.get_yozo_characters().keys())
        elif type_name == "原神（汉语）":
            self.char_combo.addItems(self.get_genshin_characters().keys())
    
    def generate_voice(self):
        text = self.text_edit.toPlainText()
        if not text:
            self.status_label.setText("请输入要生成的文本！")
            return
        
        # 如果选中了片假名转换，先转换文本
        if self.katakana_check.isChecked():
            try:
                text = chinese_to_katakana(text)
                self.text_edit.setText(text)
            except Exception as e:
                self.status_label.setText(f"片假名转换失败：{str(e)}")
                return
        
        type_name = self.type_combo.currentText()
        character = self.char_combo.currentText()
        
        try:
            if type_name == "亚托莉（日语）":
                Trans(text, 'voice.wav')
            elif type_name == "柚子社（日语）":
                yozo_dict = self.get_yozo_characters()
                Trans2(text, yozo_dict[character], 'voice.wav')
            elif type_name == "原神（汉语）":
                gs_dict = self.get_genshin_characters()
                Trans_GS(text, gs_dict[character], 'voice.wav')
            
            self.status_label.setText("语音生成成功！")
            self.play_btn.setEnabled(True)
            self.send_btn.setEnabled(True)
            self.save_btn.setEnabled(True)
        except Exception as e:
            self.status_label.setText(f"生成失败：{str(e)}")
    
    def play_voice(self):
        if not os.path.exists('voice.wav'):
            self.status_label.setText("语音文件不存在！")
            return
        
        try:
            from playsound import playsound
            playsound('voice.wav')
        except Exception as e:
            self.status_label.setText(f"播放失败：{str(e)}")

    def send_voice(self):
        target_id = self.target_id_input.text()
        if not target_id:
            QMessageBox.warning(self, "错误", "请输入目标ID！")
            return
            
        try:
            target_id = int(target_id)
        except ValueError:
            QMessageBox.warning(self, "错误", "目标ID必须是数字！")
            return
            
        target_type = "group" if self.group_radio.isChecked() else "private"
        
        # 构建语音文件的绝对路径
        voice_path = os.path.abspath('voice.wav')
        voice_url = f"file://{voice_path}"
        message = f"[CQ:record,file={voice_url}]"
        
        try:
            # 创建发送线程
            self.send_thread = SendMessageThread(target_type, target_id, message)
            self.send_thread.finished.connect(self.on_send_finished)
            self.send_btn.setEnabled(False)
            self.status_label.setText("正在发送...")
            self.send_thread.start()
        except Exception as e:
            self.status_label.setText(f"发送失败: {str(e)}")
            QMessageBox.warning(self, "错误", f"发送失败: {str(e)}")
    
    def on_send_finished(self, success, message):
        self.send_btn.setEnabled(True)
        self.status_label.setText(message)
        if success:
            QMessageBox.information(self, "成功", "语音消息发送成功！")
        else:
            QMessageBox.warning(self, "错误", message)
    
    def save_voice(self):
        if not os.path.exists('voice.wav'):
            self.status_label.setText("语音文件不存在！")
            return
        
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "保存语音文件",
                "",
                "Wave Files (*.wav)"
            )
            if filename:
                import shutil
                shutil.copy2('voice.wav', filename)
                self.status_label.setText(f"文件已保存至：{filename}")
        except Exception as e:
            self.status_label.setText(f"保存失败：{str(e)}")
    
    def closeEvent(self, event):
        try:
            os.kill(os.getpid(), signal.SIGINT)
        except Exception as e:
            print(f"关闭时出错：{str(e)}")
        event.accept()

def launch_gui():
    app = QApplication(sys.argv)
    window = VoiceGeneratorGUI()
    window.show()
    sys.exit(app.exec_())
