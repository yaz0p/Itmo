import os
import numpy as np
from qdrant_client import QdrantClient, AsyncQdrantClient
from typing import List
from uuid import uuid4
from openai import AsyncOpenAI
import asyncio
from qdrant_client.models import (
    NamedVector,
    PointStruct,
    SearchRequest,
)

BASE_URL=os.getenv("BASE_URL")
API_KEY=os.getenv("API_KEY")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

COLLECTION_NAME = "itmo_megaschool"
CLIENT = QdrantClient("http://qdrant:6333")  

async def _make_dense_embedding(text: str):
    embeding = await client.embeddings.create(
    model="text-embedding-ada-002",
    input=text,
    encoding_format="float"
)      
    return embeding.data[0].embedding


def _make_points(candidates: List[str], urls: List[str], dense_embedings: List[np.ndarray]):
    points = []
    for idx, (text, url, dense_vector) in enumerate(
        zip(candidates, urls, dense_embedings)
    ):
        point = PointStruct(
            id=str(uuid4()),
            payload={
                "text": text,
                "metadata": {
                        "source": url,
                        }
            },
            vector={
                "text-dense": dense_vector.tolist(),
            },
        )
        points.append(point)
    return points


async def insert_into_db(candidates: List[str], urls: List[str]):
    tasks = [_make_dense_embedding(candidate) for candidate in candidates]
    dense_embedings = await asyncio.gather(*tasks)
    dense_embedings = [np.asarray(array, dtype=np.float32) for array in dense_embedings]
    points = _make_points(candidates, urls, dense_embedings)
    CLIENT.upsert(collection_name=COLLECTION_NAME, points=points)


async def search(query_text: str):
    dense_embedings = await _make_dense_embedding(query_text)
    search_results = CLIENT.search_batch(
        collection_name=COLLECTION_NAME,
        requests=[
            SearchRequest(
                vector=NamedVector(
                    name="text-dense",
                    vector=dense_embedings,
                ),
                limit=3,
                with_payload=True,
            ),
        ],
    )
    return search_results
