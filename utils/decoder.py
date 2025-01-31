from openai import OpenAI
from schemas.structured_output import ValidataionReasoningResponse
import os

BASE_URL=os.getenv("BASE_URL")
API_KEY=os.getenv("API_KEY")

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)


def validate_request(query, information = None) -> ValidataionReasoningResponse:
    completion = client.beta.chat.completions.parse(
    model="openai/gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant. Guide the user through the solution step by step."},
        {"role": "user", "content":     f"""Пожалуйста, оцени возможность ответить на поставленный вопрос. Тебе нужно действовать по следующему алгоритму:
                                        Проверь, дана ли тебе информация для ответа на вопрос. Если есть информация, то оцени её релевантность относительно запроса и оцени смог бы ли ты дать ответ на заданный вопрос, опираясь на контекст.
                                        Если такой информации нет, то
                                            1.1 Проверь, есть ли в заданном вопросе предложенные ответы на вопрос и выдеди их в виде словаря с ключом в виде номера ответа и значения в виде ответа на вопрос.
                                            1.2 Если вариантов ответа нет, то ответь None

                                        Если информация для ответа есть: 
                                            Оцени свою возможность для на ответа на вопрос. Если ты сможешь точно ответить на вопрос, с предоставленной информацией, то ответь 1, если не сможешь, то выведи 0.
                                    -----------
                                    **Запрос:** {query}
                                    **Информация для составления ответа:** {information}
                                    """
    }
    ],
    response_format=ValidataionReasoningResponse,
    )
    
    reasoning = completion.choices[0].message.parsed

    return reasoning
