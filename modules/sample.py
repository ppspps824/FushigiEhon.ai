from PIL import Image

end_image = Image.open("assets/header.png")
base_width= 300
wpercent = (base_width / float(end_image.size[0]))
hsize = int((float(end_image.size[1]) * float(wpercent)))
end_image = end_image.resize((base_width, hsize), Image.Resampling.LANCZOS)
end_dst = Image.new(
    "RGB",
    (1024, 512),
    "#fafafa",
)
end_dst.paste(end_image,(512-end_image.width//2,256-end_image.height//2))

end_dst.show()