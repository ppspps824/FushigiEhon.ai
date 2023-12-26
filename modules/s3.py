import json
import os

import boto3
import streamlit as st

# AWSクレデンシャルを環境変数から取得
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
REGION_NAME = "ap-northeast-1"

# S3クライアントの初期化
s3_client = boto3.client(
    "s3",
    aws_access_key_id=st.secrets["aws_access_key_id"],
    aws_secret_access_key=st.secrets["aws_secret_access_key"],
    region_name=st.secrets["region_name"],
)


def get_all_book_titles(bucket_name, user_id):
    """指定されたユーザーのすべてのえほんのタイトルを取得"""
    try:
        # 指定されたユーザーのbook_infoフォルダ内のオブジェクトをリストアップ
        response = s3_client.list_objects_v2(
            Bucket=bucket_name, Prefix=f"{user_id}/book_info/", Delimiter="/"
        )
        titles = []

        # 各サブフォルダ（えほんのタイトル）を抽出
        for content in response.get("CommonPrefixes", []):
            title = content["Prefix"].split("/")[-2]  # タイトルを抽出
            titles.append(title)
        return titles
    except Exception as e:
        st.error(f"タイトル取得エラー: {e}")
        return []


def s3_upload(bucket_name, file_data, key):
    """S3バケットにファイルをアップロード"""
    try:
        s3_client.put_object(Bucket=bucket_name, Key=key, Body=file_data)
    except Exception as e:
        print(f"アップロードエラー: {e.args}")


@st.cache_data
def s3_download(bucket_name, key):
    """S3バケットからファイルをダウンロード"""
    # print(bucket_name, key)
    try:
        file = s3_client.get_object(Bucket=bucket_name, Key=key)
        return file["Body"].read()
    except Exception as e:
        print("ダウンロードエラー", bucket_name, key)
        print(e)
        return None


def s3_delete_folder(bucket_name, prefix):
    """S3バケット内の指定されたプレフィックス（フォルダ）にあるすべてのオブジェクトを削除"""
    try:
        # フォルダ内のすべてのオブジェクトをリストアップ
        objects_to_delete = s3_client.list_objects(Bucket=bucket_name, Prefix=prefix)

        # 削除対象がある場合、それらを削除
        if "Contents" in objects_to_delete:
            delete_keys = {
                "Objects": [
                    {"Key": obj["Key"]} for obj in objects_to_delete["Contents"]
                ]
            }
            result = s3_client.delete_objects(Bucket=bucket_name, Delete=delete_keys)

    except Exception as e:
        print(f"フォルダ削除エラー: {e}")


def get_book_data(bucket_name, user_id, title):
    base_path = f"{user_id}/book_info/{title}/"
    book_content = {
        "create_date": "",
        "tales": {},
        "images": {"title": "", "content": []},
        "audios": [],
    }

    # tales.jsonの取得
    tales_path = base_path + "tales.json"
    book_content["tales"] = json.loads(s3_download(bucket_name, tales_path))

    # タイトル画像の取得
    title_image_path = base_path + "images/title.jpeg"
    book_content["images"]["title"] = s3_download(bucket_name, title_image_path)

    # ページ毎の画像とオーディオの取得
    for ix in range(len(book_content["tales"]["content"])):
        image_path = base_path + f"images/image_{ix}.jpeg"
        audio_path = base_path + f"audios/audio_{ix}.mp3"
        book_content["images"]["content"].append(s3_download(bucket_name, image_path))
        book_content["audios"].append(s3_download(bucket_name, audio_path))

    return book_content
