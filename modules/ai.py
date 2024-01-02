import base64
import io
import json
import urllib

import const
import openai
import requests
import streamlit as st
from PIL import Image
from modules.utils import check_credits, culc_use_credits
import modules.database as db
import asyncio

def post_text_api(prompt):
    event = "テキスト生成"
    check_credits(st.session_state.user_id, [event])
    response = openai.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "system", "content": prompt}],
    )
    content_text = response.choices[0].message.content
    db.adding_credits(user_id=st.session_state.user_id, event=event, value=culc_use_credits([event]))

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
                print(f"プロンプト{content}")
                continue

    if tales:
        # st.write(tales)
        return tales
    else:
        st.toast("文章の生成に失敗しました。")
        return ""


async def post_image_api(prompt, size=(512,512)):
    event = "イラスト生成"
    check_credits(st.session_state.user_id, [event])
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
        image.save(buffer, format="jpeg", quality=50)
        db.adding_credits(
            user_id=st.session_state.user_id, value=culc_use_credits([event]), event=event
        )
        return buffer.getvalue()
    else:
        return ""

async def generate_image(tale, title, description, theme, characters):
    print(tale)
    # Combine the individual pieces of information into a single prompt string.
    prompt = (
        const.IMAGES_PROMPT.replace("%%title_placeholder%%", title)
        .replace("%%description_placeholder%%", description)
        .replace("%%theme_placeholder%%", theme)
        .replace("%%characters_placeholder%%", characters)
        .replace("%%tale_placeholder%%", tale)
    )
    # Call post_image_api with the properly formatted prompt and the size.
    image = await post_image_api(prompt, (1024, 1024))  # Adjust the size as needed.
    return image

async def create_images(tales: dict) -> dict:
    images = {"title": "", "content": []}
    
    title = tales["title"]
    description = tales["description"]
    theme = tales["theme"]
    characters = json.dumps(tales["characters"], ensure_ascii=False)
    title_prompt = (
        const.DESCRIPTION_IMAGE_PROMPT.replace("%%title_placeholder%%", title)
        .replace("%%description_placeholder%%", description)
        .replace("%%theme_placeholder%%", theme)
        .replace("%%characters_placeholder%%", characters)
    )
    images["title"] = await post_image_api(title_prompt, (512, 512))

    # Asynchronously generate images for each item in tales["content"]
    tasks = []
    for tale in tales["content"]:
        task = asyncio.create_task(generate_image(tale, title, description, theme, characters))
        tasks.append(task)

    images["content"] = await asyncio.gather(*tasks)
    return images


def create_audios(tales):
    audios = []
    for num, tale in enumerate(tales["content"]):
        with st.spinner(f'生成中...(音声) {num+1}/{len(tales["content"])}'):
            audios.append(post_audio_api(tale))

    return audios


def post_audio_api(tale):
    event = "オーディオ生成"
    check_credits(st.session_state.user_id, [event])
    response = openai.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=tale,
    )
    db.adding_credits(user_id=st.session_state.user_id, value=culc_use_credits([event]),event=event)
    return response.content


def image_upgrade(image,characters, tale):
    event = "イラスト生成"
    check_credits(st.session_state.user_id, [event])
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
            "max_tokens": 1000,
        }
        with st.spinner("イラストを補正中..."):
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {openai.api_key}"},
                json=payload,
            ).json()
            response_text = response["choices"][0]["message"]["content"]
            prompt = (
                const.IMAGE_UP_PROMPT
                .replace("%%characters_placeholder%%", characters)
                .replace("%%tale_placeholder%%", tale + "\n\n" + response_text)
            )
            result = post_image_api(prompt, size=(1024, 1024))
            if result:
                db.adding_credits(user_id=st.session_state.user_id, value=culc_use_credits([event]),event=event)
            else:
                st.toast("イラストの補正に失敗しました。")

        return result


def create_one_tale(num):
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
                str(st.session_state.tales["number_of_pages"]),
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


def create_one_audio(num, tale):
    with st.spinner("生成中...(音声)"):
        st.session_state.audios[num] = post_audio_api(tale)


def create_one_image(num, tale):
    with st.spinner("生成中...(イラスト)"):
        result = post_image_api(
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
        if result:
            st.session_state.images["content"][num] = result
        else:
            st.toast("イラストの生成に失敗しました。テキスト内容を変更して再実行してみてください。")
