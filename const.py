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

DESCRIPTION_PLACEHOLDER = """入力なしでランダム生成します。"""

MAX_PAGE_NUM = 20

TALES_PROMPT = """
あなたはプロの絵本作家です。与えられた内容から以下の内容に沿って絵本の物語を作成してください。

## タイトル
%%title_placeholder%%

## あらすじ
%%description_placeholder%%

## ページ数
%%page_number_placeholder%%

## 1ページの文字数
%%characters_per_page_placeholder%%

## 注意事項
- 起承転結にわけて作成する。
- すべてひらがなで作成する。
- 出力はJsonで、出力サンプルに指定した形式に必ず従う。
- 出力は```json ```で囲わない

## 出力サンプル
{
"title":"ももたろう",
"description":"おおきなももからうまれたすてきなおとこのこ、ももたろうのぼうけんをかいています。ももたろうは、おじいさんとおばあさんとしあわせにくらしていましたが、あるひ、むらのひとたちをたすけるために、おおきなぼうけんにでかけることにしますよ。ももたろうは、いぬ、さる、きじというともだちをつくりながら、わくわくどきどきのたびをすすめます。",
"content":[
    "おおきなももがかわをながれてきて、なかからいさましいおとこのこがあらわれます。おじいさんとおばあさんはよろこび、ももたろうとなづけます。",
    "ももたろうはおにがむらをこまらせているときき、おにたいじをけついします。いぬ、さる、きじとなかよくなり、いっしょにたびだちます。",
    "ももたろうとなかまたちはおにがしまにむかい、おにたちとたたかいます。むずかしいしょうぶでも、やさしいこころとちからをあわせてがんばります。",
    "ももたろうたちはおにをやっつけて、たからものをてにいれます。むらにかえり、みんなでしあわせにくらすようになります。"
    ]
}
"""

ONE_TALE_PROMPT = """
あなたはプロの絵本作家です。与えられた内容から1ページ分の内容を作成してください。

## タイトル
%%title_placeholder%%

## あらすじ
%%description_placeholder%%

## ページ数
%%page_number_placeholder%%

## 1ページの文字数
%%characters_per_page_placeholder%%

## 前の内容
%%pre_pages_info_placeholder%%

## 後の内容
%%post_pages_info_placeholder%%

## 注意事項
- 前の内容と後の内容に繋がるように作成する。
- 前の内容や後の内容が指定されない場合は、タイトルとあらすじから生成する。
- すべてひらがなで作成する。
- 出力はテキストのみで説明等は出力しない。

"""

DESCRIPTION_PROMPT = """
あなたはプロの絵本作家です。与えられた内容から以下の内容に沿って絵本の物語を作成してください。

## タイトル
%%title_placeholder%%

## 内容
%%tales_placeholder%%

## 注意事項
- 40字程度で作成する。
- すべてひらがなで作成する。

"""


IMAGES_PROMPT = """
あなたはプロの絵本作家です。与えられたテキストから絵本のイラストを作成してください。

## タイトル
%%title_placeholder%%

## あらすじ
%%description_placeholder%%

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
}
.column-right{
  float: right;
  width: 47.5%;
  text-align: left;
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
