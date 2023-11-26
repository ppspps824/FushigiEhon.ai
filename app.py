import datetime
import json

import const
import hydralit as hy
import openai
import pytz
import streamlit as st
from modules.create import create
from modules.play import play


def init():
    if "login" not in st.session_state:
        st.session_state.client = None
        st.session_state.login = False
        st.session_state.guest_login = False
        st.session_state.user_id = ""


def login():
    """
    ログインページ
    - ログイン画面（ゲストログインもあり）
    ユーザーIDとパスワードを入力
    """
    correct_login = False
    with st.form("ログイン"):
        user_id = st.text_input("User ID")
        password = st.text_input("Password", type="password")

        if st.form_submit_button("ログイン"):
            # 認証処理
            if user_id == "papasim824":
                correct_login = True

            if correct_login:
                st.session_state.login = True
                st.experimental_rerun()
            else:
                st.error("ログイン失敗")

    if st.button("ゲストログイン"):
        st.session_state.guest_login = True
        st.experimental_rerun()


if __name__ == "__main__":
    init()

    if st.session_state.login or st.session_state.guest_login:
        app = hy.HydraApp(
            title="ehon",
            hide_streamlit_markers=True,
            use_loader=False,
        )

        @app.addapp(title="えほんをつくる")
        def page1():
            create()

        if st.session_state.login:

            @app.addapp(title="えほんをよむ")
            def page2():
                play()

        app.run()
    else:
        login()
