from fastapi import APIRouter, HTTPException
import uuid
from ..services.cosmos_service import CosmosService
from ..services.embedding_service import EmbeddingService
from ..models.document import VectorDocument, SearchQuery
from ..models.document import SearchQuery

router = APIRouter()
cosmos_service = CosmosService()
embedding_service = EmbeddingService()

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

class VectorizeRequest(BaseModel):
    query: dict


@router.post("/vectorize")
async def vectorize_text(request: VectorizeRequest):
    try:
        text = request.query["text"]
        category = request.query["category"]
        
        # Create embedding
        vector = embedding_service.create_embedding(text)
        
        # Create document
        document = VectorDocument(
            id=str(uuid.uuid4()),
            text=text,
            vector=vector,
            category=category
        )
        
        # Store in Cosmos DB (synchronously)
        result = cosmos_service.store_document(document)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search")
async def search_similar(request: SearchQuery):
    try:
        # Generate embedding for search query
        vector = embedding_service.create_embedding(request.query)
        
        # Use the correct method name as defined in CosmosService
        results = cosmos_service.search_similar_documents(
            vector=vector,
            top_k=request.top_k,
            category=request.category
        )
        
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
