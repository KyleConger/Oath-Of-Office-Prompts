import os; import sys
from openai import OpenAI
client = OpenAI()
from query_storage import ChatTree
from newsapi import NewsApiClient
from datetime import date, timedelta
newsapi = NewsApiClient(api_key=(os.getenv('NEWS_KEY')))
import requests
session = requests.Session()
import random; import string

current_date = date.today()
oldestdate = current_date - timedelta(days=21)
newestdate = current_date - timedelta(days=14)

def generate_random_filename(extension="txt"):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(10))
    return f"{random_string}.{extension}"

def call_chat(variable):
    chat = getattr(ChatTree, variable, None)
    
    if not chat:
        raise ValueError(f"No chat configuration found for variable: {variable}")
    
    messages = [{"role": "system", "content": chat['system']}]
    
    for i in range(1, 5):
        example_input_key = f'example_input{i}'
        example_output_key = f'example_output{i}'
        if example_input_key in chat and example_output_key in chat:
            messages.append({"role": "user", "content": chat[example_input_key]})
            messages.append({"role": "assistant", "content": chat[example_output_key]})
    
    if chat['prompt']:
        messages.append({"role": "user", "content": chat['prompt']})
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=chat['temperature'],
        max_tokens=chat['max_tokens'],
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    return response.choices[0].message.content

def get_effected_topics():
    return [
        "Russia", "Europe", "Poor", "Middle Class", "Rich", "Defense Industry", 
        "Financial Industry", "Immigrants", "Nationalists", "Youth", 
        "Environmentalists", "Resources Industry", "China", "The Commonwealth", 
        "Technology Industry", "Native Americans", "The Economy", 
        "Average Tax Rate", "Global Stability", "Military Strength", 
        "The Environment", "Crime", "Civil Rights", "Inflation", "Unemployment"
    ]

top_headlines = []
for page in range(1, 5):  # Loop through pages
    response = newsapi.get_everything(
        language='en',
        sort_by='publishedAt',
        sources='associated-press,cnn,politico,the-washington-post',
        page=page,
        from_param=oldestdate,
        to=newestdate
    )
    top_headlines.extend(response['articles'])

headlines = [article['title'] for article in top_headlines]

headlines_with_yes = [] #This is where all the approved topics are stored
for headline in headlines:
    response = call_chat("ApprovedTopics")
    if "Yes" in response:
        headlines_with_yes.append(headline)

filename = generate_random_filename()

Issues = [] #This is where all the written prompts are stored
for headline in headlines_with_yes:
    response = call_chat("IssueCreator")
    Issues.append(response)
for issue in Issues:
    print(issue)
    print("\n")
    with open(filename, 'a') as file:
        for issue in Issues:
            file.write(issue + "\n\n--\n\n")


