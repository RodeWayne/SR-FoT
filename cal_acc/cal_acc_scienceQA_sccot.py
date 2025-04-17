import csv
import json
#f = open('result/titile_examples_result.csv', 'r')
f = open('result/scienceQA_sccot_deepseek_all_test_2024-06-04 02:15:43_fixed_ccot.csv', 'r')
# fo = open('result/scienceQA_syllogism_multi_deepseek_diff.csv', 'w')
reader = csv.reader(f)
# writer = csv.writer(fo)
data_f = open('dataset/ScienceQA/problems_all_test_balanced.csv', 'r')
json_f = open('dataset/ScienceQA/problems.json', 'r')
reader_data = csv.reader(data_f)
json_data = json.loads(json_f.read())
data_list = []
for line in reader_data:
    data_list.append(line)


data = [line for line in reader]
print(len(data))
answer_list = {}
acc = 0
cnt = 0
diff = 0
subjects = {'natural science':0,'social science':0,'language science':0}
grades = {'grade1':0,'grade2':0,'grade3':0,'grade4':0,'grade5':0,'grade6':0,'grade7':0,'grade8':0,'grade9':0,'grade10':0,'grade11':0,'grade12':0}
right_subjects = {'natural science':0,'social science':0,'language science':0}
right_grades = {'grade1':0,'grade2':0,'grade3':0,'grade4':0,'grade5':0,'grade6':0,'grade7':0,'grade8':0,'grade9':0,'grade10':0,'grade11':0,'grade12':0}

answer_dic = {}
label_dic = {}
line_dic = {}
for line in data:
    id = str(line[:2])
    if line[1] == 'options' or line[1] == 'question':
        continue
    answer_dic[id] = {'0':0, '1':0, '2':0, '3':0}
    label_dic[id] = line[-1]
    line_dic[id] = line
    
for line in data:
    # if line[-2] != 'True' and line[-2] != 'False':
    #     print(line[-2])
    #     diff += 1
    if line[1] == 'options' or line[1] == 'question':
        continue
    answer = line[-2]
    label = line[-1]
    index = line[0]+line[1]
    idx = 0
    for line2 in data_list:
        index2 = line2[0]+line2[1]
        if index == index2:
            idx = line2[-3]
            break
    print(idx)
    print(json_data[idx]['subject'])
    subjects[json_data[idx]['subject']] += 1
    grades[json_data[idx]['grade']] += 1

    #sccot下面三行
    sid = answer.find('is')
    eid = answer.find('reasoning process step by step')
    answer = answer[sid + 3:eid - 1].strip(',').strip('\'')    
    # eid = answer.find('.')
    # answer = answer[:eid].replace('The answer is ', '').strip('\'').strip()
    if answer == 'Option 1':
        answer = '0'
    if answer == 'Option 2' or answer == 'Option B':
        answer = '1'
    if answer == 'Both are physical changes.':
        answer = 'Both are only physical changes.'
    options = eval(line[1])
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

    if answer != '0' and answer != '1' and answer != '2' and answer != '3':
        continue
    else:
        answer_dic[str(line[:2])][answer] += 1 

for key in answer_dic.keys():
    answer = ''
    num = 0
    for _ in answer_dic[key].keys():
        if answer_dic[key][_] > num:
            num = answer_dic[key][_]
            answer = _
    if answer == '':
        # writer.writerow(line_dic[key])
        diff += 1
    if answer == label_dic[key]:
        acc += 1
        idx = 0
        index = eval(key)[0]+eval(key)[1]
        for line2 in data_list:
            index2 = line2[0]+line2[1]
            if index == index2:
                idx = line2[-3]
                break
        print(idx)
        right_subjects[json_data[idx]['subject']] += 1
        right_grades[json_data[idx]['grade']] += 1
        
    cnt += 1
    
    
print(acc, cnt, diff)
print(acc / cnt)
print(acc / (cnt - diff))
print(subjects)
print(grades)
print(right_subjects)
print(right_grades)

for item in right_subjects.keys():
    print(item,right_subjects[item]/subjects[item])

grade1_6 = 0
grade1_6_right = 0
grade7_12 = 0
grade7_12_right = 0

for item in right_grades.keys():
    if item in ['grade1','grade2','grade3','grade4','grade5','grade6']:
        grade1_6 += grades[item]
        grade1_6_right += right_grades[item]
    if item in ['grade7','grade8','grade9','grade10','grade11','grade12']:
        grade7_12 += grades[item]
        grade7_12_right += right_grades[item]
    
print(grade1_6_right/grade1_6)
print(grade7_12_right/grade7_12)