import datetime
import json
import random
import time

import const
import pytz
import streamlit as st
import streamlit_antd_components as sac
from modules.ai import (
    create_audios,
    create_images,
    create_tales,
    draw_image,
    post_audio_api,
    post_image_api,
    post_text_api,
)
from modules.s3 import get_all_book_titles, get_book_data, s3_delete_folder, s3_upload
from modules.utils import image_select_menu


def view_edit(mode):
    st.write("---")
    content_place = st.container()
    num = sac.pagination(
        total=len(st.session_state.tales["content"]),
        page_size=1,
        index=1,
        align="center",
        jump=True,
    )
    with content_place:
        title_col1, title_col2, title_col3 = st.columns([2, 4, 1])
        st.session_state.tales["title"] = title_col1.text_input(
            "タイトル", value=st.session_state.tales["title"]
        )
        st.session_state.tales["description"] = title_col1.text_area(
            "テーマ・メッセージ", value=st.session_state.tales["theme"]
        )
        st.session_state.tales["description"] = title_col2.text_area(
            "あらすじ", value=st.session_state.tales["description"], height=185
        )
        with title_col3:
            st.write("")
            st.write("")
            if st.button("えほんを保存する"):
                create_date = datetime.datetime.now(pytz.timezone("Asia/Tokyo"))
                create_date_yyyymdd = create_date.strftime("%Y%m%d_%H%M%S")

                book_content = {
                    "create_date": create_date_yyyymdd,
                    "tales": st.session_state.tales,
                    "title_image": st.session_state.title_image,
                    "images": st.session_state.images,
                    "audios": st.session_state.audios,
                }
                save_book(book_content, st.session_state.tales["title"])
            if st.button("えほんを削除する", key="delete_book_button", type="primary"):
                delete_book(st.session_state.tales["title"])
        if num == 1:
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                tab_name = sac.tabs(
                    [
                        sac.TabsItem(label="表示"),
                        sac.TabsItem(label="描く"),
                    ],
                    format_func="title",
                )

                if tab_name == "表示":
                    try:
                        st.image(st.session_state.title_image, width=450)
                    except:
                        st.image("assets/noimage.png")
                elif tab_name == "描く":
                    st.session_state.title_image = draw_image(
                        num="draw_title", mode="title"
                    )

            with col2:
                st.write("")
                st.write("")
                st.write("")
                if st.button("次のページを追加する", key="adding_page_button"):
                    adding_page(0)
                    st.rerun()

                ai_container = st.container(border=True)
                with ai_container:
                    st.write("AI機能")
                    if st.button(
                        "あらすじ、テーマ・メッセージを生成する",
                        key="description_create_button",
                    ):
                        tales_text = "\n".join(st.session_state.tales["content"])
                        with st.spinner("生成中...(あらすじ)"):
                            st.session_state.tales["description"] = post_text_api(
                                const.DESCRIPTION_PROMPT.replace(
                                    "%%tales_placeholder%%", tales_text
                                )
                                .replace(
                                    "%%title_placeholder%%",
                                    st.session_state.tales["title"],
                                )
                                .replace(
                                    "%%theme_placeholder%%",
                                    st.session_state.tales["theme"],
                                )
                                .replace(
                                    "%%characters_placeholder%%",
                                    json.dumps(
                                        st.session_state.tales["characters"],
                                        ensure_ascii=False,
                                    ),
                                )
                            )
                            modify()
                            st.rerun()

                    if st.button("表紙を生成する", key="title_image_create_button"):
                        title = st.session_state.tales["title"]
                        description = st.session_state.tales["description"]
                        characters = json.dumps(
                            st.session_state.tales["characters"], ensure_ascii=False
                        )
                        prompt = (
                            const.DESCRIPTION_IMAGE_PROMPT.replace(
                                "%%title_placeholder%%", title
                            )
                            .replace("%%description_placeholder%%", description)
                            .replace(
                                "%%theme_placeholder%%",
                                st.session_state.tales["theme"],
                            )
                            .replace("%%characters_placeholder%%", characters)
                        )
                        with st.spinner("生成中...(表紙)"):
                            st.session_state.title_image = post_image_api(
                                prompt, size=(512, 512)
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

        else:
            page_num = num - 1
            tale = st.session_state.tales["content"][page_num]
            image = st.session_state.images[page_num]
            audio = st.session_state.audios[page_num]
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                # ページ画像の表示
                tab1, tab2 = st.tabs(["表示", "描く"])
                with tab1:
                    try:
                        st.image(image, width=450)
                    except:
                        st.image("assets/noimage.png")
                with tab2:
                    draw_image(num=page_num, mode="page")

            with col2:
                # ページのテキスト内容の編集
                st.write("")
                st.session_state.tales["content"][page_num] = st.text_area(
                    "内容",
                    key=f"{page_num}_tale",
                    value=tale,
                    label_visibility="hidden",
                )

                # ページのオーディオの表示
                try:
                    st.audio(audio)
                except:
                    pass
                # 新しいページの追加
                if st.button(
                    "次のページを追加する", key=f"{page_num}_adding_page_button"
                ):
                    adding_page(page_num + 1)
                    st.rerun()

                ai_container = st.container(border=True)
                with ai_container:
                    st.write("AI機能")
                    col2_1, col2_2 = st.columns(2)
                    # AIによるコンテンツ生成機能
                    with col2_1:
                        if st.button(
                            "内容を生成する", key=f"{page_num}_tale_create_button"
                        ):
                            create_one_tale(page_num)
                            st.rerun()

                        if st.button(
                            "イラストを生成する", key=f"{page_num}_image_create_button"
                        ):
                            create_one_image(page_num, tale)
                            st.rerun()

                    with col2_2:
                        if st.button(
                            "音声を生成する", key=f"{page_num}_audio_create_button"
                        ):
                            create_one_audio(page_num, tale)
                            st.rerun()
                        if st.button(
                            "次のページを生成する",
                            key=f"{page_num}_adding_and_create_page_button",
                        ):
                            adding_page(page_num + 1)
                            create_one_tale(page_num + 1)
                            create_one_image(page_num + 1, tale)
                            create_one_audio(page_num + 1, tale)
                            st.rerun()

            with col3:
                # ページの削除
                st.write("")
                st.write("")
                st.write("")
                if st.button(
                    "ページを削除する", key=f"{page_num}_del_button", type="primary"
                ):
                    delete_page(page_num)


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
                "%%theme_placeholder%%",
                st.session_state.tales["theme"],
            )
            .replace(
                "%%characters_placeholder%%",
                json.dumps(st.session_state.tales["characters"], ensure_ascii=False),
            )
            .replace(
                "%%page_number_placeholder%%",
                str(num),
            )
            .replace(
                "%%characters_per_page_placeholder%%",
                str(st.session_state.characters_per_page),
            )
            .replace(
                "%%using_text_types_placeholder%%",
                st.session_state.using_text_types,
            )
            .replace(
                "%%age_placeholder%%",
                st.session_state.age,
            )
            .replace(
                "%%pre_pages_info_placeholder%%",
                "\n".join(st.session_state.tales["content"][:num]),
            )
            .replace(
                "%%post_pages_info_placeholder%%",
                "\n".join(st.session_state.tales["content"][num + 1 :]),
            )
        )
        generated_tale = post_text_api(prompt)
        if num < len(st.session_state.tales["content"]):
            st.session_state.tales["content"][num] = generated_tale
        else:
            st.session_state.tales["content"].append(generated_tale)
        modify()


