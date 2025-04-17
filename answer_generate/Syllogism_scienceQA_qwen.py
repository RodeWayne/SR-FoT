from openai import OpenAI
from prompt.scienceQA_syllogism_prompt import *
import csv
import time
import json
import requests
from concurrent.futures import ThreadPoolExecutor
import concurrent

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

def process(id, T, p, ori_question, options, context, label):
    # if len(context) == 0:
    #     context = 'None'
    print('No.{} begins.'.format(id))
    sid = ori_question.find('?')
    question_context = ori_question[sid + 2 :] if sid != len(ori_question) - 1 else ''
    
    #Question Explaination
    prompt = explain_prompt.format(ori_question=ori_question, options=options, context=context)
    explanation = 'Error'
    while explanation == 'Error':
        try:
            explanation = get_answer(prompt, T, p)
        except:
            explanation = 'Error'
    explanation = explanation.replace('Explanation: ','')
    print(explanation)
    #Major Premise Production
    prompt = premise_prompt.format(ori_question=ori_question, options = options, context = context + '\n' + explanation)
    major = 'Error'
    while major == 'Error':
        try:
            major = get_answer(prompt, T, p)
        except:
            major = 'Error'
    major = major.replace('Major Premise: ','')
    print(major)
    #Posing Minor Premise Question
    prompt = problem_prompt.format(ori_question = ori_question, major = major, context = context)
    minor_question = 'Error'
    while minor_question == 'Error':
        try:
            minor_question = get_answer(prompt, T, p)
        except:
            minor_question = 'Error'
    minor_question = minor_question.replace('Minor Premise Question: ','')
    print(minor_question)
    #Minor Premise Production
    prompt = answer_prompt.format(options = options, context = context + '\n' + question_context, minor_question = minor_question)
    #prompt = answer_prompt.format(ori_question = ori_question, options = options, context = context, major = major, minor_question = minor_question)
    minor = 'Error'
    while minor == 'Error':
        try:
            minor = get_answer(prompt, T, p)
        except:
            minor = 'Error'
    minor = minor.replace('Answer: ','')
    print(minor)
    #Final Syllogistic Reasoning
    prompt = final_prompt.format(major = major, minor = minor, ori_question = ori_question, options = options)
    answer = 'Error'
    while answer == 'Error':
        try:
            answer = get_answer(prompt, T, p)
        except:
            answer = 'Error'
    answer = answer.replace('Answer: ','')
    print(answer)
    
    #Post Processing
    ori_answer = answer
    # sid = answer.find('is')
    # eid = answer.find('The reasoning process of syllogism is as follows')
    # answer = answer[sid + 3:eid - 1].strip('.').strip('\'')
    # options = eval(options)
    # for i in range(len(options)):
    #     if options[i] == answer:
    #         answer = str(i) 
    #         break
    # if answer != '0' and answer != '1' and answer != '2' and answer != '3':
    #     answer = answer.strip(' ').strip('\'').strip('\"')
    #     answer = answer.replace('\\n', '\n').replace(' miles', 'miles').replace(' hours', 'hours').replace(' kilometers', 'kilometers')
    #     for i in range(len(options)):
    #         if options[i].find(answer) != -1:
    #             answer = str(i)
    #             break
    # if answer != '0' and answer != '1' and answer != '2' and answer != '3':
    #     for i in range(len(options)):
    #         if answer.find(options[i]) != -1:
    #             answer = str(i)
    #             break
    print(answer)
    return id, [ori_question, options, context, explanation, major, minor_question, minor, ori_answer, answer, label]

if __name__ == '__main__':
    T = 0.9
    p = 0.7
    # f = open('result/scienceQA_syllogism_deepseek_all_test_2024-06-05 02:40:52.csv', 'r')
    fi = open('dataset/ScienceQA/problems_all_test_balanced.csv', 'r')
    fo = open('result/scienceQA_syllogism_multi_Qwen_1_5_32B_test_{}.csv'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())), 'w')
    # reader_ = csv.reader(f)
    reader = csv.reader(fi)
    writer = csv.writer(fo)
    
    # cnt_dic = {}
    # for line in reader_:
    #     if line[0] == 'question':
    #         continue
    #     key = str(line[:2])
    #     if key not in cnt_dic:
    #         cnt_dic[key] = 1
    #     else:
    #         cnt_dic[key] += 1
    # print(cnt_dic)

    
    data = [line[:7] for line in reader]
    print(len(data))
    writer.writerow(['question','options','context','explanation','major','minor_question','minor','full_answer','prediction', 'label'])

    start_time = time.time()
    executor = ThreadPoolExecutor(max_workers=8)

    # futures = [
    #     executor.submit(process, j, T, p, data[j][0], data[j][1], data[j][3], data[j][2])
    #     for j in range(1, len(data))
    # ]
    futures = []
    for j in range(1, len(data)):
        for i in range(10):
            futures.append(executor.submit(process, j, T, p, data[j][0], data[j][1], data[j][3], data[j][2]))

    for future in concurrent.futures.as_completed(futures):
        i, return_list = future.result()
        writer.writerow(return_list)
        fo.flush()
        
    end_time = time.time()
    print('Time cost: {}s.\n'.format(end_time - start_time))