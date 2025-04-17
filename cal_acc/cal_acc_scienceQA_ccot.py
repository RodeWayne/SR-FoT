import csv

#f = open('/home/wentao/IJCAI_2024/llm_halluc_reduce/output/titile_examples_result.csv', 'r')
f = open('/home/wentao/IJCAI_2024/llm_halluc_reduce/output/scienceQA_sccot_v5_deepseek_all_test_2024-06-04 02:15:43.csv', 'r')
fo = open('/home/wentao/IJCAI_2024/llm_halluc_reduce/output/scienceQA_ccot_multi_deepseek_diff.csv', 'w')
reader = csv.reader(f)
writer = csv.writer(fo)
data = [line for line in reader]
answer_list = {}
acc = 0
cnt = 0
diff = 0
answer_dic = {}
label_dic = {}
options_dic = {}
line_dic = {}
for line in data:
    id = str(line[:2])
    answer = line[-2]
    label = line[-1]
    if line[1] == 'options' or line[1] == 'question':
        continue
    answer_dic[id] = {'0':0, '1':0, '2':0, '3':0}
    label_dic[id] = label
    options_dic[id] = line[1]
    line_dic[id] = line
    if id in answer_list.keys():
        answer_list[id].append(answer)
    else:
        answer_list[id] = [answer]
    

for id in answer_list.keys():
    answer_list[id] = sorted(answer_list[id], key=len, reverse=True)
    for i in range(max(1, int(len(answer_list[id])/2))):
        answer = answer_list[id][i]
        label = label_dic[id]
        options = eval(options_dic[id])
        sid = answer.find('is')
        eid = answer.find('reasoning process step by step')
        answer = answer[sid + 3:eid - 1].strip(',').strip('\'')    
        
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

        if answer != '0' and answer != '1' and answer != '2' and answer != '3':
            continue
        else:
            answer_dic[id][answer] += 1 

for key in answer_dic.keys():
    answer = ''
    num = 0
    for _ in answer_dic[key].keys():
        if answer_dic[key][_] > num:
            num = answer_dic[key][_]
            answer = _
    if answer == '':
        writer.writerow(line_dic[key])
        print(line_dic[key])
        diff += 1
    if answer == label_dic[key]:
        acc += 1
    
    cnt += 1
    
    
print(acc, cnt, diff)
print(acc / cnt)
print(acc / (cnt - diff))
