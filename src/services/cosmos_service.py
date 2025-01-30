from azure.cosmos import CosmosClient, PartitionKey
from ..config.settings import settings
from ..models.document import VectorDocument
from typing import List, Optional

class CosmosService:
    def __init__(self):
        self.client = CosmosClient(settings.COSMOS_ENDPOINT, settings.COSMOS_KEY)
        self.database = self.client.get_database_client(settings.DATABASE_NAME)
        self.container = self.database.get_container_client(settings.CONTAINER_NAME)

    def store_document(self, document: VectorDocument):
        try:
            # Convert document to dict before storing
            doc_dict = document.dict()
            # Create item synchronously
            return self.container.create_item(body=doc_dict)
        except Exception as e:
            raise Exception(f"Error storing document: {str(e)}")

    def search_similar(self, vector: List[float], top_k: int = 5, category: Optional[str] = None):
        try:
            # Convert vector list to string representation
            vector_str = str(vector).replace('[', '').replace(']', '')
            
            # Build the query without ORDER BY
            if category:
                query = f"""
                SELECT TOP @top_k *,
                ST_DISTANCE(c.vector, [{vector_str}]) as similarity
                FROM c
                WHERE c.category = @category
                """
                parameters = [
                    {"name": "@top_k", "value": top_k},
                    {"name": "@category", "value": category}
                ]
            else:
                query = f"""
                SELECT TOP @top_k *,
                ST_DISTANCE(c.vector, [{vector_str}]) as similarity
                FROM c
                """
                parameters = [
                    {"name": "@top_k", "value": top_k}
                ]
            
            # Execute query with parameters
            items = list(self.container.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=True
            ))
            
            return items
        except Exception as e:
            raise Exception(f"Error searching similar documents: {str(e)}")
    from azure.cosmos import CosmosClient, PartitionKey
from ..config.settings import settings
from ..models.document import VectorDocument
from typing import List, Optional

class CosmosService:
    def __init__(self):
        self.client = CosmosClient(settings.COSMOS_ENDPOINT, settings.COSMOS_KEY)
        self.database = self.client.get_database_client(settings.DATABASE_NAME)
        self.container = self.database.get_container_client(settings.CONTAINER_NAME)

    def store_document(self, document: VectorDocument):
        try:
            doc_dict = document.dict()
            return self.container.create_item(body=doc_dict)
        except Exception as e:
            raise Exception(f"Error storing document: {str(e)}")

    def search_similar_documents(self, vector: List[float], top_k: int = 5, category: Optional[str] = None):
        try:
            vector_str = str(vector).replace('[', '').replace(']', '')
            
            # Specify exact columns instead of using *
            query = """
            SELECT c.id, c.text, c.category, c.timestamp, 
                ST_DISTANCE(c.vector, [{0}]) AS similarity
            FROM c
            WHERE IS_ARRAY(c.vector)
            """.format(vector_str)

            if category:
                query += " AND c.category = @category"
                parameters = [{"name": "@category", "value": category}]
            else:
                parameters = []

            items = list(self.container.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=True
            ))
            
            # Sort by similarity score and limit results
            items.sort(key=lambda x: x.get('similarity', float('inf')))
            return {
                "results": items[:top_k],
                "total_count": len(items)
            }
        except Exception as e:
            raise Exception(f"Error searching similar documents: {str(e)}")
