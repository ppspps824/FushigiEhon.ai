import io

import boto3
import json
import streamlit as st


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
    book_object={
    st.session_state.tales : json.loads(get_tales(title)),
    st.session_state.images["title"] : get_title_image(title),
    st.session_state.images["content"] : get_images(title),
    st.session_state.audios : get_audios(title),
    }

    return book_object

def s3_get(key):
    bucket = get_client_bucket()
    result =bucket.objects.filter(Prefix=key)
    print(result)
    return result

def get_tales(title):
    return s3_get(f"{st.session_state.user_id}/book_info/{title}/tales.json")

def get_title_image(title):
    return s3_get(f"{st.session_state.user_id}/book_info/{title}/images/title.jpeg")

def get_images(title):
    return s3_get(f"{st.session_state.user_id}/book_info/{title}/images/")

def get_audios(title):
    return s3_get(f"{st.session_state.user_id}/book_info/{title}/audios/")

@st.cache_resource(show_spinner=False)
def get_all_objects():
    bucket = get_client_bucket()

    return bucket.objects.filter(Prefix=f"{st.session_state.user_id}/book_info/")
