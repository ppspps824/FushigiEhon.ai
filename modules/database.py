from datetime import datetime

import pytz
import streamlit as st
from supabase import Client, create_client

# SupabaseプロジェクトのURLと公開APIキーを設定
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_API_KEY"]
supabase: Client = create_client(url, key)

jst_tz = pytz.timezone("Asia/Tokyo")


def create_user(user_id: str, email: str):
    """新しいユーザーを作成する"""
    now = datetime.now(jst_tz).isoformat()
    data = {"user_id": user_id, "created_at": now, "email": email}
    supabase.table("users").insert(data).execute()


def adding_credits(user_id: str, event: str, value: int = 1):
    """クレジット消費を記録する"""
    now = datetime.now(jst_tz).isoformat()
    data = {
        "created_at": now,
        "user_id": user_id,
        "event": event,
        "value": value,
    }
    supabase.table("credits").insert(data).execute()


@st.cache_resource(show_spinner=False)
def read_credits(user_id: str):
    """ユーザー情報のクレジット消費情報を取得する"""
    return supabase.table("credits").select("*").eq("user_id", user_id).execute()


@st.cache_resource(show_spinner=False)
def read_user(user_id: str):
    """ユーザー情報を取得する"""
    return supabase.table("users").select("*").eq("user_id", user_id).execute()


def delete_user(user_id: str):
    """ユーザーを削除する"""
    supabase.table("users").delete().eq("user_id", user_id).execute()
