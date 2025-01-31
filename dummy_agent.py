from openai import AsyncOpenAI
from schemas.structured_output import DummyRelevanceChecklist, DummyAnsweringChecklist
import os

BASE_URL=os.getenv("BASE_URL")
API_KEY=os.getenv("API_KEY")


client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)



def GET_RELEVANCE_DUMMY_PROMPT(query, knowledge_base):
    return"""
Ты AI-агент, созданный, чтобы отвечать на вопросы пользователей.
Тебе дан пул ответов из базы знаний.
Если ты видишь в них ответ на заданный тебе вопрос с прикрепленным списком ответов,
то напиши 1, если нет — 0. В таком случае я отправлю запрос в поисковую систему и буду искать релевантную информацию, чтобы ты смог ответить на вопрос.
Если списка ответов нет, то ищи предположительный ответ на вопрос, и если ты его найдешь, то пиши 1, если нет — 0.
Вопросы, которые задаются тебе, почти всегда содержат варианты ответов, пронумерованные цифрами от 1 до 10, так что будь внимателен!
От твоего ответа зависит мое поступление на магистратуру моей мечта. Не подведи меня.

Первый пример:
    Вопрос пользователя: 'В каком рейтинге (по состоянию на 2021 год) ИТМО впервые вошёл в топ-400 мировых университетов?\n1. ARWU (Shanghai Ranking)\n2. Times Higher Education (THE) World University Rankings\n3. QS World University Rankings\n4. U.S. News & World Report Best Global Universities'

    Данные из базы знаний:  ['https://itmo.ru/ru/ratings/ratings.htm', 'https://gge.ru/press-center/massmedia/gorod-plus-tv-universitet-itmo-voshel-v-mirovoy-top-100-po-kompyuternym-tekhnologiyam/', 'https://topreytings.ru/itmo-reyting-vuzov-mira/'] ['В 2021 году Университет ИТМО впервые вошёл в топ-400 мировых университетов по версии Times Higher Education World University Rankings.', 'ИТМО включили в престижный рейтинг университетов мира QS World University Rankings by Subject 2021. Он стал единственным петербургским вузом, вошедшим в мировой топ-100 по компьютерным наукам, заняв 74-е место. Кроме того, ИТМО укрепил позиции еще в четырех предметах. Так, вуз продвинулся с 351-400 мест в топ-300 по математике, а по химии - с 451-500 места в группу 351-400.', 'Университет ИТМО вошел в мировой ТОП-400 вузов в рейтинге QS World University Rankings.']

    Ответ: 1


Первый пример:
    Вопрос пользователя: 'В каком году Университет ИТМО был включён в число Национальных исследовательских университетов России?\n1. 2007\n2. 2009\n3. 2011\n4. 2015'

    Данные из базы знаний:  ['https://ru.wikipedia.org/wiki/Университет_ИТМО', 'https://ru.wikipedia.org/wiki/История_Университета_ИТМО', 'https://museum.itmo.ru/page/128/'] ['Статус национального исследовательского университета (НИУ) ИТМО присвоили в 2009 году.', 'В 2009 получил статус национального исследовательского университета.', 'В 2009 году по результатам заседаний конкурсного отбора Министерства образования и науки Российской Федерации вуз получил категорию "национальный исследовательский университет".']

    Ответ: 1


Реальный вопрос:
Вопрос пользователя: {query}

Данные из базы знаний: {knowledge_base}
    """

