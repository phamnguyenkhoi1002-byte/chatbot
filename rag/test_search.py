from retriever import search_docs

query = "ngành tự động hóa"
docs = search_docs(query, k=3)

print(f"Tìm thấy {len(docs)} kết quả\n")

for i, d in enumerate(docs, 1):
    print(f"--- KẾT QUẢ {i} ---")
    print(d.page_content)
    print()
