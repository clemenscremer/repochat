import streamlit as st
import os
from dotenv import load_dotenv
import datetime
from autogen import ConversableAgent
from autogen.token_count_utils import count_token
import traceback
import time

from config import config_list
from ingest_repo import ingest_repository

# for image support
from PIL import Image
import io
#load_dotenv()

# --------------------------------------------
# initialize autogen 
# --------------------------------------------
def create_agent(system_prompt, filtered_cl):
    return ConversableAgent(
        "chatbot",
        system_message=system_prompt,
        llm_config=filtered_cl[0],
        human_input_mode="NEVER",
    )

def get_reply(agent, messages):
    # Use all messages in the conversation history
    reply = agent.generate_reply(messages=messages)
    if isinstance(reply, str):
        return reply
    else:
        return reply.get("content", "")

# --------------------------------------------
# Helper functions
# --------------------------------------------
def log_message(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log.txt", "a") as file:
        file.write(f"[{timestamp}] {message}\n")

def ingest_repo_safely(repo_path):
    try:
        repo_content = ingest_repository(repo_path, "")
        lines = repo_content.count("\n")
        st.sidebar.write(f"Lines in repo: {lines}")
        return repo_content
    except Exception as e:
        st.sidebar.error(f"Error ingesting repository: {str(e)}")
        return None

def count_tokens(text, model):
    return count_token(text, model)

def estimate_cost(prompt_tokens, completion_tokens, model_config):
    prompt_cost = prompt_tokens * model_config.get('price_per_prompt_token', 0)
    completion_cost = completion_tokens * model_config.get('price_per_completion_token', 0)
    return prompt_cost + completion_cost

def format_usage_summary(prompt_tokens, completion_tokens, cost):
    return (f"Prompt tokens: {prompt_tokens}\n"
            f"Completion tokens: {completion_tokens}\n"
            f"Total tokens: {prompt_tokens + completion_tokens}\n"
            f"Estimated cost: ${cost:.6f}")

# --------------------------------------------
# Streamlit app
# --------------------------------------------
def main():
    load_dotenv()

    # Sidebar
    with st.sidebar:
        user_repo = st.text_input("Folder or GitHub repo", value="./GNN", key="user_repo")

        if st.button("Ingest repo"):
            repo_content = ingest_repo_safely(user_repo)
            if repo_content:
                st.session_state.repo_content = repo_content
                st.session_state.repo_tokens = count_tokens(repo_content, "gpt-3.5-turbo-0613")
                st.sidebar.write(f"Repository tokens: {st.session_state.repo_tokens}")

        model = st.radio("Model", ["Claude-3.5-Haiku", "Claude-3.0-Haiku", "Claude-3.5-Sonnet", "Llama-3.1-8b", "Llama-3.1-70b", "gpt-4o-mini", "gpt-4o"])

        if st.button("Clear messages"):
            st.session_state.messages = []
            st.session_state.repo_content = ""  # Clear repo content
            st.session_state.repo_tokens = 0  # Clear repo tokens
            log_message("Conversation cleared")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "repo_content" not in st.session_state:
        st.session_state.repo_content = ""
    if "repo_tokens" not in st.session_state:
        st.session_state.repo_tokens = 0
    if "agent" not in st.session_state:
        st.session_state.agent = None

    # System prompt
    system_prompt = f"""
    You are a highly skilled python developer and machine learning specialist. 
    Your task is to answer questions based on python code from a repository (repo). 
    The code (.py) of the repo including markdown (.md) and yaml as well as text files will be 
    included after a structure of the entire repo and its folders and files in the information shared with you below. 
    File paths will be included before each snippet following the format: 
    --- ./dummy_repo/src/more.py --- 

    # Repo content 
    {st.session_state.repo_content}
    """

    # Display chat messages
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
        if "response_time" in msg:
            st.text(f"Response time: {msg['response_time']:.2f} seconds")
        if "usage_summary" in msg:
            st.text(msg["usage_summary"])

    # Chat input
    if prompt := st.chat_input():
        start_time = time.time()  # Start timing

        try:
            filter_dict = {"tags": [model]}
            filtered_cl = [config for config in config_list if model in config.get("tags", [])]

            if not filtered_cl:
                st.error(f"No configuration found for model: {model}")
                return

            if st.session_state.agent is None or st.session_state.agent.llm_config != filtered_cl[0]:
                st.session_state.agent = create_agent(system_prompt, filtered_cl)

            # Count tokens for the entire context (system prompt + repo content + conversation history + new prompt)
            context = system_prompt + "\n".join([msg["content"] for msg in st.session_state.messages]) + prompt
            prompt_tokens = count_tokens(context, model)

            messages = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages]
            messages.append({"role": "user", "content": prompt})
            reply = get_reply(st.session_state.agent, messages)

            completion_tokens = count_tokens(reply, model)

            end_time = time.time()  # End timing
            response_time = end_time - start_time

            # Estimate cost
            model_config = filtered_cl[0]
            estimated_cost = estimate_cost(prompt_tokens, completion_tokens, model_config)

            usage_summary = format_usage_summary(prompt_tokens, completion_tokens, estimated_cost)

            st.session_state.messages.append({
                "role": "user", 
                "content": prompt,
            })
            st.chat_message("user").write(prompt)

            st.session_state.messages.append({
                "role": "assistant", 
                "content": reply,
                "response_time": response_time,
                "usage_summary": usage_summary
            })
            st.chat_message("assistant").write(reply)
            st.text(f"Response time: {response_time:.2f} seconds")
            st.text(usage_summary)

            log_message(f"User: {prompt}")
            log_message(f"Assistant: {reply}")
            log_message(f"Response time: {response_time:.2f} seconds")
            log_message(f"Usage summary: {usage_summary}")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.error(traceback.format_exc())
            log_message(f"Error: {str(e)}")

if __name__ == "__main__":
    main()