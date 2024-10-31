import streamlit as st
import zipfile
import gzip
from io import BytesIO
import os

st.set_page_config(page_title="GB to kB Compression Tool", layout="centered")

# Initialize session state for file data
if "original_file_data" not in st.session_state:
    st.session_state["original_file_data"] = None
    st.session_state["original_filename"] = None

# Header
st.title("GB to kB Compression Tool")
st.write("Upload a file to attempt extreme compression. This tool is optimized for highly compressible files like text or JSON.")

# Step 1: Upload the file
uploaded_file = st.file_uploader("Upload a file", type=None)

# Step 2: Compress the file using multiple algorithms
if uploaded_file is not None:
    # Save original file details in session state
    st.session_state["original_file_data"] = uploaded_file.read()
    st.session_state["original_filename"] = uploaded_file.name

    def extreme_compress(data):
        """Compress the data in multiple steps to achieve extreme reduction."""
        
        # Step 1: Gzip Compression
        gzip_buffer = BytesIO()
        with gzip.GzipFile(fileobj=gzip_buffer, mode="wb") as gz:
            gz.write(data)
        gzip_compressed_data = gzip_buffer.getvalue()

        # Step 2: Zip Compression on top of Gzip
        final_compressed_buffer = BytesIO()
        with zipfile.ZipFile(final_compressed_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.writestr("compressed_file.gz", gzip_compressed_data)
        final_compressed_buffer.seek(0)
        
        return final_compressed_buffer.getvalue()

    # Perform the extreme compression
    compressed_data = extreme_compress(st.session_state["original_file_data"])

    # Display compression results
    original_size = len(st.session_state["original_file_data"]) / (1024 * 1024)
    compressed_size = len(compressed_data) / 1024
    st.write(f"Original Size: {original_size:.2f} MB")
    st.write(f"Compressed Size: {compressed_size:.2f} kB")

    # Step 3: Download the compressed file
    st.download_button(
        label="Download Compressed File",
        data=compressed_data,
        file_name="extremely_compressed_" + st.session_state["original_filename"] + ".zip",
        mime="application/zip"
    )

# Step 4: Restore the file from compression
if st.button("Restore Original File") and st.session_state["original_file_data"] is not None:
    # Download the original file
    st.download_button(
        label="Download Restored File",
        data=st.session_state["original_file_data"],
        file_name=st.session_state["original_filename"],
        mime="application/octet-stream"
    )

st.write("Note: Extreme compression works best with highly redundant files (e.g., text or JSON). Images, videos, and other media are less compressible.")