def GET_ANSWER_DUMMY_PROMPT(query, knowledge_base):
    return f"""
Ты AI-агент, созданный, чтобы отвечать на вопросы пользователей.
Тебе дан пул ответов из базы знаний.
Твой коллега сказал, что здесь лежит ответ на заданный пользователем вопрос.
Пожалуйста, посмотри внимательно вопрос с вариантами ответа и предложенную тебе информацию.
Ты должен сопоставить номер ответа с информацией из базы знаний и ответить числом.
Если вариантов ответа со стороны пользователя нет, то ты ОБЯЗАН ответить: '0'
Вопросы, которые задаются тебе, почти всегда содержат варианты ответов, пронумерованные цифрами от 1 до 10, так что будь внимателен!
От твоего ответа зависит мое поступление на магистратуру моей мечта. Не подведи меня.

Первый пример:
    Вопрос пользователя: 'В каком рейтинге (по состоянию на 2021 год) ИТМО впервые вошёл в топ-400 мировых университетов?\n1. ARWU (Shanghai Ranking)\n2. Times Higher Education (THE) World University Rankings\n3. QS World University Rankings\n4. U.S. News & World Report Best Global Universities'

    Данные из базы знаний:  ['https://itmo.ru/ru/ratings/ratings.htm', 'https://gge.ru/press-center/massmedia/gorod-plus-tv-universitet-itmo-voshel-v-mirovoy-top-100-po-kompyuternym-tekhnologiyam/', 'https://topreytings.ru/itmo-reyting-vuzov-mira/'] ['В 2021 году Университет ИТМО впервые вошёл в топ-400 мировых университетов по версии Times Higher Education World University Rankings.', 'ИТМО включили в престижный рейтинг университетов мира QS World University Rankings by Subject 2021. Он стал единственным петербургским вузом, вошедшим в мировой топ-100 по компьютерным наукам, заняв 74-е место. Кроме того, ИТМО укрепил позиции еще в четырех предметах. Так, вуз продвинулся с 351-400 мест в топ-300 по математике, а по химии - с 451-500 места в группу 351-400.', 'Университет ИТМО вошел в мировой ТОП-400 вузов в рейтинге QS World University Rankings.']

    Ответ: 3


Первый пример:
    Вопрос пользователя: 'В каком году Университет ИТМО был включён в число Национальных исследовательских университетов России?\n1. 2007\n2. 2009\n3. 2011\n4. 2015'

    Данные из базы знаний:  ['https://ru.wikipedia.org/wiki/Университет_ИТМО', 'https://ru.wikipedia.org/wiki/История_Университета_ИТМО', 'https://museum.itmo.ru/page/128/'] ['Статус национального исследовательского университета (НИУ) ИТМО присвоили в 2009 году.', 'В 2009 получил статус национального исследовательского университета.', 'В 2009 году по результатам заседаний конкурсного отбора Министерства образования и науки Российской Федерации вуз получил категорию "национальный исследовательский университет".']

    Ответ: 2

    Вопрос пользователя: 'В каком рейтинге (по состоянию на 2021 год) ИТМО впервые вошёл в топ-400 мировых университетов?'

    Данные из базы знаний:  ['https://itmo.ru/ru/ratings/ratings.htm', 'https://gge.ru/press-center/massmedia/gorod-plus-tv-universitet-itmo-voshel-v-mirovoy-top-100-po-kompyuternym-tekhnologiyam/', 'https://topreytings.ru/itmo-reyting-vuzov-mira/'] ['В 2021 году Университет ИТМО впервые вошёл в топ-400 мировых университетов по версии Times Higher Education World University Rankings.', 'ИТМО включили в престижный рейтинг университетов мира QS World University Rankings by Subject 2021. Он стал единственным петербургским вузом, вошедшим в мировой топ-100 по компьютерным наукам, заняв 74-е место. Кроме того, ИТМО укрепил позиции еще в четырех предметах. Так, вуз продвинулся с 351-400 мест в топ-300 по математике, а по химии - с 451-500 места в группу 351-400.', 'Университет ИТМО вошел в мировой ТОП-400 вузов в рейтинге QS World University Rankings.']

    Ответ: -1


Реальный вопрос:
Вопрос пользователя: {query}

Данные из базы знаний: {knowledge_base}
"""


async def check_relevance_information(query, knowledge_base):
    completion = await client.beta.chat.completions.parse(
    model="openai/gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant. Guide the user through the solution step by step."},
        {"role": "user", "content":  GET_RELEVANCE_DUMMY_PROMPT(query, knowledge_base)}
    ],
    response_format=DummyRelevanceChecklist,
    )
    
    reasoning = completion.choices[0].message.parsed

    return reasoning


async def get_answer(query, knowledge_base):
    completion = await client.beta.chat.completions.parse(
    model="openai/gpt-4o-2024-11-20",
    messages=[
        {"role": "system", "content": "You are a helpful assistant. Guide the user through the solution step by step."},
        {"role": "user", "content": GET_ANSWER_DUMMY_PROMPT(query, knowledge_base)}
    ],
    response_format=DummyAnsweringChecklist,
    )
    
    reasoning = completion.choices[0].message.parsed

    return reasoning

