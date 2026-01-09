import os
import glob
import shutil  # Thư viện để xóa thư mục cũ
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# --- CẤU HÌNH ---
DATA_PATH = "data"  # Thư mục chứa file
DB_PATH = "./vector_db"  # Thư mục lưu trí nhớ
# Model này hiểu tiếng Việt tốt hơn model mặc định
MODEL_NAME = "keepitreal/vietnamese-sbert"


def create_db():
    # 1. Khởi tạo Model nhúng (Embedding)
    print("⏳ Đang tải model ngôn ngữ tiếng Việt (lần đầu sẽ hơi lâu)...")
    embedding_model = HuggingFaceEmbeddings(model_name=MODEL_NAME)

    # 2. Đọc dữ liệu từ file
    documents = []
    print(f"📂 Đang quét thư mục: {DATA_PATH}...")

    # Tìm tất cả file .txt và .pdf trong thư mục và thư mục con
    files_txt = glob.glob(os.path.join(DATA_PATH, "**/*.txt"), recursive=True)
    files_pdf = glob.glob(os.path.join(DATA_PATH, "**/*.pdf"), recursive=True)

    all_files = files_txt + files_pdf
    print(f"-> Tìm thấy tổng cộng {len(all_files)} file.")

    for file_path in all_files:
        try:
            if file_path.endswith(".txt"):
                # Encoding utf-8 để không lỗi font tiếng Việt
                loader = TextLoader(file_path, encoding="utf-8")
                documents.extend(loader.load())
            elif file_path.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())
        except Exception as e:
            print(f"❌ Lỗi khi đọc file {file_path}: {e}")

    if not documents:
        print("⚠️ Không đọc được tài liệu nào cả! Hãy kiểm tra lại thư mục data.")
        return

    # 3. Chia nhỏ văn bản (Chunking)
    # Chia thành đoạn 500 ký tự, gối đầu 100 ký tự để giữ mạch văn
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(documents)
    print(f"-> Đã chia thành {len(chunks)} đoạn nhỏ thông tin.")

    # 4. Xóa dữ liệu cũ (Quan trọng khi đổi Model)
    if os.path.exists(DB_PATH):
        shutil.rmtree(DB_PATH)
        print("🗑️ Đã xóa bộ nhớ cũ để nạp mới.")

    # 5. Tạo Vector DB mới và lưu xuống ổ cứng
    print("🚀 Đang tạo Vector Database (ChromaDB)...")
    Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=DB_PATH
    )

    print("✅ THÀNH CÔNG! Dữ liệu đã được nạp. Bây giờ hãy chạy main.py")


if __name__ == "__main__":
    create_db()