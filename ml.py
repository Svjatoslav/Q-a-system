import io
import fitz
from langchain.vectorstores import FAISS
from openai import OpenAI
from langchain.llms import HuggingFaceHub
import openai
from langchain.document_loaders import PyPDFLoader
from langchain_community.embeddings.openai import OpenAIEmbeddings
import os
from CFG import CFG
from private import TOKEN_OPENAI
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from pypdf import PdfReader


os.environ['OPENAI_API_KEY'] = TOKEN_OPENAI
embeddings = OpenAIEmbeddings()

def get_vec_db_chroma(path, username, file_name):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    with open(f'{path}.txt','w', encoding='utf-8') as file:
        file.write(text)

    loader = TextLoader(f'{path}.txt', encoding='utf-8')
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    all_splits = text_splitter.split_documents(documents)
    vectordb = Chroma.from_documents(documents=all_splits, embedding=embeddings, persist_directory=f"Vector_dbs/{username}/{file_name}_db")
    vectordb.persist()


def get_the_best_chunk(question, choice, username):
    vectordb = Chroma(persist_directory=f'Vector_dbs/{username}/{choice}', embedding_function=embeddings)
    chunk = vectordb.similarity_search(question)
    print(chunk)
    return chunk




def get_texts_from_file(file_content):
    buffer = io.BytesIO(file_content)
    doc = fitz.open(stream=buffer)
    TEXT = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        TEXT.append(page.get_text())
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.create_documents(TEXT)
    return texts

def get_texts_from_texts(content):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.create_documents([content])
    return texts

def get_vector_db(file_content, text_flag = None):
    if text_flag:
        texts = get_texts_from_texts(file_content)
    else:
        texts = get_texts_from_file(file_content)

    ### create embeddings and DB
    vectordb = FAISS.from_documents(
        documents=texts,
        embedding=embeddings
    )
    return vectordb


def get_text_from_db(question, choice, username):
    vectordb = FAISS.load_local(
        f'{CFG.vector_db_path}/{username}/{choice}',
        embeddings
    )
    text = vectordb.similarity_search(question)
    return text

def get_answer_gpt(Promt):
    client = OpenAI()
    response = client.chat.completions.create(
      model="gpt-3.5-turbo-1106",
      # response_format={ "type": "json_object" },
      messages=[
        {"role": "system", "content": f"{Promt}"}
        # {"role": "user", "content": q}
      ]
    )
    return (response.choices[0].message.content)

# def get_llm():
#     llm = HuggingFaceHub(
#         repo_id = CFG.model_name,
#         model_kwargs={
#             "max_new_tokens": CFG.max_new_tokens,
#             "temperature": CFG.temperature,
#             "top_p": CFG.top_p,
#             "repetition_penalty": CFG.repetition_penalty,
#             "do_sample": CFG.do_sample,
#             "num_return_sequences": CFG.num_return_sequences
#         }
#     )
#     return llm


# if __name__ == '__main__':
    # loader = TextLoader("tt.txt",
    #                     encoding="utf8")
    # documents = loader.load()
    # loader = PyPDFLoader(r'C:\Users\Bruhonog\PycharmProjects\Docs_q-a\Vector_dbs\55\Konspekt_UD_1_1.pdf')
    # documents = loader.load()
    # with open('doc.txt', 'w',encoding='utf-8') as file:
    #     file.write(str(documents))

    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    # all_splits = text_splitter.split_documents(documents)
    # vectordb = Chroma.from_documents(documents=all_splits, embedding=embeddings)
    # r = vectordb.similarity_search_with_score('Есть ли в таблице внутри документа человек с фамилией Иванов ?')
    # print(r)

    # from pypdf import PdfReader
    #
    # reader = PdfReader(r"C:\Users\Bruhonog\PycharmProjects\Docs_q-a\Vector_dbs\55\Konspekt_UD_1_1.pdf")
    # text = ""
    # for page in reader.pages:
    #     text += page.extract_text() + "\n"
    # with open('doc.txt', 'w',encoding='utf-8') as file:
    #     file.write(text)
    # loader = TextLoader("doc.txt",
    #                     encoding="utf8")
    # documents = loader.load()
    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    # all_splits = text_splitter.split_documents(documents)
    # vectordb = Chroma.from_documents(documents=all_splits, embedding=embeddings)
    # r = vectordb.similarity_search_with_score('Есть ли в таблице внутри документа человек с фамилией Иванов ?')
    # print(r)
    # r = get_vec_db_chroma('e', '551', 'Konspekt_UD_1_1.pdf')
    # chunk = get_the_best_chunk('Есть ли в таблице внутри документа человек с фамилией Иванов ?','Konspekt_UD_1_1.pdf_db', '551' )
    # print(chunk)