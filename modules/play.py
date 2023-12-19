import base64

import const
import reveal_slides as rs
import streamlit as st
from modules.s3 import get_all_book_titles, get_book_data
from modules.utils import image_select_menu
from streamlit_modal import Modal


def bytes_to_base64(bytes):
    data_base64 = base64.b64encode(bytes)
    img_str = data_base64.decode("utf-8")
    return img_str


def open_main_modal(modal_place, modal2, content_markdown):
    with modal_place:
        with modal2.container():
            rs.slides(
                content_markdown,
                theme="simple",
                height=500,
                config={
                    "height": 450,
                },
                display_only=True,
            )


def play():
    modal_place = st.container()
    select_book, captions = image_select_menu(
        get_all_book_titles("story-user-data", st.session_state.user_id),
        "じぶんのえほん",
    )

    if select_book:
        book_info = get_book_data(
            "story-user-data",
            st.session_state.user_id,
            captions[select_book - 1],
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

            if num % 2 == 0:
                base_markdown = const.PAGE_MARKDOWN_RIGHT
            else:
                base_markdown = const.PAGE_MARKDOWN_LEFT

            if b64_image:
                page_markdown = base_markdown.replace(
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
        if st.button("よむ", type="primary", key="button1"):
            with modal_place:
                modal1 = Modal(
                    f'　{book_info["tales"]["title"]}',
                    key="modal1",  # Optional
                    padding=-70,
                )
                modal2 = Modal(
                    f'　{book_info["tales"]["title"]}',
                    key="modal2",  # Optional
                    padding=-70,
                )
                with modal1.container():
                    _, col1, col2, _ = st.columns([0.1, 1, 1, 0.1])
                    with col1:
                        st.image(title_image)
                    with col2:
                        st.write(f'### {book_info["tales"]["description"]}')

                        st.button(
                            "よむ",
                            type="primary",
                            on_click=open_main_modal,
                            args=(modal_place, modal2, content_markdown),
                            key="button2",
                        )
