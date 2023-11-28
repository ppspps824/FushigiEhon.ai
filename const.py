DESCRIPTION_PLACEHOLDER = """入力なしでランダム生成します。"""

MAX_PAGE_NUM = 20

TALES_PROMPT = """
あなたはプロの絵本作家です。与えられた内容から以下の内容に沿って絵本の物語を作成してください。

## 内容
%%description_placeholder%%

## ページ数
%%page_number_placeholder%%

## 1ページの文字数
%%characters_per_page_placeholder%%

## ページごとの内容
%%page_info_placeholder%%

## 注意事項
- 起承転結にわけて作成する。
- すべてひらがなで作成する。
- 出力はJsonで、出力サンプルに指定した形式に必ず従う。

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

DESCRIPTION_PROMPT = """
あなたはプロの絵本作家です。与えられた内容から以下の内容に沿って絵本の物語を作成してください。

## タイトル
%%title_placeholder%%

## 内容
%%tales__placeholder%%

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

END_ROLE = """

# おしまい

"""
