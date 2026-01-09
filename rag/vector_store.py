print("🚀 vector_store.py ĐANG CHẠY")

from langchain_community.vectorstores import Chroma
from data_processing import load_and_split_data
from embedding import get_embedding_model
import os


def build_vector_db():
    print("🔍 Đang đọc & chia dữ liệu...")

    docs = load_and_split_data("data")
    print("DEBUG docs:", len(docs))      # 👈 THÊM DÒNG NÀY

    embedding = get_embedding_model()
    print("DEBUG embedding:", embedding) # 👈 THÊM DÒNG NÀY

    db = Chroma.from_documents(
        documents=docs,
        embedding=embedding,
        persist_directory="chroma_db"
    )

    db.persist()
    print("✅ Đã lưu Chroma DB vào thư mục chroma_db/")


if __name__ == "__main__":
    build_vector_db()
