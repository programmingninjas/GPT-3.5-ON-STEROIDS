"""
This is where the program starts
"""

import openai
import time
import json
import sys
import streamlit as st
from consts import OPENAI_API_KEY, SETUP_PROMPT, INSTRUCTION_PROMPT, now
from funcs import (
    google_tool,
    browse_website,
    write_to_file,
    append_to_file,
    read_file,
    open_file,
    search_wiki,
)

# TOOLS
tools = {
    "google": google_tool,
    "browse_website": browse_website,
    "write_to_file": write_to_file,
    "append_to_file": append_to_file,
    "read_file": read_file,
    "open_file": open_file,
    "wikipedia": search_wiki,
}


def main():
    # INITIAL SETUP
    st.title("GPT-3.5 on Steroids")
    openai.api_key = OPENAI_API_KEY

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # GETTING USER PROMPT
    prompt = st.chat_input("Enter Task")
    if not prompt:
        sys.exit()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    init_messages = [{"role": "system", "content": SETUP_PROMPT}]
    init_messages.append(
        {"role": "user", "content": prompt},
    )
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=init_messages, temperature=0
    )
    reply = chat.choices[0].message.content
    prompt1 = f"{reply}\n{INSTRUCTION_PROMPT}\nThe current time and date is {now}"

    init_messages.append(
        {"role": "system", "content": prompt1},
    )
    init_messages.append(
        {
            "role": "user",
            "content": "Determine which next command to use, and respond using the format specified above:",
        }
    )
    init_chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=init_messages, temperature=0
    )
    init_reply = json.loads(
        init_chat.choices[0].message.content, strict=False
    )  # converting response to json
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in init_reply["thoughts"]["text"]:
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
            messages = [
                {
                    "role": "system",
                    "content": prompt1
                    + "\n"
                    + "This reminds you of these events from your past:\nI was created and nothing new has happened.",
                }
            ]
            messages.append(
                {
                    "role": "user",
                    "content": "Determine which next command to use, and respond using the format specified above:",
                }
            )
            messages.append({"role": "assistant", "content": json.dumps(reply)})
            messages.append(
                {
                    "role": "system",
                    "content": f"Command {reply['command']['name']} returned: "
                    + result,
                }
            )
            messages.append(
                {
                    "role": "user",
                    "content": "Determine which next command to use, and respond using the format specified above:",
                }
            )
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages, temperature=0
            )
            reply = json.loads(chat.choices[0].message.content, strict=False)
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                for response in reply["thoughts"]["text"]:
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


if __name__ == "__main__":
    main()
