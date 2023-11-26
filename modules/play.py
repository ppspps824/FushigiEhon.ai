import glob
import json
import os
import streamlit as st
import pickle


def play():
    if "page_index" not in st.session_state:
        st.session_state.page_index=0

    def book_list():
        # 保存している情報を読み込み
        paths = glob.glob("books/*")
        user_contents = {}
        for path in paths:
            name=os.path.splitext(os.path.basename(path))[0]
            with open(path, 'rb') as f:
                user_contents[name] = pickle.load(f)

        book_names=[value for value in user_contents.keys()]

        select_book=st.selectbox(" ",options=book_names,label_visibility="collapsed",placeholder="おはなしをえらんでね",index=None)
        if select_book:
            book_info = user_contents[select_book]
            # 表紙
            title=book_info["about"]["title"]
            st.header(title)
            col1,col2=st.columns(2)
            with col1:
                st.image(book_info["about"]["title_image"])
            with col2:
                st.write(f'### {book_info["about"]["description"]}')
            st.write("---")

            tales=book_info["details"]["tales"]["content"]
            images=book_info["details"]["images"]["content"]
            audios=book_info["details"]["audios"]

            for num,info in enumerate(zip(tales,images,audios)):
                tale,image,audio = info
                key = f"{title}_{num}"
                col1,col2 = st.columns(2)
                if num % 2 ==0:
                    with col1:
                            st.header(tale)
                            st.audio(audio)
                    with col2:
                        st.image(image)
                else:
                    with col2:
                            st.header(tale)
                            st.audio(audio)
                    with col1:
                        st.image(image)


    book_list()
