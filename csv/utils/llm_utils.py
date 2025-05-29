import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_google_genai import ChatGoogleGenerativeAI

def get_llm():
    load_dotenv()
    model = os.getenv("LLM_MODEL")
    model_provider = os.getenv("LLM_MODEL_PROVIDER")
    print(f"LLM_MODEL={model} and LLM_MODEL_PROVIDER={model_provider}")

    if model_provider == "google_genai":
        return ChatGoogleGenerativeAI(
            model=model,
            google_api_key=os.getenv("GEMINI_API_KEY")
        )

    return init_chat_model(model=model, model_provider=model_provider)
