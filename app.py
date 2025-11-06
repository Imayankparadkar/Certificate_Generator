import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io


st.set_page_config(page_title="Certificate Generator ", layout="centered")
st.title("Certificate Generator ")

with st.sidebar:
    st.header("Upload certificate Template")
    uploaded_template = st.file_uploader("Upload Template (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])
    st.markdown("---")
    st.header("Font Settings")

    use_custom_font = st.checkbox("Use Custom .ttf font")
    uploaded_font = None
    font_path = "arial.ttf"

    if use_custom_font:
        uploaded_font = st.file_uploader("Upload .ttf Font", type=["ttf"])
    else:
        font_path = st.selectbox("Choose built-in Font", ["arial.ttf", "times.ttf", "cour.ttf"])
    
    font_size = st.slider("Font Size", 10, 150, 40)
    font_color = st.color_picker("Font Color", "#000000")

    st.markdown("---")
    st.header("Text Position")
    x = st.number_input("X Position ", min_value=0, value=40, step=10)
    y = st.number_input("Y position", min_value=0, value=40, step=10)

    st.markdown("---")
    st.header("Output Format")
    output_format = st.selectbox("Download Format", ["png", "jpg", "jpeg"])

if uploaded_template:
    template = Image.open(uploaded_template).convert("RGB")

    st.subheader("Enter Names (One Per Line)")
    names_input = st.text_area("Names", "SufLearning \n yt_channel")
    names = [name.strip() for name in names_input.splitlines() if name.strip()]

    if names:
        selected_name = st.selectbox("Select Name to Preview", names)
        cert = template.copy()
        draw = ImageDraw.Draw(cert)

        try: 
            font = ImageFont.truetype(uploaded_font if uploaded_font else font_path, font_size)
        except:
            font = ImageFont.load_default()

        draw.text((x, y), selected_name, font=font, fill=font_color)
        st.image(cert, caption=f"Preview for: {selected_name}", use_container_width=True)

        img_bytes = io.BytesIO()
        cert.save(img_bytes, format=output_format.upper())

        st.download_button(
            label=f"Download '{selected_name}' as {output_format}",
            data=img_bytes.getvalue(),
            file_name=f"{selected_name}.{output_format.lower()}",
            mime=f"image/{output_format.lower()}",
        )
    else:
        st.warning("Enter at least one name above. ")
else:
    st.info("Please upload a certificate template from the sidebar. ")
