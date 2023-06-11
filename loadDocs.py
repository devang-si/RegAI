import json
import os
from dotenv import load_dotenv, find_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import GoogleDriveLoader
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex, \
                        LLMPredictor, PromptHelper

_ = load_dotenv(find_dotenv())

def initialize_qa():
    folder_id = "1jRxpAwHVEHzYoMAlsM-sTITGRmRLB7U1"
    loader = GoogleDriveLoader(
        folder_id=folder_id,
        recursive=False
    )
    docs = loader.load()    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=4000, chunk_overlap=0.2, separators=[" ", ",", "n"]
    )

    texts = text_splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()
    db = Chroma.from_documents(texts, embeddings)
    retriever = db.as_retriever()

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

    return qa

def initialize_index():
    # define policyFolder which directs to policies folder in the same directory
    policyFolder = os.path.join(os.path.dirname(__file__), 'policies')

    # policyFolder = '/Policies/'
    print(os.listdir(policyFolder))
    loaders = [UnstructuredPDFLoader(os.path.join(policyFolder, fn) for fn in os.listdir(policyFolder))]

    index = VectorStoreIndexCreator().from_loaders(loaders)

    return index


# def get_answer_from_index(index, query):
#     answer = index.query(query)
#     return answer

def get_answer(qa, data):


    name = data['name']
    age = data['age']
    salary = data['salary']
    gender = data['gender']
    caste = data['caste']
    state = data['state']
    additionalInfo = data['additionalInfo']

    query = "My name is " + name + " salary is " + str(salary) + " age is " + str(age) + " gender is " + gender + " caste is " + caste + " state is " + state + "additional info about me is: " + additionalInfo + ". I want to know about policies available for me. give the response in the json format with policies as array of objects and each object having three fields: policy, summary, benefits. give only policies array in output no extra data. [JSON]"

    answer = qa.run(query)
    parsed_response = json.loads(answer)
    print(parsed_response)
    return parsed_response

def index_documents(folder):
    max_input_size    = 4096
    num_output       = 512
    chunk_overlap_ratio = 0.2
    chunk_size_limit  = 600

    prompt_helper = PromptHelper(max_input_size = max_input_size, 
                                 num_output = num_output, 
                                 chunk_overlap_ratio = chunk_overlap_ratio, 
                                 chunk_size_limit = chunk_size_limit)
    
    llm_predictor = LLMPredictor(
        llm = ChatOpenAI(temperature = 0.7, 
                         model_name = "gpt-3.5-turbo")
        )

    documents = SimpleDirectoryReader(folder).load_data()

    index = GPTVectorStoreIndex.from_documents(
                documents, 
                llm_predictor = llm_predictor, 
                prompt_helper = prompt_helper)

    index.storage_context.persist(persist_dir=".") # save in current directory