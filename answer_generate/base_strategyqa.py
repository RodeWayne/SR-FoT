import random
import csv
import time
import json
import requests
from concurrent.futures import ThreadPoolExecutor
import concurrent
from chat_api import get_answer
from prompt.strategyqa_base_prompt import base_prompt

def process(id, T, p, question, facts):
    print('No.{} begins.'.format(id))
    context = ''
    for i in range(len(facts)):
        context += '{}.{}\n'.format(i + 1, facts[i])
    context = context.strip('\n')
    # print(question)
    # print(content)
    prompt = base_prompt.format(context=context, question=question)
    answer = get_answer(prompt, T, p)

    print(prompt)
    print(answer)

    return id, [question, facts, answer]

if __name__ == '__main__':
    f = open('dataset/StrategyQA/strategyqa_train.json', 'r')
    fo = open('result/strategyqa_base_T0.2_p0.3_{}.csv'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())), 'w')
    writer = csv.writer(fo)  
    writer.writerow(['question', 'facts', 'answer','label'])
    cnt = 0
    data = json.loads(f.read())
    print(len(data))
    s = time.time()
    
    executor = ThreadPoolExecutor(max_workers=2)

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