import os
import io
from PIL import Image
import streamlit as st
import pandas as pd


def get_img_details(file_path):
    image_info = {"Name": os.path.basename(file_path)}

    try:
        with Image.open(file_path) as img:
            image_info["Size"] = f"{img.width}x{img.height}"
            image_info["Resolution"] = f"{img.info.get('dpi', (0, 0))} dpi"
            image_info["Depth"] = img.mode
            image_info["Compression"] = img.info.get("compression", "N/A")
    except Exception as e:
        st.error(f"Error processing image {file_path}: {e}")
        return None

    return image_info


def get_image_details(file, file_name):
    image_info = {"Name": file_name}

    try:
        with Image.open(file) as img:
            image_info["Size"] = f"{img.width}x{img.height}"
            image_info["Resolution"] = f"{img.info.get('dpi', (0, 0))} dpi"
            image_info["Depth"] = img.mode
            image_info["Compression"] = img.info.get("compression", "N/A")
    except Exception as e:
        st.error(f"Error processing image {file_name}: {e}")
        return None

    return image_info


def main():
    st.title("Image Information App")

    folder_path = st.text_input("Enter the path of the folder containing images:")
    uploaded_files = st.file_uploader("Choose images:", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    clear_button = st.button("Clear")

    data = []

    if clear_button:
        folder_path = ""
        uploaded_files.clear()
        st.empty()
        data.clear()

    if folder_path and not os.path.exists(folder_path):
        st.warning("Directory doesn't exist")
        return

    image_formats = (".jpg", ".jpeg", ".png")

    if folder_path:
        data.clear()
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(image_formats):
                    file_path = os.path.join(root, file)
                    info = get_img_details(file_path)
                    if info:
                        data.append([info['Name'], info['Size'], info['Resolution'], info['Depth'], info['Compression']])

    if uploaded_files:
        data.clear()
        for uploaded_file in uploaded_files:
            info = get_image_details(io.BytesIO(uploaded_file.read()), uploaded_file.name)
            if info:
                data.append([info['Name'], info['Size'], info['Resolution'], info['Depth'], info['Compression']])

    if data:
        columns = ["Filename", "Size (px)", "Resolution (dot/inch)", "Color depth", "Image compression"]
        df = pd.DataFrame(data, columns=columns)
        st.table(df)


if __name__ == "__main__":
    main()
