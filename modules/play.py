import base64

import const
import reveal_slides as rs
import streamlit as st
from modules.s3 import get_all_book_titles, get_book_data
from modules.utils import image_select_menu


def bytes_to_base64(bytes):
    data_base64 = base64.b64encode(bytes)
    img_str = data_base64.decode("utf-8")
    return img_str


def play():
    if "page_index" not in st.session_state:
        st.session_state.page_index = 0
    with st.container(border=True):
        select_book, captions = image_select_menu(
            get_all_book_titles("story-user-data", st.session_state.user_id),
            "じぶんのえほん",
        )
    with st.container(border=True):
        select_book, captions = image_select_menu(
            get_all_book_titles("story-user-data", st.session_state.user_id),
            "あたらしいえほん",
        )
    with st.container(border=True):
        select_book, captions = image_select_menu(
            get_all_book_titles("story-user-data", st.session_state.user_id),
            "にんきのえほん",
        )
    with st.container(border=True):
        st.write("えほんをさがす")
        with st.form("search"):
            search_title = st.text_input("たいとる")
            col2_1, col2_2 = st.columns(2)
            with col2_1:
                search_age_group = st.selectbox(
                    "ねんれいべつ", options=[""] + const.AGE_GROUP
                )
            with col2_2:
                search_character_set = st.selectbox(
                    "もじのしゅるい", options=[""] + const.CHARACTER_SET
                )
            search_submit = st.form_submit_button("さがす")
        if search_submit:
            select_book, captions = image_select_menu(
                get_all_book_titles("story-user-data", st.session_state.user_id),
                "けんかくけっか",
            )

    if select_book:
        with st.spinner("よみこみちゅう..."):
            book_info = get_book_data(
                "story-user-data", st.session_state.user_id, captions[select_book - 1]
            )
            title = book_info["tales"]["title"]
            title_image = book_info["images"]["title"]
            tales = book_info["tales"]["content"]
            images = book_info["images"]["content"]
            audios = book_info["audios"]

            content_markdown = ""
            if title_image:
                b64_title_image = bytes_to_base64(title_image)
                content_markdown += const.TITLE_MARKDOWN.replace(
                    "%%title_placeholder%%", title
                ).replace("%%title_image_placeholder%%", b64_title_image)
            else:
                content_markdown += const.NO_IMAGE_TITLE_MARKDOWN.replace(
                    "%%title_placeholder%%", title
                )
            for num, (tale, image, audio) in enumerate(zip(tales, images, audios)):
                page_content = tale
                b64_image = bytes_to_base64(image) if image else ""
                b64_audio = base64.b64encode(audio).decode() if audio else ""

                if b64_image:
                    page_markdown = const.PAGE_MARKDOWN.replace(
                        "%%content_placeholder%%", page_content
                    )
                    page_markdown = page_markdown.replace(
                        "%%page_image_placeholder%%", b64_image or ""
                    )
                    page_markdown = page_markdown.replace(
                        "%%page_audio_placeholder%%", b64_audio
                    )
                else:
                    page_markdown = const.NO_IMAGE_PAGE_MARKDOWN.replace(
                        "%%content_placeholder%%", page_content
                    )
                    page_markdown = page_markdown.replace(
                        "%%page_audio_placeholder%%", b64_audio
                    )

                content_markdown += page_markdown

            content_markdown += const.END_ROLE

            rs.slides(content_markdown, theme="solarized", display_only=True)
