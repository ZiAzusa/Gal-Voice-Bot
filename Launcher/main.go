package main

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"sync"
	"syscall"
	"time"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/dialog"
	"fyne.io/fyne/v2/widget"
)

type ProcessManager struct {
	processes []*exec.Cmd
	mu        sync.Mutex
}

func NewProcessManager() *ProcessManager {
	return &ProcessManager{
		processes: make([]*exec.Cmd, 0),
	}
}

func (pm *ProcessManager) AddProcess(cmd *exec.Cmd) {
	pm.mu.Lock()
	defer pm.mu.Unlock()
	pm.processes = append(pm.processes, cmd)
}

func (pm *ProcessManager) KillAll() {
	pm.mu.Lock()
	defer pm.mu.Unlock()
	for _, process := range pm.processes {
		if process != nil && process.Process != nil {
			process.Process.Kill()
		}
	}
	// 清空进程列表
	pm.processes = pm.processes[:0]
}

func hideWindow(cmd *exec.Cmd) {
	cmd.SysProcAttr = &syscall.SysProcAttr{
		HideWindow: true,
	}
}

func main() {
	// 创建应用实例
	myApp := app.New()
	window := myApp.NewWindow("Gal-Voice 启动器")

	// 创建进程管理器
	pm := NewProcessManager()

	// 创建状态标签
	status := widget.NewLabel("准备就绪")
	status.Alignment = fyne.TextAlignCenter

	updateStatus := func(text string) {
		status.SetText(text)
	}

	// 创建启动按钮
	startButton := widget.NewButton("启动", func() {
		// 创建确认对话框
		confirmDialog := dialog.NewConfirm(
			"重要提示",
			"为了向QQ植入机器人程序，需要关闭当前正在运行的QQ再重新登录QQ，登录后的QQ将自动接入GalVoice。\n注意：如果继续，将自动退出当前登录的QQ\n是否继续？",
			func(ok bool) {
				if ok {
					go func() {
						// 首先执行 killQQ.bat
						updateStatus("正在关闭当前QQ...")
						killQQPath := filepath.Join(filepath.Dir(os.Args[0]), "NapCatOnce", "killQQ.bat")
						killQQCmd := exec.Command("cmd", "/C", killQQPath)
						hideWindow(killQQCmd)
						killQQCmd.Dir = filepath.Dir(killQQPath)
						err := killQQCmd.Run()

						// 等待一小段时间确保QQ完全关闭
						time.Sleep(2 * time.Second)

						// 首先执行 killQQ.bat
						updateStatus("正在关闭当前QQ...")
						rekillQQPath := filepath.Join(filepath.Dir(os.Args[0]), "NapCatOnce", "killQQ.bat")
						rekillQQCmd := exec.Command("cmd", "/C", rekillQQPath)
						hideWindow(rekillQQCmd)
						rekillQQCmd.Dir = filepath.Dir(rekillQQPath)
						err = rekillQQCmd.Run()

						// 等待一小段时间确保QQ完全关闭
						time.Sleep(1 * time.Second)

						updateStatus("正在启动QQ机器人...")
						napCatPath := filepath.Join(filepath.Dir(os.Args[0]), "NapCatOnce", "NapCatWinBootMain.exe")
						napCatCmd := exec.Command(napCatPath)
						napCatCmd.Dir = filepath.Join(filepath.Dir(os.Args[0]), "NapCatOnce")
						err = napCatCmd.Start()
						if err != nil {
							updateStatus(fmt.Sprintf("启动 NapCatWinBootMain.exe 失败: %v", err))
							return
						}
						pm.AddProcess(napCatCmd)

						updateStatus("正在启动 Python bot...")
						// 切换到 GeneratorGUI 目录并启动 Python bot
						botCmd := exec.Command("Python38/python", "bot.py")
						botCmd.Dir = filepath.Join(filepath.Dir(os.Args[0]), "GeneratorGUI")
						err = botCmd.Start()
						if err != nil {
							updateStatus(fmt.Sprintf("启动 Python bot 失败: %v", err))
							return
						}
						pm.AddProcess(botCmd)

						updateStatus("所有程序已成功启动！请重新登录QQ以完成接入。")

						// 显示提示对话框
						dialog.ShowInformation("操作提示",
							"请现在重新登录QQ。\n登录后的QQ将自动接入GalVoice。",
							window)
					}()
				}
			},
			window,
		)
		confirmDialog.SetDismissText("取消")
		confirmDialog.SetConfirmText("继续")
		confirmDialog.Show()
	})

	// 创建停止按钮
	stopButton := widget.NewButton("停止", func() {
		pm.KillAll()
		updateStatus("所有程序已停止，启动器将退出。")
		time.Sleep(1 * time.Second)
		// 退出启动器
		myApp.Quit()
	})

	// 创建按钮容器
	buttons := container.NewHBox(startButton, stopButton)

	// 创建主界面布局
	content := container.NewVBox(
		widget.NewLabel("Gal-Voice 启动器"),
		status,
		buttons,
	)

	window.SetContent(content)
	window.Resize(fyne.NewSize(400, 250))

	// 设置关闭窗口时的操作
	window.SetOnClosed(func() {
		pm.KillAll()
	})

	window.ShowAndRun()
}
