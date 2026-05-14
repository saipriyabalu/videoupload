import base64
from pathlib import Path

import streamlit as st
from langchain_core.messages import HumanMessage
from langchain_oci import ChatOCIGenAI

VIDEO_FILENAME = "H264630-1_04212026133650.mp4"
DEFAULT_PROMPT = (
    "Show the bar code, color inside the bin, and number of bins is number of barcodes"
)


def run_analysis(prompt: str, video_bytes: bytes) -> str:
    llm = ChatOCIGenAI(
        model_id="ocid1.generativeaimodel.oc1.us-chicago-1.amaaaaaask7dceyavwtf4vi3u7mpzniugmfbinljhtnktexnmnikwolykzma",
        service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
        compartment_id="ocid1.compartment.oc1..aaaaaaaau6qr32nfvybiw7red7xbhamiu7tl4dch662ur3rmpdgv6o2dy7la",
        model_kwargs={"max_tokens": 5000},
    )

    video_data = base64.b64encode(video_bytes).decode("utf-8")

    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {
                "type": "video_url",
                "video_url": {"url": f"data:video/mp4;base64,{video_data}"},
            },
        ]
    )

    response = llm.invoke([message])
    return str(response.content)


if __name__ == "__main__":
    st.title("Video Upload Analysis")
    st.write("Upload a video (or use the sample) and display extracted details.")

    prompt_text = st.text_area("Prompt", value=DEFAULT_PROMPT, height=100)
    uploaded_video = st.file_uploader(
        "Upload a video file",
        type=["mp4", "mov", "avi", "mkv", "webm"],
    )

    sample_video_path = Path(__file__).resolve().parent / VIDEO_FILENAME
    video_bytes: bytes | None = None

    if uploaded_video is not None:
        video_bytes = uploaded_video.getvalue()
        st.video(video_bytes)
        st.caption(f"Using uploaded video: {uploaded_video.name}")
    else:
        if sample_video_path.exists():
            video_bytes = sample_video_path.read_bytes()
            st.video(video_bytes)
            st.caption(f"Using sample video: {VIDEO_FILENAME}")
        else:
            st.warning(
                "Upload a video to continue. Sample video file was not found next to this app."
            )

    if st.button("Run Analysis", type="primary"):
        with st.spinner("Analyzing video..."):
            try:
                if video_bytes is None:
                    raise FileNotFoundError("No video available for analysis.")

                output = run_analysis(prompt_text, video_bytes)
                st.success("Analysis complete.")
                with st.container(border=True):
                    st.markdown("### Analysis Result")
                    st.markdown(output)
            except FileNotFoundError as err:
                st.error(str(err))
            except Exception as err:  # noqa: BLE001
                st.error(f"Analysis failed: {err}")
