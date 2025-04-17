import os
import json
# from chat_api import get_answer
import warnings
warnings.filterwarnings('ignore')

import requests
import json
import random
from openai import OpenAI

original_path = 'result/BoolQ_sccot_deepseek_2024-06-04 02:22:06.json'
pathList = [
    'result/BoolQ_sccot_deepseek_2024-06-04 02:22:06.json',
    'result/BoolQ_sccot_deepseek_2024-06-11 19:08:26.json',
]
client = OpenAI(api_key="sk-", base_url="https://api.deepseek.com")
def get_answer(prompt):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt},
            ],
        stream=False
        )
    return response.choices[0].message.content


def getOutputFileName(original_path):
    """Change new file name with _fixed as appendix"""
    path, filename = os.path.split(original_path)
    filename_base, ext = os.path.splitext(filename)
    fixed_name = filename_base + '_fixed' + ext
    fixed_path = os.path.join(path, fixed_name)
    return fixed_path

def is_data_point_invalid(data):
    """check if data point is invalid"""
    required_fields = ["question", "passage", "prediction"]
    return any(data.get(field) in (None, '', 'None') for field in required_fields)

def main():
    for original_path in pathList:
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

                if prediction.find('Yes\'') != -1 or prediction.find('Yes.') != -1 or prediction.find('True') != -1 or prediction.find('Yes') == 0:
                    transform_prediction = 'True'
                    correct += 1
                elif prediction.find('No\'') != -1 or prediction.find('No.') != -1 or prediction.find('False') != -1 or prediction.find('No') == 0:
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
                        # non api error, using prompt to tackle, and record new answer
                        # fixed_prediction = "Test fixed"
                        try:
                            fixed_prediction = get_answer(prompt)
                        except:
                            fixed_prediction = "error"
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