from sentence_transformers import SentenceTransformer
from ..config.settings import settings

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(settings.MODEL_NAME)

    def create_embedding(self, text: str) -> list:
        try:
            vector = self.model.encode(text).tolist()
            return vector
        except Exception as e:
            raise Exception(f"Error creating embedding: {str(e)}")

    def batch_create_embeddings(self, texts: list) -> list:
        try:
            vectors = self.model.encode(texts).tolist()
            return vectors
        except Exception as e:
            raise Exception(f"Error creating batch embeddings: {str(e)}")
