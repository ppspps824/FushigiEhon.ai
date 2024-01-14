import glob
import os

X_SHARE_HTML = """
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
        "height": "50%",
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
                div[data-testid="stStatusWidget"] {
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
                .block-container {
                padding-top: 2rem;
                padding-bottom: 5rem;
                }

                .loader-text {
                    color: white; /* テキストの色 */
                    margin-top: 20px; /* ローダーとの間隔 */
                    font-size: 20px; /* テキストサイズ */
                    text-align: center; /* 中央揃え */
                    }

                /* ローダー要素のスタイル定義 */
                .loader {
                    position: relative;
                    width: 75px;
                    height: 100px;
                    background-repeat: no-repeat;
                    background-image: linear-gradient(#DDD 50px, transparent 0),
                                    linear-gradient(#DDD 50px, transparent 0),
                                    linear-gradient(#DDD 50px, transparent 0),
                                    linear-gradient(#DDD 50px, transparent 0),
                                    linear-gradient(#DDD 50px, transparent 0);
                    background-size: 8px 100%;
                    background-position: 0px 90px, 15px 78px, 30px 66px, 45px 58px, 60px 50px;
                    animation: pillerPushUp 4s linear infinite;
                }
                .loader:after {
                    content: '';
                    position: absolute;
                    bottom: 10px;
                    left: 0;
                    width: 10px;
                    height: 10px;
                    background: #de3500;
                    border-radius: 50%;
                    animation: ballStepUp 4s linear infinite;
                }

                @keyframes pillerPushUp {
                0% , 40% , 100%{background-position: 0px 90px, 15px 78px, 30px 66px, 45px 58px, 60px 50px}
                50% ,  90% {background-position: 0px 50px, 15px 58px, 30px 66px, 45px 78px, 60px 90px}
                }

                @keyframes ballStepUp {
                0% {transform: translate(0, 0)}
                5% {transform: translate(8px, -14px)}
                10% {transform: translate(15px, -10px)}
                17% {transform: translate(23px, -24px)}
                20% {transform: translate(30px, -20px)}
                27% {transform: translate(38px, -34px)}
                30% {transform: translate(45px, -30px)}
                37% {transform: translate(53px, -44px)}
                40% {transform: translate(60px, -40px)}
                50% {transform: translate(60px, 0)}
                57% {transform: translate(53px, -14px)}
                60% {transform: translate(45px, -10px)}
                67% {transform: translate(37px, -24px)}
                70% {transform: translate(30px, -20px)}
                77% {transform: translate(22px, -34px)}
                80% {transform: translate(15px, -30px)}
                87% {transform: translate(7px, -44px)}
                90% {transform: translate(0, -40px)}
                100% {transform: translate(0, 0);}
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
                        display: flex;
                        justify-content: center;
                        align-items: center;
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
60

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
- 60字程度で作成してください。

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


IMAGE_UP_PROMPT = """
あなたはプロの絵本作家です。与えられたテキストから素晴らしい絵本のイラストを作成してください。

## 注意事項
- 絵本にふさわしいかわいらしいタッチ

## 登場人物
%%characters_placeholder%%

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

STRIPE_URL = "https://buy.stripe.com/test_3cs5mb83A6th3G84gg"

LEGAL = """
https://orchid-background-17a.notion.site/e1f71b4ecd2c414ba04dc5ff69495896
"""

IMAGE_MODEL = "dall-e-3"
