import asyncio
import base64
import io
import json

import const
import modules.database as db
import streamlit as st
from modules.utils import culc_use_credits
from openai import AsyncOpenAI
from PIL import Image

client = AsyncOpenAI(api_key=st.secrets["OPEN_AI_KEY"])


async def post_text_api(prompt):
    event = "テキスト生成"
    response = await client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "system", "content": prompt}],
    )
    content_text = response.choices[0].message.content
    db.adding_credits(
        user_id=st.session_state.user_id, event=event, value=culc_use_credits([event])
    )

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
    for _ in range(3):
        try:
            content_text = asyncio.run(post_text_api(content))
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


async def post_image_api(prompt, user_id):
    print("async run post_image_api")
    event = "イラスト生成"
    b64_json = ""
    gen_size = "1024x1024"

    for _ in range(3):
        try:
            response = await client.images.generate(
                model=const.IMAGE_MODEL,
                prompt=prompt,
                size=gen_size,
                quality="standard",
                n=1,
                response_format="b64_json",
            )
            b64_json = response.data[0].b64_json
            break
        except Exception as e:
            print(e.args)
            return ""

    if b64_json:
        decoded_b64_json = base64.b64decode(b64_json)
        image = Image.open(io.BytesIO(decoded_b64_json))
        image = image.resize((512, 512))

        buffer = io.BytesIO()
        image.save(buffer, format="jpeg", quality=50)
        db.adding_credits(user_id=user_id, value=culc_use_credits([event]), event=event)
        return buffer.getvalue()
    else:
        return ""


async def create_images(tales: dict, user_id: str) -> dict:
    print("async run create_images")
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

    # Prepare the page prompts
    page_prompts = []
    for tale in tales["content"]:
        page_prompt = (
            const.IMAGES_PROMPT.replace("%%title_placeholder%%", title)
            .replace("%%description_placeholder%%", description)
            .replace("%%theme_placeholder%%", theme)
            .replace("%%characters_placeholder%%", characters)
            .replace("%%tale_placeholder%%", tale)
        )
        page_prompts.append(page_prompt)

    # Concurrently generate all content images
    content_image_tasks = [post_image_api(title_prompt, user_id)] + [
        post_image_api(page_prompt, user_id) for page_prompt in page_prompts
    ]
    results = await asyncio.gather(*content_image_tasks)

    images["title"] = results[0]
    images["content"] = results[1:]

    return images


async def create_audios(tales):
    content_audio_tasks = [post_audio_api(tale) for tale in tales]
    results = await asyncio.gather(*content_audio_tasks)

    return results


async def post_audio_api(tale):
    event = "オーディオ生成"
    try:
        response = await client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=tale,
        )
        db.adding_credits(
            user_id=st.session_state.user_id,
            value=culc_use_credits([event]),
            event=event,
        )
        return response.content
    except Exception:
        st.toast("エラーが発生しました。")
        return []


async def images_upgrade(images, characters, tales, user_id):
    content_image_tasks = [
        image_upgrade(image, characters, tale, user_id)
        for image, tale in zip(images, tales)
    ]

    results = await asyncio.gather(*content_image_tasks)

    images = {"title": results[0], "content": results[1:]}

    return images


async def image_upgrade(image, characters, tale, user_id):
    event = "イラスト生成"
    result = None
    if image:
        base_prompt = """
        あなたの役割は入力された画像と説明を理解し、より詳細な画像を生成するためのプロンプトテキストを生成することです。
        画像が非常に簡素なものであってもできる限りの特徴を捉え、それにあった色や背景についても最大限に想像力を働かせて表現してください。
        絵のスタイルは絵本にふさわしいポップなものにしてください。
        説明等は不要ですので、必ずプロンプトテキストのみ出力してください。"""

        response = await client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
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
            max_tokens=1000,
        )
        response_text = response.choices[0].message.content
        prompt = const.IMAGE_UP_PROMPT.replace(
            "%%characters_placeholder%%", characters
        ).replace("%%tale_placeholder%%", tale + "\n\n" + response_text)
        result = await post_image_api(prompt, user_id)
        if result:
            db.adding_credits(
                user_id=user_id,
                value=culc_use_credits([event]),
                event=event,
            )
        else:
            # Replace with appropriate error handling for your application
            print("イラストの補正に失敗しました。")

    return result


def create_one_tale(num):
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
    generated_tale = asyncio.run(post_text_api(prompt))
    if num < len(st.session_state.tales["content"]):
        st.session_state.tales["content"][num] = generated_tale
    else:
        st.session_state.tales["content"].append(generated_tale)


def create_one_audio(num, tale):
    st.session_state.audios[num] = asyncio.run(post_audio_api(tale))


def create_one_image(num, tale, user_id):
    result = asyncio.run(
        post_image_api(
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
            user_id,
        )
    )

    if result:
        st.session_state.images["content"][num] = result
    else:
        st.toast(
            "イラストの生成に失敗しました。テキスト内容を変更して再実行してみてください。"
        )
