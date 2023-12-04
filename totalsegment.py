import streamlit as st
import nibabel as nib
import tempfile
import os
from totalsegmentator.python_api import totalsegmentator

st.title("NIfTI Image Viewer vat")

uploaded_file = st.file_uploader("Upload a file")

if uploaded_file is not None:
    # Save the uploaded file to a temporary directory
    with tempfile.NamedTemporaryFile(delete=False, suffix='.nii.gz') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    try:
        # Process the image with TotalSegmentator
        result_nifti_image = totalsegmentator(input=tmp_file_path, output=tempfile.gettempdir(), task="vertebrae_body")

        # Save the result to a temporary file
        result_file_path = os.path.join(tempfile.gettempdir(), "result_segmentation.nii.gz")
        nib.save(result_nifti_image, result_file_path)

        # Provide a button to download the result
        with open(result_file_path, "rb") as file:
            st.download_button(
                label="Download segmentation result",
                data=file,
                file_name="result_segmentation.nii.gz",
                mime="application/gzip"
            )

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")

    finally:
        # Delete the temporary input file
        os.unlink(tmp_file_path)
        # Optionally delete the output file as well if you don't want to keep it on the server
        # os.unlink(result_file_path)
