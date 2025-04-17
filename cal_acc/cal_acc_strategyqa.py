import csv

# 计算acc只需要修改对应的example即可
# example = 'gpt_base_v2_fixed'
# example = 'gpt_base_v2'
# example = 'gpt_cot_v2'
# example = 'gpt_cot_v2_fixed'
# example = 'gpt_cot_v2'
# example = 'gpt_ccot_v2'
# example = 'gpt_sccot_v2'
# example = 'gpt_syllogism_v16_signle_round'
# example = 'deepseek_syllogism_v16_multi_round'
example = 'deepseek_base_v2'
# example = 'deepseek_base_v2_fixed'
# example = 'deepseek_cot_v2'
# example = 'deepseek_cot_v2_fixed'
# example = 'deepseek_sccot_v2'
# example = 'deepseek_ccot_v2'
# example = 'deepseek_syllogism_v16_single_round'
# example = 'gpt_syllogism_v16_multi_round'
# example = 'qwen2_70B_base'
# example = 'qwen2_70B_cot'
# example = 'qwen2_70B_syllogism_v16_single_round'
# example = 'qwen1.5_32B_base'
# example = 'qwen1.5_32B_cot'
# example = 'qwen1.5_32B_syllogism_v16_single_round'
# example = 'deepseek_syllogism_v16_final_prompt'
pathDic = {
    'gpt_base_v2': '/home/wentao/IJCAI_2024/llm_halluc_reduce/strategyqa_output/strategyqa_base_v2_T0.2_p0.3_2024-06-04 19:19:52.csv',
    'gpt_base_v2_fixed': '/home/wentao/IJCAI_2024/llm_halluc_reduce/strategyqa_output/strategyqa_base_v2_T0.2_p0.3_2024-06-04 19:19:52_fixed.csv',
    'gpt_cot_v2': '/home/wentao/IJCAI_2024/llm_halluc_reduce/strategyqa_output/strategyqa_cot_v2_T0.2_p0.3_2024-06-04 19:19:28.csv',
    'gpt_cot_v2_fixed': '/home/wentao/IJCAI_2024/llm_halluc_reduce/strategyqa_output/strategyqa_cot_v2_T0.2_p0.3_2024-06-04 19:19:28_fixed.csv',
    'gpt_sccot_v2': '/home/wentao/IJCAI_2024/llm_halluc_reduce/strategyqa_output/strategyqa_sccot_v2_T0.9_p0.7_2024-06-09 02:57:00.csv',
    'gpt_ccot_v2': '/home/wentao/IJCAI_2024/llm_halluc_reduce/strategyqa_output/strategyqa_sccot_v2_T0.9_p0.7_2024-06-09 02:57:00.csv',
    'gpt_syllogism_v16_signle_round': '/home/wentao/IJCAI_2024/llm_halluc_reduce/strategyqa_output/strategyqa_syllogism_v16_T0.2_p0.3_2024-06-07 10:02:40.csv',
    'gpt_syllogism_v16_multi_round': '/home/wentao/IJCAI_2024/llm_halluc_reduce/strategyqa_output/strategyqa_syllogism_v16_multi_T0.9_p0.7_2024-06-11 20:28:41.csv',

    'deepseek_base_v2': '/home/wentao/IJCAI_2024/llm_halluc_reduce/strategyqa_output/strategyqa_base_v2_deepseek_2024-06-05 15:57:20.csv',
    'deepseek_base_v2_fixed': '/home/wentao/IJCAI_2024/llm_halluc_reduce/strategyqa_output/strategyqa_base_v2_deepseek_2024-06-05 15:57:20_fixed.csv',
    'deepseek_cot_v2': '/home/wentao/IJCAI_2024/llm_halluc_reduce/strategyqa_output/strategyqa_cot_v2_deepseek_2024-06-05 16:20:53.csv',
    'deepseek_cot_v2_fixed': '/home/wentao/IJCAI_2024/llm_halluc_reduce/strategyqa_output/strategyqa_cot_v2_deepseek_2024-06-05 16:20:53_fixed.csv',
    'deepseek_sccot_v2': '/home/wentao/IJCAI_2024/llm_halluc_reduce/strategyqa_output/strategyqa_sccot_v2_deepseek_2024-06-09 15:40:02.csv',
    'deepseek_ccot_v2': '/home/wentao/IJCAI_2024/llm_halluc_reduce/strategyqa_output/strategyqa_sccot_v2_deepseek_2024-06-09 15:40:02.csv',
    'deepseek_syllogism_v16_single_round': '/home/wentao/IJCAI_2024/llm_halluc_reduce/strategyqa_output/strategyqa_syllogism_v16_deepseek_2024-06-06 17:57:41.csv',
    'deepseek_syllogism_v16_multi_round': '/home/wentao/IJCAI_2024/llm_halluc_reduce/strategyqa_output/strategyqa_syllogism_v16_deepseek_multi_2024-06-11 16:35:33.csv',
    'deepseek_syllogism_v16_b':'/home/wentao/IJCAI_2024/llm_halluc_reduce/strategyqa_output/strategyqa_syllogism_v16_deepseek_ablation2_b_2024-06-15 14:02:05.csv',
    'deepseek_syllogism_v16_c':'/home/wentao/IJCAI_2024/llm_halluc_reduce/strategyqa_output/strategyqa_syllogism_v16_deepseek_ablation2_b_2024-06-15 14:29:27.csv',
    
    'qwen2_70B_base':'/home/wentao/IJCAI_2024/llm_halluc_reduce/strategyqa_output/strategyqa_base_v2_qwen2_70B_2024-06-12 17:47:49.csv',
    'qwen2_70B_cot':'/home/wentao/IJCAI_2024/llm_halluc_reduce/strategyqa_output/strategyqa_cot_v2_qwen2_70B_2024-06-12 18:18:59.csv',
    'qwen2_70B_syllogism_v16_single_round':'/home/wentao/IJCAI_2024/llm_halluc_reduce/strategyqa_output/strategyqa_syllogism_v16_qwen2_one_2024-06-12 19:37:37.csv',
    'qwen1.5_32B_base':'/home/wentao/IJCAI_2024/llm_halluc_reduce/strategyqa_output/strategyqa_base_v2_qwen1.5_32B_2024-06-13 00:26:19.csv',
    'qwen1.5_32B_cot':'/home/wentao/IJCAI_2024/llm_halluc_reduce/strategyqa_output/strategyqa_cot_v2_qwen1.5_32B_2024-06-13 01:06:46.csv',
    'qwen1.5_32B_sccot':'/home/wentao/IJCAI_2024/llm_halluc_reduce/strategyqa_output/strategyqa_sc-cot_v2_qwen1.5_32B_2024-06-15 11:57:23.csv',
    'qwen1.5_32B_ccot':'/home/wentao/IJCAI_2024/llm_halluc_reduce/strategyqa_output/strategyqa_sc-cot_v2_qwen1.5_32B_2024-06-15 11:57:23.csv',
    'qwen1.5_32B_syllogism_v16_single_round':'/home/wentao/IJCAI_2024/llm_halluc_reduce/strategyqa_output/strategyqa_syllogism_v16_qwen1.5_32B_2024-06-13 01:05:58.csv'
}

