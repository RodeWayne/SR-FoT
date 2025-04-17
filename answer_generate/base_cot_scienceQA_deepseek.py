from openai import OpenAI
from prompts.scienceQA_base_prompt import prompt
import csv
import time
import json
import requests
from concurrent.futures import ThreadPoolExecutor
import concurrent
import jsonlines

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

def process(id, question, options, context, label):
    print('No.{} begins.'.format(id))
    prompt_= l2m_prompt.format(question=question,options=options,context=context)
    print(prompt_)
    # answer = get_answer(prompt_).strip('\'')
    answer = get_answer(prompt_)
    print(answer)
    options = eval(options)
    for i in range(len(options)):
        if options[i] == answer:
            answer = i 
            break
    
    return id, [question, options, context, answer, label]

if __name__ == '__main__':
    client = OpenAI(api_key="", base_url="https://api.deepseek.com")
    fi = open('dataset/ScienceQA/problems_all_test_balanced.csv', 'r')
    fo = open('result/scienceQA_base_deepseek_all_test_{}.csv'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())), 'w')
    reader = csv.reader(fi)
    writer = csv.writer(fo)
    data = [line for line in reader]
    writer.writerow(['question','options','context','prediction', 'label'])
    
    # cnt_dic = {}
    # f = open('/home/wentao/IJCAI_2024/llm_halluc_reduce/output/scienceQA_sccot_v5_deepseek_all_test_2024-06-04 02:15:43.csv', 'r')
    # reader_ = csv.reader(f)
    # for line in reader_:
    #     key = str(line[:2])
    #     if key in cnt_dic:
    #         cnt_dic[key] += 1
    #     else:
    #         cnt_dic[key] = 1
    
    start_time = time.time()
    
    executor = ThreadPoolExecutor(max_workers=8)

    futures = [
        executor.submit(process, j, data[j][0], data[j][1], data[j][3], data[j][2])
        for j in range(1, len(data))
    ]
    # futures = []
    # for j in range(1, len(data)):
    #     key = str(data[j][:2])
    #     left_cnt = 10 - cnt_dic[key] if key in cnt_dic.keys() else 10
    #     for i in range(left_cnt):
    #         futures.append(executor.submit(process, j, data[j][0], data[j][1], data[j][3], data[j][2]))

    for future in concurrent.futures.as_completed(futures):
        i, return_list = future.result()
        writer.writerow(return_list)
        fo.flush()
        
    end_time = time.time()
    print('Time cost: {}s.\n'.format(end_time - start_time))