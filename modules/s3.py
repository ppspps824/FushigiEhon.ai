import io
import pickle

import boto3
import streamlit as st


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
    with st.spinner("保存中..."):
        bucket = get_client_bucket()
        with io.BytesIO() as bf:
            pickle.dump(file, bf)
            bf.seek(0)
            result = bucket.upload_fileobj(bf, key)


def s3_pickle_get(key):
    bucket = get_client_bucket()
    with io.BytesIO() as f:
        bucket.download_fileobj(key, f)
        f.seek(0)
        result = pickle.load(f)

    return result


def get_all_objects():
    bucket = get_client_bucket()

    return bucket.objects.filter(Prefix=f"{st.session_state.user_id}/book_info/")
