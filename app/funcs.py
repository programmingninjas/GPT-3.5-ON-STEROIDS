"""
This module includes all functions used by the program.
"""

import time
import json
import wikipedia
import streamlit as st
from serpapi import GoogleSearch
from trafilatura import fetch_url, extract
from consts import (
    SERP_API_KEY,
    encoding,
)


def search_wiki(command) -> str:
    """Searches wikipedia
    Args:
        command: a dictionary containing the query
    Returns:
        str: results returned by wikipedia
    """
    return "Command wikipedia returned: " + wikipedia.summary(command["query"])


def write_to_file(command) -> str:
    """Writes text to a file
    Args:
        command: a dictionary containing the "filename" and "text"
    Returns:
        str: success message
    """
    with open(command["filename"], "w", encoding="utf-8") as file:
        file.write(command["text"])
    return "Command write_to_file returned: File was written successfully"


def append_to_file(command) -> str:
    """Appends text to a file
    Args:
        command: a dictionary containing the "filename" and "text"
    Returns:
        str: success message
    """
    with open(command["filename"], "a", encoding="utf-8") as file:
        file.write(command["text"])
    return "Command append_to_file returned: File was appended successfully"


def read_file(command) -> str:
    """Returns text from a file
    Args:
        command: a dictionary containing the "filename"
    Returns:
        str: text stored in the file
    """
    with open(command["filename"], "r", encoding="utf-8") as file:
        data = file.read()
        return f"Command read_file returned: {data}"


def open_file(command) -> str:
    """Shows a download button on the Streamlit interface to download the file generated by GPT.
    Args:
        command: a dictionary containing the "path" to the file
    Returns:
        str: a success message
    """
    with open(command["path"], "r", encoding="utf-8") as file:
        st.download_button("Open File", file, file_name=command["path"])
    return "Command open_file returned: File was opened successfully"


def browse_website(command) -> str:
    """Browse website and extract main content upto 4000 tokens
    Args:
        command: a dictionary containing "url" to the website
    Returns
        str: the content of that website in json format
    """
    # grab a HTML file to extract data from
    downloaded = fetch_url(command["url"])

    # output main content and comments as plain text
    result = extract(downloaded, output_format="json")

    if len(encoding.encode(str(result))) < 4000:
        return "Command browse_website returned: " + str(result)
    return "Command browse_website returned: " + str(result)[:4000]


def google_tool(command) -> str:
    """Searches google for query and returns upto 4000 tokens of results
    Args:
        command: a dictionary containing "query"
    Returns:
        str: response in json format
    """
    params = {
        "q": str(command["query"]),
        "location": "Delhi,India",
        "first": 1,
        "count": 10,
        "num": 4,
        "api_key": SERP_API_KEY,
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    organic_results = []
    page_count = 0
    page_limit = 1

    while "error" not in results and page_count < page_limit:
        organic_results.extend(results.get("organic_results", []))

        params["first"] += params["count"]
        page_count += 1
        results = search.get_dict()

    response = json.dumps(organic_results, indent=2, ensure_ascii=False)
    if len(encoding.encode(response)) < 4000:
        return "Command google returned: " + response
    return "Command google returned: " + response[:4000]


def type_message(text) -> None:
    """Displays text on the screen with a typewriter effect
    Args:
        text: any string
    Returns:
        None
    """
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in text:
            full_response += response
            time.sleep(0.02)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)