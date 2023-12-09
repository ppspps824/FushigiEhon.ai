import datetime
import time
import random
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
import json
import io
from modules.s3 import s3_delete, s3_joblib_get, s3_upload
from modules.utils import image_select_menu


def view_edit(mode):
    with st.expander(f"タイトル:{st.session_state.tales['title']}", expanded=True):
        st.session_state.tales["title"] = st.text_input(
            "タイトル", value=st.session_state.tales["title"]
        )
        st.session_state.tales["description"] = st.text_area(
            "あらすじ", value=st.session_state.tales["description"]
        )
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            try:
                st.image(st.session_state.images["title"])
            except:
                st.image("assets/noimage.png")
        with col2:
            if st.button("えほんを保存する"):
                create_date = datetime.datetime.now(pytz.timezone("Asia/Tokyo"))
                create_date_yyyymdd = create_date.strftime("%Y%m%d_%H%M%S")

                book_content = {
                    "create_date": create_date_yyyymdd,
                    "details": {
                        "tales": st.session_state.tales,
                        "images": st.session_state.images,
                        "audios": st.session_state.audios,
                    },
                }
                # 保存処理
                save_book(book_content, st.session_state.tales["title"])

            if st.button("次のページを追加する", key="adding_page_button"):
                adding_page(0)

            ai_container = st.container(border=True)
            with ai_container:
                st.write("AI機能")

                if st.button("あらすじを生成する", key="description_create_button"):
                    tales_text = "\n".join(st.session_state.tales["content"])
                    with st.spinner("生成中...(あらすじ)"):
                        st.session_state.tales["description"] = post_text_api(
                            const.DESCRIPTION_PROMPT.replace(
                                "%%tales_placeholder%%", tales_text
                            ).replace(
                                "%%title_placeholder%%", st.session_state.tales["title"]
                            )
                        )
                        modify()
                        st.rerun()

                if st.button("表紙を生成する", key="title_image_create_button"):
                    with st.spinner("生成中...(イラスト)"):
                        st.session_state.images["title"] = post_image_api(
                            st.session_state.tales["description"], (720, 720)
                        )
                        modify()
                        st.rerun()
                if st.button(
                    "テキスト以外を一括で生成する", key="description_create_all"
                ):
                    book_content = create_all(ignore_tale=True)
                    save_book(book_content, st.session_state.tales["title"])
                    modify()
                    st.rerun()

                if st.button(
                    "次のページを生成する", key="adding_page_and_create_button"
                ):
                    adding_and_create_page(0)
                    st.rerun()

        with col3:
            if not mode:
                if st.button(
                    "えほんを削除する", key="delete_book_button", type="primary"
                ):
                    delete_book(st.session_state.tales["title"])

    for num, info in enumerate(
        zip(
            st.session_state.tales["content"],
            st.session_state.images["content"],
            st.session_state.audios,
        )
    ):
        tale, image, audio = info
        with st.expander(f"ページ{num + 1}: {tale}"):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                try:
                    st.image(image)
                except:
                    st.image("assets/noimage.png")
            with col2:
                st.session_state.tales["content"][num] = st.text_area(
                    "内容", key=f"{num}_tale", value=tale
                )

                try:
                    st.audio(audio)
                except:
                    pass

                if st.button("次のページを追加する", key=f"{num}_adding_page_button"):
                    adding_page(num + 1)

                ai_container = st.container(border=True)
                with ai_container:
                    st.write("AI機能")
                    if st.button(
                        "次のページを生成する",
                        key=f"{num}_adding_page_and_create_button",
                    ):
                        adding_and_create_page(num + 1)
                        st.rerun()

                    if st.button("内容を生成する", key=f"{num}_tale_create_button"):
                        create_one_tale(num)
                        st.rerun()

                    if st.button(
                        "イラストを生成する", key=f"{num}_image_create_button"
                    ):
                        create_one_image(num, tale)
                        st.rerun()

                    if st.button("音声を生成する", key=f"{num}_audio_create_button"):
                        create_one_audio(num, tale)
                        st.rerun()

            with col3:
                if st.button(
                    "ページを削除する", key=f"{num}_del_button", type="primary"
                ):
                    delete_page(num)


def create_one_audio(num, tale):
    with st.spinner("生成中...(音声)"):
        st.session_state.audios[num] = post_audio_api(tale)
    modify()


