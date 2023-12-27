import base64
import io
import const
import streamlit as st
import streamlit.components.v1 as components
from modules.s3 import get_all_book_titles, get_book_data, s3_download
from modules.utils import get_images,add_caption_transparent


def pil_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return img_str

    
def play():
    images, captions = get_images(
        get_all_book_titles(
            "story-user-data",
            const.TITLE_BASE_PATH.replace("%%user_id%%", st.session_state.user_id),
        ),
        st.session_state.user_id,
    )
    guest_images, guest_captions = get_images(
        get_all_book_titles(
            "story-user-data",
            const.TITLE_BASE_PATH.replace("%%user_id%%", "guest"),
        ),
        "guest",
    )

    imageCarouselComponent = components.declare_component(
        "image-carousel-component", path="frontend/public"
    )

    images = [add_caption_transparent(image,caption) for image,caption in zip(images,captions)]
    guest_images = [add_caption_transparent(image,caption) for image,caption in zip(guest_images,guest_captions)]

    captions+=guest_captions
    captions=sorted(set(captions), key=captions.index)

    imageUrls = [
        f"data:image/png;base64,{base64.b64encode(image).decode()}" for image in images
    ]
    guest_imageUrls = [
        f"data:image/png;base64,{base64.b64encode(image).decode()}"
        for image in guest_images
    ]

    imageUrls += guest_imageUrls
    imageUrls = sorted(set(imageUrls), key=imageUrls.index)

    selectedImageUrl = imageCarouselComponent(imageUrls=imageUrls, height=200)

    is_guest = selectedImageUrl in guest_imageUrls

    if selectedImageUrl:
        select_book = imageUrls.index(selectedImageUrl) + 1
        book_info = get_book_data(
            "story-user-data",
            st.session_state.user_id,
            captions[select_book - 1],
            is_guest=is_guest,
        )

        title = book_info["tales"]["title"]

        video_data = s3_download(
            "story-user-data",
            f'{const.BASE_PATH.replace("%%user_id%%", "guest").replace("%%title%%", title)}{title}.mp4'
            if is_guest
            else f'{const.BASE_PATH.replace("%%user_id%%", st.session_state.user_id).replace("%%title%%", title)}{title}.mp4',
        )

        pdf_data = s3_download(
            "story-user-data",
            f'{const.BASE_PATH.replace("%%user_id%%", "guest").replace("%%title%%", title)}{title}.pdf'
            if is_guest
            else f'{const.BASE_PATH.replace("%%user_id%%", st.session_state.user_id).replace("%%title%%", title)}{title}.pdf',
        )
        if video_data:
            st.video(video_data)
            cols=st.columns([2,2,1,1])
            with cols[0]:
                components.html(const.X_SHARE_HTML.replace("%%title%%",title))
            with cols[1]:
                components.html(const.FB_SHARE_HTML.replace("%%title%%",title))
            
            with cols[2]:
                st.download_button(
                    label="動画を保存",
                    data=video_data,
                    file_name=f"{title}.mp4",
                    mime="video/mp4",
                )
        else:
            st.error("データの読み込みに失敗しました。")

        if pdf_data:
            with cols[3]:
                st.download_button(
                    label="PDFを保存",
                    data=pdf_data,
                    file_name=f"{title}.pdf",
                    mime="application/pdf",
                )
