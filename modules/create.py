import datetime
import os

import const
import pytz
import streamlit as st
from modules.ai import (
    create_audios,
    create_images,
    create_tales,
    post_audio_api,
    post_image_api,
    post_text_api,
)
from modules.play import reading_book
from modules.s3 import get_all_objects, s3_pickle_get, s3_upload


def view_edit():
    with st.expander(f"タイトル:{st.session_state.title}"):
        st.session_state.title = st.text_input("タイトル", value=st.session_state.title)
        st.session_state.description = st.text_area(
            "あらすじ", value=st.session_state.description
        )
        try:
            st.image(st.session_state.title_image)
        except:
            pass

        if st.button("あらすじを生成する", key="description_create_button"):
            tales_text = "\n".join(st.session_state.tales)
            with st.spinner("生成中...(あらすじ)"):
                st.session_state.description = post_text_api(
                    const.DESCRIPTION_PROMPT.replace(
                        "%%tales__placeholder%%", tales_text
                    ).replace("%%title_placeholder%%", st.session_state.title),
                    response_format=None,
                )
                modify()

        if st.button("表紙を生成する", key="title_image_create_button"):
            with st.spinner("生成中...(イラスト)"):
                st.session_state.title_image = post_image_api(
                    st.session_state.description, (720, 720)
                )
                modify()

    for num, info in enumerate(
        zip(
            st.session_state.tales,
            st.session_state.images,
            st.session_state.audios,
        )
    ):
        tale, image, audio = info
        with st.expander(f"ページ{num + 1}: {tale}"):
            col1, col2 = st.columns(2)
            with col1:
                try:
                    st.image(image)
                except:
                    pass
            with col2:
                st.session_state.tales[num] = st.text_area(
                    "内容", key=f"{num}_tale", value=tale
                )
                if st.button("イラストを生成する", key=f"{num}_image_create_button"):
                    with st.spinner("生成中...(イラスト)"):
                        st.session_state.images[num] = post_image_api(
                            const.IMAGES_PROMPT.replace("%%tale_placeholder%%", tale)
                            .replace("%%title_placeholder%%", st.session_state.title)
                            .replace(
                                "%%description_placeholder%%",
                                st.session_state.description,
                            ),
                            (512, 512),
                        )

                    modify()

                if st.button("音声を生成する", key=f"{num}_audio_create_button"):
                    with st.spinner("生成中...(音声)"):
                        st.session_state.audios[num] = post_audio_api(tale)

                    modify()

                st.button(
                    "削除",
                    key=f"{num}_del_button",
                    on_click=delete_page,
                    args=(num,),
                )

            try:
                st.audio(audio)
            except:
                pass

    st.button("ページを追加", on_click=adding_page)

    if st.button("保存する"):
        create_date = datetime.datetime.now(pytz.timezone("Asia/Tokyo"))
        create_date_yyyymdd = create_date.strftime("%Y%m%d_%H%M%S")
        book_about = {
            "create_date": create_date_yyyymdd,
            "title": st.session_state.title,
            "title_image": st.session_state.title_image,
            "description": st.session_state.description,
        }

        book_content = {
            "about": book_about,
            "details": {
                "tales": {"content": st.session_state.tales},
                "images": {"content": st.session_state.images},
                "audios": st.session_state.audios,
            },
        }

        # 保存処理
        save_book(book_content, st.session_state.title)


def save_book(book_content, title):
    try:
        all_image = s3_pickle_get(
            f"{st.session_state.user_id}/title_images/{st.session_state.user_id}.pickle"
        )
        all_image[title] = book_content["about"]["title_image"]
    except Exception as e:
        print(e.args)
        all_image = {title: book_content["about"]["title_image"]}

    s3_upload(
        all_image,
        f"{st.session_state.user_id}/title_images/{st.session_state.user_id}.pickle",
    )

    s3_upload(
        book_content,
        f"{st.session_state.user_id}/book_info/{title}.pickle",
    )
    st.info("保存しました。")


def modify():
    st.session_state.not_modify = False


def delete_page(num):
    del st.session_state.tales[num]
    del st.session_state.images[num]
    del st.session_state.audios[num]
    modify()


def adding_page():
    st.session_state.tales.append("")
    st.session_state.images.append("")
    st.session_state.audios.append("")
    modify()


def clear_session_state():
    st.session_state.title = ""
    st.session_state.title_image = ""
    st.session_state.description = ""
    st.session_state.tales = []
    st.session_state.images = []
    st.session_state.audios = []
    st.session_state.not_modify = True


def create():
    page_infos = []

    mode = st.selectbox(
        "つくりかた",
        options=["おまかせでつくる", "いちからつくる", "つくりなおす"],
        on_change=clear_session_state,
    )
    col1, col2 = st.columns(2)

    if mode == "おまかせでつくる":
        with col1:
            page_num = st.number_input(
                "ページ数", min_value=1, max_value=const.MAX_PAGE_NUM, value=5
            )
        with col2:
            characters_per_page = st.number_input(
                "ページごとの文字数", min_value=10, max_value=100, value=40
            )

        title = st.text_input("タイトル", placeholder=const.DESCRIPTION_PLACEHOLDER)
        description = st.text_area(
            "設定やあらすじ", placeholder=const.DESCRIPTION_PLACEHOLDER
        )

        if st.button("作成する"):
            if title or description:
                # 生成処理
                # 物語を生成
                tales = create_tales(
                    title,
                    description,
                    str(page_num),
                    str(characters_per_page),
                    page_infos,
                )

                # イラストを生成
                images = create_images(tales)

                # 音声を生成
                audios = create_audios(tales)

                create_date = datetime.datetime.now(pytz.timezone("Asia/Tokyo"))
                create_date_yyyymdd = create_date.strftime("%Y%m%d_%H%M%S")
                book_about = {
                    "create_date": create_date_yyyymdd,
                    "title": tales.get("title"),
                    "title_image": images.get("title"),
                    "description": tales.get("description"),
                }

                book_content = {
                    "about": book_about,
                    "details": {
                        "tales": tales,
                        "images": images,
                        "audios": audios,
                    },
                }

                save_book(book_content, tales.get("title"))

                st.write(book_about["title"])
                st.image(book_about["title_image"])
                st.write(book_about["description"])

            else:
                st.info("タイトルかあらすじを内容を入力してください。")

    if mode in ["いちからつくる", "つくりなおす"]:
        if mode == "つくりなおす":
            book_names = [
                os.path.splitext(os.path.basename(obj.key))[0]
                for obj in iter(get_all_objects())
            ]

            book_names = [book_name for book_name in book_names if book_name]

            select_book = st.selectbox(
                " ",
                options=book_names,
                label_visibility="collapsed",
                placeholder="絵本を選ぶ",
                index=None,
            )

            if select_book:
                if st.session_state.not_modify or st.session_state.title != select_book:
                    book_info = reading_book(
                        f"{st.session_state.user_id}/book_info/{select_book}.pickle"
                    )
                    st.session_state.title = book_info["about"]["title"]
                    st.session_state.title_image = book_info["about"]["title_image"]
                    st.session_state.description = book_info["about"]["description"]

                    st.session_state.tales = book_info["details"]["tales"]["content"]
                    st.session_state.images = book_info["details"]["images"]["content"]
                    st.session_state.audios = book_info["details"]["audios"]

                view_edit()
        else:
            view_edit()
