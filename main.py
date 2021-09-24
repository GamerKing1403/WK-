import requests
import json
import pandas as pd


headers = {"Authorization": "Bearer b77ec7da-663a-40a6-a2f3-ef92d9b2ac24"}
df = pd.DataFrame({''})

for i in range(0, 10000, 1000):
    url = f'https://api.wanikani.com/v2/subjects?page_after_id={i}'
    response = json.loads(requests.get(url=url, headers=headers).content.decode('utf-8'))
    for j in range(1000):
        try:
            subject = response['data'][j]
            identity = subject['id']
            obj = subject['object']
            level = subject['data']['level']
            char = subject['data']['characters']
            if obj != 'radical':
                components = subject['data']['component_subject_ids']
            else:
                components = None

            compData = {'ID': identity, 'Object': obj, 'Level': level, 'Char': char, 'Components': components}
            df = df.append(compData, ignore_index=True)
        except IndexError:
            continue

df.to_excel('test.xlsx')
