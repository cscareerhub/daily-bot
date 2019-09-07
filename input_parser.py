import json
import urllib.request

def json_parser(url : str):
    request = urllib.request.Request(url, headers={'User-Agent' : "DailyBot Browser"})
    with urllib.request.urlopen(request) as web:
        data = json.loads(web.read().decode())

        questions = []

        for row in data:
            questions.append((row['title'], row['ds'], row['body']))

        return questions