# Video upload Streamlit app

This folder holds the main Streamlit UI (`frontend.py`) and [`videouploadanalysis.py`](videouploadanalysis.py). `frontend.py` imports the latter from the same directory (only analysis helpers run on import; the standalone UI in that module runs when you execute it directly with `streamlit run videouploadanalysis.py`).

For project-wide setup, prerequisites, and layout, see the [repository README](../README.md).

## Run from this folder

From the repository root you already ran `uv sync`. Then:

```bash
cd videoupload
uv run streamlit run frontend.py --server.headless true
```

Open the URL Streamlit prints (usually `http://localhost:8501`).

## OCI Generative AI access

1. Configure credentials the OCI Python SDK accepts for your account (for example a profile in `~/.oci/config` built from a user API key). See [SDK configuration](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm).
2. Ensure an IAM policy allows the principal to use generative AI in the right compartment, for example:

   `allow any-user to use generative-ai-family in compartment <compartment-name> where ALL {request.principal.type='generativeaiapikey'}`

The Streamlit analysis path uses `ChatOCIGenAI` in this folder’s `videouploadanalysis.py` (standard OCI SDK auth).

If you use the separate OpenAI-compatible example in `video.py`, that script reads `OCI_GENAI_API_KEY`:

```bash
export OCI_GENAI_API_KEY=<value-from-your-setup>
```

## Sample video

If the sample file named in `VIDEO_FILENAME` inside `videouploadanalysis.py` is present in this directory, the app uses it when no file is uploaded.
