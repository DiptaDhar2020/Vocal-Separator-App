import streamlit as st
import os
from audio_separator.separator import Separator
import tempfile
import shutil

# Configure Streamlit page
st.set_page_config(
    page_title="Vocal Separator",
    page_icon="🎵",
    layout="wide"
)

# Title and description
st.title("🎵 Vocal Separator")
st.markdown("""
This app separates vocals from instrumentals in your music files using AI-powered source separation.
Upload an audio file (MP3, WAV, FLAC, etc.) and get separate vocal and instrumental tracks!
""")

# Sidebar for model selection
st.sidebar.header("⚙️ Settings")
model_options = {
    "MDX23C-8KFFT-InstVoc_HQ": "High Quality (Recommended)",
    "UVR-MDX-NET-Inst_HQ_3": "Fast & Good Quality",
    "Kim_Vocal_2": "Alternative Model",
    "UVR_MDXNET_KARA_2": "Karaoke Optimized"
}

selected_model = st.sidebar.selectbox(
    "Select Separation Model",
    options=list(model_options.keys()),
    format_func=lambda x: f"{x} - {model_options[x]}"
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### About
This app uses state-of-the-art AI models to separate:
- 🎤 **Vocals**: Singer's voice
- 🎸 **Instrumentals**: Background music

### Supported Formats
- MP3, WAV, FLAC, M4A, OGG, and more
""")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload your audio file",
        type=["mp3", "wav", "flac", "m4a", "ogg", "aac"],
        help="Select an audio file to separate vocals from instrumentals"
    )

with col2:
    if uploaded_file:
        st.info(f"**File:** {uploaded_file.name}")
        st.info(f"**Size:** {uploaded_file.size / (1024*1024):.2f} MB")

# Process button and separation logic
if uploaded_file is not None:
    # Play original audio
    st.subheader("🎧 Original Audio")
    st.audio(uploaded_file)

    # Separation button
    if st.button("🚀 Separate Vocals", type="primary"):
        try:
            # Create temporary directories for processing
            with tempfile.TemporaryDirectory() as temp_dir:
                # Save uploaded file
                input_path = os.path.join(temp_dir, uploaded_file.name)
                with open(input_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Progress indicator
                with st.spinner("🎵 Processing audio... This may take a few minutes depending on file size..."):
                    # Initialize separator
                    separator = Separator(
                        output_dir=temp_dir,
                        output_format="mp3"
                    )

                    # Load the selected model
                    separator.load_model(model_filename=selected_model)

                    # Perform separation
                    output_files = separator.separate(input_path)

                st.success("✅ Separation complete!")

                # Display results
                st.subheader("📁 Separated Tracks")

                col1, col2 = st.columns(2)

                # Find and display the output files
                for output_file in output_files:
                    if os.path.exists(output_file):
                        file_name = os.path.basename(output_file)

                        # Read the file
                        with open(output_file, "rb") as f:
                            audio_bytes = f.read()

                        # Determine if it's vocals or instrumental
                        if "Vocals" in file_name or "vocals" in file_name:
                            with col1:
                                st.markdown("### 🎤 Vocals")
                                st.audio(audio_bytes, format="audio/mp3")
                                st.download_button(
                                    label="⬇️ Download Vocals",
                                    data=audio_bytes,
                                    file_name=f"vocals_{uploaded_file.name}",
                                    mime="audio/mp3"
                                )
                        else:
                            with col2:
                                st.markdown("### 🎸 Instrumental")
                                st.audio(audio_bytes, format="audio/mp3")
                                st.download_button(
                                    label="⬇️ Download Instrumental",
                                    data=audio_bytes,
                                    file_name=f"instrumental_{uploaded_file.name}",
                                    mime="audio/mp3"
                                )

        except Exception as e:
            st.error(f"❌ Error during separation: {str(e)}")
            st.info("Try uploading a different file or selecting another model.")

else:
    # Instructions when no file is uploaded
    st.info("👆 Please upload an audio file to get started!")

    # Example use cases
    st.markdown("---")
    st.subheader("💡 Use Cases")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **🎤 Karaoke**
        Create karaoke tracks by removing vocals from your favorite songs
        """)

    with col2:
        st.markdown("""
        **🎼 Music Production**
        Extract vocals or instrumentals for remixing and sampling
        """)

    with col3:
        st.markdown("""
        **📚 Music Learning**
        Study individual parts of songs to learn instruments or vocals
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Made with ❤️ using Streamlit and Audio Separator</p>
    <p><small>Powered by Ultimate Vocal Remover (UVR) models</small></p>
</div>
""", unsafe_allow_html=True)
