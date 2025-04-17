import csv
# from chat_api import get_answer
# from openai import OpenAI
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

# pathList = {
#     'base_v5': '/home/wentao/IJCAI_2024/llm_halluc_reduce/output/scienceQA_base_deepseek_all_test_v5_2024-06-03 01:52:49.csv',
#     'cot_v5': '/home/wentao/IJCAI_2024/llm_halluc_reduce/output/scienceQA_cot_v5_deepseek_all_test_2024-06-03 02:11:48.csv',
# }
# path = pathList['base_v5']
# f = open(path, 'r')
f = open('result/scienceQA_cot_all_test_T0.2_p0.3_2024-01-21 14:51:55.csv', 'r')
fo = open('result/scienceQA_cot_all_test_T0.2_p0.3_2024-01-21 14:51:55_error_samples.csv', 'w')
reader = csv.reader(f)
writer = csv.writer(fo)

acc = 0
cnt = 0
diff = 0
diff_list = []

def answer_transform(answer, choices):
    #base
    # eid = answer.find('\n\n')
    # if eid != -1:
    #     answer = answer[:eid].replace('Answer: ', '').strip()

    #cot
    sid = answer.find('The answer is ')
    eid = answer.find('reasoning')
    if sid != -1 and eid != -1:
        answer = answer[sid + 15 : eid - 3].strip('\'').strip('\"')
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
    if answer != '0' and answer != '1' and answer != '2' and answer != '3':
        answer = answer.strip(' ').strip('\'').strip('\"')
        answer = answer.replace('\\n', '\n').replace(' miles', 'miles').replace(' hours', 'hours').replace(' kilometers', 'kilometers')
        for i in range(len(choices)):
            if choices[i].find(answer) != -1:
                answer = str(i)
                break
    if answer != '0' and answer != '1' and answer != '2' and answer != '3':
        answer = answer.replace('miles', ' miles').replace('hours', ' hours').replace('kilometers', ' kilometers')
        for i in range(len(choices)):
            if answer.find(choices[i]) != -1:
                answer = str(i)
                break
    return answer
            
for line in reader:
    # if line[-2] != 'True' and line[-2] != 'False':
    #     print(line[-2])
    #     diff += 1
    if line[1] == 'options':
        continue
    answer = line[-3]
    label = line[-2]

    # sid = answer.find('the answer is') + 15
    # answer = answer[sid : ]
    answer = answer_transform(answer, eval(line[1]))
    
    if answer != '0' and answer != '1' and answer != '2' and answer != '3':
        print(answer)
        diff_list.append(line)
        diff += 1
    # else:
    #     writer.writerow(line)
    if label == answer:
        acc += 1
    else:
        writer.writerow(line)
    cnt += 1
    

print(acc, cnt, diff)
print(acc / cnt)
print(acc / (cnt - diff))

exit()
for line in diff_list:
    print(line)
    prompt = re_prompt.format(question=line[0], options=line[1], context=line[2])
    print(prompt)
    # answer = get_answer(prompt, 0.2, 0.3)
    answer = 'Error'
    while answer == 'Error':
        try:
            answer = get_answer(prompt, 0.2, 0.3)
        except:
            answer = 'Error'
    
    answer = answer_transform(answer, eval(line[1]))
    print(answer)
    if answer == line[-1]:
        acc += 1
    if not (answer != '0' and answer != '1' and answer != '2' and answer != '3'):
        diff -= 1
    line[-2] = answer
    # writer.writerow(line)

print(acc, cnt, diff)
print(acc / cnt)
print(acc / (cnt - diff))
    
