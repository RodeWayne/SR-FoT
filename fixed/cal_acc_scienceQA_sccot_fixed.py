import csv
# from chat_api import get_answer
from openai import OpenAI
import requests
def get_answer(prompt, T, p):
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
        "authorization": "Bearer sk-"
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response)
    return eval(response.text)['choices'][0]['message']['content']

re_prompt = """Question:{question}
Options:{options}
Context:{context}
Rethink the above context, identify the information you find useful, and then choose an answer from the options.
"""
# Explanation:{explanation}
# Major:{major}
# Minor Question:{minor_question}
# Minor:{minor}

#f = open('result/titile_examples_result.csv', 'r')
f = open('result/scienceQA_syllogism_multi_Qwen_1_5_32B_test_v5_2024-07-31 12:56:46.csv', 'r')
# fo = open('result/scienceQA_syllogism_deepseek_all_test_multi_2024-06-13 16:50:03_fixed.csv', 'w')
reader = csv.reader(f)
# writer = csv.writer(fo)

data = [line for line in reader]
print(len(data))
answer_list = {}
acc = 0
cnt = 0
diff = 0
answer_dic = {}
label_dic = {}
line_dic = {}
diff_list = []
def answer_transform(answer, options):
    #sccot below 3 lines
    # sid = answer.find('is')
    # eid = answer.find('reasoning process step by step')
    # answer = answer[sid + 3:eid - 1].strip(',').strip('\'') 
    
    if answer == 'Option 1' or answer == 'Option A' or answer.find('the first') != -1 or answer.find('The first') != -1:
        answer = '0'
    if answer == 'Option 2' or answer == 'Option B' or answer.find('the second') != -1 or answer.find('The second') != -1:
        answer = '1'
    if answer == 'Both are physical changes.':
        answer = 'Both are only physical changes.'
    if answer == 'Yes':
        answer = 'yes'
    if answer == 'No':
        answer = 'no'
    # if answer.find(',') != -1:
    #     answer = answer.replace(', ', ',\n')
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
    return answer

for line in data:
    id = str(line[:2])
    if line[1] == 'options' or line[1] == 'question':
        continue
    answer_dic[id] = {'0':0, '1':0, '2':0, '3':0}
    label_dic[id] = line[-1]
    line_dic[id] = line

answer_dic_2 = {}
for line in data:
    # if line[-2] != 'True' and line[-2] != 'False':
    #     print(line[-2])
    #     diff += 1
    if line[1] == 'options' or line[1] == 'question':
        continue
    answer = line[-2]
    label = line[-1]
    
    answer = answer_transform(answer, eval(line[1]))
    if answer != '0' and answer != '1' and answer != '2' and answer != '3':
        continue
    else:
        answer_dic[str(line[:2])][answer] += 1
        # writer.writerow(line)
        k = str([str(line[:2]), answer])
        if k in answer_dic_2.keys():
            answer_dic_2[k].append(line)
        else:
            answer_dic_2[k] = [line]

for key in answer_dic.keys():
    answer = ''
    num = 0
    for _ in answer_dic[key].keys():
        if answer_dic[key][_] > num:
            num = answer_dic[key][_]
            answer = _
    if answer == '':
        diff_list.append(line_dic[key])
        diff += 1
    if answer == label_dic[key]:
        acc += 1
    if answer != '':
        print(answer_dic_2[str([key, answer])][0])
        # writer.writerow(answer_dic_2[str([key, answer])][0])
       
    cnt += 1
    
    
print(acc, cnt, diff)
print(acc / cnt)
print(acc / (cnt - diff))

exit()
for line in diff_list:
    print(line)
    #  explanation=line[3], major=line[4], minor_question=line[5], minor=line[6]
    prompt = re_prompt.format(question=line[0], options=line[1], context=line[2])
    print(prompt)
    # answer = get_answer(prompt)
    answer = "Error"
    while answer == 'Error':
        try:
            answer = get_answer(prompt, 0.2, 0.3)
        except:
            answer = 'Error'
    answer = answer_transform(answer, eval(line[1]))
    print(answer)
    if answer == line[-2]:
        acc += 1
    if not (answer != '0' and answer != '1' and answer != '2' and answer != '3'):
        diff -= 1
    line[-2] = answer
    # writer.writerow(line)

print(acc, cnt, diff)
print(acc / cnt)
print(acc / (cnt - diff))
    
