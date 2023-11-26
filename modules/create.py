import datetime
import json
import io

import urllib.request
import boto3
import const
import openai
import pytz
import streamlit as st
from PIL import Image
import pickle



def create():
    openai.api_key = st.secrets["OPEN_AI_KEY"]

    def create_tales(description,page_num,characters_per_page,page_infos=[]):
        tales = ""
        content = const.TALES_PROMPT.replace("%%description_placeholder%%", description).replace("%%page_number_placeholder%%", page_num).replace("%%characters_per_page_placeholder%%", characters_per_page).replace("%%page_info_placeholder%%", "\n".join(page_infos))
        with st.spinner("生成中...(文章)"):
            for _ in range(3):
                try:
                    response = openai.chat.completions.create(
                        model="gpt-4-1106-preview",
                        response_format={"type": "json_object"},
                        messages=[{"role": "system", "content": content}],
                    )
                    content_text = response.choices[0].message.content
                    tales = json.loads(content_text)
                    break
                except Exception as e:
                    print(e.args)
                    continue

        if tales:
            return tales
        else:
            st.info("リトライしてください")
            st.stop

    def post_image_api(prompt,size):
        image_url = ""
        for _ in range(3):
            try:
                response = openai.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
                image_url = response.data[0].url
                break
            except Exception as e:
                print(e.args)
                continue

        if image_url:
            with urllib.request.urlopen(image_url) as web_file:
                image_data = web_file.read()

            image = Image.open(io.BytesIO(image_data))
            image = image.resize(size)

            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            return buffered.getvalue()
        else:
            st.info("リトライしてください")
            st.stop

    def create_images(tales):
        images = {"description": "", "content": []}

        title = tales["title"]
        description = tales["description"]
        images["title"] = post_image_api(description,size=(512,512))
        pages = len(tales["content"])
        for num, tale in enumerate(tales["content"]):
            with st.spinner(f"生成中...(イラスト {num+1}/{pages})"):
                prompt = (
                    const.IMAGES_PROMPT.replace("%%title_placeholder%%", title)
                    .replace("%%description_placeholder%%", description)
                    .replace("%%tale_placeholder%%", tale)
                )
                images["content"].append(post_image_api(prompt,size=(512,512)))

        return images

    def create_audios(tales):
        audios = []
        pages = len(tales["content"])
        for num, tale in enumerate(tales["content"]):
            with st.spinner(f"生成中...(音声 {num}/{pages})"):
                response = openai.audio.speech.create(
                    model="tts-1",
                    voice="nova",
                    input=tale,
                )

            # Convert the binary response content to a byte stream
            audios.append(io.BytesIO(response.content))

        return audios

    def create_book():
        page_infos=[]

        col1,col2,col3 = st.columns(3)
        with col1:
            mode = st.selectbox("作り方",options=["一括","ページごと"])
        with col2:
            page_num=st.number_input("ページ数",min_value=1,max_value=const.MAX_PAGE_NUM,value=5)
        with col3:
            characters_per_page=st.number_input("ページごとの文字数",min_value=10,max_value=100,value=40)

        description = st.text_area(
            "タイトル、あらすじなど", placeholder=const.DESCRIPTION_PLACEHOLDER
        )

        if mode == "ページごと":
            page_infos = [st.text_area(f"page{num+1} 内容", placeholder=const.DESCRIPTION_PLACEHOLDER) for num in range(page_num)]

        if st.button("作成する"):
            if description:
                # 生成処理
                # 物語を生成
                tales = create_tales(description,str(page_num),str(characters_per_page),page_infos)

                # イラストを生成
                images = create_images(tales)

                # 音声を生成
                audios = create_audios(tales)

                create_date = datetime.datetime.now(pytz.timezone("Asia/Tokyo"))
                create_date_yyyymdd = create_date.strftime("%Y%m%d_%H%M%S")
                book_about = {
                    "create_date": create_date_yyyymdd,
                    "title": tales.get("title"),
                    "title_image": images.get("title"),
                    "description": tales.get("description"),
                }

                book_content = {
                    "about": book_about,
                    "details": {
                        "tales": tales,
                        "images": images,
                        "audios": audios,
                    },
                }

                with open(f"books/{tales.get('title')}.pickle ", "wb") as f:
                    pickle.dump(book_content,f)
                    
                # ログイン時は自動で保存される
                if st.session_state.login:
                    # 保存処理
                    st.info("保存しました。")

                st.write(book_about["title"])
                st.image(book_about["title_image"])
                st.write(book_about["description"])

            else:
                st.info("内容を入力してください。")

    create_book()
