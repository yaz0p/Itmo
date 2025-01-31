import asyncio
from duckduckgo_search import DDGS
from markdownify import markdownify
import re
import aiohttp
from openai import AsyncOpenAI
from schemas.structured_output import ClearingWebpageResponse
from typing import List, Union
import os

from concurrent.futures import ThreadPoolExecutor
from googlesearch import search


WEB_PAGE_COUNT = 3
BASE_URL=os.getenv("BASE_URL")
API_KEY=os.getenv("API_KEY")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)


def get_relavant_links(query: str):
    return list(search(query,  num_results=3, unique=True, lang="ru"))



async def use_browser(query: str) -> List[str]:
    """
    Асинхронно выполняет поиск в интернете
    """
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, lambda: DDGS().text(query, max_results=WEB_PAGE_COUNT))
    return [i['href'] for i in result]


async def visit_webpage(url: str, query: str, session: aiohttp.ClientSession) -> Union[str, None]:
    """
    Асинхронно загружает и обрабатывает веб-страницу
    """
    try:
        async with session.get(url, timeout=3) as response:
            if response.status in (402, 403):
                return None
            response.raise_for_status()
            html = await response.text()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

    markdown_content = await asyncio.to_thread(
        lambda: markdownify(html).strip()
    )
    markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)
    markdown_content = ' '.join(markdown_content.split())[:100_000]
    return await clear_webpage(markdown_content, query)


async def clear_webpage(webpage_text: str, query: str) -> str:
    """
    Асинхронно ищет необходимое содержимое страницы через OpenAI
    """
    try:
        completion = await client.beta.chat.completions.parse(
            model="openai/gpt-4o-mini",
            messages=[
            {"role": "system", "content": "You are a helpful assistant. Guide the user through the solution step by step."},
            {"role": "user", "content": f"""
            Ты -- профессиональный редактор, который ищет ответ на вопрос в предоставленном тексте из вебстраницы с грязными данными. Ты должен вернуть отрывок текста, дающий ответ на заданный вопрос.
            Вопрос: {query}
            Текст страницы: {webpage_text}
            """}],
            response_format=ClearingWebpageResponse,
        )
        return completion.choices[0].message.parsed.clear_text
    except Exception as e:
        print(f"Error cleaning content: {e}")
        return ""


async def main(query: str):
    urls = get_relavant_links(query)#await use_browser(query)
    
    async with aiohttp.ClientSession() as session:
        tasks = [visit_webpage(url, query, session) for url in urls]
        results = await asyncio.gather(*tasks)
        print(urls,results)
        
    return urls, results
        # for url, content in zip(urls, results):
        #     if content:
        #         print(f"{url}:")
        #         print(content)

if __name__ == "__main__":
    asyncio.run(main('В каком году Университет ИТМО был включён в число Национальных исследовательских университетов России?\n1. 2007\n2. 2009\n3. 2011\n4. 2015'))
