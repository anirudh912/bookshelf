import streamlit as st
import os
import tempfile
from file_handler import upload_to_s3, download_from_s3, list_files_in_s3, delete_file_from_s3

st.title("BookShelf")
st.write("All your documents organized within reach!")

profile_name="books"
bucket_name = "bookshelf-db"

#sidebar
with st.sidebar:
    st.header("Upload File")
    uploaded_file = st.file_uploader("Choose a file to upload")
    object_name = st.text_input("Give the document a name(optional)", value="")
    if st.button("Upload") and uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name
        try:
            if upload_to_s3(temp_file_path, bucket_name, object_name or uploaded_file.name, profile_name):
                st.success("File uploaded successfully!")
            else:
                st.error("File upload failed.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            os.unlink(temp_file_path)

#main
st.header("Your Files")
if st.button("Refresh", key="refresh"):
    st.rerun()
files = list_files_in_s3(bucket_name, profile_name)
if files:
    for file in files:
        col1, col2, col3 = st.columns([4, 1, 1])
        with col1:
            st.write(file)
        with col2:
            if st.button("Download", key=f"download_{file}"):
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file_path = temp_file.name
                try:
                    if download_from_s3(bucket_name, file, temp_file_path, profile_name):
                        with open(temp_file_path, "rb") as f:
                            st.download_button("Download", data=f, file_name=file)
                    else:
                        st.error("File download failed.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                finally:
                    os.unlink(temp_file_path)
            with col3:
                if st.button("Delete", key=f"delete_{file}"):
                    try:
                        if delete_file_from_s3(bucket_name, file, profile_name):
                            st.success("File deleted successfully!")
                            st.rerun()
                        else:
                            st.error("File deletion failed.")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
else:
    st.write("No files here. Add some!")