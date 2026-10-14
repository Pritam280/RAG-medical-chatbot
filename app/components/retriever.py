
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

from app.components.llm import load_llm
from app.components.vector_store import load_vector_store

from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

CUSTOM_PROMPT_TEMPLATE = """
You are a medical information assistant.

Answer the question in 2 to 3 lines maximum using only the information
provided in the context.

If the context does not contain enough information to answer the question,
clearly say that the provided documents do not contain the answer.
Do not invent medical facts.

Context:
{context}

Question:
{question}

Answer:
"""


def set_custom_prompt():
    return PromptTemplate(
        template=CUSTOM_PROMPT_TEMPLATE,
        input_variables=["context", "question"],
    )


def create_qa_chain():
    try:
        logger.info("Loading vector store for context")
        db = load_vector_store()

        if db is None:
            raise CustomException("Vector store not present or empty")

        logger.info("Loading Ollama LLM")
        llm = load_llm()

        if llm is None:
            raise CustomException("LLM not loaded")

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=db.as_retriever(
                search_kwargs={"k": 3}
            ),
            return_source_documents=False,
            chain_type_kwargs={
                "prompt": set_custom_prompt()
            },
        )

        logger.info("Successfully created the QA chain")
        return qa_chain

    except Exception as e:
        logger.exception("Failed to create the QA chain")
        raise CustomException("Failed to make a QA chain", e) from e
