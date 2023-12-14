import io

import streamlit as st
from modules.s3 import s3_download
from PIL import Image
from streamlit_image_select import image_select


def image_select_menu(titles, label):
    try:
        all_image = {
            title: s3_download(
                "story-user-data",
                f"{st.session_state.user_id}/book_info/{title}/images/title.jpeg",
            )
            for title in titles
        }
    except Exception as e:
        print(e.args)
        all_image = {}

    images = []
    for data in all_image.values():
        if data:
            # バイト型データをPIL.Imageオブジェクトに変換
            image = Image.open(io.BytesIO(data))
            # 画像のリサイズ
            resized_image = image.resize((256, 256))
            images.append(resized_image)
        else:
            images.append("assets/noimage.png")

    captions = list(all_image.keys())

    if images:
        select_book = (
            image_select(
                label=label,
                images=images,
                captions=titles,
                return_value="index",
                index=-1,
                use_container_width=False,
                key=label,
            )
            + 1
        )

        return select_book, captions
    else:
        st.info(
            "おはなしがありません。「えほんをつくる」をおして、えほんをつくりましょう。"
        )
        st.stop()
