import requests
import uuid
import json
import os

# Add your key and endpoint
key = " "
endpoint = "https://api.cognitive.microsofttranslator.com"

# Location, also known as region.
location = "southeastasia"

path = '/translate'
constructed_url = endpoint + path

params = {
    'api-version': '3.0',
    'from': 'te',  # telgu
    'to': ['hi']   # Hindi
}

headers = {
    'Ocp-Apim-Subscription-Key': key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

def translate_text(text):
    body = [{'text': text}]
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    translated_text = response[0]['translations'][0]['text']
    return translated_text

def process_json_file(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    output_data = []

    for entry in data:
        original_text = entry['sentence']
        translated_text = translate_text(original_text)
        
        new_entry = {
            'speaker': entry['speaker'],
            'sentence': translated_text,
            'start_time': entry['start_time'],
            'end_time': entry['end_time'],
            'confidence':entry['confidence']
        }
        
        output_data.append(new_entry)

    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(output_data, file, ensure_ascii=False, indent=4)

    print(f"Translation complete. Output saved to {output_file_path}")

# Define the input and output file paths
input_file_path = 'transcription.json'  # Replace with your input JSON file path
output_file_path = 'translation.json'  # Replace with your desired output JSON file path

process_json_file(input_file_path, output_file_path)
