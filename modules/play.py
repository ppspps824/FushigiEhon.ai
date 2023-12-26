import base64
import io

import const
import streamlit as st
import streamlit.components.v1 as components
from modules.s3 import get_all_book_titles, get_book_data, s3_download
from modules.utils import image_select_menu


def pil_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return img_str


def play():
    select_book, captions = image_select_menu(
        get_all_book_titles(
            "story-user-data",
            const.TITLE_BASE_PATH.replace("%%user_id%%", st.session_state.user_id),
        ),
        "",
    )

    if select_book:
        with st.spinner("よみこみちゅう..."):
            book_info = get_book_data(
                "story-user-data",
                st.session_state.user_id,
                captions[select_book - 1],
            )

            title = book_info["tales"]["title"]

            video_data = s3_download(
                "story-user-data",
                f'{const.BASE_PATH.replace("%%user_id%%", st.session_state.user_id).replace("%%title%%", title)}{title}.mp4',
            )

            pdf_data = s3_download(
                "story-user-data",
                f'{const.BASE_PATH.replace("%%user_id%%", st.session_state.user_id).replace("%%title%%", title)}{title}.pdf',
            )
            st.video(video_data)

            components.html(const.POST_HTML.replace("%%title_placeholder%%", title))

            st.download_button(
                label="動画を保存",
                data=video_data,
                file_name=f"{title}.mp4",
                mime="video/mp4",
            )
            st.download_button(
                label="PDFを保存",
                data=pdf_data,
                file_name=f"{title}.pdf",
                mime="application/pdf",
            )
