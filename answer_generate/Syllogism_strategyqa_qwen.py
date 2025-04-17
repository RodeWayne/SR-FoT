import random
import csv
import time
import json
import requests
from concurrent.futures import ThreadPoolExecutor
import concurrent
from prompt.strategyqa_syllogism_prompt import *

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

    return eval(response.text)['choices'][0]['message']['content']

def process(id, T, p, facts, question):
    
    print('No.{} begins.'.format(id))
    
    context = ''
    for i in range(len(facts)):
        context += '{}.{}\n'.format(i + 1, facts[i])
    context = context.strip('\n')
    
    #Question Explaination
    prompt = explain_prompt.format(context=context, question=question)
    explanation = 'Error'
    while explanation == 'Error':
        try:
            explanation = get_answer(prompt, T, p)
        except:
            explanation = 'Error'
    explanation = explanation.replace('Explanation: ','')
    print(explanation)
    #Major Premise Production
    prompt = major_prompt.format(context=context, question=question, explanation=explanation)
    # print(prompt)
    major = 'Error'
    while major == 'Error':
        try:
            major = get_answer(prompt, T, p)
        except:
            major = 'Error'
    major = major.replace('Major Premise: ','')
    print(major)
    #Posing the Minor Premise Question
    prompt = problem_prompt.format(question=question, major=major, context=context)
    # prompt = problem_prompt.format(question=question, major=major)
    minor_question = 'Error'
    while minor_question == 'Error':
        try:
            minor_question = get_answer(prompt, T, p)
        except:
            minor_question = 'Error'
    minor_question = minor_question.replace('Minor Premise Question: ','')
    print(minor_question)
    #Minor Premise Production
    prompt = minor_prompt.format(context=context, minor_question=minor_question)
    # print(prompt)
    minor = 'Error'
    while minor == 'Error':
        try:
            minor = get_answer(prompt, T, p)
        except:
            minor = 'Error'
    minor = minor.replace('Answer: ','')
    print(minor)
    #Final Syllogistic Reasoning
    prompt = final_prompt.format(question=question, major=major, minor=minor)
    # print(prompt)
    answer = 'Error'
    while answer == 'Error':
        try:
            answer = get_answer(prompt, T, p)
        except:
            answer = 'Error'
    answer = answer.replace('Answer: ','')
    print(answer)
    return id, [question, facts, explanation, major, minor_question, minor, answer]

if __name__ == '__main__':
    T = 0.2
    p = 0.3
    f = open('dataset/StrategyQA/strategyqa_train.json', 'r')
    fo = open('result/strategyqa_syllogism_Qwen_1_5_32B_T0.2_p0.3_{}.csv'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())), 'w')
    writer = csv.writer(fo)  
    writer.writerow(['question', 'facts', 'explanation', 'general_statement', 'particular_information_question', 'particular_information', 'answer','label'])
    cnt = 0
    data = json.loads(f.read())
    print(len(data))
    
    s = time.time()

    executor = ThreadPoolExecutor(max_workers=6)

    futures = [
        executor.submit(process, i, T, p, data[i]['facts'], data[i]['question'])
        for i in range(0, len(data))
    ]
    # futures = []
    # for j in range(1200, len(data)):
    #     for i in range(10):
    #         futures.append(executor.submit(process, j, 0.9, 0.7, data[j]['facts'], data[j]['question']))


    for future in concurrent.futures.as_completed(futures):
        i, return_list = future.result()
        return_list.append(data[i]['answer'])
        writer.writerow(return_list)
        fo.flush()
    
    e = time.time()
    print('Time cost: {}'.format(e - s))

