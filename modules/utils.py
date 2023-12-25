import io
import tempfile

import numpy as np
import streamlit as st
from modules.s3 import s3_download
from moviepy.editor import (
    AudioFileClip,
    CompositeAudioClip,
    ImageClip,
    concatenate_videoclips,
)
from PIL import Image, ImageDraw, ImageFont
from streamlit_image_select import image_select


# オーバーレイを表示
def show_overlay():
    st.markdown(
        '<div class="overlay" style="display:block"></div>', unsafe_allow_html=True
    )
    pass


# オーバーレイを非表示
def hide_overlay():
    st.markdown(
        """
    <style>
    .spinner, .overlay {
        display: none !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
    pass


def get_images(titles):
    try:
        all_image = {
            title: s3_download(
                "story-user-data",
                f"{st.session_state.user_id}/book_info/{title}/images/title.jpeg",
            )
            for title in titles
        }
    except Exception as e:
        print(e.args)
        all_image = {}

    images = []
    for data in all_image.values():
        if data:
            # バイト型データをPIL.Imageオブジェクトに変換
            image = Image.open(io.BytesIO(data))
            # 画像のリサイズ
            resized_image = image.resize((256, 256))
            images.append(resized_image)
        else:
            images.append("assets/noimage.png")
    return images, all_image


def create_text_img(text, width, height, font_size, margin=20):
    # Create image object with white background
    im = Image.new("RGB", (width, height), "#fafafa")
    draw = ImageDraw.Draw(im)

    # Load a font that supports Japanese
    font = ImageFont.truetype("assets/ZenMaruGothic-Bold.ttf", font_size)

    # Calculate wrap width considering margins
    wrap_width = (width - 2 * margin) // font_size

    # Prepare list to hold wrapped text
    wrap_list = []
    for i in range(0, len(text), wrap_width):
        wrap_list.append(text[i : i + wrap_width])

    # Calculate the y position start for vertical centering considering margins
    total_height = (font_size + 2) * len(wrap_list)  # +2 for line spacing
    y_start = max(margin, (height - total_height) // 2)

    # Draw the text on the image
    y = y_start
    for line in wrap_list:
        # Calculate x position for horizontal centering considering margins
        line_width = draw.textlength(line, font=font)
        x = max(margin, (width - line_width) // 2)

        draw.text((x, y), line, fill=(0, 0, 0), font=font)
        y += font_size + 2  # Move down to next line

    return im


@st.cache_data(show_spinner=False)
def create_movie_and_pdf(book_info):
    with st.spinner("読み込み中..."):
        title = book_info["tales"]["title"]
        title_image_bytes = book_info["images"]["title"]
        tales = book_info["tales"]["content"]
        images = book_info["images"]["content"]
        audios = book_info["audios"]

        title_text_img = create_text_img(title, 512, 512, font_size=42)
        if title_image_bytes:
            title_image = Image.open(io.BytesIO(title_image_bytes))
        else:
            title_image = Image.new("RGB", (512, 512), "#fafafa")

        title_dst = Image.new(
            "RGB",
            (title_image.width + title_text_img.width, title_image.height),
            "#fafafa",
        )
        title_dst.paste(title_image, (0, 0))
        title_dst.paste(title_text_img, (title_image.width, 0))

        np_title_image = np.array(title_dst)

        # タイトル画像の準備 (PIL.Image形式)
        title_image_clip = ImageClip(np_title_image).set_duration(3)

        # エンディング画像の準備 (PIL.Image形式)
        end_image = Image.open("assets/header.png")
        end_image = end_image.resize((end_image.width // 3, end_image.height // 3))
        end_dst = Image.new(
            "RGB",
            (1024, 512),
            "#fafafa",
        )
        end_dst.paste(
            end_image, (0 + end_image.width // 2, 256 - end_image.height // 2)
        )
        np_end_image = np.array(end_dst)
        end_image_clip = ImageClip(np_end_image).set_duration(3)

        clips = []
        result_images = []
        for num, (tale, image, audio) in enumerate(zip(tales, images, audios)):
            page_text_image = create_text_img(tale, 512, 512, font_size=32)
            if image:
                page_image = Image.open(io.BytesIO(image))
            else:
                page_image = Image.new("RGB", (512, 512), "#fafafa")

            page_image = page_image.resize((512, 512))
            dst = Image.new(
                "RGB", (page_image.width + page_text_image.width, page_image.height)
            )
            if num % 2 == 1:
                dst.paste(page_image, (0, 0))
                dst.paste(page_text_image, (page_image.width, 0))
            else:
                dst.paste(page_text_image, (0, 0))
                dst.paste(page_image, (page_text_image.width, 0))

            result_images.append(dst)

            # PIL Imageをnumpy arrayに変換
            np_image = np.array(dst)

            # 画像クリップを作成
            img_clip = ImageClip(np_image)  # fpsは適宜調整してください

            # 音声バイトデータからAudioFileClipを作成
            if audio:
                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=".mp3"
                ) as temp_audio:  # 適切な拡張子を使用してください
                    temp_audio.write(audio)
                    temp_audio.seek(0)  # ファイルの先頭にシーク

                    # 一時ファイルのパスを使用してAudioFileClipを作成
                    audio_clip = AudioFileClip(temp_audio.name)

                    # 画像の表示時間を音声の長さに設定
                    img_clip = img_clip.set_duration(audio_clip.duration + 1)

                    # 画像クリップに音声を設定
                    img_clip = img_clip.set_audio(audio_clip)

                    # クリップをリストに追加
                    clips.append(img_clip)
            else:
                # 画像の表示時間を音声の長さに設定
                img_clip = img_clip.set_duration(5)

                # クリップをリストに追加
                clips.append(img_clip)

        bgm_clip = AudioFileClip("assets/お昼のうた.mp3")

        # すべてのクリップを結合
        final_clip = concatenate_videoclips(
            [title_image_clip] + clips + [end_image_clip], method="compose"
        )

        original_audio = final_clip.audio

        # 最終的な動画の長さに合わせてBGMを設定（必要に応じてループやフェードイン・アウトを追加）
        bgm_clip = bgm_clip.set_duration(final_clip.duration)
        bgm_clip = bgm_clip.volumex(0.05)
        bgm_clip = bgm_clip.audio_fadeout(3)

        if original_audio:
            # BGMと既存の音声を混ぜる
            mixed_audio = CompositeAudioClip([original_audio, bgm_clip])

            # 最終的な動画に混合された音声を設定
            final_clip.audio = mixed_audio
        else:
            final_clip.audio = bgm_clip

        # 一時的なビデオファイルを作成するためにtempfileを使用
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
            final_clip.write_videofile(
                temp_video.name,  # write_videofileに一時ファイル名を提供
                fps=24,
                codec="libx264",
                audio_codec="aac",
                temp_audiofile="temp-audio.m4a",
                remove_temp=True,
            )

            # ファイルからビデオを読み込んで表示
            temp_video.seek(0)
            video_data = temp_video.read()

        pdf_bytes = io.BytesIO()
        title_image.save(
            pdf_bytes, format="PDF", save_all=True, append_images=result_images
        )

    return video_data, pdf_bytes


def image_select_menu(titles, label):
    images, all_image = get_images(titles)
    captions = list(all_image.keys())

    if images:
        select_book = (
            image_select(
                label=label,
                images=images,
                captions=titles,
                return_value="index",
                index=-1,
                use_container_width=False,
                key=label,
            )
            + 1
        )

        return select_book, captions
    else:
        st.info(
            "おはなしがありません。「えほんをつくる」をおして、えほんをつくりましょう。"
        )
        st.stop()
