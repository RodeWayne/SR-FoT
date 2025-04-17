import random
import csv
import time
import json
import requests
from concurrent.futures import ThreadPoolExecutor
import concurrent
from chat_api import get_answer
from prompt.strategyqa_base_prompt import base_prompt

def get_answer(prompt, T, p):
    # response = client.chat.completions.create(
    #     model="deepseek-chat",
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant"},
    #         {"role": "user", "content": prompt},
    #         ],
    #     stream=False
    #     )
    # return response.choices[0].message.content
    url = "https://api.siliconflow.cn/v1/chat/completions"
    payload = {
    "model": "Qwen/Qwen1.5-32B-Chat",
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ],
    "stream": False,
    "max_tokens": 2536,
    "temperature": T,
    "top_p": p,
    "top_k": 50,
    "frequency_penalty": 0.5,
    "n": 1
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer sk-"
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response)
    while eval(response.text)['choices'][0]['message']['content'].strip('\n') == 'Error':
        response = requests.post(url, json=payload, headers=headers)
        
    return eval(response.text)['choices'][0]['message']['content'].strip('\n')

def process(id, T, p, question, facts):
    print('No.{} begins.'.format(id))
    context = ''
    for i in range(len(facts)):
        context += '{}.{}\n'.format(i + 1, facts[i])
    context = context.strip('\n')
    # print(question)
    # print(content)
    prompt = base_prompt.format(context=context, question=question)
    print(prompt)
    answer = 'Error'
    while answer == 'Error':    
        try:
            answer = get_answer(prompt, T, p)
        except:
            answer = 'Error'
    # answer = get_answer(prompt, T, p)
        
    print(answer)

    return id, [question, facts, answer]

if __name__ == '__main__':
    f = open('dataset/StrategyQA/strategyqa_train.json', 'r')
    fo = open('result/strategyqa_base_Qwen_1_5-32B_{}.csv'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())), 'w')
    writer = csv.writer(fo)  
    writer.writerow(['question', 'facts', 'answer','label'])
    cnt = 0
    data = json.loads(f.read())
    print(len(data))
    s = time.time()
    

    executor = ThreadPoolExecutor(max_workers=8)

    futures = [
        executor.submit(process, j, 0.2, 0.3, data[j]['question'], data[j]['facts'])
        for j in range(len(data))
    ]

    # futures = []
    # for j in range(len(data)):
    #     for i in range(10):
    #         futures.append(executor.submit(process, j, 0.9, 0.7, data[j]['question'], data[j]['facts']))


    for future in concurrent.futures.as_completed(futures):
        i, return_list = future.result()
        return_list += [data[i]['answer']]
        writer.writerow(return_list)
        fo.flush()
            
    e = time.time()
    print('Time Cost: {}'.format(e - s))