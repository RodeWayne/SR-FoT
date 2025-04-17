import random
import csv
import time
import json
import jsonlines
import requests
from concurrent.futures import ThreadPoolExecutor
import concurrent
from prompt.BoolQ_syllogism_prompt import *
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
    "max_tokens": 2048,
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
        
    return eval(response.text)['choices'][0]['message']['content']

def process(id, T, p, data):
    print('No.{} begins.'.format(id))
    question = data['question']
    passage = data['passage']
    
    #Question Explaination
    prompt = explanation_prompt.format(q=question, p=passage)
    explanation = 'Error'
    while explanation == 'Error':
        try:
            explanation = get_answer(prompt, T, p)
        except:
            explanation = 'Error'
    explanation = explanation.replace('Explanation: ','')
    print(explanation)
    #Major Premise Production
    prompt = premise_prompt.format(q=question, p=passage, e = explanation)
    major = 'Error'
    while major == 'Error':
        try:
            major = get_answer(prompt, T, p)
        except:
            major = 'Error'
    major = major.replace('Major Premise: ','')
    print(major)
    #Posing the Minor Premise Question
    prompt = problem_prompt.format(q=question, major=major, p=passage)
    minor_q = 'Error'
    while minor_q == 'Error':
        try:
            minor_q = get_answer(prompt, T, p)
        except:
            minor_q = 'Error'
    minor_q = minor_q.replace('Minor Premise Question: ','')
    print(minor_q)
    #Minor Premise Production
    prompt = minor_prompt.format(minor_q=minor_q, p=passage)
    minor = 'Error'
    while minor == 'Error':
        try:
            minor = get_answer(prompt, T, p)
        except:
            minor = 'Error'
    minor = minor.replace('Yes,','').strip('')
    minor = minor.replace('Answer: ','')
    print(minor)
    #Final Syllogistic Reasoning
    prompt = final_prompt.format(q=question, major=major, minor=minor )
    answer = 'Error'
    while answer == 'Error':
        try:
            answer = get_answer(prompt, T, p)
        except:
            answer = 'Error'
    answer = answer.replace('Answer: ','')
    # print(prompt)
    print(answer)

    
    data.update({"explanation": explanation})
    data.update({"major":major})
    data.update({"minor_question": minor_q})
    data.update({"minor":minor})
    data.update({"prediction":answer})
    data.update({'id':id})

    return id, data

def generate(T, p):
    fo = open('result/BoolQ_syllogism_Qwen_1_5_32B_part_3_T{}_p{}_{}.json'.format(T, p, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())), 'a')
    #reader = csv.reader(fs)
    # writer = csv.writer(fo)

    data = list()
    with open('dataset/BoolQ/dev.jsonl', 'r') as f:
        for line in jsonlines.Reader(f):
            data.append(line)
    print(len(data))
    
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
        json.dump(return_list, fo, indent=4)
        # writer.writerow(data['question'], data['passage'], data['explanation'], data['major'], data['minor_question'], data['minor'], data['prediction'], data['answwer'], data['id'])
        fo.flush()
    
    e = time.time()
    print('Time cost:{}'.format(e - s))

if __name__ == '__main__':
    generate(0.2, 0.3)