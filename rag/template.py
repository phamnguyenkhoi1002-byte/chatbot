from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_google_genai import ChatGoogleGenerativeAI
MY_TEMPLATE = """
Hãy trả lời câu hỏi của thí sinh dựa trên thông tin (Context) dưới đây.

Bối cảnh (CONTEXT):
{context}

Câu hỏi của thí sinh:
{input}

Note:
- Chỉ trả lời dựa trên thông tin có trong phần (CONTEXT)
- Nếu câu hỏi của thí sinh không liên quan đến tuyển sinh hoặc không có trong (CONTEXT), hãy trả lời: "XIN_LOI_NGOAI_PHAM_VI".
- Trả lời ngắn gọn, rõ ràng bằng tiếng Việt.
- Xưng hô thân thiện (Ví dụ: Chào bạn, Thân chào thí sinh...).
"""

# Tạo object prompt để file khác có thể gọi dùng
admission_prompt = ChatPromptTemplate.from_template(MY_TEMPLATE)

GOOGLE_API_KEY = "AIzaSyBbar2W_GgD2g2xKQJ6m3bOz3ZPfXJgmLU"

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    google_api_key=GOOGLE_API_KEY,
    temperature=0.3,          
    max_retries=2
)

admission_chain = admission_prompt | llm | StrOutputParser()