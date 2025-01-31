# import requests
# import json
# def main():
#     with open('utils/hyde.txt', 'r', encoding='utf-8') as file:
#         content = file.read()
#
#     questions = content.split('\n')
#     headers = {
#         'accept': 'application/json',
#         'Content-Type': 'application/json'
#     }
#
#     formatted_questions = []
#     for id in range(50):
#         clean_question = questions[id].strip()
#         clean_question = clean_question.split('. ')
#         if clean_question != '':  # Это позволит игнорировать пустые строки
#             formatted_question = dict(f"id:{id + 1}, query:{clean_question}")
#             formatted_questions.append(formatted_question)
#
#     for fq in formatted_questions:
#         id = fq['id']
#         query = fq['query'][1]
#         data = {
#                 "id": id,
#                 "query": query
#         }
#         response = requests.post("http://localhost:8000/query", headers=headers, data=json.dumps(data))


import requests
import json

def main():
    with open('utils/hyde.txt', 'r', encoding='utf-8') as file:
        content = file.read()

    questions = content.split('\n')
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    formatted_questions = []
    for id in range(50):
        clean_question = questions[id].strip()
        if clean_question:
            formatted_question = {
                "id": id + 1,
                "query": clean_question
            }
            formatted_questions.append(formatted_question)

    for fq in formatted_questions:
        id = fq['id']
        query = fq['query']
        data = {
            "id": id,
            "query": query
        }
        response = requests.post("http://localhost:8080/api/request", headers=headers, data=json.dumps(data))
        print(response.status_code, response.json())

if __name__ == "__main__":
    main()

