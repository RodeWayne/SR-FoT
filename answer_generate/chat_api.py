import requests
import json
import random

def chat(prompt,idx,T,p):
    url = ''
    gpt_keys = []
    
    gpt_key = gpt_keys[idx]

    headers = {
        'Authorization': f'Bearer {gpt_key}',
        'Content-Type': 'application/json'
        }
    
    try:
        response =  requests.post(url, headers=headers, json={
                    "model": "gpt-3.5-turbo",
                    "temperature": T,
                    'max_tokens': 3096,
                    'top_p': p,
                    'frequency_penalty': 0,
                    'presence_penalty': 0,
                    'messages':[{
                        "role":'user',
                        'content': prompt
                    }]
                    },
                    stream=False,
                    verify=False,
                    timeout=60
                )
        data = response.content.decode()
        json_data = json.loads(data)
        # return json_data
        return json_data['choices'][0]['message']['content']
    except requests.exceptions.Timeout:
        return 'timeout'    
    except Exception as e:
        print(e)
        # count += 1
        # print(f"An error occurred: {e},retry time:{count}")
    
        #prog = response.choices[0]['text'].lstrip('\n').rstrip('\n')
        return None

def get_answer(prompt, T, p):
    idx = random.randint(0, 1)
    answer = chat(prompt=prompt, idx = idx, T=T, p=p)
    #cnt = 0
    while answer == 'timeout' or answer == None:
        idx = random.randint(0, 1)
        #cnt += 1
        answer = chat(prompt=prompt, idx = idx, T=T, p=p)
        print(answer)
    return answer

