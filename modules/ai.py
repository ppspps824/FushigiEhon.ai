import base64
import io
import json
import urllib

import const
import openai
import requests
import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas


def post_text_api(prompt):
    response = openai.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "system", "content": prompt}],
    )
    content_text = response.choices[0].message.content

    return content_text


def create_tales(
    title, description, theme, page_num, characters_per_page, using_text_types, age
):
    tales = ""
    content = (
        const.TALES_PROMPT.replace("%%title_placeholder%%", title)
        .replace("%%description_placeholder%%", description)
        .replace("%%theme_placeholder%%", theme)
        .replace("%%page_number_placeholder%%", page_num)
        .replace("%%characters_per_page_placeholder%%", characters_per_page)
        .replace("%%using_text_types_placeholder%%", using_text_types)
        .replace("%%age_placeholder%%", age)
    )
    with st.spinner("生成中...(テキスト)"):
        for _ in range(3):
            try:
                content_text = post_text_api(content)
                content_text = content_text.replace("json", "").replace("```", "")
                tales = json.loads(content_text)
                break
            except Exception as e:
                print(e.args)
                print(f"生成された内容：{content_text}")
                continue

    if tales:
        st.write(tales)
        return tales
    else:
        st.info("文章の生成に失敗しました。")
        st.stop()


def post_image_api(prompt, size):
    print(prompt)
    image_url = ""
    if st.session_state.image_model == "dall-e-3":
        gen_size = "1024x1024"
    else:
        gen_size = "512x512"

    for _ in range(3):
        try:
            response = openai.images.generate(
                model=st.session_state.image_model,
                prompt=prompt,
                size=gen_size,
                quality="standard",
                n=1,
            )
            image_url = response.data[0].url
            break
        except Exception as e:
            print(e.args)
            st.error("イラストの生成に失敗しました。")
            st.stop()

    if image_url:
        with urllib.request.urlopen(image_url) as web_file:
            image_data = web_file.read()

        image = Image.open(io.BytesIO(image_data))
        image = image.resize(size)

        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=50)

        return buffer.getvalue()
    else:
        st.error("イラストの生成に失敗しました。")
        st.stop()


def create_images(tales):
    images = {"description": "", "content": []}

    title = tales["title"]
    description = tales["description"]
    theme = tales["theme"]
    characters = json.dumps(tales["characters"], ensure_ascii=False)
    prompt = (
        const.DESCRIPTION_IMAGE_PROMPT.replace("%%title_placeholder%%", title)
        .replace("%%description_placeholder%%", description)
        .replace("%%theme_placeholder%%", theme)
        .replace("%%characters_placeholder%%", characters)
    )
    with st.spinner("生成中...(表紙)"):
        images["title"] = post_image_api(prompt, size=(512, 512))
    try:
        st.image(images["title"], width=512)
    except Exception as e:
        print(e.args)
        st.error("イラストの生成に失敗しました。")
        st.stop()

    pages = len(tales["content"])
    for num, tale in enumerate(tales["content"]):
        with st.spinner(f"生成中...(イラスト {num+1}/{pages})"):
            prompt = (
                const.IMAGES_PROMPT.replace("%%title_placeholder%%", title)
                .replace("%%description_placeholder%%", description)
                .replace("%%theme_placeholder%%", theme)
                .replace("%%characters_placeholder%%", characters)
                .replace("%%tale_placeholder%%", tale)
            )
            result = post_image_api(prompt, size=(1024, 1024))
            images["content"].append(result)
            try:
                st.image(result, width=512)
            except Exception as e:
                print(e.args)
                st.error("イラストの生成に失敗しました。")
                st.stop()

    return images


def create_audios(tales):
    audios = []
    pages = len(tales["content"])
    for num, tale in enumerate(tales["content"]):
        with st.spinner(f"生成中...(音声 {num+1}/{pages})"):
            audios.append(post_audio_api(tale))

    return audios


def post_audio_api(tale):
    response = openai.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=tale,
    )

    return io.BytesIO(response.content)


def draw_image(num, mode):
    col1, col2, col3 = st.columns([1, 4, 2])
    with col1:
        stroke_color = st.color_picker("色: ", key=f"color_picke1_{num}")
    with col2:
        stroke_width = st.slider("線の太さ: ", 1, 25, 3, key=f"slider1_{num}")
    with col3:
        st.write("")
        button_place = st.empty()

    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 1.0)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color="#EEEEEE",
        update_streamlit=False,
        height=450,
        width=450,
        drawing_mode="freedraw",
        key=f"canvas_{num}",
    )
    if canvas_result.image_data is not None:
        image = canvas_result.image_data
        image = Image.fromarray(image.astype("uint8"), mode="RGBA")

    if button_place.button("AI補正", key=num):
        if image:
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            image = buffered.getvalue()
            base_prompt = """
            あなたの役割は入力された画像と説明を理解し、より詳細な画像を生成するためのプロンプトテキストを生成することです。
            画像が非常に簡素なものであってもできる限りの特徴を捉え、それにあった色や背景についても最大限に想像力を働かせて表現してください。
            絵のスタイルは絵本にふさわしいポップなものにしてください。
            説明等は不要ですので、必ずプロンプトテキストのみ出力してください。"""
            payload = {
                "model": "gpt-4-vision-preview",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": base_prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64.b64encode(image).decode()}"
                                },
                            },
                        ],
                    }
                ],
                "max_tokens": 300,
            }
            with st.spinner("生成中..."):
                response = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {openai.api_key}"},
                    json=payload,
                ).json()
                response_text = response["choices"][0]["message"]["content"]
            if mode == "title":
                st.session_state.title_image = post_image_api(
                    response_text, size=(1024, 1024)
                )
            else:
                st.session_state.images[num] = post_image_api(
                    response_text, size=(1024, 1024)
                )
            st.rerun()
