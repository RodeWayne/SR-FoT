import os
import json
# from chat_api import get_answer
import warnings
warnings.filterwarnings('ignore')

pathDic = {
    'gpt_boolq_base_v1': 'result/BoolQ_dev_base_T0.2_p0.3_2024-06-10 20:38:17.json',
    'gpt_boolq_base_v2': 'result/BoolQ_dev_base_v2_T0.2_p0.3_2024-06-14 14:52:31.json'
}
import requests
import json
import random

def chat(prompt,idx,T,p):
    # print(prompt)
    url = ''
    gpt_keys = [
        'sk-',
        'sk-'
    ]

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

def get_answer(prompt, T, p):
    idx = random.randint(0, 1)
    answer = chat(prompt=prompt, idx = idx, T=T, p=p)
    #cnt = 0
    while answer == 'timeout' or answer == None:
        idx = random.randint(0, 1)
        #cnt += 1
        answer = chat(prompt=prompt, idx = idx, T=T, p=p)
        print(answer)
    return answer

def getOutputFileName(original_path):
    """Change new file name with _fixed as appendix"""
    path, filename = os.path.split(original_path)
    filename_base, ext = os.path.splitext(filename)
    fixed_name = filename_base + '_fixed' + ext
    fixed_path = os.path.join(path, fixed_name)
    return fixed_path

def is_data_point_invalid(data):
    """check if data is invalid"""
    required_fields = ["question", "passage", "prediction"]
    return any(data.get(field) in (None, '', 'None') for field in required_fields)

def main():
    pathName = 'gpt_boolq_base_v2'
    original_path = pathDic[pathName]
    fixed_path = getOutputFileName(original_path)
    print("Processing...")
    print("Original file path: ", original_path)
    print("Fixed Path: ", fixed_path)
    
    total = 0
    correct = 0
    api_invalid = 0
    all_invalid = 0
    prediction_invalid = 0
    with open(original_path, 'r') as f, open(fixed_path, 'w') as fo:
        data_points = f.read().split('}{')
        for i, data_point in enumerate(data_points):
            total += 1
            # print(f'Processing {i+1}/{total}')
            if i == 0:
                data_point = data_point + '}'
            elif i == len(data_points) - 1:
                data_point = '{' + data_point
            else:
                data_point = '{' + data_point + '}'
            
            data = json.loads(data_point)
            question = data["question"]
            title = data["title"]
            answer = data["answer"]
            passage = data["passage"]
            prediction = data["prediction"]
            # id = data["id"]
            transform_prediction = ""

            if prediction.find('True') != -1 or prediction.find('true') != -1 or prediction.find('Yes') != -1:
                transform_prediction = 'True'
                correct += 1
            elif prediction.find('False') != -1 or prediction.find('false') != -1 or prediction.find('No') != -1:
                transform_prediction = 'False'
            else:
                transform_prediction = 'Invalid'
                all_invalid += 1
            
            if transform_prediction == 'Invalid':
                prompt = f"""
                Question: {question}
                Passage: {passage}
                Title: {title}
                Rethink the above context, identify the information you find useful, and then provide your answer with either 'True' or 'False'.
                """
                if is_data_point_invalid(data):
                    print("Api invalid")
                    print("question: ", {question})
                    # api error, do nothing
                    # new_answer = "Error"
                    api_invalid += 1
                    pass
                else:
                    # non api error, using prompt to tackle and record new answer
                    # fixed_prediction = "Test fixed"
                    fixed_prediction = get_answer(prompt, 0.2, 0.3)
                    prediction_invalid += 1
                    # print("Fixed id: ", data['id'])
                    print("Old prediction: ", data['prediction'])
                    print("Fiexed prediction: ", fixed_prediction)
                    data["prediction"] = fixed_prediction

            json.dump(data, fo, indent=4)
            # if i < len(data_points) - 1:
            #     fo.write("}{")
    print(original_path)
    print(fixed_path)
    print(all_invalid)

if __name__ == "__main__":
    main()