def create_one_audio(num, tale):
    with st.spinner("生成中...(音声)"):
        st.session_state.audios[num] = post_audio_api(tale)
    modify()


def create_one_image(num, tale):
    with st.spinner("生成中...(イラスト)"):
        st.session_state.images[num] = post_image_api(
            const.IMAGES_PROMPT.replace("%%tale_placeholder%%", tale)
            .replace("%%title_placeholder%%", st.session_state.tales["title"])
            .replace(
                "%%description_placeholder%%", st.session_state.tales["description"]
            )
            .replace(
                "%%theme_placeholder%%",
                st.session_state.tales["theme"],
            )
            .replace(
                "%%characters_placeholder%%",
                json.dumps(st.session_state.tales["characters"], ensure_ascii=False),
            ),
            (512, 512),
        )
    modify()


def delete_book(title):
    if title:
        with st.spinner("えほんを削除中..."):
            bucket_name = "story-user-data"
            user_id = st.session_state.user_id
            s3_delete_folder(bucket_name, f"{user_id}/book_info/{title}")
            st.info("削除しました。")
            time.sleep(0.5)
            st.rerun()
    else:
        st.info("タイトルを入力してください")


def save_book(book_content, title):
    if title:
        with st.spinner("えほんを保存中..."):
            bucket_name = "story-user-data"
            user_id = st.session_state.user_id
            base_path = f"{user_id}/book_info/{title}/"

            # タイトル画像の保存
            title_image_path = base_path + "images/title.jpeg"
            title_image = book_content["title_image"]
            s3_upload(bucket_name, title_image, title_image_path)

            # 物語の内容（tales.json）の保存
            tales_path = base_path + "tales.json"
            tales_data = json.dumps(
                book_content["tales"], indent=4, ensure_ascii=False
            ).encode()
            s3_upload(bucket_name, tales_data, tales_path)

            # ページ毎の画像とオーディオの保存
            for ix, (image, audio) in enumerate(
                zip(book_content["images"], book_content["audios"])
            ):
                image_path = base_path + f"images/image_{ix}.jpeg"
                audio_path = base_path + f"audios/audio_{ix}.mp3"
                s3_upload(bucket_name, image, image_path)
                s3_upload(bucket_name, audio, audio_path)

            st.info("保存しました。")
    else:
        st.info("タイトルを入力してください")


