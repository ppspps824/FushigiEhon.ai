import base64
import io
import json
import urllib

import const
import openai
import requests
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
    title,
    description,
    characters,
    theme,
    age_group,
    number_of_pages,
    characters_per_page,
    character_set,
    sentence_structure,
):
    tales = ""
    content = (
        const.TALES_PROMPT.replace("%%title_placeholder%%", title)
        .replace("%%description_placeholder%%", description)
        .replace("%%characters_placeholder%%", characters)
        .replace("%%theme_placeholder%%", theme)
        .replace("%%age_group_placeholder%%", age_group)
        .replace("%%sentence_structure_placeholder%%", sentence_structure)
        .replace("%%number_of_pages_placeholder%%", number_of_pages)
        .replace("%%characters_per_page_placeholder%%", characters_per_page)
        .replace("%%character_set_placeholder%%", character_set)
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
        # st.write(tales)
        return tales
    else:
        st.error("文章の生成に失敗しました。")
        return ""


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
            return ""

    if image_url:
        with urllib.request.urlopen(image_url) as web_file:
            image_data = web_file.read()

        image = Image.open(io.BytesIO(image_data))
        image = image.resize(size)

        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=50)

        return buffer.getvalue()
    else:
        return ""


def create_images(tales):
    images = {"title": "", "content": []}

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
    if not images["title"]:
        st.error("表紙の生成に失敗しました。")

    for num, tale in enumerate(tales["content"]):
        with st.spinner(f'生成中...(イラスト {num+1}/{len(tales["content"])})'):
            prompt = (
                const.IMAGES_PROMPT.replace("%%title_placeholder%%", title)
                .replace("%%description_placeholder%%", description)
                .replace("%%theme_placeholder%%", theme)
                .replace("%%characters_placeholder%%", characters)
                .replace("%%tale_placeholder%%", tale)
            )
            result = post_image_api(prompt, size=(1024, 1024))
            images["content"].append(result)
            if not result:
                st.error("イラストの生成に失敗しました。")
    return images


def create_audios(tales):
    audios = []
    for num, tale in enumerate(tales["content"]):
        with st.spinner(f'生成中...(音声) {num+1}/{len(tales["content"])}'):
            audios.append(post_audio_api(tale))

    return audios


def post_audio_api(tale):
    response = openai.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=tale,
    )

    return response.content


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
        st.markdown('<div class="overlay">', unsafe_allow_html=True)
        # with st_lottie_spinner(const.LOTTIE):
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

        st.markdown("</div>", unsafe_allow_html=True)
        return result


def create_one_tale(num):
    st.markdown('<div class="overlay">', unsafe_allow_html=True)
    # with st_lottie_spinner(const.LOTTIE):
    with st.spinner("生成中...(内容)"):
        prompt = (
            const.ONE_TALE_PROMPT.replace(
                "%%title_placeholder%%", st.session_state.tales["title"]
            )
            .replace(
                "%%description_placeholder%%",
                st.session_state.tales["description"],
            )
            .replace(
                "%%theme_placeholder%%",
                st.session_state.tales["theme"],
            )
            .replace(
                "%%sentence_structure_placeholder%%",
                st.session_state.tales["sentence_structure"],
            )
            .replace(
                "%%characters_placeholder%%",
                json.dumps(st.session_state.tales["characters"], ensure_ascii=False),
            )
            .replace(
                "%%number_of_pages_placeholder%%",
                st.session_state.tales["number_of_pages"],
            )
            .replace(
                "%%character_set_placeholder%%",
                st.session_state.tales["character_set"],
            )
            .replace(
                "%%age_group_placeholder%%",
                st.session_state.tales["age_group"],
            )
            .replace(
                "%%pre_pages_info_placeholder%%",
                "\n".join(st.session_state.tales["content"][:num]),
            )
            .replace(
                "%%post_pages_info_placeholder%%",
                "\n".join(st.session_state.tales["content"][num + 1 :]),
            )
        )
        generated_tale = post_text_api(prompt)
        if num < len(st.session_state.tales["content"]):
            st.session_state.tales["content"][num] = generated_tale
        else:
            st.session_state.tales["content"].append(generated_tale)
    st.markdown("</div>", unsafe_allow_html=True)


def create_one_audio(num, tale):
    with st.spinner("生成中...(音声)"):
        st.session_state.audios[num] = post_audio_api(tale)


def create_one_image(num, tale):
    st.markdown('<div class="overlay">', unsafe_allow_html=True)
    # with st_lottie_spinner(const.LOTTIE):
    with st.spinner("生成中...(イラスト)"):
        st.session_state.images["content"][num] = post_image_api(
            const.IMAGES_PROMPT.replace("%%tale_placeholder%%", tale)
            .replace("%%title_placeholder%%", st.session_state.tales["title"])
            .replace(
                "%%description_placeholder%%", st.session_state.tales["description"]
            )
            .replace(
                "%%theme_placeholder%%",
                st.session_state.tales["theme"],
            )
            .replace(
                "%%characters_placeholder%%",
                json.dumps(st.session_state.tales["characters"], ensure_ascii=False),
            ),
            (512, 512),
        )
    st.markdown("</div>", unsafe_allow_html=True)
