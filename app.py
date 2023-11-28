import hydralit as hy
import streamlit as st
from modules.create import create
from modules.play import play
from streamlit_cognito_auth import CognitoAuthenticator

if __name__ == "__main__":
    if "login" not in st.session_state:
        st.session_state.client = None
        st.session_state.login = False
        st.session_state.guest_login = False
        st.session_state.user_id = ""

    if not st.session_state.login:
        authenticator = CognitoAuthenticator(
            pool_id=st.secrets["pool_id"],
            app_client_id=st.secrets["app_client_id"],
            app_client_secret=st.secrets["app_client_secret"],
        )

        st.session_state.login = authenticator.login()
        st.link_button(
            "Signup",
            st.secrets["signup_url"],
        )

        if not st.session_state.login:
            st.stop()

        st.session_state.user_id = authenticator.get_username()
        st.experimental_rerun()
    else:
        app = hy.HydraApp(
            title="ふしぎえほん.ai",
            hide_streamlit_markers=True,
            use_loader=False,
        )

        @app.addapp(title="えほんをつくる")
        def page1():
            create()

        @app.addapp(title="えほんをよむ")
        def page3():
            play()

        app.run()
