

import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

# write a function that takes in a query and returns an answer

def function(query):
    return "This is a test answer"


from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import GoogleDriveLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
# import openai

# openai.openai_api_key='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'




folder_id = "1_tRD6uhQnv7V72m6L8XmDxSWJHtUNmIg"
loader = GoogleDriveLoader(
    folder_id=folder_id,
    recursive=False
)
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=4000, chunk_overlap=0, separators=[" ", ",", "\n"]
    )

texts = text_splitter.split_documents(docs)
embeddings = OpenAIEmbeddings()
db = Chroma.from_documents(texts, embeddings)
retriever = db.as_retriever()

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

# 


while True:
    query = input("> ")
    answer = qa.run(query)
    print(answer)

   