# from duckduckgo_search import DDGS
# from markdownify import markdownify
# import re
# import requests
# from openai import OpenAI
# from schemas.structured_output import ClearingWebpageResponse
#
#
# client = OpenAI(
#     api_key="",
#     base_url="",
# )
#
#
# def use_browser(query: str) -> str:
#     """
#     Позволяет воспользоваться браузером для поиска по интернету
#
#     Args:
#         query: То, что ты хочешь найти
#
#     Returns:
#         Все ссылки, в которых лежит информация по твоему запросу
#     """
#     result = DDGS().text(query, max_results=10)
#     result = [i['href'] for i in result]
#     return result
#
# def visit_webpage(url: str) -> str:
#     """Посети вебстраницу и верни контент оттуда в виде markdown.
#
#     Args:
#         url: URL веб-страницы для посещения.
#
#     Returns:
#         Контент веб-страницы в markdown.
#     """
#     # Send a GET request to the URL
#     response = requests.get(url)
#     if response.status_code in (402, 403):
#         return None
#
#     response.raise_for_status()  # Raise an exception for bad status codes
#
#     # Convert the HTML content to Markdown
#     markdown_content = markdownify(response.text).strip()
#
#     # Remove multiple line breaks
#     markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)
#     markdown_content = ' '.join(markdown_content.split())
#     markdown_content =markdown_content [0:120_000]
#
#     clear_data = clear_webpage(markdown_content)
#     return clear_data
#
# def clear_webpage(webpage_text: str) -> str:
#     completion = client.beta.chat.completions.parse(
#     model="openai/gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant. Guide the user through the solution step by step."},
#         {"role": "user", "content": f"""
#         Ты -- профессиональный разметчик, который очищает текст вебстраницы от грязных данных, которой является реклама, ссылки и другой вид визуального мусора. Ты должен вернуть ВЕСЬ ИМЕЮЩИЙСЯ ТЕКСТ, НО ОЧИЩЕННЫЙ ОТ МУСОРА.
#         Текст страницы: {webpage_text}
#         """
#     }
#     ],
#     response_format=ClearingWebpageResponse,
#     )
#
#     reasoning = completion.choices[0].message.parsed
#
#     return reasoning
#
#
# print([visit_webpage(i) for i in use_browser('В каком году Университет ИТМО был включён в число Национальных исследовательских университетов России?')])




