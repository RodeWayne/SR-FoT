import random
import csv
import time
import json
import jsonlines
import requests
from concurrent.futures import ThreadPoolExecutor
import concurrent
from prompt.BoolQ_prompt_base import prompt
import time
from openai import OpenAI

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
    "max_tokens": 512,
    "temperature": T,
    "top_p": p,
    "top_k": 50,
    "frequency_penalty": 0.5,
    "n": 1
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer "
    }

    response = requests.post(url, json=payload, headers=headers)
        
    return eval(response.text)['choices'][0]['message']['content']

def process(id, T,p, data):
    print('No.{} begins.'.format(id))
    question = data['question']
    passage = data['passage']

    
    prompt = prompt.format(q=question, p=passage)
    answer = 'Error'
    while answer == 'Error':
        try:
            answer = get_answer(prompt, T, p)
        except:
            answer = 'Error'

    print(prompt)
    print(answer)

    
    data.update({"prediction":answer})

    return id, data

def generate(T, p):
    # fs = open('result/BoolQ_base_deepseek_2024-06-03 19:50:04.csv', 'r')
    fo = open('result/BoolQ_base_Qwen_1_5_32B_{}.json'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())), 'a')
    # writer = csv.writer(fo)
    # reader = csv.reader(fs)
    
    # s = set()
    # for line in reader:
    #     print(line)
    #     dic = eval(line[0])
    #     s.add(dic['question'])
        
    data = list()
    with open('dataset/BoolQ/dev.jsonl', 'r') as f:
        for line in jsonlines.Reader(f):
            # if line['question'] not in s:
            data.append(line)
    
    s = time.time()
    
    left_idxs = []
    for i in range(0, len(data)):
        left_idxs.append(i)
    print(len(left_idxs))

    # while i < len(data):
    #     print('No.{} begins.'.format(i))
    #     question = data[i][0]
    #     options = data[i][1]
    #     label = data[i][2]
    #     context = data[i][3]
    #     if question == 'question':
    #         i += 1
    #         continue
    #     return_list = process(T, p, question, options, context)
    #     return_list.append(label)
    #     writer.writerow(return_list)
    #     fo.flush()
    #     i += 1
    
    executor = ThreadPoolExecutor(max_workers=8)

    # result_collection = []
    futures = [
        executor.submit(process, j, T, p, data[j])
        for j in left_idxs
    ]
    # futures = []
    # for j in left_idxs:
    #     for i in range(10):
    #         futures.append(executor.submit(process, j, T, p, data[j]))

    for future in concurrent.futures.as_completed(futures):
        i, return_list = future.result()
        # result_collection.append(return_list)
        json.dump(return_list, fo, indent=4)
        fo.flush()
    
    e = time.time()
    print('Time cost:{}'.format(e - s))

if __name__ == '__main__':
    #client = OpenAI(api_key="", base_url="https://api.deepseek.com")
    generate(0.2, 0.3)   