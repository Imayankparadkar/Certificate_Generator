import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# ----------------------------
# Streamlit Page Configuration
# ----------------------------
st.set_page_config(page_title="Certificate Generator", layout="centered")
st.title("Certificate Generator")

# ----------------------------
# Sidebar - Upload & Settings
# ----------------------------
with st.sidebar:
    st.header("Upload Certificate Template")
    uploaded_template = st.file_uploader(
        "Upload Template (PNG, JPG, JPEG)",
        type=["png", "jpg", "jpeg"]
    )
    st.markdown("---")

    # Font settings
    st.header("Font Settings")
    use_custom_font = st.checkbox("Use Custom .ttf Font")
    uploaded_font = None
    font_path = "DejaVuSans.ttf"  # Default fallback font (always available)

    if use_custom_font:
        uploaded_font = st.file_uploader("Upload .ttf Font", type=["ttf"])
    else:
        font_path = st.selectbox(
            "Choose Built-in Font",
            ["DejaVuSans.ttf", "arial.ttf", "times.ttf", "cour.ttf"]
        )

    font_size = st.slider("Font Size", 10, 150, 40)
    font_color = st.color_picker("Font Color", "#000000")

    st.markdown("---")
    st.header("Text Position")
    x = st.number_input("X Position", min_value=0, value=40, step=10)
    y = st.number_input("Y Position", min_value=0, value=40, step=10)

    st.markdown("---")
    st.header("Output Format")
    output_format = st.selectbox("Download Format", ["png", "jpg", "jpeg"])

# ----------------------------
# Main Area - Certificate Preview
# ----------------------------
if uploaded_template:
    template = Image.open(uploaded_template).convert("RGB")

    st.subheader("Enter Names (One Per Line)")
    names_input = st.text_area("Names", "SufLearning\nyt_channel")
    names = [name.strip() for name in names_input.splitlines() if name.strip()]

    if names:
        selected_name = st.selectbox("Select Name to Preview", names)

        cert = template.copy()
        draw = ImageDraw.Draw(cert)

        # ----------------------------
        # Correct Font Handling
        # ----------------------------
        try:
            if use_custom_font and uploaded_font is not None:
                # Read uploaded font bytes
                font_bytes = uploaded_font.read()
                font = ImageFont.truetype(io.BytesIO(font_bytes), font_size)
            else:
                # Use built-in font (must exist in environment)
                font = ImageFont.truetype(font_path, font_size)
        except Exception as e:
            st.warning(f"Could not load font properly. Using default font. Error: {e}")
            font = ImageFont.load_default()

        # Draw the name text on certificate
        draw.text((x, y), selected_name, font=font, fill=font_color)

        # Show preview
        st.image(cert, caption=f"Preview for: {selected_name}", use_container_width=True)

        # Save image for download
        img_bytes = io.BytesIO()
        cert.save(img_bytes, format=output_format.upper())
        img_bytes.seek(0)

        st.download_button(
            label=f"Download '{selected_name}' as {output_format}",
            data=img_bytes.getvalue(),
            file_name=f"{selected_name}.{output_format.lower()}",
            mime=f"image/{output_format.lower()}",
        )
    else:
        st.warning("Enter at least one name above.")
else:
    st.info("Please upload a certificate template from the sidebar.")
