from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from rag.retriever import (
    search,
    AUTOMATION_STATIC_ANSWER,
    IT_STATIC_ANSWER,
    TRUONG_STATIC_ANSWER,
    HOSO_STATIC_ANSWER,
    NNANH_STATIC_ANSWER,
    KTHH_STATIC_ANSWER,
    TKDH_STATIC_ANSWER,
    TKVM_STATIC_ANSWER
)
from rag.template import admission_chain
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class ChatInput(BaseModel):
    message: str
@app.post("/chat")
async def chat_endpoint(input_data: ChatInput):
    query = input_data.message
    print(f"📩 Nhận câu hỏi: {query}")

    results = search(query)

    if results == "NGOAI_PHAM_VI":
        return {
            "answer": "Xin lỗi, câu hỏi này nằm ngoài phạm vi tư vấn tuyển sinh.",
            "status": "out_of_scope"
        }
    if results == "TKDH_STATIC":
        return {
            "answer": TKDH_STATIC_ANSWER,
            "status": "success"
        }
    if results == "TKVM_STATIC":
        return {
            "answer": TKVM_STATIC_ANSWER,
            "status": "success"
        }
    if results == "AUTOMATION_STATIC":
        return {
            "answer": AUTOMATION_STATIC_ANSWER,
            "status": "success"
        }
    if results == "NNANH_STATIC":
        return {
            "answer": NNANH_STATIC_ANSWER,
            "status": "success"
        }
    if results == "KTHH_STATIC":
        return {
            "answer": KTHH_STATIC_ANSWER,
            "status": "success"
        }
    if results == "IT_STATIC":
        return {
            "answer": IT_STATIC_ANSWER,
            "status": "success"
        }
    if results == "TRUONG_STATIC":
        return {
            "answer": TRUONG_STATIC_ANSWER,
            "status": "success"
        }
    if results == "HOSO_STATIC":
        return {
            "answer": HOSO_STATIC_ANSWER,
            "status": "success"
        }
    try:
        context_text = "\n\n".join(doc.page_content for doc in results)
        response = admission_chain.invoke({
            "context": context_text,
            "input": query
        })
        return {
            "answer": response,
            "status": "success"
        }
    except Exception as e:
        print("❌ Lỗi:", e)
        raise HTTPException(status_code=500, detail=str(e))
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)