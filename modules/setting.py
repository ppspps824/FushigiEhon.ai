import const
import streamlit as st
    
def setting():
    table_data={
        "利用開始日":"2023/1/1",
        "保有クレジット":200,
        "累計消費クレジット":1200
    }
    st.table(table_data,columns=["カテゴリ","内容"])