HIDE_ST_STYLE = """
                <style>
div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
				        .appview-container .main .block-container{
                            padding-top: 1rem;
                            padding-right: 3rem;
                            padding-left: 3rem;
                            padding-bottom: 1rem;
                        }  
                        .appview-container .sidebar-content {
                            padding-top: 0rem;
                        }
                        .reportview-container {
                            padding-top: 0rem;
                            padding-right: 3rem;
                            padding-left: 3rem;
                            padding-bottom: 0rem;
                        }
                        .reportview-container .sidebar-content {
                            padding-top: 0rem;
                        }
                        header[data-testid="stHeader"] {
                            z-index: -1;
                        }
                        div[data-testid="stToolbar"] {
                        z-index: 100;
                        }
                        div[data-testid="stDecoration"] {
                        z-index: 100;
                        }
                        .reportview-container .sidebar-content {
                            padding-top: 0rem;
                        }
                </style>
                """

PAGE_NUM = 5
CHARACTORS_PER_PAGE = 40
USING_TEXT_TYPE = ["ひらがなのみ", "ひらがなとカタカナ", "制限なし"]
AGE = ["1～2歳", "3～5歳", "6～10歳", "11歳～"]


THEME_PLACEHOLDER = """入力なしの場合自動で生成します。"""
DESCRIPTION_PLACEHOLDER = """入力なしの場合自動で生成します。"""

MAX_PAGE_NUM = 20

TALES_PROMPT = """
あなたはプロの絵本作家です。与えられた内容から以下の内容に沿って素晴らしい絵本の物語を作成してください。

## タイトル
%%title_placeholder%%

## あらすじ
%%description_placeholder%%

## テーマ・メッセージ
%%theme_placeholder%%

## ページ数
%%page_number_placeholder%%

## 1ページの文字数
%%characters_per_page_placeholder%%

## 利用する文字種類の制限
%%using_text_types_placeholder%%

## 読者の年齢
%%age_placeholder%%

## 注意事項
- 指定された1ページの文字数以下で生成することを必ず守ってください。
- 起承転結にわけて作成してください。
- 登場人物の見た目は、大きさ、色、服装、髪型、質感などできる限り詳細に記載してください。
- 出力はJsonで、出力サンプルに指定した形式に必ず従ってください。
- 出力は```json ```で囲わないでください。

## 出力サンプル
{
  "title": "ももたろう",
  "description": "おおきなももからうまれたすてきなおとこのこ、ももたろうのぼうけんをかいています。ももたろうは、おじいさんとおばあさんとしあわせにくらしていましたが、あるひ、むらのひとたちをたすけるために、おおきなぼうけんにでかけることにしますよ。ももたろうは、いぬ、さる、きじというともだちをつくりながら、わくわくどきどきのたびをすすめます。",
  "theme": "困難に立ち向かう勇気、悪に対する正義、そして異なる存在が協力することの重要性",
  "characters": {
    "lead": { "name": "ももたろう", "appearance": "短い黒髪と明るい目を持ち、勇気と冒険心を象徴するような表情をしています。日本の伝統的な衣装、短い着物や袴を着ています。この着物は青や赤などの鮮やかな色で、勇敢さや力強さを象徴する模様や紋様が施されています。腰には刀や腰袋を差し、頭には頭巾を巻いています" },
    "others": [
      { "name": "いぬ", "appearance": "茶色の毛を持つ大型の犬です。頭には短い耳があり、大きな目で友好的な表情をしています。首には首輪を着用しており、伝統的な日本の装飾が施されています。"},
      { "name": "きじ", "appearance": "色鮮やかな羽を持つ鳥で、長い尾と強い足が特徴です。羽色は主に赤や金色で、日本の伝統的な美しさを表しています。目は鋭く、狩猟の際に必要な鋭敏さを象徴しています。" },
      { "name": "さる", "appearance": "茶色の毛皮を持ち、顔はピンク色で、目は知恵に満ちています。猿はしばしば手に物を持っている。" },
      { "name": "おに", "appearance": "大きくて筋肉質の体格をしているのが特徴です。肌の色は通常、赤や青といった鮮やかな色で、大きな角が頭にあります。顔には野性的な表情をしており、大きな口と鋭い歯が目立ちます。鬼は伝統的な鬼の褌を着用し、手にはしばしば棍棒を持っています。" }
    ]
  },
  "content": [
    "おおきなももがかわをながれてきて、なかからいさましいおとこのこがあらわれます。おじいさんとおばあさんはよろこび、ももたろうとなづけます。",
    "ももたろうはおにがむらをこまらせているときき、おにたいじをけついします。いぬ、さる、きじとなかよくなり、いっしょにたびだちます。",
    "ももたろうとなかまたちはおにがしまにむかい、おにたちとたたかいます。むずかしいしょうぶでも、やさしいこころとちからをあわせてがんばります。",
    "ももたろうたちはおにをやっつけて、たからものをてにいれます。むらにかえり、みんなでしあわせにくらすようになります。"
  ]
}

"""

