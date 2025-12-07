from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI # Switched imports for Gemini
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from typing import Optional

from app.core.config import settings # Updated import path

class RAGService:
    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings( # Switched to GoogleGenerativeAIEmbeddings
            model=settings.GEMINI_EMBEDDING_MODEL,
            google_api_key=settings.GEMINI_API_KEY
        )
        self.llm = ChatGoogleGenerativeAI( # Switched to ChatGoogleGenerativeAI
            model=settings.GEMINI_CHAT_MODEL,
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0,
            convert_system_message_to_human=True # Can be useful for some Gemini models
        )
        
        # Initialize Qdrant client directly
        self.qdrant_client_instance = QdrantClient(
            url=settings.QDRANT_CLOUD_URL, 
            api_key=settings.QDRANT_API_KEY
        )

        # Initialize LangChain Qdrant vector store with the client instance
        self.vectorstore = QdrantVectorStore(
            client=self.qdrant_client_instance,
            collection_name=settings.QDRANT_COLLECTION_NAME,
            embedding=self.embeddings,
        )
        self.retriever = self.vectorstore.as_retriever()

        # Define the prompt template for RAG
        self.rag_template = """
You are a helpful assistant for the "Physical AI & Humanoid Robotics" online course.
Answer the question based only on the following context.
If the answer is not in the context, say that you don't have enough information to answer.
Keep the answer concise and to the point.

Context:
{context}

Question: {question}

Answer:
"""
        self.rag_prompt = PromptTemplate.from_template(self.rag_template)

        # Define the prompt template for selected text only
        self.selected_text_template = """
You are a helpful assistant for the "Physical AI & Humanoid Robotics" online course.
Answer the question based ONLY on the following text selected by the user.
If the answer is not in the selected text, say that you cannot answer from the provided text.
Keep the answer concise and to the point.

Selected Text:
{selected_text}

Question: {question}

Answer:
"""
        self.selected_text_prompt = PromptTemplate.from_template(self.selected_text_template)


    def get_rag_chain(self):
        """
        Creates and returns the RAG chain for full document search.
        """
        return (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | self.rag_prompt
            | self.llm
            | StrOutputParser()
        )
    
    def get_selected_text_chain(self):
        """
        Creates and returns a chain for selected text Q&A.
        """
        return (
            {"selected_text": RunnablePassthrough(), "question": RunnablePassthrough()}
            | self.selected_text_prompt
            | self.llm
            | StrOutputParser()
        )


    def answer_query(self, query: str, selected_text: Optional[str] = None, user_id: Optional[str] = None) -> str:
        """
        Answers a query using the RAG pipeline or selected text only.
        If selected_text is provided, it answers ONLY from selected text (no vector DB).
        Else, it uses the full RAG pipeline.
        """
        if selected_text:
            chain = self.get_selected_text_chain()
            return chain.invoke({"selected_text": selected_text, "question": query})
        else:
            chain = self.get_rag_chain()
            return chain.invoke(query)

# Instantiate the service
rag_service = RAGService()
