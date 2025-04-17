import random
import csv
import time
import json
import requests
from concurrent.futures import ThreadPoolExecutor
import concurrent
from prompt.scienceQA_base_prompt import prompt
from chat_api import get_answer

def process(id, T, p, question, options, context):
    prompt_= prompt.format(question=question,options=options,context=context)
    print(prompt_)
    answer = get_answer(prompt_, T, p).strip('\'')
    print(answer)
    options = eval(options)
    for i in range(len(options)):
        if options[i] == answer:
            answer = i 
            break
    
    return id, [question, options, context, answer]

def generate(T, p):
    f = open('datasets/ScienceQA/problems_all_test_balanced.csv', 'r')
    fo = open('result/scienceQA_base_all_test_T{}_p{}_{}.csv'.format(T, p, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())), 'w')
    reader = csv.reader(f)
    writer = csv.writer(fo)


    data = [line for line in reader]
    print(len(data))
    
    s = time.time()
    executor = ThreadPoolExecutor(max_workers=2)

    futures = [
        executor.submit(process, i, T, p, data[i][0], data[i][1], data[i][3])
        for i in range(1, len(data))
    ]

    for future in concurrent.futures.as_completed(futures):
        i, return_list = future.result()
        return_list.append(data[i][2])
        writer.writerow(return_list)
        fo.flush()
    
    e = time.time()
    print('Time cost: {}'.format(e - s))

if __name__ == '__main__':
    # Ts = [0.1, 0.2, 0.3]
    # ps = [0.1, 0.2, 0.3]
    # for T in Ts:
    #     for p in ps:
    #         generate(T, p)
    generate(0.2, 0.3)