def create_one_image(num, tale):
    with st.spinner("生成中...(イラスト)"):
        st.session_state.images["content"][num] = post_image_api(
            const.IMAGES_PROMPT.replace("%%tale_placeholder%%", tale)
            .replace("%%title_placeholder%%", st.session_state.tales["title"])
            .replace(
                "%%description_placeholder%%",
                st.session_state.tales["description"],
            ),
            (512, 512),
        )

    modify()


def create_one_tale(num):
    with st.spinner("生成中...(内容)"):
        prompt = (
            const.ONE_TALE_PROMPT.replace(
                "%%title_placeholder%%", st.session_state.tales["title"]
            )
            .replace(
                "%%description_placeholder%%",
                st.session_state.tales["description"],
            )
            .replace(
                "%%page_number_placeholder%%",
                str(st.session_state.page_num),
            )
            .replace(
                "%%characters_per_page_placeholder%%",
                str(st.session_state.characters_per_page),
            )
            .replace(
                "%%using_text_types_placeholder%%",
                str(st.session_state.using_text_types),
            )
            .replace(
                "%%age_placeholder%%",
                st.session_state.age,
            )
            .replace(
                "%%pre_pages_info_placeholder%%",
                "\n".join(st.session_state.tales["content"][: num - 1]),
            )
            .replace(
                "%%post_pages_info_placeholder%%",
                "\n".join(st.session_state.tales["content"][num - 1 :]),
            )
        )
        st.session_state.tales["content"][num] = post_text_api(prompt)
        modify()


def delete_book(title):
    if title:
        with st.spinner("えほんを削除中..."):
            all_image = s3_joblib_get(
                f"{st.session_state.user_id}/title_images/{st.session_state.user_id}.joblib"
            )
            del all_image[title]

            s3_upload(
                all_image,
                f"{st.session_state.user_id}/title_images/{st.session_state.user_id}.joblib",
            )

            s3_delete(f"{st.session_state.user_id}/book_info/{title}")

            st.cache_data.clear()
            st.rerun()


def save_book(book_content, title):
    if title:
        with st.spinner("えほんを保存中..."):
            save_infos = []
            
            title_image_path=f"{st.session_state.user_id}/book_info/{title}/images/title.jpeg"
            tales_path=f"{st.session_state.user_id}/book_info/{title}/tales.json"

            bf = io.BytesIO()
            book_content["details"]["images"]["title"].save(bf, format="jpeg")
            save_infos.append(
                [
                    bf.getvalue(),
                    title_image_path
                ]
            )

            save_infos.append(
                [
                    json.dumps(
                        book_content["details"]["tales"], indent=4, ensure_ascii=False
                    ).encode(),
                    tales_path
                ],
            )

            for ix, file in enumerate(book_content["details"]["images"]["content"]):
                bf = io.BytesIO()
                file.save(bf, format="jpeg")
                bytes = bf.getvalue()
                save_infos.append(
                    [
                        bytes,
                        f"{st.session_state.user_id}/book_info/{title}/images/image_{ix}.jpeg"
                    ]
                )

            for ix, file in enumerate(book_content["details"]["audios"]):
                save_infos.append(
                    [
                        file.getvalue(),
                        f"{st.session_state.user_id}/book_info/{title}/audios/audio_{ix}.mp3"
                    ]
                )

            [s3_upload(file, path) for file, path in save_infos]

        st.info("保存しました。")
        time.sleep(0.5)
        st.cache_data.clear()
        st.rerun()
    else:
        st.info("タイトルを入力してください")


def modify():
    st.session_state.not_modify = False


def delete_page(num):
    del st.session_state.tales["content"][num]
    del st.session_state.images["content"][num]
    del st.session_state.audios[num]
    modify()
    st.rerun()


def adding_page(num):
    st.session_state.tales["content"].insert(num, "")
    st.session_state.images["content"].insert(num, "")
    st.session_state.audios.insert(num, "")
    modify()


def adding_and_create_page(num):
    adding_page(num)
    create_one_tale(num)
    create_one_image(num, st.session_state.tales["content"][num])
    create_one_audio(num, st.session_state.tales["content"][num])
    st.rerun()


def clear_session_state():
    st.session_state.tales = {"title": "", "description": "", "content": []}
    st.session_state.images = {"title": "", "content": []}
    st.session_state.audios = []
    st.session_state.not_modify = True


