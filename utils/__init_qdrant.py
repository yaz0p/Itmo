from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
)

COLLECTION_NAME = "itmo_megaschool"
CLIENT = QdrantClient("http://qdrant:6333")  

def _init_qdrant():
    CLIENT.recreate_collection(
    COLLECTION_NAME,
    vectors_config={
        "text-dense": VectorParams(
            size=1536,
            distance=Distance.DOT,
        )
    },
)

_init_qdrant()