def modify():
    st.session_state.not_modify = False


def delete_page(num):
    # 物語の内容から指定されたページを削除
    if num < len(st.session_state.tales["content"]):
        del st.session_state.tales["content"][num]

    # タイトル画像以外の画像から指定されたページを削除
    if num < len(st.session_state.images):
        del st.session_state.images[num]

    # オーディオから指定されたページを削除
    if num < len(st.session_state.audios):
        del st.session_state.audios[num]

    modify()
    st.rerun()


def adding_page(num):
    # 物語の内容に空のページを追加
    st.session_state.tales["content"].insert(num, "")

    # 画像に空のページを追加
    st.session_state.images.insert(num, "")

    # オーディオに空のページを追加
    st.session_state.audios.insert(num, "")

    modify()


def adding_and_create_page(num):
    adding_page(num)
    create_one_tale(num)
    create_one_image(num, st.session_state.tales["content"][num])
    create_one_audio(num, st.session_state.tales["content"][num])
    st.rerun()


def clear_session_state():
    st.session_state.page_num = const.PAGE_NUM
    st.session_state.characters_per_page = const.CHARACTORS_PER_PAGE
    st.session_state.using_text_types = "ひらがなのみ"
    st.session_state.age = "1～2歳"
    st.session_state.tales = {
        "title": "",
        "description": "",
        "theme": "",
        "characters": {
            "lead": {"name": "", "appearance": ""},
            "others": [
                {"name": "", "appearance": ""},
            ],
        },
        "content": [],
    }
    st.session_state.title_image = ""
    st.session_state.images = []
    st.session_state.audios = []
    st.session_state.not_modify = True


