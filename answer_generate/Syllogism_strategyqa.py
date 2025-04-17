import random
import csv
import time
import json
import requests
from concurrent.futures import ThreadPoolExecutor
import concurrent
from prompts.strategyqa_syllogism_prompt import *
from chat_api import get_answer

def process(id, T, p, facts, question):
    
    print('No.{} begins.'.format(id))
    
    context = ''
    for i in range(len(facts)):
        context += '{}.{}\n'.format(i + 1, facts[i])
    context = context.strip('\n')
    
    #Question Explaination
    prompt = explain_prompt.format(context=context, question=question)
    explanation = get_answer(prompt, T, p)
    
    #Major Premise Production
    prompt = major_prompt.format(context=context, question=question, explanation=explanation)
    print(prompt)
    major = get_answer(prompt, T, p)
    
    #Posing the Minor Premise Question
    prompt = problem_prompt.format(question=question, major=major, context=context)
    minor_question = get_answer(prompt, T, p)
    
    #Minor Premise Production
    prompt = minor_prompt.format(context=context, minor_question=minor_question)
    print(prompt)
    minor = get_answer(prompt, T, p)
    
    #Final Syllogistic Reasoning
    prompt = final_prompt.format(question=question, major=major, minor=minor)
    print(prompt)
    answer = get_answer(prompt, T, p)
    
    return id, [question, facts, explanation, major, minor_question, minor, answer]

if __name__ == '__main__':
    T = 0.2
    p = 0.3
    f = open('dataset/StrategyQA/strategyqa_train.json', 'r')
    fo = open('result/strategyqa_syllogism_T0.2_p0.3_{}.csv'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())), 'w')
    writer = csv.writer(fo)  
    writer.writerow(['question', 'facts', 'explanation', 'major', 'minor_question', 'minor', 'answer','label'])
    cnt = 0
    data = json.loads(f.read())
    print(len(data))
    
    s = time.time()

    executor = ThreadPoolExecutor(max_workers=4)

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

