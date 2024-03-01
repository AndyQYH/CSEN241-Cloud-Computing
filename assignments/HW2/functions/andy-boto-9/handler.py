import re
import requests
from datetime import datetime
import random
import os
import subprocess

# Building a dictionary of responses
responses={
    'hello':	{
    		'1':'Hello! How can I help you?',
    		'2':'Hi! What can I do for you?',
    		'3':'Hola! Como Estas?',
    		},
    'name':	{
    		'1':'My name is andy boto, nice to meet you!',
    		'2':'Me llamo andy boto, Encantado de conocerte',
    		'3':'Wo de ming zi shi Andy boto, hen gang xin ren shi ni!'
    		},
    'time':	{
    		'1':'Current time is ...',
    		'2':'Uhm I think is ...,',
    		'3':'From my watch, it is ...',
    		},
    'date':	{
    		'1':'Today is ...',
    		'2':'Look at the calendar, it is ...,',
    		'3':'The date is ... our date of course ^_^',
    		},
    'figlet':	{
    		'1':'faas-cli invoke figlet'
    		},
    'fallback': {
    		'1':'I dont quite understand. Could you repeat that?',
    		'2':'I was lagging, please try again ...'
    		}
}

figlet_url = "http://10.62.0.5:8080/function/figlet"
# Building a list of Keywords
list_words=['hello', 'name', 'time', 'date', 'figlet']
list_syn={}

list_syn['name'] = set(['name','names','credentials','info'])
list_syn['hello'] = set(['hi','hello','halo','hey','howddy', 'greetings', 'what\'s up'])
list_syn['time'] = set(['time', 'times', 'timing', 'moment', 'clock'])
list_syn['date'] = set(['date', 'dates', 'day'])
list_syn['figlet'] = set(['figlet', 'figlets'])

# Building dictionary of Intents & Keywords
keywords={}
keywords_dict={}

# Defining a new key in the keywords dictionary
keywords['name']=[]
# Populating the values in the keywords dictionary with synonyms of keywords formatted with RegEx metacharacters 
for synonym in list(list_syn['name']):
    keywords['name'].append('.*\\b'+synonym+'\\b.*')
    
# Defining a new key in the keywords dictionary
keywords['hello']=[]
# Populating the values in the keywords dictionary with synonyms of keywords formatted with RegEx metacharacters 
for synonym in list(list_syn['hello']):
    keywords['hello'].append('.*\\b'+synonym+'\\b.*')

# Defining a new key in the keywords dictionary
keywords['time']=[]
# Populating the values in the keywords dictionary with synonyms of keywords formatted with RegEx metacharacters 
for synonym in list(list_syn['time']):
    keywords['time'].append('.*\\b'+synonym+'\\b.*')
    
# Defining a new key in the keywords dictionary
keywords['date']=[]
# Populating the values in the keywords dictionary with synonyms of keywords formatted with RegEx metacharacters 
for synonym in list(list_syn['date']):
    keywords['date'].append('.*\\b'+synonym+'\\b.*')
    
# Defining a new key in the keywords dictionary
keywords['figlet']=[]
# Populating the values in the keywords dictionary with synonyms of keywords formatted with RegEx metacharacters 
for synonym in list(list_syn['figlet']):
    keywords['figlet'].append('.*\\b'+synonym+'\\b.*')
    
for intent, keys in keywords.items():
    # Joining the values in the keywords dictionary with the OR (|) operator updating them in keywords_dict dictionary
    keywords_dict[intent]=re.compile('|'.join(keys))


def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
        has three intents: (1) name (2) time/date (3) figlet
    Res:
    	return a chatbot message to the following questions
    """
	
    user_input = req.lower()
     
    matched_intent = None 
    for intent,pattern in keywords_dict.items():
        # Using the regular expression search function to look for keywords in user input
        if re.search(pattern, user_input): 
            # if a keyword matches, select the corresponding intent from the keywords_dict dictionary
            matched_intent=intent  
    # The fallback intent is selected by default
    key='fallback' 
    if matched_intent in responses:
        # If a keyword matches, the fallback intent is replaced by the matched intent as the key for the responses dictionary
        key = matched_intent
    # The chatbot prints the response that matches the selected intent
   
    content = ''
    if key == 'figlet':
    	context = req.split(key)[-1].split('for')[-1]
    	# print('figlet for: ', context)
    	response = requests.post(figlet_url, data = context)
    	#print(response.text)
    	content = response.text
    if key == 'date':
    	now = datetime.now()
    	content = now.strftime("%B %d, %Y")
	#print("d2 =", d2)
    if key == 'time':
    	now = datetime.now()
    	content = now.strftime("%H:%M:%S")
	#print("d2 =", d2)
    rand_key, rand_val = random.choice(list(responses[key].items()))
 
    return rand_val + '\n' + content
