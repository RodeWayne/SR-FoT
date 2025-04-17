import csv
import sys
import random
import requests
import json
#sys.path.append("/home/wentao/IJCAI_2024/llm_halluc_reduce")

from openai import OpenAI
import chat_api

fix_switch = True
# example = 'gpt_base_v2_fixed'
# example = 'gpt_base_v2'
# example = 'gpt_cot_v2'
# example = 'gpt_cot_v2_fixed'
# example = 'gpt_cot_v2'
# example = 'gpt_ccot_v2'
# example = 'gpt_sccot_v2'
# example = 'gpt_syllogism_v16_signle_round'
# example = 'gpt_syllogism_v16_multi_round'
# example = 'deepseek_base_v2'
# example = 'deepseek_base_v2_fixed'
# example = 'deepseek_cot_v2'
# example = 'deepseek_cot_v2_fixed'
# example = 'deepseek_sccot_v2'
# example = 'deepseek_ccot_v2'
example = 'deepseek_syllogism_Ablation_study_5'
# example = 'gpt_syllogism_Ablation_study_5'
# example = 'deepseek_syllogism_v16_multi_round'
# example = 'qwen2_70B_base'
# example = 'qwen2_70B_cot'
# example = 'qwen2_70B_syllogism_v16_single_round'
# example = 'qwen1.5_32B_base'
# example = 'qwen1.5_32B_cot'
# example = 'qwen1.5_32B_syllogism_v16_single_round'
# example = 'deepseek_syllogism_v16_final_prompt'
# example = 'deepseek_syllogism_Ablation_study_1'
# example = 'deepseek_syllogism_Ablation_study_2'
# example = 'deepseek_syllogism_Ablation_study_3'
# example = 'deepseek_syllogism_Ablation_study_4'

pathDic = {
    'gpt_base_v2': 'result/strategyqa_base_v2_T0.2_p0.3_2024-06-04 19:19:52.csv',
    'gpt_base_v2_fixed': 'result/strategyqa_base_v2_T0.2_p0.3_2024-06-04 19:19:52_fixed.csv',
    'gpt_cot_v2': 'result/strategyqa_cot_v2_T0.2_p0.3_2024-06-04 19:19:28.csv',
    'gpt_cot_v2_fixed': 'result/strategyqa_cot_v2_T0.2_p0.3_2024-06-04 19:19:28_fixed.csv',
    'gpt_sccot_v2': 'result/strategyqa_sccot_v2_T0.9_p0.7_2024-06-09 02:57:00.csv',
    'gpt_ccot_v2': 'result/strategyqa_sccot_v2_T0.9_p0.7_2024-06-09 02:57:00.csv',
    'gpt_syllogism_v16_signle_round': 'result/strategyqa_syllogism_v16_T0.2_p0.3_2024-06-07 10:02:40.csv',
    'gpt_syllogism_v16_multi_round': 'result/strategyqa_syllogism_v16_multi_T0.9_p0.7_2024-06-11 20:28:41.csv',

    'deepseek_base_v2': 'result/strategyqa_base_v2_deepseek_2024-06-05 15:57:20.csv',
    'deepseek_base_v2_fixed': 'result/strategyqa_base_v2_deepseek_2024-06-05 15:57:20_fixed.csv',
    'deepseek_cot_v2': 'result/strategyqa_cot_v2_deepseek_2024-06-05 16:20:53.csv',
    'deepseek_cot_v2_fixed': 'result/strategyqa_cot_v2_deepseek_2024-06-05 16:20:53_fixed.csv',
    'deepseek_sccot_v2': 'result/strategyqa_sccot_v2_deepseek_2024-06-09 15:40:02.csv',
    'deepseek_ccot_v2': 'result/strategyqa_sccot_v2_deepseek_2024-06-09 15:40:02.csv',
    'deepseek_syllogism_v16_single_round': 'result/strategyqa_normal_v16_deepseek_2024-07-27 18:26:56.csv',
    'deepseek_syllogism_v16_multi_round': 'result/strategyqa_syllogism_v16_deepseek_multi_2024-06-11 16:35:33.csv',
    'deepseek_syllogism_v16_b':'result/strategyqa_syllogism_v16_deepseek_ablation2_b_2024-06-15 14:02:05.csv',
    'deepseek_syllogism_v16_c':'result/strategyqa_syllogism_v16_deepseek_ablation2_b_2024-06-15 14:29:27.csv',
    
    'qwen2_70B_base':'result/strategyqa_base_v2_qwen2_70B_2024-06-12 17:47:49.csv',
    'qwen2_70B_cot':'result/strategyqa_cot_v2_qwen2_70B_2024-06-12 18:18:59.csv',
    'qwen2_70B_syllogism_v16_single_round':'result/strategyqa_syllogism_v16_qwen2_one_2024-06-12 19:37:37.csv',
    'qwen1.5_32B_base':'result/strategyqa_base_v2_qwen1.5_32B_2024-06-13 00:26:19.csv',
    'qwen1.5_32B_cot':'result/strategyqa_cot_v2_qwen1.5_32B_2024-06-13 01:06:46.csv',
    'qwen1.5_32B_sccot':'result/strategyqa_sc-cot_v2_qwen1.5_32B_2024-06-15 11:57:23.csv',
    'qwen1.5_32B_ccot':'result/strategyqa_sc-cot_v2_qwen1.5_32B_2024-06-15 11:57:23.csv',
    'qwen1.5_32B_syllogism_v16_single_round':'result/strategyqa_syllogism_v16_qwen1.5_32B_2024-06-13 01:05:58.csv',

    'deepseek_syllogism_Ablation_study_1':'result/strategyqa_syllogism_v16_deepseek_ablation2_b_2024-06-15 14:02:05.csv',
    'deepseek_syllogism_Ablation_study_2':'result/strategyqa_syllogism_v16_deepseek_ablation2_b_2024-06-15 14:29:27.csv',
    'deepseek_syllogism_Ablation_study_3':'result/strategyqa_syllogism_v16_deepseek_2024-06-06 17:57:41.csv',
    'deepseek_syllogism_Ablation_study_4':'result/strategyqa_syllogism_v12_deepseek_2024-06-05 16:25:27.csv',
    
    'deepseek_syllogism_Ablation_study_5':'result/strategyqa_syllogism_v16_deepseek_all_in_one_2024-07-27 20:02:02.csv',
    'gpt_syllogism_Ablation_study_5':'result/strategyqa_syllogism_v16_all_in_one.csv'

}

