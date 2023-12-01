import io
import json
import urllib

import const
import openai
import streamlit as st
from PIL import Image


def post_text_api(prompt):
    response = openai.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "system", "content": prompt}],
    )
    content_text = response.choices[0].message.content

    return content_text


def create_tales(
    title, description, page_num, characters_per_page, using_text_types, age
):
    tales = ""
    content = (
        const.TALES_PROMPT.replace("%%title_placeholder%%", title)
        .replace("%%description_placeholder%%", description)
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
        return tales
    else:
        st.info("生成に失敗しました。リトライしてください")
        st.stop()


def post_image_api(prompt, size):
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
            continue

    if image_url:
        with urllib.request.urlopen(image_url) as web_file:
            image_data = web_file.read()

        image = Image.open(io.BytesIO(image_data))
        image = image.resize(size)

        return image
    else:
        st.info("生成に失敗しました。リトライしてください")
        st.stop()


def create_images(tales):
    images = {"description": "", "content": []}

    title = tales["title"]
    description = tales["description"]
    with st.spinner("生成中...(表紙)"):
        images["title"] = post_image_api(description, size=(720, 720))

    pages = len(tales["content"])
    for num, tale in enumerate(tales["content"]):
        with st.spinner(f"生成中...(イラスト {num+1}/{pages})"):
            prompt = (
                const.IMAGES_PROMPT.replace("%%title_placeholder%%", title)
                .replace("%%description_placeholder%%", description)
                .replace("%%tale_placeholder%%", tale)
            )
            images["content"].append(post_image_api(prompt, size=(1024, 1024)))

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
