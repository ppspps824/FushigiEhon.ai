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
    st.session_state.title = ""
    st.session_state.title_image = ""
    st.session_state.description = ""
    st.session_state.tales = []
    st.session_state.images = []
    st.session_state.audios = []
    st.session_state.not_modify = True

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
    st.experimental_rerun()
else:
    if st.session_state.api_key:
        openai.api_key = st.session_state.api_key
    else:
        openai.api_key = st.secrets["OPEN_AI_KEY"]

    selected = option_menu(
        "ふしぎえほん.ai",
        ["つかいかた", "つくる", "みる", "せってい"],
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
                "text-align": "left",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "004a55"},
        },
    )

    if selected == "つかいかた":
        about()
    elif selected == "つくる":
        create()
    elif selected == "みる":
        play()
    elif selected == "せってい":
        settings()