examplePath = pathDic[example]
f = open(examplePath, 'r')
# fo = open('result/strategyqa_syllogism_v17_error_sample.csv', 'w')

reader = csv.reader(f)
# writer = csv.writer(fo)

client = OpenAI(api_key="sk-", base_url="https://api.deepseek.com")
def chat(prompt,idx,T,p):
    # print(prompt)
    url = ''
    gpt_keys = ['sk-', 
                'sk-']
    gpt_key = gpt_keys[idx]

    headers = {
        'Authorization': f'Bearer {gpt_key}',
        'Content-Type': 'application/json'
        }
    
    try:
        response =  requests.post(url, headers=headers, json={
                    "model": "gpt-3.5-turbo",
                    "temperature": T,
                    'max_tokens': 3096,
                    'top_p': p,
                    'frequency_penalty': 0,
                    'presence_penalty': 0,
                    'messages':[{
                        "role":'user',
                        'content': prompt
                    }]
                    },
                    stream=False,
                    verify=False,
                    timeout=60
                )
        data = response.content.decode()
        json_data = json.loads(data)
        # return json_data
        return json_data['choices'][0]['message']['content']
    except requests.exceptions.Timeout:
        return 'timeout'    
    except Exception as e:
        print(e)
        # count += 1
        # print(f"An error occurred: {e},retry time:{count}")
    
        #prog = response.choices[0]['text'].lstrip('\n').rstrip('\n')
        return None

idx = 0

def get_answer_gpt(prompt, T, p):
    idx = random.randint(0, 1)
    answer = chat(prompt=prompt, idx = idx, T=T, p=p)
    #cnt = 0
    while answer == 'timeout' or answer == None:
        idx = random.randint(0, 1)
        #cnt += 1
        answer = chat(prompt=prompt, idx = idx, T=T, p=p)
    return answer


def get_answer(prompt):
    response = ""
    if 'gpt_' in example:
        # print("use_gpt")
        response = get_answer_gpt(prompt.lower(), 0.2, 0.3)
        return response
    else:
        # print("use_deepseek")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt},
                ],
            stream=False
            )
    
    return response.choices[0].message.content

def answer_transform(answer):
    # if answer == 'Error' or answer == '' or answer == None:
    #     return 'api_error'
    #
    sid = answer.find('the answer to the question is ') 
    if '_syllogism' in example:
        # print("syl")
        sid = answer.find('the answer to the question is ') 
    else:
        sid = answer.find('the answer is ')
    if sid != -1:
        eid = answer.find('.', sid)
        answer = answer[sid: eid]
        if 'True' in answer or 'true' in answer or '\'yes\'' in answer or '\'Yes\'' in answer:
            answer = 'True'
        elif 'False' in answer or 'false' in answer or '\'no\'' in answer or '\'No\'' in answer:
            answer = 'False'
        else:
            # print(answer)
            # answer = 'answer_error'
            answer = 'Error'
    elif answer.find('True') == 0 or answer.find('true') == 0:
        answer = 'True'
    elif answer.find('False') == 0 or answer.find('false') == 0:
        answer = 'False'
    else:
        if ('True' in answer or 'true' in answer) and not('False' in answer or 'false' in answer):
            answer = 'True'
        elif ('False' in answer or 'false' in answer) and not ('True' in answer or 'true' in answer):
            answer = 'False'
        else:
            # print(answer)
            # answer = 'answer_error'
            answer = 'Error'
    return answer

