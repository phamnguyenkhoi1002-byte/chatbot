from data_processing import load_documents
from embedding import get_embedding_model

docs = load_documents("data")
print(f"Đã load {len(docs)} tài liệu")

embeddings = get_embedding_model()
vec = embeddings.embed_query("ngành tự động hóa là gì")

print("Embedding OK, chiều vector =", len(vec))