def create_all(only_tale=False, ignore_tale=False):
    # 生成処理
    # 物語を生成
    if ignore_tale:
        pass
    else:
        st.session_state.tales = create_tales(
            st.session_state.tales["title"],
            st.session_state.tales["description"],
            str(st.session_state.page_num),
            str(st.session_state.characters_per_page),
            st.session_state.using_text_types,
            st.session_state.age,
        )
    if only_tale:
        st.session_state.images["content"] = [
            "" for _ in range(len(st.session_state.tales["content"]))
        ]

        st.session_state.audios = [
            "" for _ in range(len(st.session_state.tales["content"]))
        ]
    else:
        # イラストを生成
        st.session_state.images = create_images(st.session_state.tales)

        # 音声を生成
        st.session_state.audios = create_audios(st.session_state.tales)

    create_date = datetime.datetime.now(pytz.timezone("Asia/Tokyo"))
    create_date_yyyymdd = create_date.strftime("%Y%m%d_%H%M%S")

    book_content = {
        "create_date": create_date_yyyymdd,
        "details": {
            "tales": st.session_state.tales,
            "images": st.session_state.images,
            "audios": st.session_state.audios,
        },
    }

    return book_content


def create_random_book_info():
    title_set_ix = random.randint(0, len(const.TITLE_SET) - 1)
    st.session_state.tales["title"] = const.TITLE_SET[title_set_ix]["title"]
    st.session_state.tales["description"] = const.TITLE_SET[title_set_ix]["description"]
    st.session_state.page_num = const.TITLE_SET[title_set_ix]["page_num"]
    st.session_state.characters_per_page = const.CHARACTORS_PER_PAGE
    st.session_state.using_text_types = const.USING_TEXT_TYPE.index(
        const.TITLE_SET[title_set_ix]["using_text_types"]
    )
    st.session_state.age = const.AGE.index(const.TITLE_SET[title_set_ix]["age"])


def create():
    mode = st.selectbox(
        "あたらしくつくる",
        options=["", "おまかせでつくる", "いちからつくる"],
        on_change=clear_session_state,
    )

    if mode == "おまかせでつくる":
        request_container = st.container(border=True)
        with request_container:
            st.write("リクエスト内容　※指定した内容で生成されないことがあります。")
            create_random_book_info()
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.session_state.page_num = st.number_input(
                    "ページ数",
                    min_value=1,
                    max_value=const.MAX_PAGE_NUM,
                    value=st.session_state.page_num,
                )
            with col2:
                st.session_state.characters_per_page = st.number_input(
                    "ページごとの文字数",
                    min_value=10,
                    max_value=100,
                    value=st.session_state.characters_per_page,
                )
            with col3:
                st.session_state.using_text_types = st.selectbox(
                    "使用文字",
                    options=const.USING_TEXT_TYPE,
                    index=st.session_state.using_text_types,
                )
            with col4:
                st.session_state.age = st.selectbox(
                    "対象年齢",
                    options=const.AGE,
                    index=st.session_state.age,
                )

            st.session_state.tales["title"] = st.text_input(
                "タイトル ※必須",
                placeholder=const.DESCRIPTION_PLACEHOLDER,
                value=st.session_state.tales["title"],
            )
            st.session_state.tales["description"] = st.text_area(
                "設定やあらすじ",
                placeholder=const.DESCRIPTION_PLACEHOLDER,
                value=st.session_state.tales["description"],
            )
            only_tale = st.toggle("テキストだけ作成する")

        if st.button("作成する"):
            if st.session_state.tales["title"] or st.session_state.tales["description"]:
                book_content = create_all(only_tale=only_tale)

                save_book(book_content, st.session_state.tales["title"])

                st.write(book_content["details"]["tales"]["title"])
                try:
                    st.image(book_content["details"]["images"]["title"])
                except:
                    st.image("assets/noimage.png")
                st.write(book_content["details"]["tales"]["description"])

            else:
                st.info("タイトルかあらすじを内容を入力してください。")

    elif mode == "いちからつくる":
        view_edit(mode)
    else:
        select_book, captions = image_select_menu()
        if select_book:
            if (
                st.session_state.not_modify
                or st.session_state.tales["title"] != captions[select_book - 1]
            ):
                book_info = s3_joblib_get(
                    f"{st.session_state.user_id}/book_info/{captions[select_book-1]}.joblib"
                )
                st.session_state.tales = book_info["details"]["tales"]
                st.session_state.images = book_info["details"]["images"]
                st.session_state.audios = book_info["details"]["audios"]
            view_edit(mode)
