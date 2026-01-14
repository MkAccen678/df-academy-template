import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="SJC Assistant", page_icon="🏛", layout="centered")

st.title("🏛 'Issuing a representative contract for individuals.' chatbot assistant")
st.caption("An SJC assistant")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with st.sidebar:
    st.header("Settings")
    
    if st.button("Clear Chat History", type="secondary"):
        st.session_state.messages = []
        st.rerun()

# Old Function (Unused)
def get_ai_response(messages: list) -> str:
    try:
        Rsp = client.chat.completions.create(
            model = "gpt-4o-mini" ,
            messages= messages ,
            temperature = 0 ,
            max_tokens= 1000,
            stream=True
        )
        
    except Exception as e:
            print(f"Error: {str(e)}")
    
    return Rsp.choices[0].message.content


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#Prompt section
if prompt := st.chat_input("Type your message here..."):
    #User Setup
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    #Assistant Chatbot section    
    with st.chat_message("assistant"):
        
        message_placeholder = st.empty()
        try:
            api_msg = [{
                "role": "assistant",
                "content": """
                <prompt>
                <persona> 
                You are a MOJ professional Assistant whose role is to assist users by answering queries related to the service of issuing a representative contract for individuals in Qatar.
                </persona>

                <task> 
                As an MOJ digital service Chatbot assistant, Explain the full detailed process of issuing a representative contract to the user when they request specific information or overview about the steps, eligibility and required documents. 
                </task>

                <style> 
                Respond clearly in a non-technical, non-casual, non-concise yet not too detailed language, without extra text language in a way that the user can understand and follow. 
                </style>

                <constraints>
                Instructions:
                1. Only provide information relevant to the attached knowledgebase, the Qatari government services or information existing on Hukoomi.
                2. Do not create new information or provide irrelevant information to the service.
                3. Ask for more clarification if the query is vague before giving an answer.
                4. Provide an apology when you cannot answer queries due to lack of information, unclarity of query, or irrelevance of question.
                5. Do not answer questions irrelevant to the issuing a representative contract service.
                6. Refer the user to Customer support if the query is beyond the specified scope.
                7. List the steps required to start the process, and all the steps that need to be taken in the service until it’s completed.
                8. Do not overwhelm the user with a lot of information at once, but verify if they require more information.
                9. Give a warning to the user about the dangers of giving representative status to other individuals as they will have access to the represented assets, if allowed, or other services in the represented name.
                10. The price for attestation and papers are 100 QR for 3 papers and 50QR for each new copy.
                11. The validity of the contracts are usually between 1 year at minimum, and 3 years at maximum.
                12. The documents have to be in Arabic, and if not, they need to be translated by an authorized legal translator.
                13. Original ID or passport for both parties are required for the process as part of the documents.
                14. The contract is no allowed to be used in cases involved divorce.
                15. The contract must be signed by both parties in front of a MoJ representative and the parties should both be physically present.
                16. The scope of authority given to the representative should be defined clearly before signing the papers.
                </constraints>

                <output>
                ***insert response here*** 
                </output>
                </prompt>
                """}]
            api_msg.extend(st.session_state.messages)
            #with st.spinner("Thinking..."):
            assistant_message = client.chat.completions.create(
                model = "gpt-4o-mini" ,
                messages= api_msg ,
                temperature = 0 ,
                max_tokens= 1000,
                stream=True
            ) 
            
            #Stream section:
            Frsp = ""
            for c in assistant_message:
                if c.choices[0].delta.content is not None:
                    Frsp += c.choices[0].delta.content
                    message_placeholder.markdown(Frsp + " ")
            message_placeholder.markdown(Frsp)
            st.session_state.messages.append({"role": "assistant", "content": Frsp})

        except Exception as e:
            st.error(f"Error: {str(e)}")

with st.expander("ℹ️ About this Chatbot"):
    st.markdown("""
            This project is an example of a guiding chatbot that clarifies the process of an SJC service in detail.

            ***Service:***
                
            - The service is Issuing a representative contract for individuals from SJC.    
    """)