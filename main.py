import time
from typing import List

from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import HttpUrl
from schemas.request import PredictionRequest, PredictionResponse
from utils.logger import setup_logger
from utils.search_tool import main as search_tool
from utils.vdb_tool import insert_into_db, search, _make_dense_embedding
from dummy_agent import get_answer, check_relevance_information

# Initialize
app = FastAPI()
logger = None


@app.on_event("startup")
async def startup_event():
    global logger
    logger = await setup_logger()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    body = await request.body()
    await logger.info(
        f"Incoming request: {request.method} {request.url}\n"
        f"Request body: {body.decode()}"
    )

    response = await call_next(request)
    process_time = time.time() - start_time

    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk

    await logger.info(
        f"Request completed: {request.method} {request.url}\n"
        f"Status: {response.status_code}\n"
        f"Response body: {response_body.decode()}\n"
        f"Duration: {process_time:.3f}s"
    )

    return Response(
        content=response_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type,
    )


@app.post("/api/request", response_model=PredictionResponse)
async def predict(body: PredictionRequest):
    try:
        NEW_INFO = False
        await logger.info(f"Processing prediction request with id: {body.id}")
        # Здесь будет вызов вашей модели
        query = body.query
        logger.info(query)
        naive_candidates = await search(query)

        if await check_relevance_information(query, naive_candidates) != 1:
            knowlege_base = await search_tool(query)
            ulrs = knowlege_base[0]
            texts = knowlege_base[1]
            NEW_INFO = True
        agent_answer = await get_answer(query, knowlege_base)
        reasoning = ' '.join(i.explanation for i in agent_answer.steps)
        
        logger.info(agent_answer)
        
        asnwer = agent_answer.answer
        if asnwer == 0:
            asnwer = None
        sources: List[HttpUrl] = [HttpUrl(url) for url in ulrs]
        if NEW_INFO:
            try:
                await insert_into_db(texts, ulrs)
            except Exception as e:
                logger.error(e)
        response = PredictionResponse(
            id=body.id,
            answer=asnwer,
            reasoning=reasoning+'\nCгенерировано gpt-4o-2024-11-20',
            sources=sources,
        )
        await logger.info(f"Successfully processed request {body.id}")
        return response
    except ValueError as e:
        error_msg = str(e)
        await logger.error(f"Validation error for request {body.id}: {error_msg}")
        raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
        await logger.error(f"Internal error processing request {body.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
