import streamlit as st
from PIL import Image


def autorotate(path, rotation=0):
    """This function autorotates a picture"""
    image = Image.open(path)
    exif = image._getexif()

    (width, height) = image.size
    print(exif)
    # print "\n===Width x Heigh: %s x %s" % (width, height)
    if exif:
        orientation_key = 274  # cf ExifTags
        if orientation_key in exif:
            orientation = exif[orientation_key]
            rotate_values = {3: 180, 6: 270, 8: 90}
            if orientation in rotate_values:
                # Rotate and save the picture
                image = image.rotate(rotate_values[orientation], expand=True)
                image.save(path, quality=100, exif=str(exif))
                st.write(f"Saved image with rotation {rotate_values[orientation]}")
        elif rotation > 0:
            image = image.rotate(rotation, expand=True)
            image.save(path, quality=100, exif=str(exif))
            st.write(f"Saved image with rotation {rotation}")
    elif rotation > 0:
        image = image.rotate(rotation, expand=True)
        image.save(path, quality=100)
        st.write(f"Saved image with rotation {rotation}")
    return image
