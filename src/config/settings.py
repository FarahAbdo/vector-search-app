from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    COSMOS_ENDPOINT: str = "https://your_cosmos_account.documents.azure.com"
    COSMOS_KEY: str
    DATABASE_NAME: str = "ai-demo-db"
    CONTAINER_NAME: str = "ai-vectors"
    MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Add the Azure OpenAI fields
    azure_openai_key: str
    azure_openai_endpoint: str
    azure_openai_deployment: str
    
    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
