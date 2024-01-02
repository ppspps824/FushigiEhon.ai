import glob
import os

X_SHARE_HTML =     """
<a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" data-size="large"
    data-text="%%title%% - ふしぎえほん.ai" data-url="https://fushigiehonai.streamlit.app/" data-hashtags="絵本,AI,ふしぎえほん"
    data-show-count="false">Tweet</a>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
    """

TITLE_LINK_BOX_STYLE = {
    "title": {"color": "#fafafa"},
    "text": {"color": "#fafafa"},
    "card": {
        "padding": "10px",
        "margin": "0px",
        "width": "100%",
        "height":"50%",
        "border-radius": "10px",
        "box-shadow": "0 0 2px rgba(0,0,0,0.5)",
    },
    "filter": {
        "background-color": "#004a55"  # <- make the image not dimmed anymore
    },
}
TITLE_BOX_STYLE = {
    "title": {"color": "#004a55"},
    "text": {"color": "#004a55"},
    "card": {
        "padding": "0px",
        "margin": "0px",
        "width": "100%",
        "border-radius": "10px",
        "box-shadow": "0 0 2px rgba(0,0,0,0.5)",
    },
    "filter": {
        "background-color": "rgba(250, 250, 250, 0)"  # <- make the image not dimmed anymore
    },
}

BASE_PATH = "users/%%user_id%%/book_info/%%title%%/"
TITLE_BASE_PATH = "users/%%user_id%%/book_info/"
BGM_LIST = [
    os.path.splitext(os.path.basename(path))[0]
    for path in glob.glob("assets/*")
    if "mp3" in path
]
BGM_OPTIONS = ["ランダム", "なし"] + BGM_LIST


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
                .overlay {
                    position: fixed;
                    width: 100%;
                    height: 100%;
                    top: 0;
                    left: 0;
                    background-color: rgba(0,0,0,0.5);
                    z-index: 99;
                    cursor: not-allowed;
                    display: flex; /* Flexboxを使用して中央配置/
                    justify-content: center; /* 水平中央/
                    align-items: center; /* 垂直中央/
                }
				        .appview-container .main .block-container{
                            padding-top: 1rem;
                            padding-right: 3rem;
                            padding-left: 3rem;
                            padding-bottom: 7rem;
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

POST_HTML = """
<a href="https://twitter.com/share?ref_src=twsrc%5Etfw"
    class="twitter-share-button"
    data-size="large"
    data-text="%%title_placeholder%%"
    data-url="https://fushigiehonai.streamlit.app/"
    data-hashtags="絵本作成,AI,ふしぎえほん"
    >Tweet
</a>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
"""

CHARACTORS_PER_PAGE = 30
SENTENCE_STRUCTURE_SET = ["バランス", "ナレーション中心", "会話中心"]
CHARACTER_SET = ["ひらがなのみ", "ひらがなとカタカナ", "制限なし"]
AGE_GROUP = ["1～2歳", "3～5歳", "6～10歳", "11歳～"]
MAX_PAGE_NUM = 10

RAMDOM_PLACEHOLDER = """入力なしの場合自動で生成します。"""

MAX_NUMBER_OF_PAGES = 20

TALES_PROMPT = """
あなたはプロの絵本作家です。与えられた内容から以下の内容に沿って素晴らしい絵本の物語を作成してください。

## タイトル
%%title_placeholder%%

## あらすじ
%%description_placeholder%%

## 登場人物
%%characters_placeholder%%

## テーマ・メッセージ
%%theme_placeholder%%

## ページ数
%%number_of_pages_placeholder%%

## 1ページの文字数
40

## 利用する文字種類の制限
%%character_set_placeholder%%

## 読者の年齢
%%age_group_placeholder%%

## 文章の構成
%%sentence_structure_placeholder%%

## 注意事項
- 指定された1ページの文字数以下で生成することを必ず守ってください。
- 起承転結にわけて作成してください。
- 登場人物の見た目は、大きさ、色、服装、髪型、質感などできる限り詳細に記載してください。
- 出力はJsonで、出力サンプルに指定した形式に必ず従ってください。
- 出力は```json ```で囲わないでください。

## 出力サンプル
{
  "title": "ももたろう",
  "number_of_pages":4,
  "sentence_structure":"ナレーション中心",
  "age_group":"1～2歳",
  "character_set":"ひらがなのみ",
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
%%number_of_pages_placeholder%%

## 1ページの文字数
40

## 利用する文字種類の制限
%%character_set_placeholder%%

## 読者の年齢
%%age_group_placeholder%%

## 文章の構成
%%sentence_structure_placeholder%%

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
%%character_set_placeholder%%

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

<img src="data:image/jpg;base64,%%image_placeholder%%" height="400" />
---

"""

PAGE_MARKDOWN = """

<img src="data:image/jpg;base64,%%image_placeholder%%" height="400" />
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

LOTTIE = "https://lottie.host/fc04f21d-abcf-4e8c-840a-548301d00539/2wqct1sOBx.json"

STRIPE_URL="https://buy.stripe.com/test_3cs5mb83A6th3G84gg"

LEGAL="""
https://orchid-background-17a.notion.site/e1f71b4ecd2c414ba04dc5ff69495896
"""