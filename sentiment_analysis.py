import os
import json
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Authenticate the client using your key and endpoint 
def authenticate_client():
    language_key = "9d0e7251889644fda17659b06b67d96a"
    language_endpoint = "https://vox-sentiment.cognitiveservices.azure.com/"
    ta_credential = AzureKeyCredential(language_key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=language_endpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

# Function to read JSON file and extract sentences
def read_texts_from_json(json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {json_file_path} was not found.")
    except json.JSONDecodeError:
        raise ValueError(f"The file {json_file_path} is not a valid JSON file.")
    
    sent_list = data.get("SentList", None)
    if sent_list is None:
        raise ValueError("The JSON file does not contain the key 'SentList'.")
    if not isinstance(sent_list, list):
        raise ValueError("The 'SentList' key must be associated with a list of dictionaries.")
    if not sent_list:
        raise ValueError("The 'SentList' list is empty.")

    documents = [item["sentence"] for item in sent_list if "sentence" in item]
    if not documents:
        raise ValueError("No valid 'sentence' entries found in 'SentList'.")
    return documents

# Example method for detecting sentiment and opinions in text
def sentiment_analysis_with_opinion_mining_example(client, documents):
    for i in range(0, len(documents), 10):
        batch = documents[i:i+10]
        result = client.analyze_sentiment(batch, show_opinion_mining=True)
        doc_result = [doc for doc in result if not doc.is_error]

        for document in doc_result:
            print("Document Sentiment: {}".format(document.sentiment))
            print("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
                document.confidence_scores.positive,
                document.confidence_scores.neutral,
                document.confidence_scores.negative,
            ))
            for sentence in document.sentences:
                print("Sentence: {}".format(sentence.text))
                print("Sentence sentiment: {}".format(sentence.sentiment))
                print("Sentence score:\nPositive={0:.2f}\nNeutral={1:.2f}\nNegative={2:.2f}\n".format(
                    sentence.confidence_scores.positive,
                    sentence.confidence_scores.neutral,
                    sentence.confidence_scores.negative,
                ))
                for mined_opinion in sentence.mined_opinions:
                    target = mined_opinion.target
                    print("......'{}' target '{}'".format(target.sentiment, target.text))
                    print("......Target score:\n......Positive={0:.2f}\n......Negative={1:.2f}\n".format(
                        target.confidence_scores.positive,
                        target.confidence_scores.negative,
                    ))
                    for assessment in mined_opinion.assessments:
                        print("......'{}' assessment '{}'".format(assessment.sentiment, assessment.text))
                        print("......Assessment score:\n......Positive={0:.2f}\n......Negative={1:.2f}\n".format(
                            assessment.confidence_scores.positive,
                            assessment.confidence_scores.negative,
                        ))
                print("\n")
            print("\n")

# Path to your JSON file
json_file_path = 'transliteration.json'

# Read texts from JSON file
try:
    documents = read_texts_from_json(json_file_path)
except Exception as e:
    print(f"An error occurred: {e}")
    documents = []

# Run sentiment analysis if documents are available
if documents:
    sentiment_analysis_with_opinion_mining_example(client, documents)
else:
    print("No documents to analyze.")