def processContext(facts):
    data = eval(facts)
    context = ''
    for i in range(len(data)):
        context += '{}.{}\n'.format(i + 1, data[i])
    context = context.strip('\n')
    return context

def reTry(question,facts,label):
    if not fix_switch:
        return 'Error'
    prompt = f"""
    Question: {question}
    Context: {facts}
    Rethink the above context, identify the information you find useful, and then provide your answer with either 'True' or 'False'.
    """
    # print(prompt)
    # non api error, call prompt to tackle, and record new ansewer
    # fixed_prediction = "Test fixed"
    answer = ""
    try:
        answer = get_answer(prompt.lower())
    except:
        pass

    # print(answer)
    fixed_prediction = answer_transform(answer.lower())
    # print(fixed_prediction)
    if fixed_prediction == label:
        print("right:",fixed_prediction,",",label)
    else:
        print("wrong:",fixed_prediction,",",label)
    return fixed_prediction

# def reTry_syllogism(question,facts,explanation,major,minor_question,minor,label):
def reTry_syllogism(question,facts,answer,label):
    if not fix_switch:
        return 'Error'
    # question,facts,explanation,major,minor_question,minor,answer,label
    # prompt = f"""
    # Question: {question}
    # Facts: {facts}
    # Explanation: {explanation}
    # Major: {major}
    # Minor_question: {minor_question}
    # Minor: {minor}
    # Rethink the above context, identify the information you find useful, and then provide your answer with either 'True' or 'False'.
    # """
    prompt = f"""
    Question: {question}
    Facts: {facts}
    Answer: {answer}
    Rethink the above context, identify the information you find useful, and then provide your answer with either 'True' or 'False'.
    """
    # print(prompt)
    # non api error, call prompt to tackle, and record new ansewer
    # fixed_prediction = "Test fixed"
    answer = ""
    try:
        answer = get_answer(prompt.lower())
    except:
        pass
    fixed_prediction = answer_transform(answer.lower())
    if fixed_prediction == label:
        print("reTry_syllogism_ok:",fixed_prediction,",",label)
    else:
        print("reTry_syllogism_bad:",fixed_prediction,",",label)
    return fixed_prediction

def base():
    acc = 0
    cnt = 0
    error = 0
    pass_list = []
    api_error_list = []
    answer_error_list = []
    for line in reader:
        label = line[-1]
        # answer = line[-2].strip()
        answer = line[-2]
        answer = answer_transform(answer)
        # eid = answer.find('\n\n')
        # if eid != -1:
        #     answer = answer[:eid].replace('Answer: ', '').replace('answer: ', '')
        if label == 'label':
            continue
        if answer == 'Yes' or answer == 'yes' or answer == 'true':
            answer = 'True'
        if answer == 'No' or answer == 'no' or answer == 'false':
            answer = 'False'
        if answer == label:
            acc += 1
        if answer == 'Error':
            error += 1
            reTry_result = reTry(line[0],line[1],label)
            if reTry_result != 'Error':
                error -= 1
            if reTry_result == label:
                acc += 1
        # if answer == 'answer_error':
        #     error += 1
        #     print(answer,label)
        #     answer_error_list.append(line)
        # elif answer == 'api_error':
        #     api_error_list.append(line)
        # else:
        #     pass_list.append(line)
        cnt += 1
    print(example, examplePath)
    print(acc, cnt)
    print(acc / cnt)
    print(error)
    print(acc / (cnt-error))
    # return pass_list, api_error_list, answer_error_list
    
    
def syllogism():
    acc = 0
    cnt = 0
    diff = 0
    for line in reader:
        label = line[-1]
        answer = line[-2].lower()
        if label == 'label':
            continue
        answer = answer_transform(answer)
        if answer == label:
            acc += 1
        if answer == 'Error':
            diff += 1
            # reTry_result = reTry_syllogism(line[0],line[1],line[2],line[3],line[4],line[5],label)
            reTry_result = reTry_syllogism(line[0],line[1],line[2],label)
            if reTry_result != 'Error':
                diff -= 1
            if reTry_result == label:
                acc += 1
        # if answer == 'answer_error':
        #     error += 1
        #     print(answer,label)
        #     answer_error_list.append(line)
        # elif answer == 'api_error':
        #     api_error_list.append(line)

        # else:
        #     writer.writerow(line)
        cnt += 1
    print(acc, diff, cnt)
    print(acc / cnt)
    print(acc / (cnt - diff))

