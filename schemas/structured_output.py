from typing import Literal, Optional
from pydantic import BaseModel, Field

class ValidataionReasoningSolutionChecklist(BaseModel):
    query: str = Field(..., description="The query to be checked")
    response_options: list[str] = Field(..., description="The response options; Answer [], if you do not find response options; if you find response options, then answer ['number_of_option: option_text', ...]")

class ValidataionReasoningStep(BaseModel):
    explanation: str = Field(..., description="Explanation of the step")

class ValidataionReasoningResponse(BaseModel):
    checklist: ValidataionReasoningSolutionChecklist
    steps: list[ValidataionReasoningStep]
    answer: Literal[0, 1] = Field(..., description="Answer the question. Can we answer this question? If you can answer the question from the proposed options, then answer `1`, if we have an empty list of questions, then answer `0`. If you can’t see information to answer the question, the response `internet_search`.")


class ClearingWebpageResponse(BaseModel):
    clear_text: str


class DummyRelevanceChecklist(BaseModel):
    checklist: ValidataionReasoningSolutionChecklist
    steps: list[ValidataionReasoningStep] = Field(... ,description="Reasoning why you choose your answer.")
    answer: Literal[0, 1] = Field(..., description="Find or not find information for get accurate answer. If you can answer the question from the proposed options, then answer `1`, if we have an empty list of questions, then answer `0`.")


class DummyAnsweringChecklist(BaseModel):
    checklist: ValidataionReasoningSolutionChecklist
    steps: list[ValidataionReasoningStep]
    answer: Literal[-1,0,1,2,3,4,5,6,7,8,9,10] = Field(..., description="Если ты не видишь вариант ответа, который предложил пользователь, то отвечай -1. При ответе на вопрос внимательно следи за своими рассуждениями.")
