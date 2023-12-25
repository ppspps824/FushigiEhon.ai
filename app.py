import const
import openai
import streamlit as st
from modules.create import create
from modules.play import play
from modules.streamlit_google_oauth import google_oauth2_required
from PIL import Image
from streamlit_option_menu import option_menu


@google_oauth2_required
def main():
    if st.session_state.api_key:
        openai.api_key = st.session_state.api_key
    else:
        openai.api_key = st.secrets["OPEN_AI_KEY"]
    header_cols = st.columns([1, 3, 1])
    header_cols[0].image("assets/header.png")
    header_cols[2].caption(
        f'logged in {st.session_state.user_email.replace("@gmail.com","")}'
    )
    selected = option_menu(
        None,
        ["よむ", "つくる"],
        icons=["bi-play-btn", "bi-brush"],
        menu_icon=None,
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {
                "margin": "0px !important",
                "background-color": "#fafafa",
            },
            "icon": {"color": "fafafa", "font-size": "25px"},
            "nav-link": {
                "font-size": "20px",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "004a55"},
        },
    )
    if selected == "つくる":
        create()
    elif selected == "よむ":
        play()


if "login" not in st.session_state:
    st.session_state.client = None
    st.session_state.login = False
    st.session_state.guest_login = False
    st.session_state.user_id = ""
    st.session_state.user_email = ""
    st.session_state.api_key = ""
    st.session_state.disable_audio = False

    # create
    st.session_state.tales = {
        "title": "",
        "number_of_pages": 3,
        "characters_per_page": const.CHARACTORS_PER_PAGE,
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

    # ai
    st.session_state.text_model = "gpt-4-1106-preview"
    st.session_state.image_model = "dall-e-3"

st.set_page_config(
    page_title="ふしぎえほん.ai", page_icon=Image.open("assets/logo.png"), layout="wide"
)

st.markdown(
    const.HIDE_ST_STYLE,
    unsafe_allow_html=True,
)


main()
