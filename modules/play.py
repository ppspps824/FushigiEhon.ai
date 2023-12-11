import base64
from io import BytesIO

import const
import reveal_slides as rs
import streamlit as st
from modules.utils import image_select_menu
from modules.s3 import get_book_object,get_all_title


def pil_to_base64(img, format="jpeg"):
    buffer = BytesIO()
    img.save(buffer, format)
    img_str = base64.b64encode(buffer.getvalue()).decode("ascii")

    return img_str


def play():
    if "page_index" not in st.session_state:
        st.session_state.page_index = 0

    select_book, captions = image_select_menu(get_all_title())

    if select_book:
        with st.spinner("よみこみちゅう..."):
            book_info = get_book_object(
                captions[select_book-1]
            )
            # 表紙
            title = book_info["details"]["tales"]["title"]
            title_image = book_info["details"]["images"]["title"]

            tales = book_info["details"]["tales"]["content"]
            images = book_info["details"]["images"]["content"]
            audios = book_info["details"]["audios"]

            if title_image:
                b64_title_image = pil_to_base64(title_image)
                content_markdown = const.TITLE_MARKDOWN.replace(
                    "%%title_placeholder%%", title
                ).replace("%%title_image_placeholder%%", b64_title_image)
            else:
                content_markdown = const.NO_IMAGE_TITLE_MARKDOWN.replace(
                    "%%title_placeholder%%", title
                )

            for num, info in enumerate(zip(tales, images, audios)):
                tale, image, audio = info
                if image:
                    b64_image = pil_to_base64(image)
                if audio:
                    b64_audio = base64.b64encode(audio.getvalue()).decode()

                if image:
                    if st.session_state.disable_audio or not audio:
                        content = (
                            const.PAGE_MARKDOWN.replace("%%content_placeholder%%", tale)
                            .replace("%%page_image_placeholder%%", b64_image)
                            .replace("%%page_audio_placeholder%%", "")
                        )
                    else:
                        content = (
                            const.PAGE_MARKDOWN.replace("%%content_placeholder%%", tale)
                            .replace("%%page_image_placeholder%%", b64_image)
                            .replace("%%page_audio_placeholder%%", b64_audio)
                        )
                else:
                    if st.session_state.disable_audio or not audio:
                        content = const.NO_IMAGE_PAGE_MARKDOWN.replace(
                            "%%content_placeholder%%", tale
                        ).replace("%%page_audio_placeholder%%", "")
                    else:
                        content = const.NO_IMAGE_PAGE_MARKDOWN.replace(
                            "%%content_placeholder%%", tale
                        ).replace("%%page_audio_placeholder%%", b64_audio)

                content_markdown += content

            content_markdown += const.END_ROLE

            rs.slides(content_markdown, theme="solarized", display_only=True)
