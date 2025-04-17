import csv

#f = open('result/titile_examples_result.csv', 'r')
f = open('result/scienceQA_syllogism_multi_Qwen_1_5_32B_test_2024-07-31 12:56:46.csv', 'r')
# fo = open('result/scienceQA_syllogism_multi_deepseek_diff.csv', 'w')
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
for line in data:
    id = str(line[:2])
    if line[1] == 'options':
        print(line)
        continue
    answer_dic[id] = {'0':0, '1':0, '2':0, '3':0}
    label_dic[id] = line[-1]
    line_dic[id] = line

for line in data:
    # if line[-2] != 'True' and line[-2] != 'False':
    #     print(line[-2])
    #     diff += 1
    if line[1] == 'options':
        continue
    answer = line[-2]
    label = line[-1]

    #sccot below 3 lines
    # sid = answer.find('is')
    # eid = answer.find('reasoning process step by step')
    # answer = answer[sid + 3:eid - 1].strip(',').strip('\'')    
    eid = answer.find('.')
    answer = answer[:eid].replace('The answer is ', '').strip('\'').strip()
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
       
    cnt += 1
    
    
print(acc, cnt, diff)
print(acc / cnt)
print(acc / (cnt - diff))
