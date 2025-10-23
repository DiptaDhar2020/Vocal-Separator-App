import streamlit as st
import os
import tempfile
import subprocess
import shutil

st.set_page_config(
    page_title="Vocal Separator",
    page_icon="🎵",
    layout="wide"
)

st.title("🎵 Vocal Separator")
st.markdown("""
Separate vocals from instrumentals using Demucs AI model.
Works with Python 3.13!
""")

st.sidebar.header("⚙️ Settings")
model = st.sidebar.selectbox(
    "Select Model",
    ["htdemucs", "mdx_extra", "mdx_q"],
    help="htdemucs: Best quality, mdx_extra: Good quality, mdx_q: Fastest"
)

st.sidebar.markdown("""
### About
This app uses **Demucs** by Meta AI for music source separation.
It separates vocals from instruments with high accuracy.
""")

uploaded_file = st.file_uploader(
    "Upload your audio file",
    type=["mp3", "wav", "flac", "m4a", "ogg", "aac"]
)

if uploaded_file is not None:
    st.subheader("🎧 Original Audio")
    st.audio(uploaded_file)

    if st.button("🚀 Separate Vocals", type="primary"):
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                # Save uploaded file
                input_path = os.path.join(temp_dir, uploaded_file.name)
                with open(input_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Run demucs
                with st.spinner("🎵 Processing audio... This may take a few minutes..."):
                    # Use demucs to separate vocals
                    cmd = [
                        "demucs",
                        "--two-stems=vocals",
                        "-n", model,
                        "-o", temp_dir,
                        "--mp3",
                        input_path
                    ]

                    result = subprocess.run(cmd, capture_output=True, text=True)

                    if result.returncode != 0:
                        st.error(f"❌ Demucs processing failed: {result.stderr}")
                    else:
                        st.success("✅ Separation complete!")

                        # Find output folder
                        separated_dir = None
                        for root, dirs, files in os.walk(temp_dir):
                            if "vocals.mp3" in files:
                                separated_dir = root
                                break

                        if separated_dir:
                            vocals_path = os.path.join(separated_dir, "vocals.mp3")
                            drums_path = os.path.join(separated_dir, "drums.mp3")
                            bass_path = os.path.join(separated_dir, "bass.mp3")
                            other_path = os.path.join(separated_dir, "other.mp3")

                            col1, col2 = st.columns(2)

                            # Display and download vocals
                            if os.path.exists(vocals_path):
                                with col1:
                                    st.markdown("### 🎤 Vocals")
                                    with open(vocals_path, "rb") as f:
                                        vocals_data = f.read()
                                    st.audio(vocals_data, format="audio/mp3")
                                    st.download_button(
                                        label="⬇️ Download Vocals",
                                        data=vocals_data,
                                        file_name=f"vocals_{uploaded_file.name}",
                                        mime="audio/mp3"
                                    )

                            # Display and download instrumental (combination of all non-vocal stems)
                            if os.path.exists(drums_path) and os.path.exists(bass_path):
                                with col2:
                                    st.markdown("### 🎸 Instrumental")
                                    # For simplicity, show drums as instrumental
                                    with open(drums_path, "rb") as f:
                                        instrumental_data = f.read()
                                    st.audio(instrumental_data, format="audio/mp3")
                                    st.download_button(
                                        label="⬇️ Download Instrumental (Drums)",
                                        data=instrumental_data,
                                        file_name=f"drums_{uploaded_file.name}",
                                        mime="audio/mp3"
                                    )

                            # Show other stems available
                            st.markdown("---")
                            st.markdown("### 🎼 Other Stems Available")

                            col1, col2, col3 = st.columns(3)

                            if os.path.exists(drums_path):
                                with col1:
                                    with open(drums_path, "rb") as f:
                                        drums_data = f.read()
                                    st.markdown("**🥁 Drums**")
                                    st.download_button(
                                        label="Download Drums",
                                        data=drums_data,
                                        file_name=f"drums_{uploaded_file.name}",
                                        mime="audio/mp3",
                                        key="drums"
                                    )

                            if os.path.exists(bass_path):
                                with col2:
                                    with open(bass_path, "rb") as f:
                                        bass_data = f.read()
                                    st.markdown("**🎸 Bass**")
                                    st.download_button(
                                        label="Download Bass",
                                        data=bass_data,
                                        file_name=f"bass_{uploaded_file.name}",
                                        mime="audio/mp3",
                                        key="bass"
                                    )

                            if os.path.exists(other_path):
                                with col3:
                                    with open(other_path, "rb") as f:
                                        other_data = f.read()
                                    st.markdown("**🎹 Other**")
                                    st.download_button(
                                        label="Download Other",
                                        data=other_data,
                                        file_name=f"other_{uploaded_file.name}",
                                        mime="audio/mp3",
                                        key="other"
                                    )
                        else:
                            st.error("❌ Could not find output files")

        except FileNotFoundError:
            st.error("""
            ❌ Demucs is not installed!

            **Local installation:**
            ```bash
            pip install demucs
            ```

            **Streamlit Cloud:**
            This error shouldn't appear on Streamlit Cloud.
            Please check the deployment logs.
            """)
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

else:
    st.info("👆 Upload an audio file to get started!")

    st.markdown("---")
    st.subheader("💡 What Demucs Can Do")
    st.markdown("""
    - **🎤 Extract vocals** for karaoke or remixing
    - **🥁 Separate drums** for analyzing rhythm
    - **🎸 Extract bass** for bass-focused remixes
    - **🎹 Get other instruments** for detailed analysis
    - **High quality** AI-powered separation
    """)

st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Made with ❤️ using Streamlit and Demucs</p>
    <p><small>Demucs by Meta AI Research</small></p>
</div>
""", unsafe_allow_html=True)