def cot():
    acc = 0
    cnt = 0
    diff = 0
    index = 0
    for line in reader:
        index+=1
        label = line[-1]
        answer = line[-2].lower()
        if label == 'label':
            continue
        answer = answer_transform(answer)
        if answer == label:
            acc += 1
        if answer == 'Error':
            print(index)
            diff += 1
            reTry_result = reTry(line[0],line[1],label)
            if reTry_result != 'Error':
                diff -= 1
            if reTry_result == label:
                acc += 1
            # print(answer, label)
        # if answer == 'answer_error':
        #     error += 1
        #     print(answer,label)
        #     answer_error_list.append(line)
        # elif answer == 'api_error':
        #     api_error_list.append(line)
        # else:
        #     pass_list.append(line)
        cnt += 1
    print(acc, diff, cnt)
    print(acc / cnt)
    print(acc / (cnt - diff))

def sccot():
    acc = 0
    diff = 0
    answer_dic = {}
    label_dic = {}
    quest_dic = {}
    cnt = 0
    index = 0
    # for line in reader:
    #     cnt += 1
    # print(cnt)
    for line in reader:
        question = line[0]
        label = line[-1]
        answer = line[-2].lower()
        answer = answer_transform(answer)
        if label == 'label':
            continue
        if question not in answer_dic.keys():
            answer_dic[question] = {'True':0, 'False':0, 'Error':0}
            quest_dic[question] = line[:-2]

        label_dic[question] = label
        answer_dic[question][answer] += 1
        cnt += 1

    for key in answer_dic:
        label = label_dic[key]
        answer = max(answer_dic[key], key=answer_dic[key].get)
        if label_dic[key] == answer:
            acc += 1
        if answer == 'Error':
            diff += 1
            reTry_result = ''
            data = quest_dic[key]
            if '_syllogism' in example:
                reTry_result = reTry_syllogism(key,processContext(data[1]),data[2],data[3],data[4],data[5],label)
            else:
                reTry_result = reTry(key,processContext(quest_dic[key][1]),label)
            
            if reTry_result != 'Error':
                diff -= 1
            if reTry_result == label:
                acc += 1
        # if answer == 'answer_error':
        #     error += 1
        #     print(answer,label)
        #     answer_error_list.append(line)
        # elif answer == 'api_error':
        #     api_error_list.append(line)
        # else:
        #     pass_list.append(line)
    print(acc, diff, len(answer_dic.keys()))
    print(acc / len(answer_dic.keys()))
    print(acc / (len(answer_dic.keys()) - diff))


def ccot():
    acc = 0
    diff = 0
    question_dic = {}
    answer_dic = {}
    label_dic = {}
    fact_dic = {}

    for line in reader:
        question = line[0]
        label = line[-1]
        answer = line[-2].lower()
        if label == 'label':
            continue
        if question not in question_dic.keys():
            question_dic[question] = [answer]
            fact_dic[question] = processContext(line[1])
        else:
            question_dic[question].append(answer)
        label_dic[question] = label
        
    for key in question_dic:
        answer_dic[key] = {'True':0, 'False':0, 'Error':0}
        l = sorted(question_dic[key], key=lambda x: len(x), reverse=True)
        for i in range(5):
            answer = answer_transform(l[i])
            answer_dic[key][answer] += 1
    for key in answer_dic:
        label = label_dic[key]
        answer = max(answer_dic[key], key=answer_dic[key].get)
        if label_dic[key] == answer:
            acc += 1
        elif answer == 'Error':
            diff += 1
            reTry_result = reTry(key,fact_dic[key],label)
            if reTry_result != 'Error':
                diff -= 1
            if reTry_result == label:
                acc += 1
            
    print(len(question_dic))
    print(acc, diff, len(answer_dic.keys()))
    print(acc / len(answer_dic.keys()))
    print(acc / (len(answer_dic.keys()) - diff))

# sccot()
# syllogism()
# ccot()
# cot()
# base()

if '_base' in example:
    base()
elif '_cot' in example:
    cot()
    print("in cot")
elif '_ccot' in example:
    ccot()
    print("In ccot")
elif '_sccot' in example:
    sccot()
    print("in sccot")
elif '_syllogism' in example and 'multi_' not in example:
    syllogism()
elif '_syllogism' in example and 'multi_' in example:
    sccot()
    print("Syllogism multi round")

# syllogism()