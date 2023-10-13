"""
This is where the program starts
"""
import time
import json
import sys
import openai
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
    type_message,
    ask_gpt,
    get_youtube_transcript,
    getText
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
    "get_youtube_transcript": get_youtube_transcript,
    "type_message": type_message
}


# MAIN
def main():
    """
    Starting point of the program.
    """
    # INITIAL SETUP
    st.title("GPT-3.5 on Steroids")
    openai.api_key = OPENAI_API_KEY

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    #UPLOADING FILE
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file:
        st.write(getText(uploaded_file))

    # GETTING USER PROMPT
    prompt = st.chat_input("Enter Task")
    if not prompt:
        sys.exit()
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    init_messages = [
        {"role": "system", "content": SETUP_PROMPT},
        {"role": "user", "content": prompt},
    ]
    # FIRST REPLY
    reply = ask_gpt(init_messages)

    prompt1 = f"{reply}\n{INSTRUCTION_PROMPT}\nThe current time and date is {now}"
    init_messages += [
        {
            "role": "system",
            "content": prompt1,
        },
        {
            "role": "user",
            "content": "Determine which next command to use, and respond using the \
                format specified above:",
        },
    ]

    # SECOND REPLY
    init_reply = json.loads(ask_gpt(init_messages), strict=False)

    # DISPLAYING THE OUTPUT TO THE USER
    type_message({"text": init_reply["thoughts"]["text"]})

    def execute(reply) -> str:
        """This is a recursive function which lets GPT run tools provided to it when it needs them.
        Args:
            reply: a dictionary which contains information like thoughts and which tool to use
        Returns:
            str: returns "task_completed" after running completely
        """
        if reply["command"]["name"] == "task_complete":
            print("GPT Has done its work.")
            return "task_completed"
        try:
            time.sleep(5)
            result = tools[reply["command"]["name"]](reply["command"]["args"])
            messages = [
                {
                    "role": "system",
                    "content": prompt1
                    + "\n"
                    + "This reminds you of these events from your past:\n\
                        I was created and nothing new has happened.",
                },
                {
                    "role": "user",
                    "content": "Determine which next command to use, \
                        and respond using the format specified above:",
                },
                {"role": "assistant", "content": json.dumps(reply)},
                {
                    "role": "system",
                    "content": f"Command {reply['command']['name']} returned: "
                    + result,
                },
                {
                    "role": "user",
                    "content": "Determine which next command to use, \
                        and respond using the format specified above:",
                },
            ]
            reply = json.loads(ask_gpt(messages), strict=False)
            type_message({"text": reply["thoughts"]["text"]})
            execute(reply)

        except Exception as error:
            type_message({"text": f"Task aborted due to error: {error}"})
            return "task_completed"

    execute(init_reply)


if __name__ == "__main__":
    main()
