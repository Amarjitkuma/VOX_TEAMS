# -*- coding: utf-8 -*-

import os
import requests
import uuid
import json

# Key and endpoint setup
subscription_key = ''  # Your subscription key here
region = ''  # Your region here
endpoint = 'https://api.cognitive.microsofttranslator.com/'

# Path and parameters for the transliteration request
path = '/transliterate?api-version=3.0'
params = '&language=hi&fromScript=deva&toScript=latn'
constructed_url = endpoint + path + params

headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Ocp-Apim-Subscription-Region': region,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

# Function to perform transliteration
def transliterate_text(text):
    body = [{'text': text}]
    response = requests.post(constructed_url, headers=headers, json=body)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Read the JSON file
input_file = 'transcription.json'  # Ensure your JSON file is named correctly
output_file = 'transliteration.json'
audio_file_name = "OUT-1234000.txt"  # Replace with your actual audio file name if needed

with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Prepare the output structure
output_data = {
    "audio_file_name": audio_file_name,
    "SentList": []
}

# Iterate through the JSON data and transliterate the text
for entry in data:
    if isinstance(entry, dict):  # Ensure it's a valid entry
        original_text = entry['sentence']
        transliterated_response = transliterate_text(original_text)
        
        if transliterated_response and 'text' in transliterated_response[0]:
            transliterated_text = transliterated_response[0]['text']
        else:
            transliterated_text = original_text  # Fallback to the original text if transliteration fails
        
        new_entry = {
            "speaker": entry['speaker'],
            "sentence": transliterated_text,
            "start_time": entry['start_time'],
            "end_time": entry['end_time'],
            "confidence": entry['confidence']
        }
        output_data["SentList"].append(new_entry)

# Write the new JSON data with transliterated text to a new file
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(output_data, file, ensure_ascii=False, indent=4)

print(f"Transliteration complete. Output saved to {output_file}")
