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
from chat_api import get_answer

def process(id, T, p, data):
    print('No.{} begins.'.format(id))
    print(data)
    question = data['question']
    passage = data['passage']
    
    #Question Explaination
    prompt = explanation_prompt.format(q=question, p=passage)
    explanation = get_answer(prompt, T, p)
    
    #Major Premise Production
    prompt = premise_prompt.format(q=question, p=passage, e = explanation)
    major = get_answer(prompt, T, p)
    
    #Posing the Minor Premise Question
    prompt = problem_prompt.format(q=question, major=major, p=passage)
    minor_q = get_answer(prompt, T, p)
    
    #Minor Premise Production
    prompt = minor_prompt.format(minor_q=minor_q, p=passage)
    minor = get_answer(prompt, T, p)
    minor = minor.replace('Yes, ', '').replace('No, ', '')
    # print(minor)
    # sid = (minor.split('\n'))[-1].find(':')
    # minor = minor[sid + 1 :].strip()
    # print('------')
    # print(minor)
    
    #Final Syllogistic Reasoning
    prompt = final_prompt.format(q=question, major=major, minor=minor)
    answer = get_answer(prompt, T, p)

    print(answer)

    data.update({"explanation": explanation})
    data.update({"major":major})
    data.update({"minor_question": minor_q})
    data.update({"minor":minor})
    data.update({"prediction":answer})
    data.update({'id':id})

    return id, data

def generate(T, p):
    # fs = open('result/BoolQ_syllogism_multi_T0.9_p0.7_2024-06-13 02:09:15.csv', 'r')
    fo = open('result/BoolQ_syllogism_multi_T{}_p{}_{}.csv'.format(T, p, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())), 'a')
    # reader = csv.reader(fs)
    writer = csv.writer(fo)

    data = list()
    with open('dataset/BoolQ/dev.jsonl', 'r') as f:
        for line in jsonlines.Reader(f):
            data.append(line)
    print(len(data))
    s = time.time()
    
    left_idxs = []
    for i in range(len(data)):
        left_idxs.append(i)
    print(len(left_idxs))
    
    # cnt_dic = {}
    # for line in fs.readlines():
    #     if line.find('"id": ') != -1:
    #         id = line.replace('"id": ', '').strip()
    #         if id in cnt_dic.keys():
    #             cnt_dic[id] += 1
    #         else:
    #             cnt_dic[id] = 1
    
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
    
    executor = ThreadPoolExecutor(max_workers=4)

    futures = [executor.submit(process, j, T, p, data[j]) for j in left_idxs]

    # futures = []
    # for j in left_idxs:
    #     left_cnt = 10 if str(j) not in cnt_dic.keys() else 10 - cnt_dic[str(j)]
    #     for i in range(left_cnt):
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