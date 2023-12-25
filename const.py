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
                footer{
                    width: 100%;
                    text-align: center;
                    position: absolute;/*←絶対位置*/
                    bottom: 0; /*下に固定*/
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
                    display: none;  /* 初期状態では非表示 */
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


CHARACTORS_PER_PAGE = 20
CHARACTER_SET = ["ひらがなのみ", "ひらがなとカタカナ", "制限なし"]
AGE_GROUP = ["1～2歳", "3～5歳", "6～10歳", "11歳～"]
MAX_PAGE_NUM = 20

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


TITLE_SET = [
    {
        "title": "ふしぎなほしのたび",
        "number_of_pages": 5,
        "age_group": "3～5歳",
        "character_set": "ひらがなとカタカナ",
        "description": "あるよる、ちいさな少女と彼女のぬいぐるみが、ふしぎな星空の旅に出ます。少女は、夢と冒険に満ちたこの旅で、いろいろな星々や宇宙の不思議を体験します。",
        "theme": "夢と冒険、友情、そして宇宙の神秘と美しさ",
        "characters": {
            "lead": {
                "name": "ゆめこ",
                "appearance": "明るいピンク色の髪を持ち、きらきらと輝く目が特徴です。カラフルなワンピースを着ており、頭には星形の飾りをつけています。彼女の表情は、好奇心とワクワクに満ちています。",
            },
            "others": [
                {
                    "name": "くまちゃん",
                    "appearance": "茶色のぬいぐるみのくまで、大きなまるい目とふわふわの毛が特徴です。首には赤いリボンを着用しており、いつもゆめこのそばにいます。",
                },
                {
                    "name": "ほしのせいじん",
                    "appearance": "青い肌を持つ小さな宇宙人で、大きな瞳があります。全身はキラキラ輝く衣装で覆われており、頭には星形のアンテナがあります。",
                },
            ],
        },
        "content": [
            "あるよる、ゆめことくまちゃんはほしをみつめていました。そこに、ふしぎなひかりがふたりをつつみます。",
            "ひかりがすみると、ふたりはうちゅうせんにのっていました。うちゅうせんはきれいなほしにむかってすすみます。",
            "ほしにつくと、ふしぎなほしのせいじんにあいました。せいじんは、ふしぎなほしのひみつをおしえてくれます。",
            "ゆめことくまちゃんは、いろいろなほしをたんけんしました。きれいなほしや、おもしろいほし、きょうりょくなほしもあります。",
            "さいごに、ゆめことくまちゃんはちきゅうにかえります。ふしぎなほしのたびは、ゆめでしたが、ふしぎとしあわせをおぼえました。",
        ],
    },
    {
        "title": "かぜのまほうのぼうけん",
        "number_of_pages": 6,
        "age_group": "6～10歳",
        "character_set": "制限なし",
        "description": "この物語は、風の魔法を使える少年と彼の友達が、村を救うための冒険に出る物語です。少年は自分の力と友情の大切さを学びながら、様々な困難に立ち向かいます。",
        "theme": "勇気と友情、困難に立ち向かう心、自分自身の力を信じること",
        "characters": {
            "lead": {
                "name": "ハル",
                "appearance": "緑色の目を持ち、風になびく金色の髪が特徴です。彼は青いチュニックと茶色のズボンを着ており、首には風の魔法のペンダントを身に着けています。",
            },
            "others": [
                {
                    "name": "ミナ",
                    "appearance": "大きな茶色の目と長い茶色の髪を持つ女の子です。彼女はピンクのドレスを着ており、頭には花の冠をつけています。",
                },
                {
                    "name": "ソラ",
                    "appearance": "ハルの忠実なペットの鳥で、青い羽と鋭い目を持っています。常にハルの肩に留まっており、彼の旅の忠実な伴侶です。",
                },
                {
                    "name": "闇の魔術師",
                    "appearance": "長い黒いマントを着ており、目は冷たく輝いています。彼の周りにはいつも暗いオーラが漂っています。",
                },
            ],
        },
        "content": [
            "ハルは風の魔法を使える少年。ある日、村が闇の魔術師に脅かされていることを知ります。",
            "ミナとソラと一緒に、ハルは村を救うための冒険に出ます。森を抜け、山を越え、多くの困難に立ち向かいます。",
            "途中、ハルは自分の魔法の力を試される場面に何度も遭遇します。彼は勇気を持って困難を乗り越えます。",
            "闇の魔術師の城に到着し、ハルたちは激しい戦いに挑みます。ハルの風の魔法とミナの知恵が光ります。",
            "最後に、ハルたちは魔術師を倒し、村に平和を取り戻します。ハルは自分の力と友情の大切さを学びました。",
            "村に戻ったハルたちは、村人たちに祝福され、新たな伝説のヒーローとして讃えられます。",
        ],
    },
    {
        "title": "くものうえのひみつきち",
        "number_of_pages": 7,
        "age_group": "11歳～",
        "character_set": "制限なし",
        "description": "アキラとリコは、不思議な雲を見つけ、それに導かれて空中の隠れた秘密基地を探検する冒険に出ます。彼らはネビュラという神秘的な生き物と出会い、この空中世界の不思議を学びます。",
        "theme": "冒険と発見の喜び、友情、そして未知への好奇心",
        "characters": {
            "lead": {
                "name": "アキラ",
                "appearance": "スマートな眼鏡をかけた黒髪の少年。青いジャケットとジーンズを着ていて、頭には常に考え事をしている様子が見られます。",
            },
            "others": [
                {
                    "name": "リコ",
                    "appearance": "赤いポニーテールの女の子で、活発で好奇心旺盛な性格。彼女は黄色いワンピースを着ており、腕にはいくつかのバンドを着用しています。",
                },
                {
                    "name": "ネビュラ",
                    "appearance": "くものうえに住む神秘的な生き物で、透明で光る体を持っています。目は大きく、深い青色で、翼はまるで光る霧のようです。",
                },
            ],
        },
        "content": [
            "ある日、アキラとリコは不思議なくもを見つけます。くもは彼らを高く空中に運びます。",
            "くもの上には、驚くべきひみつきちがありました。そこは不思議な技術と魔法の世界でした。",
            "彼らはネビュラに出会います。ネビュラはくもの国の案内人で、彼らにこの世界の秘密を教えてくれます。",
            "アキラとリコは、くもの世界で様々な冒険を経験します。空を飛んだり、不思議な生き物と出会ったりします。",
            "しかし、彼らはくもの国に隠された大きな危険を知ります。その秘密を解く鍵が二人にあることがわかります。",
            "アキラとリコは、危険を克服し、くもの国を救うために力を合わせます。彼らは自分たちの勇気と知恵を試されます。",
            "最終的に、二人はくもの国を救い、地上に戻ります。彼らの冒険は、誰にも信じられない秘密として、心に残ります。",
        ],
    },
    {
        "title": "月夜の魔法の庭",
        "number_of_pages": 8,
        "age_group": "3～5歳",
        "character_set": "ひらがなのみ",
        "description": "ユイはおばあちゃんから聞いた不思議な庭を訪れます。月夜に輝くこの庭で、ユイは魔法の花とツキノウサギ、そして賢いフクロウのソフィアと出会います。",
        "theme": "自然の不思議、魔法の美しさ、そして夢を信じることの大切さ",
        "characters": {
            "lead": {
                "name": "ユイ",
                "appearance": "明るい青い目を持つ小さな女の子。ピンクのドレスを着ており、頭には小さな花のかんむりをつけています。",
            },
            "others": [
                {
                    "name": "ツキノウサギ",
                    "appearance": "白くてふわふわのうさぎ。大きな青い目があり、月光の下で輝いています。",
                },
                {
                    "name": "フクロウのソフィア",
                    "appearance": "知恵のある目を持つフクロウ。羽は茶色と白で、首には金色のリボンがあります。",
                },
            ],
        },
        "content": [
            "ユイはおばあちゃんからきいたふしぎなはなぞのばにいきます。",
            "月夜に、はなぞのばはまほうでいっぱい。ツキノウサギとあいました。",
            "ツキノウサギはユイにまほうのはなをみせます。きれいな色とかおりがあります。",
            "ユイはフクロウのソフィアにであい、はなぞのばのひみつをききます。",
            "ソフィアはユイに特別なはなのタネをわたします。タネはひかりをはなちます。",
            "ユイはタネをまき、ふしぎなはながさくのをみます。はなは夜にだけさきます。",
            "はなからはまほうのちからがでて、ユイの願いがかないます。",
            "ユイはおばあちゃんにまほうのはなぞのばのはなしをします。いつもしんじてくれます。",
        ],
    },
    {
        "title": "ひかりのしまのなぞ",
        "number_of_pages": 10,
        "age_group": "6～10歳",
        "character_set": "制限なし",
        "description": "タイチとエマは謎に満ちた光の島を探検します。彼らは古代の秘密と宝を求めて未知の島を冒険し、数々の試練に直面します。",
        "theme": "冒険心、友情、そして謎解きのスリル",
        "characters": {
            "lead": {
                "name": "タイチ",
                "appearance": "茶色の髪と勇敢な瞳を持つ少年。海賊風の服装をしており、頭には赤いバンダナを巻いています。",
            },
            "others": [
                {
                    "name": "エマ",
                    "appearance": "長い金髪と好奇心いっぱいの青い目を持つ少女。彼女は冒険家の装いをしており、手には古い地図を持っています。",
                },
                {
                    "name": "カゲ",
                    "appearance": "タイチの忠実なペットの黒猫。輝く緑色の目としなやかな体が特徴です。",
                },
            ],
        },
        "content": [
            "タイチとエマはひかりのしまのなぞを解き明かすために旅に出ます。",
            "二人は波乱に満ちた海を渡り、未知の島に到着します。",
            "しまには古代の遺跡があり、そこには謎の暗号が刻まれていました。",
            "タイチはカゲと一緒に暗号を解読し、隠された宝の手がかりを見つけます。",
            "エマは地図を使って、宝が眠る場所へと二人を導きます。",
            "彼らは罠や障害を乗り越え、ついに秘宝のある洞窟にたどり着きます。",
            "洞窟の中で、二人は輝く宝石と古代の秘密を発見します。",
            "しかし、宝を手に入れると同時に島が崩れ始めます。",
            "タイチとエマは急いで島から脱出し、無事に帰還します。",
            "彼らは宝の一部を博物館に寄贈し、冒険の物語を語り継ぎます。",
        ],
    },
    {
        "title": "くうかんのともだち",
        "number_of_pages": 9,
        "age_group": "1～2歳",
        "character_set": "ひらがなのみ",
        "description": "ケンタは空を眺めるのが大好きな男の子です。ある日、彼は不思議な生き物ふわりに出会い、ともに空の世界を冒険します。",
        "theme": "想像力の広がり、友情、そして空の不思議",
        "characters": {
            "lead": {
                "name": "ケンタ",
                "appearance": "短い黒髪と大きな目を持つ元気な男の子。色とりどりのストライプのシャツと青いズボンをはいています。",
            },
            "others": [
                {
                    "name": "ふわり",
                    "appearance": "白くてふんわりした雲のような形をした不思議な生き物。目はくりくりとしていて、いつもニコニコしています。",
                },
                {
                    "name": "ぴょんきち",
                    "appearance": "小さな緑色のうさぎ。赤いボールをいつも持っていて、跳ねるのが大好きです。",
                },
            ],
        },
        "content": [
            "ケンタはそらをながめるのがだいすき。あるひ、そらからふわりがおりてきます。",
            "ふわりはケンタにともだちになろうといいます。ケンタはうれしくてはねます。",
            "ふわりはケンタをくうちゅうへとつれていきます。そこはきれいなそらのせかい。",
            "そらのせかいで、ふわりのともだちぴょんきちにあいます。ぴょんきちはたのしいうさぎ。",
            "ぴょんきちといっしょに、ケンタはくうちゅうであそびます。たくさんのゲームやたんけん。",
            "ケンタはくうちゅうでたくさんのふしぎなものをみます。きれいなほしやかがやくほし。",
            "ふわりとぴょんきちはケンタをちきゅうにかえしてくれます。ケンタはしあわせ。",
            "ケンタはまたくうかんのともだちにあいたいとおもいます。まいにちそらをみます。",
            "そのよる、ケンタはふわりとぴょんきちのゆめをみます。たのしいゆめでした。",
        ],
    },
    {
        "title": "まほうのぼうしのひみつ",
        "number_of_pages": 12,
        "age_group": "11歳～",
        "character_set": "制限なし",
        "description": "ノリコは古いおもちゃ屋で話す魔法の帽子、ミスター・ハットを見つけます。彼女はハットとともに魔法の冒険を繰り広げ、その過程で自己発見と成長を遂げます。",
        "theme": "魔法の楽しさ、自己発見、そして成長の旅",
        "characters": {
            "lead": {
                "name": "ノリコ",
                "appearance": "長い茶色の髪と好奇心いっぱいの緑色の目を持つ少女。彼女はカラフルなワンピースを着ており、足元には赤い靴をはいています。",
            },
            "others": [
                {
                    "name": "ミスター・ハット",
                    "appearance": "おしゃべりな帽子で、深い青色で、縁には金色の装飾が施されています。目はなく、声で感情を表現します。",
                },
                {
                    "name": "ソーサラー",
                    "appearance": "年老いた魔法使いで、長い銀髪と深い青色のローブをまとっています。手には常に杖を持っています。",
                },
            ],
        },
        "content": [
            "ノリコは古いおもちゃ屋で不思議な帽子を見つけます。帽子はミスター・ハットと名乗ります。",
            "ミスター・ハットはノリコにまほうの力があることを教えます。ノリコはわくわくします。",
            "ノリコとミスター・ハットは、まほうの力を使って冒険に出ます。空を飛んだり、物を変えたりします。",
            "しかし、ミスター・ハットのまほうには秘密がありました。魔法使いソーサラーが関係しています。",
            "ノリコはソーサラーに会いに行き、帽子の真実を知ります。帽子はかつての弟子のものでした。",
            "ソーサラーはノリコに帽子の力を正しく使うことの重要性を教えます。ノリコは学びます。",
            "ノリコはミスター・ハットとともに、まほうで人を助けるようになります。多くの冒険を経験します。",
            "ノリコはまほうの力を使って、困っている人々を助けます。彼女は成長し、勇気を持ちます。",
            "ある日、ノリコはミスター・ハットを元の持ち主に返す決心をします。それは大切な決断でした。",
            "ノリコはおもちゃ屋に戻り、ミスター・ハットをソーサラーに渡します。感動的な別れとなります。",
            "ノリコはまほうの力を持たなくても、自分自身の力で多くのことができると学びます。",
            "ノリコはこれからも冒険を続けます。ミスター・ハットとの思い出とともに、勇敢に歩み続けます。",
        ],
    },
    {
        "title": "しろいうさぎとゆめの森",
        "number_of_pages": 15,
        "age_group": "3～5歳",
        "character_set": "ひらがなのみ",
        "description": "サキは森でしろいうさぎと出会い、一緒に不思議なゆめの森を探検します。彼女は森の中で様々な動物たちと出会い、魔法の鏡を通じて新しい友だちを作ります。",
        "theme": "友情と想像力の大切さ、自然の美しさと冒険の楽しみ",
        "characters": {
            "lead": {
                "name": "サキ",
                "appearance": "短い黒髪とキラキラとした目を持つ女の子。彼女は花柄のドレスを着ており、足元には黄色い靴をはいています。",
            },
            "others": [
                {
                    "name": "しろいうさぎ",
                    "appearance": "雪のように白い毛を持つ小さなうさぎ。目は青く、いつも好奇心いっぱいの表情をしています。",
                },
                {
                    "name": "もりのどうぶつたち",
                    "appearance": "色々な色と形の動物たち。森に住んでいて、それぞれユニークな特徴があります。",
                },
            ],
        },
        "content": [
            "サキはあるひ、しろいうさぎをみつけます。うさぎはサキをゆめの森へとさそいます。",
            "ゆめの森には、きれいな花と輝く川があります。サキはうっとりします。",
            "しろいうさぎはサキをもりのどうぶつたちにしょうかいします。どうぶつたちはやさしいです。",
            "サキはどうぶつたちといっしょにあそびます。かくれんぼやおんがくをたのしみます。",
            "森の中にはふしぎな木の家があります。サキはしろいうさぎといっしょに探検します。",
            "木の家の中には、まほうの鏡がありました。鏡はサキの願いをかなえてくれます。",
            "サキは新しい友だちをつくりたいと願います。鏡はきらきらと輝きます。",
            "すると、森に新しいどうぶつたちがあらわれます。サキはうれしくなります。",
            "新しい友だちと、サキはさらに森を探検します。たくさんの冒険が待っています。",
            "サキは森でたくさんのことを学びます。友だちの大切さや自然のふしぎ。",
            "日が暮れると、サキは家に帰ることにします。しろいうさぎはさみしそうに見えます。",
            "サキはしろいうさぎにまた会いに来ると約束します。うさぎはにっこりと笑います。",
            "家に帰ったサキは、ゆめの森のことをおばあちゃんに話します。おばあちゃんはにっこり。",
            "その夜、サキはゆめの森と新しい友だちの夢を見ます。楽しい夢です。",
            "サキはこれからもゆめの森に会いに行くことを楽しみにしています。新しい冒険が待っています。",
        ],
    },
]
