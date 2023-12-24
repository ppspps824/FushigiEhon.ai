import base64
import io
import json
import urllib

import const
import openai
import requests
import streamlit as st
from PIL import Image
from modules.utils import show_overlay, hide_overlay


def post_text_api(prompt):
    response = openai.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "system", "content": prompt}],
    )
    content_text = response.choices[0].message.content

    return content_text


def create_tales(
    title,
    description,
    characters,
    theme,
    number_of_pages,
    characters_per_page,
    character_set,
    age,
):
    tales = ""
    content = (
        const.TALES_PROMPT.replace("%%title_placeholder%%", title)
        .replace("%%description_placeholder%%", description)
        .replace("%%characters_placeholder%%", characters)
        .replace("%%theme_placeholder%%", theme)
        .replace("%%number_of_pages_placeholder%%", number_of_pages)
        .replace("%%characters_per_page_placeholder%%", characters_per_page)
        .replace("%%character_set_placeholder%%", character_set)
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
    images = {"title": "", "content": []}

    title = tales["title"]
    description = tales["description"]
    theme = tales["theme"]
    characters = json.dumps(tales["characters"], ensure_ascii=False)
    prompt = (
        const.DESCRIPTION_IMAGE_PROMPT.replace("rint%%title_placeholder%%", title)
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


def image_upgrade(image, title, description, theme, characters, tale):
    if image:
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
        with st.spinner("イラストを補正中..."):
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {openai.api_key}"},
                json=payload,
            ).json()
            response_text = response["choices"][0]["message"]["content"]
            prompt = (
                const.IMAGES_PROMPT.replace("%%title_placeholder%%", title)
                .replace("%%description_placeholder%%", description)
                .replace("%%theme_placeholder%%", theme)
                .replace("%%characters_placeholder%%", characters)
                .replace("%%tale_placeholder%%", tale + "\n\n" + response_text)
            )
            result = post_image_api(prompt, size=(1024, 1024))

        return result
