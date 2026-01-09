import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Gen AI Chatbot Workshop", page_icon="🤖", layout="centered")

st.title("🤖 Gen AI Chatbot")
st.caption("A training workshop demo powered by OpenAI")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with st.sidebar:
    st.header("Settings")
    
    model = st.selectbox(
        "Model",
        ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
        index=0
    )
    
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Higher values make output more random, lower values more deterministic"
    )
    
    max_tokens = st.slider(
        "Max Tokens",
        min_value=100,
        max_value=4000,
        value=1000,
        step=100,
        help="Maximum length of the response"
    )
    
    system_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful assistant.",
        height=100,
        help="Instructions that define the chatbot's behavior"
    )
    
    if st.button("Clear Chat History", type="secondary"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            messages_for_api = [{"role": "system", "content": system_prompt}]
            messages_for_api.extend(st.session_state.messages)
            
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model=model,
                    messages=messages_for_api,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            
            assistant_message = response.choices[0].message.content
            st.markdown(assistant_message)
            st.session_state.messages.append({"role": "assistant", "content": assistant_message})
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

with st.expander("ℹ️ About this Demo"):
    st.markdown("""
    **Workshop Demo Features:**
    - Adjustable model parameters (temperature, max tokens)
    - Customizable system prompt
    - Chat history management
    
    **How to use:**
    1. Configure settings in the sidebar
    2. Type your message in the input box
    3. Wait for the AI response
    """)