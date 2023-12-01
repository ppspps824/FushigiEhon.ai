import const
import openai
import streamlit as st
import streamlit.components.v1 as components
from modules.about import about
from modules.create import create
from modules.play import play
from modules.settings import settings
from streamlit_cognito_auth import CognitoAuthenticator
from streamlit_option_menu import option_menu

if "login" not in st.session_state:
    st.session_state.client = None
    st.session_state.login = False
    st.session_state.guest_login = False
    st.session_state.user_id = ""
    st.session_state.api_key = ""
    st.session_state.disable_audio = False

    # create
    st.session_state.page_num = 5
    st.session_state.characters_per_page = 40
    st.session_state.using_text_types = ""
    st.session_state.age = ""
    st.session_state.tales = {"title": "", "description": "", "content": []}
    st.session_state.images = {"title": "", "content": []}
    st.session_state.audios = []
    st.session_state.not_modify = True

    # ai
    st.session_state.text_model = "gpt-4-1106-preview"
    st.session_state.image_model = "dall-e-3"

st.set_page_config(
    page_title="ふしぎえほん.ai", page_icon="assets/logo.png", layout="wide"
)

st.markdown(
    const.HIDE_ST_STYLE,
    unsafe_allow_html=True,
)

if not st.session_state.login:
    left_co, cent_co, last_co = st.columns([1, 2, 1])
    with cent_co:
        st.image("assets/title.png")

    authenticator = CognitoAuthenticator(
        pool_id=st.secrets["pool_id"],
        app_client_id=st.secrets["app_client_id"],
        app_client_secret=st.secrets["app_client_secret"],
    )

    st.session_state.login = authenticator.login()
    components.html(
        f'<center><a href="{st.secrets["signup_url"]}" target="_blank"> Sign Up </a></center>'
    )

    if not st.session_state.login:
        st.stop()

    st.session_state.user_id = authenticator.get_username()
    st.rerun()
else:
    if st.session_state.api_key:
        openai.api_key = st.session_state.api_key
    else:
        openai.api_key = st.secrets["OPEN_AI_KEY"]

    selected = option_menu(
        "ふしぎえほん.ai",
        ["つかいかた", "えほんをつくる", "えほんをよむ", "せってい"],
        icons=["bi-universal-access", "bi-brush", "bi-play-btn", "gear"],
        menu_icon="bi-book",
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

    if selected == "つかいかた":
        about()
    elif selected == "えほんをつくる":
        create()
    elif selected == "えほんをよむ":
        play()
    elif selected == "せってい":
        settings()
