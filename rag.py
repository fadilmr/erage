from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain.vectorstores.utils import filter_complex_metadata


class bappenasRAG:
    vector_store = None
    retriever = None
    chain = None

    def __init__(self):
        self.model = ChatOllama(model="llama3.1:8b")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)
        self.prompt = PromptTemplate.from_template(
            """
            <s> [INST] Anda adalah asisten untuk tugas menjawab pertanyaan. Gunakan potongan konteks yang diambil berikut ini 
            untuk menjawab pertanyaan. Jika Anda tidak tahu jawabannya, katakan saja bahwa Anda tidak tahu. [/INST] </s> 
            [INST] Question: {question} 
            Context: {context} 
            Answer: [/INST]
            """
            # """
            # Anda adalah seorang ahli dalam mengambil pertanyaan spesifik dan mengekstrak pertanyaan yang lebih umum yang mengarah pada \
            # prinsip-prinsip dasar yang diperlukan untuk menjawab pertanyaan spesifik.
            # berikut adalah konteks yang diambil dari dokumen yang diunggah sebelumnya: {context}
            # instruksi: {question}
            # Jawaban:
            # """
        )

    def ingest(self, pdf_file_path: str):
        docs = PyPDFLoader(file_path=pdf_file_path).load()
        title = docs[0].metadata.get('title', 'Unknown Title')
        chunks = self.text_splitter.split_documents(docs)

        for chunk in chunks:
            chunk.metadata["page"] = chunk.metadata.get("page", "Unknown Page")
            chunk.metadata["title"] = title

        chunks = filter_complex_metadata(chunks)

        vector_store = Chroma.from_documents(documents=chunks, embedding=FastEmbedEmbeddings())
        self.retriever = vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 3,
                "score_threshold": 0.5,
            },
        )

        self.chain = ({"context": self.retriever, "question": RunnablePassthrough()}
                      | self.prompt
                      | self.model
                      | StrOutputParser())

    def ask(self, query: str):
        if not self.chain:
            return "Please, add a PDF document first."

        return self.chain.invoke(query)

        # if isinstance(result, list):
        #     response = ""
        #     for res in result:
        #         content = res.get("content", "No content found")
        #         title = res["metadata"].get("title", "Unknown Title")
        #         page = res["metadata"].get("page", "Unknown Page")
                
        #         # Format the response to include the content, title, and page number
        #         response += f"Answer: {content}\nFrom: {title}\nPage: {page}\n\n"
        #     return response
        # else:
        #     return result

    def clear(self):
        self.vector_store = None
        self.retriever = None
        self.chain = None