import csv
import json
# pathList = {
#     'base_v5': 'result/scienceQA_base_deepseek_all_test_v5_2024-06-03 01:52:49.csv',
#     'cot_v5': 'result/scienceQA_cot_v5_deepseek_all_test_2024-06-03 02:11:48.csv',
# }
# path = pathList['base_v5']
# f = open(path, 'r')
f = open('result/scienceQA_cot_deepseek_all_test_2024-06-03 02:11:48_fixed.csv', 'r')
# fo = open('result/scienceQA_cot_deepseek_diff.csv', 'w')
reader = csv.reader(f)
# writer = csv.writer(fo)
data_f = open('dataset/ScienceQA/problems_all_test_balanced.csv', 'r')
json_f = open('dataset/ScienceQA/problems.json', 'r')
reader_data = csv.reader(data_f)
data = json.loads(json_f.read())
data_list = []
for line in reader_data:
    data_list.append(line)


acc = 0
cnt = 0
diff = 0
subjects = {'natural science':0,'social science':0,'language science':0}
grades = {'grade1':0,'grade2':0,'grade3':0,'grade4':0,'grade5':0,'grade6':0,'grade7':0,'grade8':0,'grade9':0,'grade10':0,'grade11':0,'grade12':0}
right_subjects = {'natural science':0,'social science':0,'language science':0}
right_grades = {'grade1':0,'grade2':0,'grade3':0,'grade4':0,'grade5':0,'grade6':0,'grade7':0,'grade8':0,'grade9':0,'grade10':0,'grade11':0,'grade12':0}

for line in reader:
    # if line[-2] != 'True' and line[-2] != 'False':
    #     print(line[-2])
    #     diff += 1
    if line[1] == 'options':
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
    # print(idx)
    subjects[data[idx]['subject']] += 1
    grades[data[idx]['grade']] += 1
    # sid = answer.find('the answer is') + 15
    # answer = answer[sid : ]

    #base
    # eid = answer.find('\n\n')
    # answer = answer[:eid].replace('Answer: ', '').strip()

    #cot
    sid = answer.find('The answer is ')
    eid = answer.find('reasoning')
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
        choices = eval(line[1])
        for i in range(len(choices)):
            if choices[i].find(answer) != -1:
                answer = str(i)
                break
    if answer != '0' and answer != '1' and answer != '2' and answer != '3':
        answer = answer.replace('miles', ' miles').replace('hours', ' hours').replace('kilometers', ' kilometers')
        choices = eval(line[1])
        for i in range(len(choices)):
            if answer.find(choices[i]) != -1:
                answer = str(i)
                break
    if answer != '0' and answer != '1' and answer != '2' and answer != '3':
        print(answer)
        # writer.writerow(line)
        diff += 1
    if label == answer:
        acc += 1
        right_subjects[data[idx]['subject']] += 1
        right_grades[data[idx]['grade']] += 1
    else:
        print(answer, label)
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

