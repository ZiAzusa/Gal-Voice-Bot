from pypinyin import lazy_pinyin

pinyin_to_katakana = {
    # a开头
    'a': 'ア', 'ai': 'アイ', 'an': 'アン', 'ang': 'アン', 'ao': 'アオ',
    # b开头
    'ba': 'バ', 'bai': 'バイ', 'ban': 'バン', 'bang': 'バン', 'bao': 'バオ',
    'bei': 'ベイ', 'ben': 'ベン', 'beng': 'ベン', 'bi': 'ビー', 'bian': 'ビエン',
    'biao': 'ビアオ', 'bie': 'ビエ', 'bin': 'ビン', 'bing': 'ビン', 'bo': 'ボ', 'bu': 'ブ',
    # c开头
    'ca': 'ツァ', 'cai': 'ツァイ', 'can': 'ツァン', 'cang': 'ツァン', 'cao': 'ツァオ',
    'ce': 'ツァ', 'cen': 'ツェン', 'ceng': 'ツェン', 'cha': 'チャ', 'chai': 'チャイ',
    'chan': 'チャン', 'chang': 'チャン', 'chao': 'チャオ', 'che': 'チェ', 'chen': 'チェン',
    'cheng': 'チェン', 'chi': 'チー', 'chong': 'チョン', 'chou': 'チョウ', 'chu': 'チュウ',
    'chuai': 'チュアイ', 'chuan': 'チュアン', 'chuang': 'チュアン', 'chui': 'チュイ',
    'chun': 'チュン', 'chuo': 'チュオ', 'ci': 'ツー', 'cong': 'ツォン', 'cou': 'ツォウ',
    'cu': 'ツー', 'cuan': 'ツアン', 'cui': 'ツイ', 'cun': 'ツン', 'cuo': 'ツォ',
    # d开头
    'da': 'ダー', 'dai': 'ダイ', 'dan': 'ダン', 'dang': 'ダン', 'dao': 'ダオ',
    'de': 'ダー', 'dei': 'デイ', 'den': 'デン', 'deng': 'デン', 'di': 'ディー',
    'dia': 'ディア', 'dian': 'ディエン', 'diao': 'ディアオ', 'die': 'ディエ', 'ding': 'ディン',
    'diu': 'デュー', 'dong': 'ドン', 'dou': 'ドウ', 'du': 'ドゥー', 'duan': 'ドゥアン',
    'dui': 'ドゥイ', 'dun': 'ドゥン', 'duo': 'ドゥオ',
    # e开头
    'e': 'ア', 'ei': 'エイ', 'en': 'エン', 'eng': 'エン', 'er': 'アル',
    # f开头
    'fa': 'ファ', 'fan': 'ファン', 'fang': 'ファン', 'fei': 'フェイ', 'fen': 'フェン',
    'feng': 'フェン', 'fo': 'フォ', 'fou': 'フォウ', 'fu': 'フー',
    # g开头
    'ga': 'ガ', 'gai': 'ガイ', 'gan': 'ガン', 'gang': 'ガン', 'gao': 'ガオ',
    'ge': 'グー', 'gei': 'ゲイ', 'gen': 'ゲン', 'geng': 'ゲン', 'gong': 'ゴン',
    'gou': 'ゴウ', 'gu': 'グー', 'gua': 'グア', 'guai': 'グアイ', 'guan': 'グアン',
    'guang': 'グアン', 'gui': 'グイ', 'gun': 'グン', 'guo': 'グオ',
    # h开头
    'ha': 'ハ', 'hai': 'ハイ', 'han': 'ハン', 'hang': 'ハン', 'hao': 'ハオ',
    'he': 'ハー', 'hei': 'ヘイ', 'hen': 'ヘン', 'heng': 'ヘン', 'hong': 'ホン',
    'hou': 'ホウ', 'hu': 'フー', 'hua': 'ファ', 'huai': 'ファイ', 'huan': 'ファン',
    'huang': 'ファン', 'hui': 'フェイ', 'hun': 'フン', 'huo': 'フォ',
    # j开头
    'ji': 'ジー', 'jia': 'ジア', 'jian': 'ジエン', 'jiang': 'ジアン', 'jiao': 'ジアオ',
    'jie': 'ジエ', 'jin': 'ジン', 'jing': 'ジン', 'jiong': 'ジョン', 'jiu': 'ジウ',
    'ju': 'ジュー', 'juan': 'ジュアン', 'jue': 'ジュエ', 'jun': 'ジュン',
    # k开头
    'ka': 'カ', 'kai': 'カイ', 'kan': 'カン', 'kang': 'カン', 'kao': 'カオ',
    'ke': 'カー', 'kei': 'ケイ', 'ken': 'ケン', 'keng': 'ケン', 'kong': 'コン',
    'kou': 'コウ', 'ku': 'クー', 'kua': 'クア', 'kuai': 'クアイ', 'kuan': 'クアン',
    'kuang': 'クアン', 'kui': 'クイ', 'kun': 'クン', 'kuo': 'クオ',
    # l开头
    'la': 'ラ', 'lai': 'ライ', 'lan': 'ラン', 'lang': 'ラン', 'lao': 'ラオ',
    'le': 'ラー', 'lei': 'レイ', 'leng': 'レン', 'li': 'リー', 'lia': 'リア',
    'lian': 'リエン', 'liang': 'リアン', 'liao': 'リアオ', 'lie': 'リエ', 'lin': 'リン',
    'ling': 'リン', 'liu': 'リウ', 'long': 'ロン', 'lou': 'ロウ', 'lu': 'ルー',
    'lv': 'リュー', 'luan': 'ルアン', 'lue': 'リュエ', 'lun': 'ルン', 'luo': 'ルオ',
    # m开头
    'ma': 'マ', 'mai': 'マイ', 'man': 'マン', 'mang': 'マン', 'mao': 'マオ',
    'me': 'マー', 'mei': 'メイ', 'men': 'メン', 'meng': 'メン', 'mi': 'ミー',
    'mian': 'ミエン', 'miao': 'ミアオ', 'mie': 'ミエ', 'min': 'ミン', 'ming': 'ミン',
    'miu': 'ミウ', 'mo': 'モ', 'mou': 'モウ', 'mu': 'ムー',
    # n开头
    'na': 'ナ', 'nai': 'ナイ', 'nan': 'ナン', 'nang': 'ナン', 'nao': 'ナオ',
    'ne': 'ナー', 'nei': 'ネイ', 'nen': 'ネン', 'neng': 'ネン', 'ni': 'ニー',
    'nian': 'ニエン', 'niang': 'ニアン', 'niao': 'ニアオ', 'nie': 'ニエ', 'nin': 'ニン',
    'ning': 'ニン', 'niu': 'ニウ', 'nong': 'ノン', 'nou': 'ノウ', 'nu': 'ヌー',
    'nv': 'ニュー', 'nuan': 'ヌアン', 'nue': 'ニュエ', 'nuo': 'ヌオ',
    # o开头
    'o': 'オー', 'ou': 'オウ',
    # p开头
    'pa': 'パ', 'pai': 'パイ', 'pan': 'パン', 'pang': 'パン', 'pao': 'パオ',
    'pei': 'ペイ', 'pen': 'ペン', 'peng': 'ペン', 'pi': 'ピー', 'pian': 'ピエン',
    'piao': 'ピアオ', 'pie': 'ピエ', 'pin': 'ピン', 'ping': 'ピン', 'po': 'ポ', 'pu': 'プー',
    # q开头
    'qi': 'チー', 'qia': 'チャ', 'qian': 'チエン', 'qiang': 'チアン', 'qiao': 'チャオ',
    'qie': 'チエ', 'qin': 'チン', 'qing': 'チン', 'qiong': 'チョン', 'qiu': 'チウ',
    'qu': 'チュー', 'quan': 'チュアン', 'que': 'チュエ', 'qun': 'チュン',
    # r开头
    'ra': 'ラー', 'ran': 'ラン', 'rang': 'ラン', 'rao': 'ラオ', 're': 'レー',
    'ren': 'レン', 'reng': 'レン', 'ri': 'リー', 'rong': 'ロン', 'rou': 'ロウ',
    'ru': 'ルー', 'rua': 'ルア', 'ruan': 'ルアン', 'rui': 'ルイ', 'run': 'ルン', 'ruo': 'ルオ',
    # s开头
    'sa': 'サ', 'sai': 'サイ', 'san': 'サン', 'sang': 'サン', 'sao': 'サオ',
    'se': 'セ', 'sen': 'セン', 'seng': 'セン', 'sha': 'シャ', 'shai': 'シャイ',
    'shan': 'シャン', 'shang': 'シャン', 'shao': 'シャオ', 'she': 'シェ', 'shen': 'シェン',
    'sheng': 'シェン', 'shi': 'シー', 'shou': 'ショウ', 'shu': 'シュウ', 'shua': 'シュア',
    'shuai': 'シュアイ', 'shuan': 'シュアン', 'shuang': 'シュアン', 'shui': 'シュイ', 'shun': 'シュン', 'shuo': 'シュオ',
    'si': 'スー', 'song': 'ソン', 'sou': 'ソウ', 'su': 'スー', 'suan': 'スアン', 'sui': 'スイ', 'sun': 'スン', 'suo': 'スオ',
    # t开头
    'ta': 'ター', 'tai': 'タイ', 'tan': 'タン', 'tang': 'タン', 'tao': 'タオ',
    'te': 'ター', 'teng': 'テン', 'ti': 'ティー', 'tian': 'ティエン', 'tiao': 'ティアオ',
    'tie': 'ティエ', 'ting': 'ティン', 'tong': 'トン', 'tou': 'トウ', 'tu': 'トゥー',
    'tuan': 'トゥアン', 'tui': 'トゥイ', 'tun': 'トゥン', 'tuo': 'トゥオ',
    # w开头
    'wa': 'ワ', 'wai': 'ワイ', 'wan': 'ワン', 'wang': 'ワン', 'wei': 'ウェイ',
    'wen': 'ウェン', 'weng': 'ウェン', 'wo': 'ウォ', 'wu': 'ウー',
    # x开头
    'xi': 'シー', 'xia': 'シャ', 'xian': 'シエン', 'xiang': 'シアン', 'xiao': 'シャオ',
    'xie': 'シエ', 'xin': 'シン', 'xing': 'シン', 'xiong': 'ション', 'xiu': 'シウ',
    'xu': 'シュー', 'xuan': 'シュアン', 'xue': 'シュエ', 'xun': 'シュン',
    # y开头
    'ya': 'ヤ', 'yan': 'イエン', 'yang': 'ヤン', 'yao': 'ヤオ', 'ye': 'イエ',
    'yi': 'イー', 'yin': 'イン', 'ying': 'イン', 'yo': 'ヨ', 'yong': 'ヨン',
    'you': 'ヨウ', 'yu': 'ユー', 'yuan': 'ユエン', 'yue': 'ユエ', 'yun': 'ユン',
    # z开头
    'za': 'ザ', 'zai': 'ザイ', 'zan': 'ザン', 'zang': 'ザン', 'zao': 'ザオ',
    'ze': 'ゼ', 'zei': 'ゼイ', 'zen': 'ゼン', 'zeng': 'ゼン', 'zha': 'ジャ',
    'zhai': 'ジャイ', 'zhan': 'ジャン', 'zhang': 'ジャン', 'zhao': 'ジャオ', 'zhe': 'ジェ',
    'zhen': 'ジェン', 'zheng': 'ジェン', 'zhi': 'ジー', 'zhong': 'ジョン', 'zhou': 'ジョウ',
    'zhu': 'ジュウ', 'zhua': 'ジュア', 'zhuai': 'ジュアイ', 'zhuan': 'ジュアン', 'zhuang': 'ジュアン',
    'zhui': 'ジュイ', 'zhun': 'ジュン', 'zhuo': 'ジュオ',
    'zi': 'ズー', 'zong': 'ゾン', 'zou': 'ゾウ', 'zu': 'ズー', 'zuan': 'ズアン',
    'zui': 'ズイ', 'zun': 'ズン', 'zuo': 'ズオ'
}

def pinyin_to_kana(pinyin):
    for length in [4, 3, 2, 1]:
        key = pinyin[:length]
        if key in pinyin_to_katakana:
            return pinyin_to_katakana[key] + pinyin_to_kana(pinyin[length:])
    return ''

def chinese_to_katakana(text):
    pinyin_list = lazy_pinyin(text)
    katakana = ''.join([pinyin_to_kana(p) for p in pinyin_list])
    return katakana
