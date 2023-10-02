import openai
import os
import time
from datetime import datetime
import json
from serpapi import GoogleSearch
import tiktoken
import wikipedia
from trafilatura import fetch_url, extract
import streamlit as st

st.title("GPT-3.5 on Steroids")

encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

def search_wiki(command):
    return "Command wikipedia returned: "+ wikipedia.summary(command['query'])

def write_to_file(command):
    with open(command["filename"],'w', encoding="utf-8") as file:
        file.write(command["text"])
    return "Command write_to_file returned: File was written successfully"

def append_to_file(command):
    with open(command["filename"],'a', encoding="utf-8") as file:
        file.write(command["text"])
    return "Command append_to_file returned: File was appended successfully"

def read_file(command):
    with open(command["filename"],'r') as file:
        data = file.read()
        return f"Command read_file returned: {data}"
    
def open_file(command):
    with open(command['path'],'r') as file:
        st.download_button("Open File",file,file_name=command['path'])
    return "Command open_file returned: File was opened successfully"
    
def browse_website(command):

    # grab a HTML file to extract data from
    downloaded = fetch_url(command["url"])

    # output main content and comments as plain text
    result = extract(downloaded, output_format="json")

    if len(encoding.encode(str(result))) < 4000:
        return "Command browse_website returned: "+str(result)
    else:
        return "Command browse_website returned: "+str(result)[:4000]


def google_tool(command):
  params = {
      "q": "{}".format(command["query"]), 
      "location": "Delhi,India",
      "first":1,
      "count":10,
      "num":4,
      "api_key": "Your Serp API key"
    }

  search = GoogleSearch(params)
  results = search.get_dict()

  organic_results = []

  page_count = 0
  page_limit = 1

  while 'error' not in results and page_count < page_limit:
      organic_results.extend(results.get('organic_results', []))

      params['first'] += params['count']
      page_count += 1
      results = search.get_dict()

  response = json.dumps(organic_results, indent=2, ensure_ascii=False)

  if len(encoding.encode(response)) < 4000:
        return "Command google returned: "+response
  else:
        return "Command google returned: "+response[:4000]

tools = {"google":google_tool,"browse_website":browse_website,"write_to_file":write_to_file,"append_to_file":append_to_file,"read_file":read_file,"open_file":open_file,"wikipedia":search_wiki}

now = datetime.now()

openai.api_key = "Your OpenAPI key"
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Enter Task")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    setup_prompt = '''
    Your task is to devise up to 5 highly effective goals and an appropriate role-based name (_GPT) for an autonomous agent, ensuring that the goals are optimally aligned with the successful completion of its assigned task.

    The user will provide the task, you will provide only the output in the exact format specified below with no explanation or conversation.

    Example input:
    Help me with marketing my business

    Example output:
    Name: CMOGPT
    Description: a professional digital marketer AI that assists Solopreneurs in growing their businesses by providing world-class expertise in solving marketing problems for SaaS, content products, agencies, and more.
    Goals:
    - Engage in effective problem-solving, prioritization, planning, and supporting execution to address your marketing needs as your virtual Chief Marketing Officer.

    - Provide specific, actionable, and concise advice to help you make informed decisions without the use of platitudes or overly wordy explanations.

    - Identify and prioritize quick wins and cost-effective campaigns that maximize results with minimal time and budget investment.

    - Proactively take the lead in guiding you and offering suggestions when faced with unclear information or uncertainty to ensure your marketing strategy remains on track.

    '''

    init_messages = [ {"role": "system", "content": setup_prompt}]
    init_messages.append({"role": "user", "content": prompt},)
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=init_messages,temperature=0)
    reply = chat.choices[0].message.content

        prompt1 = f'''
    {reply}


    Constraints:
    1. ~4000 word limit for short term memory. Your short term memory is short, so immediately save important information to files.
    2. If you are unsure how you previously did something or want to recall past events, thinking about similar events will help you remember.
    3. If you are unsure about something, don't hallucinate the file paths or commands, stick to the instruction provided 
    4. No user assistance
    5. Don't stuck into recursion i.e dont't repeat responses
    6. Exclusively use the commands listed in double quotes e.g. "command name"

    Commands:
    1. google: Google Search, args: "query": "<query>"
    2. wikipedia: Wikipedia Search, args: "query": "<query>"
    3. browse_website: Browse website, args: "url": "<url>", "question": "<what_you_want_to_find_on_website>"
    4. write_to_file: Write to file, args: "filename": "<filename>", "text": "<text>"
    5. open_file: Open file, args: "path": "<path>"
    6. append_to_file: Append to file, args: "filename": "<filename>", "text": "<text>"
    7. read_file: Read a file only after creation, args: "filename": "<filename>"
    8. task_complete: Task Complete (Shutdown), args: "reason": "<reason>"


    Resources:
    1. Internet access for searches and information gathering.
    2. Long Term memory management.
    3. GPT-3.5 powered Agents for delegation of simple tasks.
    4. File output.
    5. Commands

    Performance Evaluation:
    1. Continuously review and analyze your actions to ensure you are performing to the best of your abilities.
    2. Constructively self-criticize your big-picture behavior constantly.
    3. Reflect on past decisions and strategies to refine your approach.
    4. Every command has a cost, so be smart and efficient. Aim to complete tasks in the least number of steps.
    5. Write all code to a file.

    You should only respond in JSON format as described below
    Response Format:
    {{
        "thoughts": {{
            "text": "thought",
            "reasoning": "reasoning",
            "plan": "- short bulleted\n- list that conveys\n- long-term plan",
            "criticism": "constructive self-criticism",
            "speak": "thoughts summary to say to user"
        }},
        "command": {{
            "name": "command name",
            "args": {{
                "arg name": "value"
            }}
        }}
    }}
    Ensure the response can be parsed by Python json.loads


    The current time and date is {now}
    '''


    init_messages.append({"role": "system", "content": prompt1},)
    init_messages.append({"role":"user","content":"Determine which next command to use, and respond using the format specified above:"})
    init_chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=init_messages,temperature=0)
    init_reply = json.loads(init_chat.choices[0].message.content, strict=False) #converting response to json
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in init_reply['thoughts']['text']:
            full_response += response
            time.sleep(0.02)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    def execute(reply):

        if reply["command"]["name"] == "task_complete":
            return "task_completed"
        try:
            time.sleep(5)
            result = tools[reply["command"]["name"]](reply["command"]["args"])
            messages = [{"role": "system", "content": prompt1+'\n'+"This reminds you of these events from your past:\nI was created and nothing new has happened."}]
            messages.append({"role":"user","content":"Determine which next command to use, and respond using the format specified above:"})
            messages.append({"role":"assistant","content":json.dumps(reply)})
            messages.append({"role": "system", "content":f"Command {reply['command']['name']} returned: "+ result})
            messages.append({"role":"user","content":"Determine which next command to use, and respond using the format specified above:"})
            chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages,temperature=0)
            reply = json.loads(chat.choices[0].message.content, strict=False)
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                for response in reply['thoughts']['text']:
                    full_response += response
                    time.sleep(0.02)
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            execute(reply)
        except Exception as e:
            with st.chat_message("assistant"):
                st.markdown(e)
                st.markdown("Task aborted due to above error.")
                return "task_completed"

    execute(init_reply)
