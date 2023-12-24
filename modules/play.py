import base64
import io
import streamlit as st
from modules.s3 import get_all_book_titles, get_book_data
from modules.utils import image_select_menu,create_movie_and_pdf


def pil_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return img_str


def play():
    select_book, captions = image_select_menu(
        get_all_book_titles("story-user-data", st.session_state.user_id),
        "",
    )

    if select_book:
        book_info = get_book_data(
            "story-user-data",
            st.session_state.user_id,
            captions[select_book - 1],
        )

        title = book_info["tales"]["title"]

        video_data,pdf_bytes=create_movie_and_pdf(book_info)
        st.video(video_data)
        
        st.download_button(
            label="Download data as mp4",
            data=video_data,
            file_name=f"{title}.mp4",
            mime="video/mp4",
        )
        st.download_button(
            label="Download data as PDF",
            data=pdf_bytes.getvalue(),
            file_name=f"{title}.pdf",
            mime="application/pdf",
        )
