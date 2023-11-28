import base64
import os

import const
import reveal_slides as rs
import streamlit as st
from modules.s3 import get_all_objects, s3_pickle_get


def reading_book(key):
    # 保存している情報を読み込み
    user_contents = s3_pickle_get(key)

    return user_contents


def play():
    if "page_index" not in st.session_state:
        st.session_state.page_index = 0

    st.write(f"ようこそ。{st.session_state.user_id}さん")

    book_names = [
        os.path.splitext(os.path.basename(obj.key))[0]
        for obj in iter(get_all_objects())
    ]

    select_book = st.selectbox(
        " ",
        options=book_names,
        label_visibility="collapsed",
        placeholder="おはなしをえらんでね",
        index=None,
    )

    if select_book:
        book_info = reading_book(f"{st.session_state.user_id}/{select_book}.pickle")
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
