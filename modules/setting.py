import modules.database as db
import streamlit as st


def setting():
    st.cache_data.clear()
    user_info = db.read_user(st.session_state.user_id)
    credits_info = db.read_credits(st.session_state.user_id)

    credits = abs(sum([info["value"] for info in credits_info.data]))
    sum_using_credits = abs(
        sum([info["value"] for info in credits_info.data if info["value"] > 0])
    )
    details_using_credits = [
        {
            "利用日時": info["created_at"][:19].replace("-", "/").replace("T", " "),
            "内容": info["event"],
            "消費量": info["value"],
        }
        for info in credits_info.data
    ]
    sorted_details_using_credits = sorted(
        details_using_credits, key=lambda x: (x["利用日時"], x["内容"]), reverse=True
    )

    created_at = user_info.data[0]["created_at"][:10].replace("-", "/")

    # Summary
    st.caption("ユーザー情報")
    summary_table_data = [
        {
            "利用開始日": created_at,
            "保有クレジット": credits,
            "累計消費クレジット": sum_using_credits,
        }
    ]
    st.dataframe(summary_table_data)

    # Details
    st.caption("クレジット明細")
    st.dataframe(sorted_details_using_credits)
