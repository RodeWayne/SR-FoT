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

def get_answer(prompt):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt},
            ],
        stream=False
        )
    
    return response.choices[0].message.content

def process(id, T, p, data):
    print('No.{} begins.'.format(id))
    question = data['question']
    passage = data['passage']
    
    #Question Explaination
    prompt = explanation_prompt.format(q=question, p=passage)
    try:
        explanation = get_answer(prompt)
    except:
        explanation = 'error'
    
    #Major Premise Production
    prompt = premise_prompt.format(q=question, p=passage, e = explanation)
    try:
        major = get_answer(prompt)
    except:
        major = 'error'
        
    #Posing the Minor Premise Question
    prompt = problem_prompt.format(q=question, major=major, p=passage)
    try:
        minor_q = get_answer(prompt)
    except:
        minor_q = 'error'
    
    #Minor Premise Production
    prompt = minor_prompt.format(minor_q=minor_q, p=passage)
    try:
        minor = get_answer(prompt)
    except:
        minor = 'error'
    minor = minor.replace('Yes, ', '').replace('No, ', '')
    
    #Final Syllogistic Reasoning
    prompt = final_prompt.format(q=question, major=major, minor=minor )
    try:
        answer = get_answer(prompt)
    except:
        answer = 'error'
    
    print(prompt)
    print(answer)

    
    data.update({"explanation": explanation})
    data.update({"major":major})
    data.update({"minor_question": minor_q})
    data.update({"minor":minor})
    data.update({"prediction":answer})
    data.update({'id':id})

    return id, data

def generate(T, p):
    fo = open('result/BoolQ_syllogism_deepseek_T{}_p{}_{}.json'.format(T, p, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())), 'a')
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
    
    executor = ThreadPoolExecutor(max_workers=20)

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
    client = OpenAI(api_key="sk-", base_url="https://api.deepseek.com")
    generate(0.2, 0.3)