import os
from CFG import *
from ml import get_answer_gpt
from promts import get_promt
from fastapi import FastAPI, UploadFile, File
from ml import get_texts_from_file, get_vector_db, get_text_from_db
# from langchain.embeddings import HuggingFaceInstructEmbeddings
from SQlite.sqlite import *
from SQlite.vector_dbs import *
from fastapi.responses import FileResponse
app = FastAPI()
from urllib.parse import unquote

# embeddings = None
# llm = None

# @app.on_event("startup")
# def startup_event():
#     global embeddings, llm
#     embeddings = HuggingFaceInstructEmbeddings(
#         model_name=CFG.embeddings_model_repo)
#     llm = get_llm()


#обработать ошибки
@app.post("/file/upload-file")
async def upload_file(file_name, username, file: UploadFile = File(...)):
    file_content = await file.read()
    db = get_vector_db(file_content)
    file_name = unquote(file_name, encoding='utf-8')
    db.save_local(f"Vector_dbs/{username}/{file_name}")
    return True

#обработать ошибки
@app.post("/text/upload-text")
async def upload_text(content, username, content_name):
    db = get_vector_db(content, text_flag=True)
    db.save_local(f"Vector_dbs/{username}/{content_name}")
    return True


# @app.post("/simularity")
# async def get_text(question):
#     text = get_text_from_db(question)
#     return text

@app.post("/getanswer")
async def get_answer_with_any_model(question, answers,choice,username):
    text = get_text_from_db(question,choice, username)
    promt = get_promt(question, text[0], answers)
    answer = get_answer_gpt(promt)
    return answer, text[0]


@app.get("/create_user_table")
async def create_usertable():
    await create_usertable()

@app.get("/login_user")
async def login(username, password):
    await login_user(username,password)






#
# @app.post("/getanswer/llm")
# async def get_answer_with_any_model(question, answers,choice,username):
#     text = get_text_from_db(question,choice, username)
#     promt = get_promt(question, text[0], answers)
#     answer = llm(promt)
#     return answer, text[0]