ONE_TALE_PROMPT = """
あなたはプロの絵本作家です。与えられた内容から1ページ分の素晴らしい内容を作成してください。

## タイトル
%%title_placeholder%%

## あらすじ
%%description_placeholder%%

## テーマ・メッセージ
%%theme_placeholder%%

## 登場人物
%%characters_placeholder%%

## ページ数
%%page_number_placeholder%%

## 1ページの文字数
%%characters_per_page_placeholder%%

## 利用する文字種類の制限
%%using_text_types_placeholder%%

## 読者の年齢
%%age_placeholder%%

## 前の内容
%%pre_pages_info_placeholder%%

## 後の内容
%%post_pages_info_placeholder%%

## 注意事項
- 指定された1ページの文字数以下で生成することを必ず守ってください。
- 前の内容と後の内容に繋がるように作成してください。
- 前の内容や後の内容が指定されない場合は、タイトルとあらすじから生成してください。
- 出力はテキストのみで説明等は出力しないでください。

"""

DESCRIPTION_PROMPT = """
あなたはプロの絵本作家です。与えられた内容から以下の内容に沿って素晴らしい絵本の物語を作成してください。

## タイトル
%%title_placeholder%%

## 内容
%%tales_placeholder%%

## テーマ・メッセージ
%%theme_placeholder%%

## 登場人物
%%characters_placeholder%%

## 利用する文字種類の制限
%%using_text_types_placeholder%%

## 注意事項
- 40字程度で作成してください。

"""


DESCRIPTION_IMAGE_PROMPT = """
あなたはプロの絵本作家です。与えられたテキストから素晴らしい絵本の表紙を作成してください。

## タイトル
%%title_placeholder%%

## あらすじ
%%description_placeholder%%

## テーマ・メッセージ
%%theme_placeholder%%

## 登場人物
%%characters_placeholder%%

## 注意事項
- 絵本にふさわしいかわいらしいタッチ

"""

IMAGES_PROMPT = """
あなたはプロの絵本作家です。与えられたテキストから素晴らしい絵本のイラストを作成してください。

## タイトル
%%title_placeholder%%

## あらすじ
%%description_placeholder%%

## テーマ・メッセージ
%%theme_placeholder%%

## 登場人物
%%characters_placeholder%%

## 注意事項
- 絵本にふさわしいかわいらしいタッチ

## 生成するイラストの内容
%%tale_placeholder%%

"""

TITLE_MARKDOWN = """

### %%title_placeholder%%

<img src="data:image/jpg;base64,%%title_image_placeholder%%" />
---

"""
NO_IMAGE_TITLE_MARKDOWN = """

### %%title_placeholder%%

---

"""

