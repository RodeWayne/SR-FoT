import random
import csv
import time
import json
import requests
from concurrent.futures import ThreadPoolExecutor
import concurrent
from prompt.scienceQA_syllogism_prompt import explain_prompt, premise_prompt, check_prompt, problem_prompt, answer_prompt, final_prompt
import time
from chat_api import get_answer

def process(id, T, p, ori_question, options, context, label):
    # if len(context) == 0:
    #     context = 'None'
    options_ = eval(options)
    label = options_[int(label)]
    print('No.{} begins.'.format(id))
    sid = ori_question.find('?')
    question_context = ori_question[sid + 2 :] if sid != len(ori_question) - 1 else ''
    
    #Question Explaination
    prompt = explain_prompt.format(ori_question=ori_question, options=options, context=context)
    print(prompt)
    explanation = get_answer(prompt,T,p)
    
    #Major Premise Production
    prompt = premise_prompt.format(ori_question=ori_question, options = options, context = context + '\n' + explanation)
    major = get_answer(prompt,T,p)
    
    # #Check if Major Premise right
    # prompt = check_prompt + major
    # check_result = get_answer(prompt,T,p)
    
    # cnt = 0
    # while check_result.find('No') != -1 and cnt < 10:
    #         prompt = premise_prompt.format(ori_question=ori_question, options = options, context = context + '\n' + explanation)
    #         major = get_answer(prompt,T,p)
                   
    #         prompt = check_prompt + major
    #         check_result = get_answer(prompt,T,p)
            
    #         cnt += 1
                
    #Posing the Minor Premise Question
    prompt = problem_prompt.format(ori_question = ori_question, major = major, context=context)
    minor_question = get_answer(prompt,T,p)
    
    # if context == 'None' and question_context == '':
    #     answer_context = 'None'
    # elif context == 'None':
    #     answer_context = question_context
    # elif question_context == '':
    #     answer_context = context
    # else:
    #     answer_context = context + '\n' + question_context
    #Minor Premise Production
    prompt = answer_prompt.format(options = options, context = context + '\n' + question_context, minor_question = minor_question)
    #prompt = answer_prompt.format(ori_question = ori_question, options = options, context = context, major = major, minor_question = minor_question)
    minor = get_answer(prompt,T,p)

    #Final Syllogistic Reasoning
    prompt = final_prompt.format(major = major, minor = minor, ori_question = ori_question, options = options)
    print(prompt)
    answer = get_answer(prompt,T,p)
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
    return id, [ori_question, options, context, explanation, major, minor_question, minor, ori_answer, answer]

def generate(T, p):
    fi = open('result/scienceQA_syllogism_all_test_multi_T0.9_p0.7_2024-06-13 18:42:45.csv', 'r')
    f = open('dataset/scinenceQA/problems_all_test_balanced.csv', 'r')
    fo = open('result/scienceQA_syllogism_all_test_multi_T{}_p{}_{}.csv'.format(T, p, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())), 'w')
    readers = csv.reader(fi)
    reader = csv.reader(f)
    writer = csv.writer(fo) 
    writer.writerow(['question', 'options', 'context', 'explanation', 'major','minor_question','minor','full_answer','answer', 'label','skill'])
    s = time.time()
    #datas = [line for line in readers]
    datas = []
    data = [line for line in reader]
    cnt_dic = {}
    for line in readers:
        key = str(line[:2])
        if key in cnt_dic.keys():
            cnt_dic[key] += 1
        else:
            cnt_dic[key] = 1
    # i = 0
    # while 1:
    #     flag = False
    #     for line in datas:
    #         if data[i][:2] == line[:2]:
    #             flag = True
    #             i += 1
    #             break
    #     if flag == False:
    #         break
    left_idxs = []
    for i in range(1, len(data)):
        flag = False
        for j in range(1, len(datas)):
            if data[i][:2] == datas[j][:2]:
                flag = True
        if flag == False:
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
    
    executor = ThreadPoolExecutor(max_workers=2)

    futures = []
    
    for j in left_idxs:
        key = str(data[j][:2])
        left_cnt = 10 if key not in cnt_dic.keys() else 10 - cnt_dic[key]
        for _ in range(left_cnt):
            futures.append(executor.submit(process, j, T, p, data[j][0], data[j][1], data[j][3], data[j][2]))

    for future in concurrent.futures.as_completed(futures):
        i, return_list = future.result()
        return_list.append(data[i][2])
        return_list.append(data[i][-1])
        writer.writerow(return_list)
        fo.flush()
    
    e = time.time()
    print('Time cost:{}'.format(e - s))

if __name__ == '__main__':
    generate(0.9, 0.7)