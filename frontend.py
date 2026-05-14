import json
from pathlib import Path

import streamlit as st

from videouploadanalysis import DEFAULT_PROMPT, VIDEO_FILENAME, run_analysis

st.set_page_config(page_title="Video Upload Analysis", page_icon="🎥", layout="wide")

st.title("🎥 Video Upload Analysis")
st.caption("Upload a video, customize the prompt, and review AI analysis results.")

left_col, right_col = st.columns([1.1, 1], gap="large")

with left_col:
    st.subheader("Input")
    prompt_text = st.text_area("Prompt", value=DEFAULT_PROMPT, height=120)
    uploaded_video = st.file_uploader(
        "Upload a video file",
        type=["mp4", "mov", "avi", "mkv", "webm"],
        key="video_upload_input",
    )

    sample_video_path = Path(__file__).resolve().parent / VIDEO_FILENAME
    selected_video_bytes: bytes | None = None
    selected_video_label: str | None = None

    if uploaded_video is not None:
        selected_video_bytes = uploaded_video.getvalue()
        selected_video_label = uploaded_video.name
    elif sample_video_path.exists():
        selected_video_bytes = sample_video_path.read_bytes()
        selected_video_label = f"Sample: {VIDEO_FILENAME}"

    if selected_video_bytes is not None:
        st.video(selected_video_bytes)
        st.caption(f"Using video: {selected_video_label}")
    else:
        st.warning("Upload a video to continue.")

    run_clicked = st.button("Run Analysis", type="primary", use_container_width=True)

with right_col:
    st.subheader("Results")
    output_container = st.container(border=True)
    with output_container:
        st.write("Run the analysis to display output.")

if run_clicked:
    if selected_video_bytes is None:
        st.error("No video available for analysis.")
    else:
        with st.spinner("Analyzing video..."):
            try:
                output_text = run_analysis(prompt_text, selected_video_bytes)
                st.success("Analysis complete.")

                with output_container:
                    st.markdown("### Parsed Result")
                    try:
                        parsed = json.loads(output_text)
                        st.json(parsed)
                    except json.JSONDecodeError:
                        st.info("Result is not strict JSON. Showing raw output below.")
                        st.markdown(output_text)

                    st.markdown("### Raw Response")
                    st.code(output_text)
            except Exception as err:  # noqa: BLE001
                st.error(f"Analysis failed: {err}")
