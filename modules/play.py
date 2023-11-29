import base64
import io

import const
import reveal_slides as rs
import streamlit as st
from modules.s3 import s3_pickle_get
from PIL import Image
from streamlit_image_select import image_select


def reading_book(key):
    # 保存している情報を読み込み
    user_contents = s3_pickle_get(key)

    return user_contents


def play():
    if "page_index" not in st.session_state:
        st.session_state.page_index = 0
    try:
        all_image = s3_pickle_get(
            f"{st.session_state.user_id}/title_images/{st.session_state.user_id}.pickle"
        )
    except:
        all_image = {}

    captions = list(all_image.keys())
    images = [
        Image.open(io.BytesIO(data)).resize((256, 256)) for data in all_image.values()
    ]

    select_book = 0
    if images:
        select_book = (
            image_select(
                label="おはなしをえらんでね",
                images=images,
                captions=captions,
                return_value="index",
                use_container_width=False,
            )
            + 1
        )
    else:
        st.info(
            "おはなしがありません。「えほんをつくる」をおして、えほんをつくりましょう。"
        )

    if select_book:
        book_info = reading_book(
            f"{st.session_state.user_id}/book_info/{captions[select_book-1]}.pickle"
        )
        # 表紙
        title = book_info["about"]["title"]
        title_image = book_info["about"]["title_image"]
        description = book_info["about"]["description"]

        tales = book_info["details"]["tales"]["content"]
        images = book_info["details"]["images"]["content"]
        audios = book_info["details"]["audios"]

        b64_title_image = base64.b64encode(title_image).decode()
        content_markdown = (
            const.TITLE_MARKDOWN.replace("%%title_placeholder%%", title)
            .replace("%%description_placeholder%%", description)
            .replace("%%title_image_placeholder%%", b64_title_image)
        )

        for num, info in enumerate(zip(tales, images, audios)):
            tale, image, audio = info
            b64_image = base64.b64encode(image).decode()
            b64_audio = base64.b64encode(audio.getvalue()).decode()
            content = (
                const.PAGE_MARKDOWN.replace("%%content_placeholder%%", tale)
                .replace("%%page_image_placeholder%%", b64_image)
                .replace("%%page_audio_placeholder%%", b64_audio)
            )
            content_markdown += content

        content_markdown += const.END_ROLE
        response_dict = rs.slides(
            content_markdown, theme="solarized", display_only=True
        )
