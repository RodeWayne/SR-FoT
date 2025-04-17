from openai import OpenAI
from prompt.scienceQA_syllogism_prompt import *
import csv
import time
import json
import requests
from concurrent.futures import ThreadPoolExecutor
import concurrent

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

def process(id, ori_question, options, context, label):
    # if len(context) == 0:
    #     context = 'None'
    print('No.{} begins.'.format(id))
    sid = ori_question.find('?')
    question_context = ori_question[sid + 2 :] if sid != len(ori_question) - 1 else ''
    
    #Question Explaination
    prompt = explain_prompt.format(ori_question=ori_question, options=options, context=context)
    explanation = get_answer(prompt)

    #Major Premise Production
    prompt = premise_prompt.format(ori_question=ori_question, options = options, context = context + '\n' + explanation)
    major = get_answer(prompt)

    #Posing the Minor Premise Question
    prompt = problem_prompt.format(ori_question = ori_question, major = major, context = context)
    minor_question = get_answer(prompt)

    #Minor Premise Production
    prompt = answer_prompt.format(options = options, context = context + '\n' + question_context, minor_question = minor_question)
    #prompt = answer_prompt.format(ori_question = ori_question, options = options, context = context, major = major, minor_question = minor_question)
    minor = get_answer(prompt)

    #Final Syllogistic Reasoning
    prompt = final_prompt.format(major = major, minor = minor, ori_question = ori_question, options = options)
    answer = get_answer(prompt)
    print(answer)
    
    #Post Processing
    ori_answer = answer
    sid = answer.find('is')
    eid = answer.find('The reasoning process of syllogism is as follows')
    answer = answer[sid + 3:eid - 1].strip('.').strip('\'')
    options = eval(options)
    for i in range(len(options)):
        if options[i] == answer:
            answer = str(i) 
            break
    if answer != '0' and answer != '1' and answer != '2' and answer != '3':
        answer = answer.strip(' ').strip('\'').strip('\"')
        answer = answer.replace('\\n', '\n').replace(' miles', 'miles').replace(' hours', 'hours').replace(' kilometers', 'kilometers')
        for i in range(len(options)):
            if options[i].find(answer) != -1:
                answer = str(i)
                break
    if answer != '0' and answer != '1' and answer != '2' and answer != '3':
        for i in range(len(options)):
            if answer.find(options[i]) != -1:
                answer = str(i)
                break
    #print(answer)
    return id, [ori_question, options, context, explanation, major, minor_question, minor, ori_answer, answer, label]

if __name__ == '__main__':
    client = OpenAI(api_key="sk-", base_url="https://api.deepseek.com")
    # f = open('result/scienceQA_syllogism_deepseek_all_test_2024-06-05 02:40:52.csv', 'r')
    fi = open('dataset/ScienceQA/problems_all_test_balanced.csv', 'r')
    fo = open('result/scienceQA_syllogism_deepseek_all_test_{}.csv'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())), 'w')
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
    executor = ThreadPoolExecutor(max_workers=20)

    futures = [
        executor.submit(process, j, data[j][0], data[j][1], data[j][3], data[j][2])
        for j in range(1, len(data))
    ]
    # futures = []
    # for j in range(1, len(data)):
    #     for i in range(10):
    #         futures.append(executor.submit(process, j, data[j][0], data[j][1], data[j][3], data[j][2]))

    for future in concurrent.futures.as_completed(futures):
        i, return_list = future.result()
        writer.writerow(return_list)
        fo.flush()
        
    end_time = time.time()
    print('Time cost: {}s.\n'.format(end_time - start_time))