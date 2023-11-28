import io
import json
import urllib

import const
import openai
import streamlit as st
from PIL import Image

openai.api_key = st.secrets["OPEN_AI_KEY"]


def post_text_api(prompt, response_format={"type": "json_object"}):
    response = openai.chat.completions.create(
        model="gpt-4-1106-preview",
        response_format=response_format,
        messages=[{"role": "system", "content": prompt}],
    )
    content_text = response.choices[0].message.content

    return content_text


def create_tales(title, description, page_num, characters_per_page, page_infos=[]):
    tales = ""
    content = (
        const.TALES_PROMPT.replace("%%title_placeholder%%", title)
        .replace("%%description_placeholder%%", description)
        .replace("%%page_number_placeholder%%", page_num)
        .replace("%%characters_per_page_placeholder%%", characters_per_page)
        .replace("%%page_info_placeholder%%", "\n".join(page_infos))
    )
    with st.spinner("生成中...(文章)"):
        for _ in range(3):
            try:
                content_text = post_text_api(content)
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


def post_image_api(prompt, size):
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
        with st.spinner(f"生成中...(音声 {num}/{pages})"):
            audios.append(post_audio_api(tale))

    return audios


def post_audio_api(tale):
    response = openai.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=tale,
    )

    return io.BytesIO(response.content)