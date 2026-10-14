
from langchain_ollama import ChatOllama
from app.config.config import OLLAMA_MODEL, OLLAMA_BASE_URL
from app.common.logger import get_logger

logger = get_logger(__name__)


def load_llm():
    try:
        logger.info("Loading local Ollama model: %s", OLLAMA_MODEL)

        llm = ChatOllama(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=0.3,
        )

        logger.info("Ollama model initialized successfully")
        return llm

    except Exception:
        logger.exception("Failed to initialize Ollama model")
        raise
