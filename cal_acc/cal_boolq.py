import json
import csv

# pathDic = {
#     'base_v1': 'result/BoolQ_base_deepseek_2024-06-10 20:02:44.json',
#     'base_v2': 'result/BoolQ_base_yesorno_deepseek_2024-06-10 19:30:26.json',
#     'cot_2_shot_v1(yes/no)': 'result/BoolQ_cot_deepseek_2024-06-03 20:21:40.json',
#     'cot_2_shot_v1_2(true/false)': 'result/deepseek_boolq_cot_0.2.json',
#     'syllogism_v2': 'result/BoolQ_syllogism_dev_v2_deepseek_T0.2_p0.3_2024-06-04 09:38:15.json',
#     'syllogism_v4': 'result/BoolQ_syllogism_dev_v4_deepseek_T0.2_p0.3_2024-06-08 11:15:05.json',
#     'syllogism_v6': 'result/BoolQ_syllogism_dev_v6_deepseek_T0.2_p0.3_2024-06-08 19:39:25.json',
#     'syllogism_v8_yes_no': 'result/BoolQ_syllogism_dev_v8_deepseek_T0.2_p0.3_2024-06-10 18:50:31.json'
# }

# path = pathDic['cot_2_shot_v1_2(true/false)']
# f = open(path, 'r')
# f = open('result/BoolQ_syllogism_dev_v6_T0.2_p0.3_2024-06-08 19:50:49_fixed.csv', 'r')
# 0.7681957186544343
# 0.8309626199139927
# f = open('result/BoolQ_syllogism_dev_v6_T0.2_p0.3_2024-06-08 19:50:49.csv', 'r')
# 0.7681957186544343
# 0.8309626199139927
path = 'result/BoolQ_syllogism_T0.2_p0.3_2024-06-08 19:50:49.csv'
f = open(path, 'r')
fo = open(path[:-4] + '_right_samples.csv', 'w')
writer = csv.writer(fo)

answer_dic = {}
label_dic = {}
full_answer_dic = {}
passage_dic = {}
major_dic = {}
explanation_dic = {}
minor_dic = {}
minor_question_dic = {}


question = ''
for line in f.readlines():
    if '\"question\": ' in line:
        question = line
    if '"answer":' in line:
        # if question in label_dic.keys():
        #     continue
        if 'true' in line:
            label_dic[question] = 'True'
        elif 'false' in line:
            label_dic[question] = 'False'
        else:
            label_dic[question] = 'Error'
    if '"passage":' in line:
        passage_dic[question] = line 
    if '"explanation":' in line:
        explanation_dic[question] = line 
    if '"major":' in line:
        major_dic[question] = line 
    if '"minor_question":' in line:
        minor_question_dic[question] = line 
    if '"minor":' in line:
        minor_dic[question] = line 
    if '"prediction":' in line:
        full_answer_dic[question] = line
        # if question in answer_dic.keys():
        #     continue
        #l2m
        sid = line.find('The final answer is')
        if sid != -1:
            line = line[sid:]
        if line.find('True') != -1 or line.find('true') != -1 or line.find('Yes\'') != -1 or line.find('Yes') == 21:
            answer_dic[question] = 'True'
        elif line.find('False') != -1 or line.find('false') != -1 or line.find('No\'') != -1 or line.find('No') == 21:
            answer_dic[question] = 'False'
        else:
            print(line)
            answer_dic[question] = 'Error'

acc = 0
diff = 0
cnt = (len(answer_dic.keys()))
for key in answer_dic.keys():
    if answer_dic[key] == 'Error':
        diff += 1
        # writer.writerow([key.replace('\"','').replace('\n', '').replace('question:', '')[:-1].strip(), passage_dic[key].replace('\"','').replace('\n', '').replace('passage:', '')[:-1].strip(), explanation_dic[key], major_dic[key], minor_question_dic[key], minor_dic[key], full_answer_dic[key], answer_dic[key], label_dic[key].replace('\"','').replace('\n', '').replace('label:', '').strip()])
        continue
    if answer_dic[key] == label_dic[key]:
        acc += 1
        writer.writerow([key, passage_dic[key], explanation_dic[key], major_dic[key], minor_question_dic[key], minor_dic[key], full_answer_dic[key], label_dic[key], answer_dic[key]])
    else:
        pass
        # try:
            #explanation_dic[key], major_dic[key], minor_question_dic[key], minor_dic[key]
            # writer.writerow([key, passage_dic[key], full_answer_dic[key], label_dic[key], answer_dic[key]])
        # except:
            # pass
print(acc, cnt, diff)
print(acc / cnt)
print(acc / (cnt - diff))
# print("Path: ", pathDic)
# print("Acc: ", acc/cnt)
# print("Acc except error:", acc/(cnt - diff))