def create_all(only_tale=False, ignore_tale=False):
    if ignore_tale:
        pass
    else:
        st.session_state.tales = create_tales(
            st.session_state.tales["title"],
            st.session_state.tales["description"],
            st.session_state.tales["theme"],
            str(st.session_state.page_num),
            str(st.session_state.characters_per_page),
            st.session_state.using_text_types,
            st.session_state.age,
        )

    if only_tale:
        st.session_state.images = {
            "title": "",
            "content": ["" for _ in st.session_state.tales],
        }
        st.session_state.audios = ["" for _ in st.session_state.tales]
    else:
        st.session_state.images = create_images(st.session_state.tales)
        st.session_state.audios = create_audios(st.session_state.tales)

    create_date = datetime.datetime.now(pytz.timezone("Asia/Tokyo"))
    create_date_yyyymdd = create_date.strftime("%Y%m%d_%H%M%S")

    book_content = {
        "create_date": create_date_yyyymdd,
        "tales": st.session_state.tales,
        "title_image": st.session_state.images["title"],
        "images": st.session_state.images["content"],
        "audios": st.session_state.audios,
    }

    return book_content


def create_random_book_info():
    title_set_ix = random.randint(0, len(const.TITLE_SET) - 1)
    st.session_state.tales["title"] = const.TITLE_SET[title_set_ix]["title"]
    st.session_state.tales["description"] = const.TITLE_SET[title_set_ix]["description"]
    st.session_state.tales["theme"] = const.TITLE_SET[title_set_ix]["theme"]
    st.session_state.page_num = const.TITLE_SET[title_set_ix]["page_num"]
    st.session_state.characters_per_page = const.CHARACTORS_PER_PAGE
    st.session_state.using_text_types = const.TITLE_SET[title_set_ix][
        "using_text_types"
    ]
    st.session_state.age = const.TITLE_SET[title_set_ix]["age"]


def create():
    mode = st.selectbox(
        "あたらしくつくる",
        options=["", "おまかせでつくる", "いちからつくる"],
        on_change=clear_session_state,
    )

    if mode == "おまかせでつくる":
        if st.button("ランダム生成"):
            create_random_book_info()
        with st.form(" ", border=True):
            st.write("リクエスト内容　※指定した内容で生成されないことがあります。")
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
                    index=const.USING_TEXT_TYPE.index(
                        st.session_state.using_text_types
                    ),
                )
            with col4:
                st.session_state.age = st.selectbox(
                    "対象年齢",
                    options=const.AGE,
                    index=const.AGE.index(st.session_state.age),
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
            st.session_state.tales["theme"] = st.text_area(
                "テーマ・メッセージメッセージ",
                placeholder=const.THEME_PLACEHOLDER,
                value=st.session_state.tales["theme"],
            )
            only_tale = st.toggle("テキストだけ作成する")

            submit = st.form_submit_button("生成開始")

        if submit:
            if st.session_state.tales["title"] or st.session_state.tales["description"]:
                book_content = create_all(only_tale=only_tale)

                save_book(book_content, st.session_state.tales["title"])

                st.write(book_content["tales"]["title"])
                try:
                    st.image(book_content["title_image"])
                except:
                    st.image("assets/noimage.png")
                st.write(book_content["tales"]["description"])

            else:
                st.info("タイトルかあらすじを内容を入力してください。")

    elif mode == "いちからつくる":
        clear_session_state()
        view_edit(mode)
    else:
        select_book, captions = image_select_menu(
            get_all_book_titles(
                "story-user-data",
                st.session_state.user_id,
            ),
        )
        if select_book:
            if (
                st.session_state.not_modify
                or st.session_state.tales["title"] != captions[select_book - 1]
            ):
                book_info = get_book_data(
                    "story-user-data",
                    st.session_state.user_id,
                    captions[select_book - 1],
                )
                st.session_state.tales["title"] = book_info["tales"]["title"]
                st.session_state.tales["description"] = book_info["tales"][
                    "description"
                ]
                st.session_state.tales["content"] = book_info["tales"]["content"]
                st.session_state.title_image = book_info["title_image"]
                st.session_state.images = book_info["images"]
                st.session_state.audios = book_info["audios"]
            view_edit(mode)
