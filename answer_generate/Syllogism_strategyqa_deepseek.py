import random
import csv
import time
import json
import requests
from concurrent.futures import ThreadPoolExecutor
import concurrent
from prompt.strategyqa_syllogism_prompt import *
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

def process(id, T, p, facts, question):
    
    print('No.{} begins.'.format(id))
    
    context = ''
    for i in range(len(facts)):
        context += '{}.{}\n'.format(i + 1, facts[i])
    context = context.strip('\n')
    
    #Question Explaination
    prompt = explain_prompt.format(context=context, question=question)
    try:
        explanation = get_answer(prompt)
    except:
        explanation = 'Error'
    
    #Major Premise Production
    prompt = major_prompt.format(context=context, question=question, explanation=explanation)
    print(prompt)
    try:
        major = get_answer(prompt)
    except:
        major = 'Error'
    
    #Posing the Minor Premise Question
    prompt = problem_prompt.format(question=question, major=major, context=context)
    # prompt = problem_prompt.format(question=question, major=major)
    try:
        minor_question = get_answer(prompt)
    except:
        minor_question = 'Error'
    
    #Minor Premise Production
    prompt = minor_prompt.format(context=context, minor_question=minor_question)
    print(prompt)
    try:
        minor = get_answer(prompt)
    except:
        minor = 'Error'
    
    #Final Syllogistic Reasoning
    prompt = final_prompt.format(question=question, major=major, minor=minor)
    print(prompt)
    try:
        answer = get_answer(prompt)
    except:
        answer = 'Error'
    print(answer)
    return id, [question, facts, explanation, major, minor_question, minor, answer]

if __name__ == '__main__':
    T = 0.2
    p = 0.3
    client = OpenAI(api_key="sk-", base_url="https://api.deepseek.com")
    f = open('dataset/StrategyQA/strategyqa_train.json', 'r')
    fo = open('result/strategyqa_syllogism_deepseek_{}.csv'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())), 'w')
    writer = csv.writer(fo)  
    writer.writerow(['question', 'facts', 'explanation', 'general_statement', 'particular_information_question', 'particular_information', 'answer','label'])
    cnt = 0
    data = json.loads(f.read())
    print(len(data))
    
    s = time.time()

    executor = ThreadPoolExecutor(max_workers=16)

    futures = [
        executor.submit(process, i, T, p, data[i]['facts'], data[i]['question'])
        for i in range(0, len(data))
    ]
    # futures = []
    # for j in range(len(data)):
    #     for i in range(10):
    #         futures.append(executor.submit(process, j, 0.9, 0.7, data[j]['facts'], data[j]['question']))


    for future in concurrent.futures.as_completed(futures):
        i, return_list = future.result()
        return_list.append(data[i]['answer'])
        writer.writerow(return_list)
        fo.flush()
    
    e = time.time()
    print('Time cost: {}'.format(e - s))

