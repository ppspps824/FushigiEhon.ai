import streamlit as st
from modules.s3 import s3_joblib_get
from streamlit_image_select import image_select


def image_select_menu():
    select_book = ""
    try:
        all_image = s3_joblib_get(
            f"{st.session_state.user_id}/title_images/{st.session_state.user_id}.joblib"
        )
    except:
        all_image = {}

    captions = list(all_image.keys())

    images = [
        data.resize((256, 256)) if data else "assets/noimage.png"
        for data in all_image.values()
    ]

    if images:
        select_book = (
            image_select(
                label="",
                images=images,
                captions=captions,
                return_value="index",
                index=-1,
                use_container_width=False,
            )
            + 1
        )

    else:
        st.info(
            "おはなしがありません。「えほんをつくる」をおして、えほんをつくりましょう。"
        )

    return select_book, captions