examplePath = pathDic[example]
f = open(examplePath, 'r')
# fo = open('/home/wentao/IJCAI_2024/llm_halluc_reduce/strategyqa_output/strategyqa_syllogism_v17_error_sample.csv', 'w')

reader = csv.reader(f)
# writer = csv.writer(fo)

def answer_transform(answer):
    # if answer == 'Error' or answer == '' or answer == None:
    #     return 'api_error'
    #三段论是上面这个
    # sid = answer.find('the answer to the question is ') 
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
            print(answer)
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
            print(answer)
            # answer = 'answer_error'
            answer = 'Error'
    return answer

def base():
    acc = 0
    cnt = 0
    error = 0
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
            print(answer, label)
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
            print(answer, label)
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
            print(answer, label)
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
    cnt = 0
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
        label_dic[question] = label
        answer_dic[question][answer] += 1
        cnt += 1

    for key in answer_dic:
        answer = max(answer_dic[key], key=answer_dic[key].get)
        if label_dic[key] == answer:
            acc += 1
        if answer == 'Error':
            diff += 1
            print(answer, label)
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
    
    for line in reader:
        question = line[0]
        label = line[-1]
        answer = line[-2].lower()
        if label == 'label':
            continue
        if question not in question_dic.keys():
            question_dic[question] = [answer]
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
        answer = max(answer_dic[key], key=answer_dic[key].get)
        if label_dic[key] == answer:
            acc += 1
        elif answer == 'Error':
            diff += 1
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