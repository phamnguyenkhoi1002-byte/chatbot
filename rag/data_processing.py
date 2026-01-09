import os
import re
from langchain_core.documents import Document

def load_and_split_data(data_dir):
    documents = []

    for root, _, files in os.walk(data_dir):
        for file in files:
            if not file.endswith(".txt"):
                continue

            path = os.path.join(root, file)

            with open(path, "r", encoding="utf-8") as f:
                text = f.read().strip()

            # --- LOGIC 1: LẤY TIÊU ĐỀ NGÀNH (2 dòng đầu) ---
            lines = text.splitlines()
            title = "\n".join(lines[:2]).strip()

            # --- LOGIC 2: TÌM PHẦN "GIỚI THIỆU" ---
            match = re.search(
                r"(1\.\s*Giới thiệu.*?)(\n\d+\.|\Z)",
                text,
                re.DOTALL | re.IGNORECASE
            )

            if match:
                intro = match.group(1).strip()
                content = title + "\n\n" + intro
            else:
                # fallback: dùng toàn bộ nội dung
                content = title + "\n\n" + text

            documents.append(
                Document(
                    page_content=content,
                    metadata={
                        "source": path,
                        "file": file
                    }
                )
            )

    print(f"DEBUG: Tạo được {len(documents)} document (mỗi ngành = 1 doc)")
    return documents