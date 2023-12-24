import base64
import io
from PIL import Image, ImageDraw, ImageFont
import textwrap
import const
import reveal_slides as rs
import streamlit as st
from modules.s3 import get_all_book_titles, get_book_data
from modules.utils import image_select_menu


def create_text_img(text, width, height, font_size, margin=20):
    # Create image object with white background
    im = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(im)

    # Load a font that supports Japanese
    font = ImageFont.truetype("assets/ZenMaruGothic-Bold.ttf", font_size)

     # Calculate wrap width considering margins
    wrap_width = (width - 2 * margin) // font_size

    # Prepare list to hold wrapped text
    wrap_list = []
    for i in range(0, len(text), wrap_width):
        wrap_list.append(text[i:i+wrap_width])

    # Calculate the y position start for vertical centering considering margins
    total_height = (font_size + 2) * len(wrap_list)  # +2 for line spacing
    y_start = max(margin, (height - total_height) // 2)

    # Draw the text on the image
    y = y_start
    for line in wrap_list:
        # Calculate x position for horizontal centering considering margins
        line_width = draw.textlength(line, font=font)
        x = max(margin, (width - line_width) // 2)

        draw.text((x, y), line, fill=(0,0,0), font=font)
        y += font_size + 2  # Move down to next line

    return im


def pil_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return img_str


def play():
    select_book, captions = image_select_menu(
        get_all_book_titles("story-user-data", st.session_state.user_id),
        "",
    )

    if select_book:
        book_info = get_book_data(
            "story-user-data",
            st.session_state.user_id,
            captions[select_book - 1],
        )
        title = book_info["tales"]["title"]
        title_image_bytes = book_info["images"]["title"]
        tales = book_info["tales"]["content"]
        images = book_info["images"]["content"]
        audios = book_info["audios"]

        content_markdown = ""
        if title_image_bytes:
            title_text_img = create_text_img(title, 512, 512, font_size=42)
            title_image = Image.open(io.BytesIO(title_image_bytes))
            title_dst = Image.new(
                "RGB",
                (title_image.width + title_text_img.width, title_image.height),
                (255, 255, 255),
            )
            title_dst.paste(title_image, (0, 0))
            title_dst.paste(
                title_text_img, (title_image.width, 0)
            )
        else:
            title_dst = Image.open(io.BytesIO(title_image_bytes))

        content_markdown += const.TITLE_MARKDOWN.replace(
            "%%image_placeholder%%", pil_to_base64(title_dst)
        )
        result_images = []
        for num, (tale, image, audio) in enumerate(zip(tales, images, audios)):
            page_text_image = create_text_img(tale, 512, 512, font_size=32)
            page_image = Image.open(io.BytesIO(image))
            page_image = page_image.resize((512, 512))
            b64_audio = base64.b64encode(audio).decode() if audio else ""
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

            content_markdown += const.PAGE_MARKDOWN.replace(
                "%%image_placeholder%%", pil_to_base64(dst)
            ).replace("%%page_audio_placeholder%%", b64_audio)

        content_markdown += const.END_ROLE

        rs.slides(
            content_markdown,
            theme="simple",
            height=500,
            config={
                "height": 450,
            },
            display_only=True,
        )

        pdf_bytes = io.BytesIO()
        title_dst.save(
            pdf_bytes, format="PDF", save_all=True, append_images=result_images
        )

        st.download_button(
            label="Download data as PDF",
            data=pdf_bytes.getvalue(),
            file_name=f"{title}.pdf",
            mime="application/pdf",
        )
