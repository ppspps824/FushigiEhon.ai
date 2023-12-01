import base64

import const
import reveal_slides as rs
import streamlit as st
from modules.utils import image_select_menu, reading_book


def play():
    if "page_index" not in st.session_state:
        st.session_state.page_index = 0

    select_book, captions = image_select_menu()

    if select_book:
        with st.spinner("よみこみちゅう..."):
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
                if st.session_state.disable_audio:
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

                content_markdown += content

            content_markdown += const.END_ROLE

            rs.slides(content_markdown, theme="solarized", display_only=True)
