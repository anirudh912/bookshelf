import streamlit as st
from file_handler import upload_to_s3, download_from_s3, list_files_in_s3, delete_file_from_s3
import boto3
from summarizer import chat_with_doc_bedrock

profile_name = "books"
bucket_name = "bookshelf-db"
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('bookshelf-text')

st.title("BookShelf: Smart Document Hub")
st.write("All your documents, summarized and searchable!")

#Sidebar to upload files
with st.sidebar:
    st.header("Upload File")
    uploaded_file = st.file_uploader("Choose a file to upload")
    object_name = st.text_input("Document name (optional)", value="")
    if st.button("Upload") and uploaded_file:
        import tempfile, os
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name
        try:
            upload_to_s3(temp_file_path, bucket_name, object_name or uploaded_file.name, profile_name)
            st.success("File uploaded successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            os.unlink(temp_file_path)

#Main section with document list and to search documents
st.header("Your Files")
search_term = st.text_input("Search by filename or summary keyword")
response = table.scan()
items = response.get('Items', [])
if search_term:
    items = [item for item in items if search_term.lower() in item['doc_id'].lower() or search_term.lower() in item.get('summary', '').lower()]

for item in items:
    with st.expander(item['doc_id']):
        st.write("**Summary:**", item.get('summary', 'No summary yet.'))
        if st.button(f"Show full text for {item['doc_id']}", key=f"text_{item['doc_id']}"):
            st.write(item.get('text', 'No text extracted.'))

        #AI Chat
        st.write("**Chat with this document:**")
        user_question = st.text_input(f"Ask a question about {item['doc_id']}:", key=f"q_{item['doc_id']}")
        if st.button(f"Ask", key=f"ask_{item['doc_id']}") and user_question:
            answer = chat_with_doc_bedrock(item.get('text', ''), user_question)
            st.write("**AI Answer:**", answer)

        #Download & delete
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Download", key=f"download_{item['doc_id']}"):
                import tempfile, os
                from file_handler import download_from_s3
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file_path = temp_file.name
                try:
                    download_from_s3(bucket_name, item['doc_id'], temp_file_path, profile_name)
                    with open(temp_file_path, "rb") as f:
                        st.download_button("Download", data=f, file_name=item['doc_id'])
                finally:
                    os.unlink(temp_file_path)
        with col2:
            if st.button("Delete", key=f"delete_{item['doc_id']}"):
                from file_handler import delete_file_from_s3
                delete_file_from_s3(bucket_name, item['doc_id'], profile_name)
                st.success("File deleted!")
                st.rerun()
