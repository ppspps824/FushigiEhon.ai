import base64
import datetime
import io
import json

import const
import pytz
import streamlit as st
import streamlit.components.v1 as components
import streamlit_antd_components as sac
import streamlit_shadcn_ui as ui
from modules.ai import (
    create_audios,
    create_images,
    create_one_audio,
    create_one_image,
    create_one_tale,
    create_tales,
    image_upgrade,
    post_image_api,
    post_text_api,
)
from modules.s3 import get_all_book_titles, get_book_data, s3_delete_folder, s3_upload
from modules.utils import (
    add_caption_transparent,
    create_movie_and_pdf,
    get_images,
    hide_overlay,
    show_overlay,
)
from PIL import Image

# from streamlit_lottie import st_lottie_spinnerf

def view_edit():
    st.write("---")
    content_place = st.container()
    total_page = len(st.session_state.tales["content"]) + 1
    num = sac.pagination(
        total=total_page if total_page > 1 else 1,
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
        st.session_state.tales["theme"] = title_col1.text_area(
            "テーマ・メッセージ", value=st.session_state.tales["theme"]
        )
        st.session_state.tales["description"] = title_col2.text_area(
            "あらすじ", value=st.session_state.tales["description"], height=185
        )

        with st.expander("キャラクター", expanded=True):
            chara_col1, chara_col2 = st.columns(2)
            with chara_col1:
                st.session_state.tales["characters"]["lead"]["name"] = st.text_input(
                    "主人公の名前",
                    placeholder=const.RAMDOM_PLACEHOLDER,
                    value=st.session_state.tales["characters"]["lead"]["name"],
                )
                st.session_state.tales["characters"]["lead"][
                    "appearance"
                ] = st.text_area(
                    "主人公の見た目",
                    placeholder=const.RAMDOM_PLACEHOLDER,
                    value=st.session_state.tales["characters"]["lead"]["appearance"],
                )
                if st.button("キャラクターを追加"):
                    st.session_state.tales["characters"]["others"].append(
                        {"name": "", "appearance": ""}
                    )
                    st.rerun()

            with chara_col2:
                if not st.session_state.tales["characters"].get("others"):
                    st.session_state.tales["characters"]["others"] = [
                        {"name": "", "appearance": ""}
                    ]

                chara_num_list = range(
                    len(st.session_state.tales["characters"]["others"])
                )

                chara_tabs = st.tabs([str(num + 1) for num in chara_num_list])
                for chara_num in chara_num_list:
                    with chara_tabs[chara_num]:
                        st.session_state.tales["characters"]["others"][chara_num][
                            "name"
                        ] = st.text_input(
                            "名前",
                            placeholder=const.RAMDOM_PLACEHOLDER,
                            value=st.session_state.tales["characters"]["others"][
                                chara_num
                            ]["name"],
                            key=f"chara_name{chara_num}",
                        )
                        st.session_state.tales["characters"]["others"][chara_num][
                            "appearance"
                        ] = st.text_area(
                            "見た目",
                            placeholder=const.RAMDOM_PLACEHOLDER,
                            value=st.session_state.tales["characters"]["others"][
                                chara_num
                            ]["appearance"],
                            key=f"chara_appearance{chara_num}",
                        )
                if st.button("削除"):
                    st.session_state.tales["characters"]["others"].pop(chara_num)
                    st.rerun()

        bgm = st.selectbox("BGM", options=const.BGM_LIST)
        if bgm:
            st.audio(f"assets/{bgm}.mp3")

        with title_col3:
            st.write("")
            st.write("")
            if st.button("えほんを保存する", help="変更した内容でえほんを保存します。",disabled=st.session_state.is_guest):
                create_date = datetime.datetime.now(pytz.timezone("Asia/Tokyo"))
                create_date_yyyymdd = create_date.strftime("%Y%m%d_%H%M%S")

                book_content = {
                    "create_date": create_date_yyyymdd,
                    "tales": st.session_state.tales,
                    "images": st.session_state.images,
                    "audios": st.session_state.audios,
                }
                show_overlay()
                save_book(book_content, st.session_state.tales["title"], bgm)
                modify()
                hide_overlay()
                st.rerun()

            book_trigger_btn = ui.button(
                text="えほんを削除する", key="book_trigger_btn",disabled=st.session_state.is_guest
            )
            if ui.alert_dialog(
                show=book_trigger_btn,
                title="えほんを削除する",
                description="本当に削除しますか",
                confirm_label="はい",
                cancel_label="いいえ",
                key="alert_dialog_book",
            ):
                delete_book(st.session_state.tales["title"])
                modify()

        with st.container(border=True):
            if num == 1:
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    try:
                        st.image(
                            st.session_state.images["title"], use_column_width="auto"
                        )
                    except:
                        st.image("assets/noimage.png", use_column_width="auto")

                    title_upload_file = st.file_uploader(
                        "画像をアップロード",
                        key="title_upload_file",
                        type=["png", "jpg"],
                    )
                    if title_upload_file:
                        if st.button("取り込み", key="title_upload_file_button"):
                            st.session_state.images[
                                "title"
                            ] = title_upload_file.getvalue()
                            modify()
                            st.rerun()

                with col2:
                    ai_container = st.container(border=True)
                    with ai_container:
                        st.write("AI機能")

                        if st.button("あらすじ、テーマ・メッセージを生成する",disabled=st.session_state.is_guest):
                            show_overlay()
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
                                hide_overlay()
                            st.rerun()

                        if st.button(
                            "次のページを生成する",
                            disabled=st.session_state.is_guest,
                            help="次のページの文章、イラスト、音声をAIによって生成します。",
                        ):
                            show_overlay()
                            adding_page(0)
                            create_one_tale(0)
                            create_one_image(0, st.session_state.tales["content"][0])
                            create_one_audio(0, st.session_state.tales["content"][0])
                            hide_overlay()
                            modify()
                            st.rerun()

                        if st.button("表紙を生成する",disabled=st.session_state.is_guest):
                            show_overlay()
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
                                st.session_state.images["title"] = post_image_api(
                                    prompt, size=(512, 512)
                                )
                            modify()
                            hide_overlay()

                            st.rerun()

                        if st.button("表紙を補正する",disabled=st.session_state.is_guest):
                            show_overlay()
                            st.session_state.images["title"] = image_upgrade(
                                st.session_state.images["title"],
                                st.session_state.tales["title"],
                                st.session_state.tales["description"],
                                st.session_state.tales["theme"],
                                json.dumps(st.session_state.tales["characters"]),
                                json.dumps(st.session_state.tales["content"]),
                            )
                            modify()
                            hide_overlay()
                            st.rerun()

                        if st.button("表紙を削除する"):
                            st.session_state.images["title"] = ""
                            modify()
                            st.rerun()
                        with st.container(border=True):
                            st.caption("全ページ一括処理")
                            if st.button("テキスト以外を一括で生成する",disabled=st.session_state.is_guest):
                                show_overlay()
                                book_content = create_all(ignore_tale=True)
                                save_book(book_content, st.session_state.tales["title"])
                                modify()
                                hide_overlay()
                                st.rerun()

                            if st.button("音声を一括で生成する",disabled=st.session_state.is_guest):
                                show_overlay()
                                for num, tale in enumerate(
                                    st.session_state.tales["content"]
                                ):
                                    create_one_audio(num, tale)

                                modify()
                                hide_overlay()
                                st.rerun()
                            if st.button("イラストを一括で生成する",disabled=st.session_state.is_guest):
                                show_overlay()
                                st.session_state.images["title"] = post_image_api(
                                    st.session_state.images["title"],
                                    st.session_state.tales["title"],
                                    st.session_state.tales["description"],
                                    st.session_state.tales["theme"],
                                    json.dumps(st.session_state.tales["characters"]),
                                    json.dumps(st.session_state.tales["content"]),
                                )

                                for num, image in enumerate(
                                    st.session_state.images["content"]
                                ):
                                    st.session_state.images["content"][
                                        num
                                    ] = post_image_api(
                                        image,
                                        st.session_state.tales["title"],
                                        st.session_state.tales["description"],
                                        st.session_state.tales["theme"],
                                        json.dumps(
                                            st.session_state.tales["characters"]
                                        ),
                                        json.dumps(st.session_state.tales["content"]),
                                    )

                                modify()
                                hide_overlay()
                                st.rerun()

                            if st.button("イラストを一括で補正する",disabled=st.session_state.is_guest):
                                show_overlay()
                                st.session_state.images["title"] = image_upgrade(
                                    st.session_state.images["title"],
                                    st.session_state.tales["title"],
                                    st.session_state.tales["description"],
                                    st.session_state.tales["theme"],
                                    json.dumps(st.session_state.tales["characters"]),
                                    json.dumps(st.session_state.tales["content"]),
                                )

                                for num, image in enumerate(
                                    st.session_state.images["content"]
                                ):
                                    st.session_state.images["content"][
                                        num
                                    ] = image_upgrade(
                                        image,
                                        st.session_state.tales["title"],
                                        st.session_state.tales["description"],
                                        st.session_state.tales["theme"],
                                        json.dumps(
                                            st.session_state.tales["characters"]
                                        ),
                                        json.dumps(st.session_state.tales["content"]),
                                    )

                                modify()
                                hide_overlay()
                                st.rerun()
                            with st.expander("画像を一括でアップロード"):
                                image_files = st.file_uploader(
                                    "",
                                    label_visibility="collapsed",
                                    accept_multiple_files=True,
                                    type=["png", "jpg"],
                                )
                                if image_files:
                                    st.image(image_files)

                                    if st.button("取り込み", key="all_image_upload"):
                                        show_overlay()
                                        with st.spinner("取り込み中..."):
                                            adding_num = len(image_files) - len(
                                                st.session_state.images["content"]
                                            )
                                            if adding_num > 0:
                                                [
                                                    adding_page(num)
                                                    for num in range(
                                                        len(
                                                            st.session_state.images[
                                                                "content"
                                                            ]
                                                        )
                                                        + adding_num
                                                    )
                                                ]
                                            for num, image in enumerate(image_files):
                                                image = Image.open(
                                                    io.BytesIO(image.getvalue())
                                                )
                                                image = image.resize((512, 512))
                                                # 空のバイトストリームを作成
                                                bytes_io = io.BytesIO()
                                                image.save(bytes_io, format="PNG")
                                                bytes_data = bytes_io.getvalue()
                                                st.session_state.images["content"][
                                                    num
                                                ] = bytes_data

                                            modify()
                                            hide_overlay()
                                            st.rerun()
                with col3:
                    if st.button(
                        "次のページを追加する",
                        help="空のページを後ろに追加します。",
                        key="adding_page_button",
                    ):
                        adding_page(0)
                        st.rerun()
            else:
                page_count = num - 2
                tale = st.session_state.tales["content"][page_count]
                image = st.session_state.images["content"][page_count]
                audio = st.session_state.audios[page_count]
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    try:
                        st.image(image, use_column_width="auto")
                    except:
                        st.image("assets/noimage.png", use_column_width="auto")
                    page_upload_file = st.file_uploader(
                        "画像をアップロード",
                        type=["png", "jpg"],
                        key=f"page_upload_file_{page_count}",
                    )
                    if page_upload_file:
                        if st.button("取り込み", key="page_upload_file_button"):
                            st.session_state.images["content"][
                                page_count
                            ] = page_upload_file.getvalue()
                            modify()
                            st.rerun()

                with col2:
                    # ページのテキスト内容の編集
                    st.session_state.tales["content"][page_count] = st.text_area(
                        "内容",
                        key=f"{page_count}_tale",
                        value=tale,
                        label_visibility="collapsed",
                    )

                    # ページのオーディオの表示
                    try:
                        st.audio(audio)
                    except:
                        pass

                    with st.container(border=True):
                        st.write("AI機能")
                        # AIによるコンテンツ生成機能
                        if st.button(
                            "次のページを生成する",
                            help="次のページの文章、イラスト、音声をAIによって生成します。",
                            disabled=st.session_state.is_guest
                        ):
                            show_overlay()
                            adding_page(page_count + 1)
                            create_one_tale(page_count + 1)
                            create_one_image(page_count + 1, tale)
                            create_one_audio(page_count + 1, tale)
                            modify()
                            hide_overlay()
                            st.rerun()
                        if st.button(
                            "内容を生成する",
                            help="このページの文章を、AIによって生成します。",
                            disabled=st.session_state.is_guest
                        ):
                            show_overlay()
                            create_one_tale(page_count)
                            modify()
                            hide_overlay()
                            st.rerun()

                        if st.button(
                            "音声を生成する",
                            help="このページの音声を、AIによって生成します。",
                            disabled=st.session_state.is_guest
                        ):
                            show_overlay()
                            create_one_audio(page_count, tale)
                            modify()
                            hide_overlay()
                            st.rerun()

                        if st.button(
                            "イラストを生成する",
                            help="このページのイラストを、文章をベースにAIによって生成します。",
                            disabled=st.session_state.is_guest
                        ):
                            show_overlay()
                            create_one_image(page_count, tale)
                            modify()
                            hide_overlay()
                            st.rerun()
                        if st.button(
                            "イラストを補正する",
                            disabled=st.session_state.is_guest,
                            help="このページのイラストを、現在のイラストと文章をベースにAIによって生成します。",
                        ):
                            show_overlay()
                            st.session_state.images["content"][
                                page_count
                            ] = image_upgrade(
                                st.session_state.images["title"],
                                st.session_state.tales["title"],
                                st.session_state.tales["description"],
                                st.session_state.tales["theme"],
                                json.dumps(st.session_state.tales["characters"]),
                                st.session_state.tales["content"][page_count],
                            )
                            modify()
                            hide_overlay()
                            st.rerun()
                        if st.button(
                            "イラストを削除する",
                            help="このページのイラストを削除します。",
                        ):
                            st.session_state.images["content"][page_count] = ""
                            modify()
                            st.rerun()

                with col3:
                    # 新しいページの追加
                    if st.button(
                        "次のページを追加する",
                        help="空のページを後ろに追加します。",
                        key=f"{page_count}_adding_page_button",
                    ):
                        adding_page(page_count + 1)
                        st.rerun()
                    page_trigger_btn = ui.button(
                        text="ページを削除する", key="page_trigger_btn"
                    )
                    if ui.alert_dialog(
                        show=page_trigger_btn,
                        title="ページを削除する",
                        description="本当に削除しますか",
                        confirm_label="はい",
                        cancel_label="いいえ",
                        key="alert_dialog_page",
                    ):
                        delete_page(page_count)

    if st.session_state.is_guest:
        if st.session_state.tales["title"]:
            if st.button("動画とPDFを生成する"):
                create_date = datetime.datetime.now(pytz.timezone("Asia/Tokyo"))
                create_date_yyyymdd = create_date.strftime("%Y%m%d_%H%M%S")
                book_info= {
                            "create_date": create_date_yyyymdd,
                            "tales": st.session_state.tales,
                            "images": st.session_state.images,
                            "audios": st.session_state.audios,
                        }
                video_data, pdf_data=create_movie_and_pdf(book_info, bgm)
                if video_data:
                    st.video(video_data)
                    st.download_button(
                        label="動画を保存",
                        data=video_data,
                        file_name=f"{st.session_state.tales["title"]}.mp4",
                        mime="video/mp4",
                    )
                else:
                    st.error("データの読み込みに失敗しました。")

                if pdf_data:
                    st.download_button(
                        label="PDFを保存",
                        data=pdf_data,
                        file_name=f"{st.session_state.tales["title"]}.pdf",
                        mime="application/pdf",
                    )


def delete_book(title):
    if title:
        bucket_name = "story-user-data"
        s3_delete_folder(
            bucket_name,
            const.BASE_PATH.replace("%%user_id%%", st.session_state.user_id).replace(
                "%%title%%", title
            ),
        )
        st.toast(f"{title}を削除しました")
    else:
        st.toast("タイトルを入力してください")


def save_book(book_content, title, bgm="こもれびの道", only_tales=False):
    if title:
        with st.spinner("えほんを保存中..."):
            bucket_name = "story-user-data"
            user_id = st.session_state.user_id
            base_path = const.BASE_PATH.replace("%%user_id%%", user_id).replace(
                "%%title%%", title
            )

            # タイトル画像の保存
            title_image_path = base_path + "images/title.jpeg"
            title_image = book_content["images"]["title"]
            s3_upload(bucket_name, title_image, title_image_path)

            # 物語の内容（tales.json）の保存
            tales_path = base_path + "tales.json"
            tales_data = json.dumps(
                book_content["tales"], indent=4, ensure_ascii=False
            ).encode()
            s3_upload(bucket_name, tales_data, tales_path)

            # ページ毎の画像とオーディオの保存
            for ix, (image, audio) in enumerate(
                zip(book_content["images"]["content"], book_content["audios"])
            ):
                image_path = base_path + f"images/image_{ix}.jpeg"
                audio_path = base_path + f"audios/audio_{ix}.mp3"
                s3_upload(bucket_name, image, image_path)
                s3_upload(bucket_name, audio, audio_path)

            # 動画とPDFの生成
            if not only_tales:
                video_path = base_path + f"{title}.mp4"
                pdf_path = base_path + f"{title}.pdf"
                video_data, pdf_data = create_movie_and_pdf(book_content, bgm)
                s3_upload(bucket_name, video_data, video_path)
                s3_upload(bucket_name, pdf_data, pdf_path)

            st.toast("保存しました。")
            st.cache_data.clear()

    else:
        st.toast("タイトルを入力してください")


def modify():
    st.session_state.not_modify = False


def delete_page(num):
    # 物語の内容から指定されたページを削除
    if num < len(st.session_state.tales["content"]):
        del st.session_state.tales["content"][num]

    # タイトル画像以外の画像から指定されたページを削除
    if num < len(st.session_state.images["content"]):
        del st.session_state.images["content"][num]

    # オーディオから指定されたページを削除
    if num < len(st.session_state.audios):
        del st.session_state.audios[num]

    modify()
    st.rerun()


def adding_page(num):
    # 物語の内容に空のページを追加
    st.session_state.tales["content"].insert(num, "")

    # 画像に空のページを追加
    st.session_state.images["content"].insert(num, "")

    # オーディオに空のページを追加
    st.session_state.audios.insert(num, "")

    modify()


def adding_and_create_page(num):
    adding_page(num)
    create_one_tale(num)
    create_one_image(num, st.session_state.tales["content"][num])
    create_one_audio(num, st.session_state.tales["content"][num])
    modify()
    st.rerun()


def clear_session_state():
    st.session_state.tales = {
        "title": "",
        "number_of_pages": 3,
        "characters_per_page": const.CHARACTORS_PER_PAGE,
        "sentence_structure": "バランス",
        "age_group": "1～2歳",
        "character_set": "ひらがなのみ",
        "description": "",
        "theme": "",
        "characters": {
            "lead": {
                "name": "",
                "appearance": "",
            },
            "others": [
                {
                    "name": "",
                    "appearance": "",
                },
            ],
        },
        "content": [],
    }
    st.session_state.images = {"title": "", "content": []}
    st.session_state.audios = []
    st.session_state.not_modify = True


def create_all(only_tale=False, ignore_tale=False):
    if ignore_tale:
        pass
    else:
        st.session_state.tales = create_tales(
            title=st.session_state.tales["title"],
            description=st.session_state.tales["description"],
            characters=json.dumps(
                st.session_state.tales["characters"], ensure_ascii=False
            ),
            theme=st.session_state.tales["theme"],
            number_of_pages=str(st.session_state.tales["number_of_pages"]),
            age_group=str(st.session_state.tales["age_group"]),
            characters_per_page=str(st.session_state.tales["characters_per_page"]),
            character_set=st.session_state.tales["character_set"],
            sentence_structure=st.session_state.tales["sentence_structure"],
        )

    if only_tale:
        st.session_state.images = {
            "title": "",
            "content": ["" for _ in st.session_state.tales["content"]],
        }
        st.session_state.audios = ["" for _ in st.session_state.tales["content"]]
    else:
        st.session_state.images = create_images(st.session_state.tales)
        st.session_state.audios = create_audios(st.session_state.tales)

    create_date = datetime.datetime.now(pytz.timezone("Asia/Tokyo"))
    create_date_yyyymdd = create_date.strftime("%Y%m%d_%H%M%S")

    book_content = {
        "create_date": create_date_yyyymdd,
        "tales": st.session_state.tales,
        "images": st.session_state.images,
        "audios": st.session_state.audios,
    }

    return book_content


def create():
    if st.session_state.is_guest:
        mode = "いちからつくる"
    else:
        mode = st.selectbox(
            "あたらしくつくる",
            options=["", "おまかせでつくる", "いちからつくる"],
            on_change=clear_session_state,
        )

    if mode == "おまかせでつくる":
        with st.container(border=True):
            st.session_state.tales["title"] = st.text_input(
                "タイトル",
                placeholder=const.RAMDOM_PLACEHOLDER,
            )
            with st.expander("こだわり設定"):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.session_state.tales["number_of_pages"] = st.number_input(
                        "ページ数",
                        min_value=3,
                        max_value=const.MAX_PAGE_NUM,
                    )
                with col2:
                    st.session_state.tales["sentence_structure"] = st.selectbox(
                        "文章の構成",
                        options=const.SENTENCE_STRUCTURE_SET,
                        index=const.SENTENCE_STRUCTURE_SET.index(
                            st.session_state.tales["sentence_structure"]
                        ),
                    )
                with col3:
                    st.session_state.tales["character_set"] = st.selectbox(
                        "使用文字",
                        options=const.CHARACTER_SET,
                    )
                with col4:
                    st.session_state.tales["age_group"] = st.selectbox(
                        "対象年齢",
                        options=const.AGE_GROUP,
                    )
                title_col1, title_col2 = st.columns([2, 4])
                st.session_state.tales["theme"] = title_col1.text_area(
                    "テーマ・メッセージ",
                    placeholder=const.RAMDOM_PLACEHOLDER,
                )
                st.session_state.tales["description"] = title_col2.text_area(
                    "設定やあらすじ",
                    placeholder=const.RAMDOM_PLACEHOLDER,
                )
                with st.container(border=True):
                    st.caption("キャラクター")
                    chara_col1, chara_col2 = st.columns(2)
                    with chara_col1:
                        st.session_state.tales["characters"]["lead"][
                            "name"
                        ] = st.text_input(
                            "主人公の名前",
                            placeholder=const.RAMDOM_PLACEHOLDER,
                        )
                        st.session_state.tales["characters"]["lead"][
                            "appearance"
                        ] = st.text_area(
                            "主人公の見た目",
                            placeholder=const.RAMDOM_PLACEHOLDER,
                        )
                        if st.button("キャラクターを追加"):
                            st.session_state.tales["characters"]["others"].append(
                                {"name": "", "appearance": ""}
                            )
                            st.rerun()

                    with chara_col2:
                        chara_num_list = range(
                            len(st.session_state.tales["characters"]["others"])
                        )
                        chara_tabs = st.tabs(
                            [str(num + 1) for num in chara_num_list]
                        )
                        for chara_num in chara_num_list:
                            with chara_tabs[chara_num]:
                                st.session_state.tales["characters"]["others"][
                                    chara_num
                                ]["name"] = st.text_input(
                                    "名前",
                                    placeholder=const.RAMDOM_PLACEHOLDER,
                                    key=f"chara_name{chara_num}",
                                )
                                st.session_state.tales["characters"]["others"][
                                    chara_num
                                ]["appearance"] = st.text_area(
                                    "見た目",
                                    placeholder=const.RAMDOM_PLACEHOLDER,
                                    key=f"chara_appearance{chara_num}",
                                )
                        if st.button("削除"):
                            st.session_state.tales["characters"]["others"].pop(
                                chara_num
                            )
                            st.rerun()
                bgm = st.selectbox("BGM", options=const.BGM_LIST)
                if bgm:
                    st.audio(f"assets/{bgm}.mp3")

            only_tales = st.toggle("テキストだけ作成する")

            submit = st.button("生成開始",disabled=st.session_state.is_guest,help="ログイン時のみ利用可能")

        if submit:
            if (
                st.session_state.tales["title"]
                or st.session_state.tales["description"]
            ):
                show_overlay()
                book_content = create_all(only_tales=only_tales)

                save_book(
                    book_content,
                    st.session_state.tales["title"],
                    bgm,
                    only_tales=only_tales,
                )

                hide_overlay()

                try:
                    st.image(
                        book_content["images"]["title"], use_column_width="auto"
                    )
                except:
                    st.image("assets/noimage.png", use_column_width="auto")
                st.write(book_content["tales"]["description"])

            else:
                st.toast("タイトルかあらすじを内容を入力してください。")

    elif mode == "いちからつくる":
        view_edit()
    else:
        images, captions = get_images(
            get_all_book_titles(
                "story-user-data",
                const.TITLE_BASE_PATH.replace(
                    "%%user_id%%", st.session_state.user_id
                ),
            ),
            st.session_state.user_id,
        )
        imageCarouselComponent = components.declare_component(
            "image-carousel-component", path="frontend/public"
        )

        images = [
            add_caption_transparent(image, caption)
            for image, caption in zip(images, captions)
        ]

        imageUrls = [
            f"data:image/png;base64,{base64.b64encode(image).decode()}"
            for image in images
        ]
        selectedImageUrl = imageCarouselComponent(imageUrls=imageUrls, height=200)

        if selectedImageUrl:
            select_book = imageUrls.index(selectedImageUrl) + 1
            try:
                caption = captions[select_book - 1]
            except:
                caption = captions[0]
            if (
                st.session_state.not_modify
                or st.session_state.tales["title"] != caption
            ):
                book_info = get_book_data(
                    "story-user-data",
                    st.session_state.user_id,
                    caption,
                )
                st.session_state.tales = book_info["tales"]
                st.session_state.images = book_info["images"]
                st.session_state.audios = book_info["audios"]
            view_edit()
