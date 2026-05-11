import os
import base64
from pathlib import Path
from openai import OpenAI

client = OpenAI(
    base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/openai/v1",
    api_key=os.getenv("OCI_GENAI_API_KEY"),
)

video_path = Path(__file__).resolve().parent.parent / "H264630-1_04212026133650.mp4"
video_data = base64.b64encode(video_path.read_bytes()).decode("utf-8")
prompt = "Show the bar code, color inside the bin, and number of bins is number of barcodes"

response = client.chat.completions.create(
    # Use a model that is available in your OCI region.
    model="google.gemini-2.5-flash",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "video_url",
                    "video_url": {"url": f"data:video/mp4;base64,{video_data}"},
                },
            ],
        }
    ],
)
print(response.choices[0].message.content)
