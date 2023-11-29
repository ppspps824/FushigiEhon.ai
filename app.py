import const
import streamlit as st
import streamlit.components.v1 as components
from modules.create import create
from modules.play import play
from streamlit_cognito_auth import CognitoAuthenticator
from streamlit_option_menu import option_menu

if "login" not in st.session_state:
    st.session_state.client = None
    st.session_state.login = False
    st.session_state.guest_login = False
    st.session_state.user_id = ""

st.set_page_config(page_title="ふしぎえほん.ai", layout="wide")

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
    selected = option_menu(
        f"ふしぎえほん.ai　{st.session_state.user_id}さん",
        ["つかいかた", "えほんをつくる", "えほんをよむ", "といあわせ"],
        icons=["house", "cloud-upload", "list-task", "gear"],
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "fafafa", "font-size": "25px"},
            "nav-link": {
                "font-size": "25px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "004a55"},
        },
    )

    if selected == "えほんをつくる":
        create()
    elif selected == "えほんをよむ":
        play()
