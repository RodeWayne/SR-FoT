from openai import OpenAI
# from prompt.scienceQA_cot_prompt import prompt
from prompt.scienceQA_base_prompt import prompt
import csv
import time
import json
import requests
from concurrent.futures import ThreadPoolExecutor
import concurrent
import jsonlines

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
    "max_tokens": 4096,
    "temperature": T,
    "top_p": p,
    "top_k": 50,
    "frequency_penalty": 0.5,
    "n": 1
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer "
    }

    response = requests.post(url, json=payload, headers=headers)
        
    return eval(response.text)['choices'][0]['message']['content']

def process(id, T, p, question, options, context, label):
    print('No.{} begins.'.format(id))
    prompt_= l2m_prompt.format(question=question,options=options,context=context)
    print(prompt_)
    answer = 'Error'
    while answer == 'Error':
        try:
            answer = get_answer(prompt_, T, p).strip('\'')
        except:
            answer = 'Error'
    # answer = get_answer(prompt_, T, p).strip('\'')
    print(answer)
    options = eval(options)
    for i in range(len(options)):
        if options[i] == answer:
            answer = i 
            break
    
    return id, [question, options, context, answer, label]

if __name__ == '__main__':

    f = open('dataset/ScienceQA/problems_all_test_balanced.csv', 'r')
    fo = open('result/scienceQA_base_all_test_Qwen_1_5_32B_T0.2_p0.3_{}.csv'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())), 'w')
    reader = csv.reader(f)
    writer = csv.writer(fo)
    data = [line for line in reader]
    writer.writerow(['question','options','context','prediction', 'label'])
    
    
    start_time = time.time()
    
    executor = ThreadPoolExecutor(max_workers=8)

    futures = [
        executor.submit(process, j, 0.2, 0.3, data[j][0], data[j][1], data[j][3], data[j][2])
        for j in range(1, len(data))
    ]

    for future in concurrent.futures.as_completed(futures):
        i, return_list = future.result()
        writer.writerow(return_list)
        fo.flush()
        
    end_time = time.time()
    print('Time cost: {}s.\n'.format(end_time - start_time))