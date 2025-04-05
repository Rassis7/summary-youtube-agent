from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

import os
from dotenv import load_dotenv

load_dotenv()


class LLM:
    @staticmethod
    def load_ollama_model(model_name, temperature=0.5):
        model = ChatOllama(
            model=model_name,
            base_url=os.getenv("OLLAMA_API_URL"),
            temperature=temperature,
        )
        return model

    @staticmethod
    def load_open_ai_model(temperature=0.5):
        model = ChatOpenAI(
            model_name=os.getenv("OPENAI_MODEL"),
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=temperature,
        )
        return model