PAGE_MARKDOWN = """

<style>
.column-left{
  float: left;
  width: 47.5%;
  text-align: left;
  font-size: 80%;
}
.column-right{
  float: right;
  width: 47.5%;
  text-align: left;
  font-size: 80%;
}
.column-one{
  float: left;
  width: 100%;
  text-align: left;
}
</style>

<div class="column-left">
<img src="data:image/jpg;base64,%%page_image_placeholder%%" />
</div>

<div class="column-right">
%%content_placeholder%%
</div>

<audio data-autoplay src="data:audio/mp3;base64,%%page_audio_placeholder%%" type="audio/mp3"></audio>

---

"""
NO_IMAGE_PAGE_MARKDOWN = """

%%content_placeholder%%

<audio data-autoplay src="data:audio/mp3;base64,%%page_audio_placeholder%%" type="audio/mp3"></audio>

---

"""

END_ROLE = """

# おしまい

"""


TITLE_SET = [
    {
        "title": "そらとぶうまのぼうけん",
        "description": "ひこうきがすきなうまが、そらをとぶゆめをかなえるはなし。",
        "theme": "ゆめをおいかけることのうれしさ",
        "page_num": 8,
        "using_text_types": "ひらがなとカタカナ",
        "age": "3～5歳",
    },
    {
        "title": "みずうみのひみつ",
        "description": "みずうみにすむいきものたちがひみつをけんきゅうするはなし。",
        "theme": "しぜんをまもることのだいじさ",
        "page_num": 5,
        "using_text_types": "ひらがなのみ",
        "age": "3～5歳",
    },
    {
        "title": "おつきみパーティー",
        "description": "どうぶつたちがおつきみのよるにパーティーをするはなし。",
        "theme": "ともだちといっしょにすごすたのしさ",
        "page_num": 6,
        "using_text_types": "ひらがなとカタカナ",
        "age": "3～5歳",
    },
    {
        "title": "ちいさなかいじゅうのおおきなゆめ",
        "description": "ちいさなかいじゅうがおおきなゆめにむかってがんばるはなし。",
        "theme": "じぶんをしんじることのちから",
        "page_num": 7,
        "using_text_types": "ひらがなのみ",
        "age": "3～5歳",
    },
    {
        "title": "ほしをかぞえるよる",
        "description": "ほしをかぞえながら、ねむれないよるをすごすはなし。",
        "theme": "ふしぎとむげんのそらへのきょうみ",
        "page_num": 5,
        "using_text_types": "ひらがなとカタカナ",
        "age": "3～5歳",
    },
    {
        "title": "かぜのたびびと",
        "description": "かぜにのってせかいじゅうをたびするはなし。",
        "theme": "ぼうけんとたんけんのわくわく",
        "page_num": 8,
        "using_text_types": "ひらがなのみ",
        "age": "3～5歳",
    },
    {
        "title": "まほうのくつ",
        "description": "まほうのくつをはいて、ふしぎなせかいをたんけんするはなし。",
        "theme": "ゆめとまほうのせかい",
        "page_num": 6,
        "using_text_types": "ひらがなとカタカナ",
        "age": "3～5歳",
    },
    {
        "title": "こおりのおうこく",
        "description": "こおりのおうこくをたんけんし、ひみつをみつけるはなし。",
        "theme": "ちえとゆうきのたいせつさ",
        "page_num": 7,
        "using_text_types": "ひらがなのみ",
        "age": "3～5歳",
    },
    {
        "title": "うちゅうせんのぼうけん",
        "description": "うちゅうせんをうんてんして、ほかのほしをたんけんするはなし。",
        "theme": "うちゅうのふしぎとおおぼけん",
        "page_num": 8,
        "using_text_types": "ひらがなとカタカナ",
        "age": "6～10歳",
    },
    {
        "title": "やさいのだいすき",
        "description": "やさいたちがおいしいものをつくるはなし。",
        "theme": "けんこうなしょくせいかつとやさいのたいせつさ",
        "page_num": 5,
        "using_text_types": "ひらがなのみ",
        "age": "3～5歳",
    },
    {
        "title": "ひみつきちのなぞ",
        "description": "子どもたちがひみつきちでかくれんぼをしているときに、なぞの地図を見つける物語。",
        "theme": "チームワークと探検の楽しさ",
        "page_num": 10,
        "using_text_types": "制限なし",
        "age": "6～10歳",
    },
    {
        "title": "宇宙海賊の冒険",
        "description": "勇敢な宇宙海賊が未知の惑星を探検し、宝物を探す物語。",
        "theme": "冒険心と新しい世界への好奇心",
        "page_num": 12,
        "using_text_types": "制限なし",
        "age": "6～10歳",
    },
    {
        "title": "時空を超える旅",
        "description": "タイムマシンを発明した少年が歴史上の出来事を体験する物語。",
        "theme": "歴史と科学への興味と学び",
        "page_num": 11,
        "using_text_types": "制限なし",
        "age": "6～10歳",
    },
    {
        "title": "魔法の森の秘密",
        "description": "魔法の森で暮らす動物たちが、森を救うために力を合わせる物語。",
        "theme": "自然保護と協力の大切さ",
        "page_num": 9,
        "using_text_types": "制限なし",
        "age": "6～10歳",
    },
    {
        "title": "ロボットシティの謎",
        "description": "未来のロボットシティで起こる謎を解決する少年探偵の物語。",
        "theme": "論理的思考と創造力",
        "page_num": 10,
        "using_text_types": "制限なし",
        "age": "6～10歳",
    },
    {
        "title": "にこにこどうぶつえん",
        "description": "にこにこするいろいろなどうぶつたちをしょうかいする絵本。",
        "theme": "どうぶつたちの表情を通じて感情を学ぶ",
        "page_num": 4,
        "using_text_types": "ひらがなのみ",
        "age": "1～2歳",
    },
    {
        "title": "おはよう、おひさま",
        "description": "おひさまがのぼるところからおやすみまでのいちにちを描いた絵本。",
        "theme": "日常のリズムと自然のサイクルを紹介",
        "page_num": 4,
        "using_text_types": "ひらがなのみ",
        "age": "1～2歳",
    },
    {
        "title": "いろいろなはなし",
        "description": "さまざまな色と形のはなを紹介するカラフルな絵本。",
        "theme": "色と形を識別する基本的なスキルの発達",
        "page_num": 4,
        "using_text_types": "ひらがなのみ",
        "age": "1～2歳",
    },
    {
        "title": "ころころだま",
        "description": "いろいろな形のボールがころがる様子を楽しく描いた絵本。",
        "theme": "動きと形の認識を促進",
        "page_num": 3,
        "using_text_types": "ひらがなのみ",
        "age": "1～2歳",
    },
    {
        "title": "おやすみなさいのほん",
        "description": "ねんねする時間に読む、ほっとする夜の物語。",
        "theme": "安心感を与える就寝前の読み聞かせ",
        "page_num": 4,
        "using_text_types": "ひらがなのみ",
        "age": "1～2歳",
    },
    {
        "title": "星空の謎解き",
        "description": "天文学を学ぶ少女が、夜空の星を通じて宇宙の謎を解き明かす物語。",
        "theme": "宇宙への好奇心と科学の魅力",
        "page_num": 12,
        "using_text_types": "制限なし",
        "age": "11歳～",
    },
    {
        "title": "忘れられた文明の探検",
        "description": "歴史に興味を持つ少年が、失われた古代文明を探求する物語。",
        "theme": "歴史の発見と冒険のスリル",
        "page_num": 15,
        "using_text_types": "制限なし",
        "age": "11歳～",
    },
    {
        "title": "未来都市の秘密",
        "description": "未来都市で起こる謎を追う少年探偵の冒険物語。",
        "theme": "未来技術と論理的思考の発展",
        "page_num": 14,
        "using_text_types": "制限なし",
        "age": "11歳～",
    },
    {
        "title": "伝説の生物を求めて",
        "description": "伝説の生物を探すため、世界中を旅する少女の物語。",
        "theme": "伝説と自然界への探求心",
        "page_num": 13,
        "using_text_types": "制限なし",
        "age": "11歳～",
    },
    {
        "title": "時間の扉を越えて",
        "description": "時間旅行をすることができる機械を発見した少年の物語。",
        "theme": "時間と空間に関する科学的探究",
        "page_num": 12,
        "using_text_types": "制限なし",
        "age": "11歳～",
    },
]
