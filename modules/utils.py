import streamlit as st
from modules.s3 import get_title_image
from streamlit_image_select import image_select


def image_select_menu(titles):
    try:
        all_image = {title:get_title_image(title) for title in titles}
    except Exception as e:
        print(e.args)
        all_image = {}


    images = [
        data.resize((256, 256)) if data else "assets/noimage.png"
        for data in all_image.values()
    ]

    if images:
        select_book = (
            image_select(
                label="",
                images=images,
                captions=titles,
                return_value="index",
                index=-1,
                use_container_width=False,
            )
            + 1
        )

        return select_book, captions
    else:
        st.info(
            "おはなしがありません。「えほんをつくる」をおして、えほんをつくりましょう。"
        )
        st.stop()

