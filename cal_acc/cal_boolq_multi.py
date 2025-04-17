import json
import csv

path = 'result/BoolQ_syllogism_multi_Qwen_1_5_32B_T0.9_p0.7_2024-07-31 12:57:57_fixed.json'
f = open(path, 'r')
# fo = open(path[:-5] + '_error_samples.csv', 'w')
# writer = csv.writer(fo)

answer_dic = {}
prediction_dic = {}
label_dic = {}
full_answer_dic = {}
passage_dic = {}
major_dic = {}
explanation_dic = {}
minor_dic = {}
minor_question_dic = {}
question = ''

for line in f.readlines():
    if '"question":' in line:
        question = line
    if '"answer":' in line:
        if question in label_dic.keys():
            continue
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
        answer = line.replace('"prediction": ', '').strip().strip('\"').strip()
        if question in answer_dic.keys():
            answer_dic[question].append(answer)
        else:
            answer_dic[question] = [answer]

def sccot():
    for question in answer_dic.keys():
        dic = {'True':0, 'False':0, 'Error':0}
        for answer in answer_dic[question]:
            # eid = answer.find('\n\n')
            # answer = answer[:eid]
            # if 'Yes.' in answer or 'Tru' in answer or 'True' in answer:
            #     answer = 'True'
            # elif 'No.' in answer or 'False' in answer or 'Fals' in answer:
            #     answer = 'False'
            if answer.find('Yes\'') != -1 or answer.find('Yes.') != -1 or answer.find('True') != -1 or answer.find('Yes') == 0:
                answer = 'True'
            elif answer.find('No\'') != -1 or answer.find('No.') != -1 or answer.find('False') != -1 or answer.find('No') == 0:
                answer = 'False'
            else:
                print(answer)
                answer = 'Error'
            dic[answer] += 1    
        prediction_dic[question] = max(dic, key=dic.get)

def ccot():
    for question in answer_dic.keys():
        answer_list = sorted(answer_dic[question], key=len, reverse=True)
        dic = {'True':0, 'False':0, 'Error':0}
        for i in range(int(len(answer_list) / 2)):
            # eid = answer_list[i].find('\n\n')
            # answer_list[i] = answer_list[i][:eid]
            # if 'Yes.' in answer_list[i] or 'Tru' in answer_list[i] or 'True' in answer_list[i]:
            #     answer = 'True'
            # elif 'No.' in answer_list[i] or 'False' in answer_list[i] or 'Fals' in answer_list[i]:
            #     answer = 'False'
            if answer_list[i].find('Yes\'') != -1 or answer_list[i].find('Yes.') != -1 or answer_list[i].find('True') != -1 or answer_list[i].find('Yes') == 0:
                answer = 'True'
            elif answer_list[i].find('No\'') != -1 or answer_list[i].find('No.') != -1 or answer_list[i].find('False') != -1 or answer_list[i].find('No') == 0:
                answer = 'False'
            else:
                print(answer)
                answer = 'Error'
            dic[answer] += 1
        prediction_dic[question] = max(dic, key=dic.get)
        
sccot()
acc = 0
diff = 0
print(len(answer_dic))
cnt = (len(prediction_dic.keys()))
for key in prediction_dic.keys():
    if prediction_dic[key] == 'Error':
        diff += 1
        continue
    if prediction_dic[key] == label_dic[key]:
        acc += 1
    # else:
    #     writer.writerow([key, passage_dic[key], explanation_dic[key], major_dic[key], minor_question_dic[key], minor_dic[key], answer_dic[key], label_dic[key]])

print(acc, cnt, diff)
print(acc/cnt)
print(acc/(cnt - diff))