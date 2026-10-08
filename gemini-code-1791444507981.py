import streamlit as st
import config
from story_generator import generate_comic_script
from image_generator import generate_panel_image
from pdf_exporter import export_comic_to_pdf

st.set_page_config(page_title="ComicCraft AI", page_icon="🎨", layout="wide")

st.title("🎨 ComicCraft — AI Comic Story Creator")
st.caption("Powered by Gemini Models & Imagen")

# Sidebar controls
with st.sidebar:
    st.header("Comic Settings")
    prompt = st.text_area("Story Prompt", "A brave explorer discovers an ancient glowing temple hidden inside a futuristic jungle.")
    art_style = st.selectbox("Select Art Style", config.ART_STYLES)
    num_panels = st.slider("Number of Panels", min_value=2, max_value=6, value=4)
    generate_btn = st.button("🚀 Create Comic", type="primary")

if generate_btn:
    if not config.GEMINI_API_KEY:
        st.error("Please set your `GEMINI_API_KEY` in the `.env` file.")
        st.stop()

    # Step 1: Script Generation
    with st.spinner("✍️ Writing comic script with Gemini..."):
        try:
            comic_script = generate_comic_script(prompt, art_style, num_panels)
            st.session_state["comic_script"] = comic_script
        except Exception as e:
            st.error(f"Failed to generate story: {e}")
            st.stop()

    # Step 2: Image Generation
    generated_images = []
    st.subheader(f"📖 {comic_script.get('title', 'Generated Comic')}")
    
    cols = st.columns(2)
    for idx, panel in enumerate(comic_script.get("panels", [])):
        with cols[idx % 2]:
            st.markdown(f"#### Panel {panel.get('panel_number', idx+1)}")
            with st.spinner(f"🎨 Rendering Panel {idx+1}..."):
                try:
                    img = generate_panel_image(panel["visual_description"], art_style)
                    generated_images.append(img)
                    st.image(img, use_container_width=True)
                except Exception as e:
                    st.warning(f"Could not render image for panel {idx+1}: {e}")

            if panel.get("caption"):
                st.info(f"📜 **Caption:** {panel['caption']}")
            if panel.get("dialogue"):
                st.success(f"💬 **Dialogue:** {panel['dialogue']}")

    st.session_state["generated_images"] = generated_images

    # Step 3: Export Option
    if len(generated_images) == len(comic_script.get("panels", [])):
        pdf_data = export_comic_to_pdf(comic_script, generated_images)
        st.download_button(
            label="📥 Download Comic PDF",
            data=pdf_data,
            file_name=f"{comic_script.get('title', 'comic').lower().replace(' ', '_')}.pdf",
            mime="application/pdf"
        )