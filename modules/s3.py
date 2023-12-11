import io

import boto3
import json
import streamlit as st
import os


@st.cache_resource(show_spinner=False)
def get_client_bucket():
    s3 = boto3.resource(
        "s3",
        aws_access_key_id=st.secrets["aws_access_key_id"],
        aws_secret_access_key=st.secrets["aws_secret_access_key"],
        region_name="ap-northeast-1",
    )

    bucket = s3.Bucket("story-user-data")
    return bucket


def s3_upload(file, key):
    bucket = get_client_bucket()
    file = io.BytesIO(file)

    bucket.upload_fileobj(file, key)


def s3_delete(key):
    with st.spinner("えほんを削除中..."):
        bucket = get_client_bucket()
        bucket.objects.filter(Prefix="key").delete()


def get_book_object(title):
    book_object = {
        "details": {
            "tales": {
                "title": title,
                "content": json.loads(get_tales(title)),
            },
            "images": {
                "title": get_title_image(title),
                "content": get_images(title),
            },
            "audios": get_audios(title),
        }
    }

    return book_object


def s3_get(key, is_folder=False):
    bucket = get_client_bucket()
    if is_folder:
        result = bucket.meta.client.list_objects(Bucket=bucket.name, Prefix=key,Delimiter="/")
        contents = [content for content in result.get('CommonPrefixes')]
    else:
        result = bucket.Object(key)
        contents = result.get()['Body'].read()
    return contents


def get_all_title():
    result = s3_get(f"{st.session_state.user_id}/book_info/",is_folder=True)
    titles = [os.path.dirname(filepath["Prefix"]).split("/")[-1] for filepath in result]
    return titles


def get_tales(title):
    return s3_get(f"{st.session_state.user_id}/book_info/{title}/tales.json")[0]


def get_title_image(title):
    path = f"{st.session_state.user_id}/book_info/{title}/images/title.jpeg"
    result=s3_get(path)[0]
    print(type(result))
    print(result)
    return result.getvalue()


def get_images(title):
    return s3_get(f"{st.session_state.user_id}/book_info/{title}/images/")


def get_audios(title):
    return s3_get(f"{st.session_state.user_id}/book_info/{title}/audios/")


@st.cache_resource(show_spinner=False)
def get_all_objects():
    bucket = get_client_bucket()

    return bucket.objects.filter(Prefix=f"{st.session_state.user_id}/book_info/")
