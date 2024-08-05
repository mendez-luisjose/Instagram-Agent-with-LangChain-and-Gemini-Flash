import streamlit as st

st.set_page_config(page_title="Instagram Agent 📷", page_icon="📸", layout="wide", initial_sidebar_state="expanded")

if "agent" not in st.session_state :
    st.session_state.agent = None  

if "ig" not in st.session_state :
    st.session_state.ig = None  

if "api_url_endpoint" not in st.session_state :
    st.session_state.api_url_endpoint = None 

if "instagram_user" not in st.session_state :
    st.session_state.instagram_user = None  

if "instagram_password" not in st.session_state :
    st.session_state.instagram_password = None   

from langchain_core.messages import AIMessage, HumanMessage
#from prompts import JJ_MESSAGE
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from audio_recorder_streamlit import audio_recorder
import time
from utils import speech_to_text
from template import AGENT_MESSAGE
import os

#agent = initialize_agent(tools=music_player_tools)

if "chat_history" not in st.session_state :
    st.session_state.chat_history = [AIMessage(content=AGENT_MESSAGE)]


def get_agent_response(user_query) :
    st_callback = StreamlitCallbackHandler(st.container())
    result = st.session_state.agent.invoke(
        {"input": user_query}, config={"configurable": {"session_id": "<foo>"}, "callbacks": [st_callback]})
    result = result["output"]
    return result

def main() :
    st.title("📸 Instagram Agent with LangChain")
    st.write("This is an Instagram Agent Built with LangChain, is Powered by using the Gemini-Pro LLM. This IG Agent can Automatically Create and Publish Instagram Posts and Storys about any Topic, also It can Changes the Notes, Biography and the Picture of the Profile from the User.")
    st.success("🛠️ Set the Credentials of your Instagram Account in the Sidebar")
    st.markdown("<hr/>", unsafe_allow_html=True)

    with st.sidebar:
        st.sidebar.markdown('''
            🧑🏻‍💻 Created by [Luis Jose Mendez](https://github.com/mendez-luisjose)
            ''')

        st.markdown("---------")
        st.title("🦜 Instagram with LangChain")
        st.subheader("🤖 Powered by Gemini-Pro, LangChain and Instagram")
        st.markdown("---------")

        st.write(
            """
            Start Talking with the Instagram LangChain Agent. \n
            """
        )

        st.info("This Agent can Automatically creates Posts, Captions and Storys.")

        st.markdown("---------")

        st.warning("🛠️ Set the Credentials of your Instagram Account")


        instagram_user = st.text_input("Instagram User Account")
        api_url_endpoint = st.text_input("API URL Endpoint")
        
        if (instagram_user != None and instagram_user != "" and api_url_endpoint != None and api_url_endpoint != "") :

            instagram_password = st.text_input("Instagram Password Account", type="password")
            st.session_state.api_url_endpoint = api_url_endpoint
            
            if (instagram_password != None and instagram_password != "") :

                st.session_state.instagram_user = instagram_user
                st.session_state.instagram_password = instagram_password
                st.session_state.ig = True

                from ai_agent import initialize_agent
                from ai_tools import ig_tools

                agent = initialize_agent(tools=ig_tools)

                st.session_state.agent = agent
                
                st.success("✅ Instagram Account was Activated Successfully")
            
                st.markdown("---------")

                chat_with_voice = st.checkbox("Talk with your Voice 🎙️", value=False)
                st.warning("Speak very Clearly to the Microphone. To Record your Voice press the Microphone Icon.")

                if chat_with_voice :
                    footer_container = st.container()
                    with footer_container:
                        audio_bytes = audio_recorder(text="🔊 Activate Microphone", icon_size="2x")
                        
                        if (audio_bytes != None) and (chat_with_voice) :
                            with st.spinner("Transcribing..."):
                                webm_file_path = "./temp/temp_audio.mp3"
                                with open(webm_file_path, "wb") as f:
                                    f.write(audio_bytes)

                                transcript = speech_to_text(webm_file_path)
                                if transcript!="Error" and transcript!= None:
                                    st.session_state.speech_to_text_history.append(transcript)
                                    os.remove(webm_file_path)

                elif chat_with_voice!=True :
                    st.session_state.speech_to_text_history = []
        else :
            st.session_state.ig = None

        st.markdown("---------")

        st.write(
            """
            Press the Following Button to Restart your Session:
            """
        )
        _, col, _ = st.columns([1, 1, 1])
        if col.button("🗑️ Restart Session", type="primary") :
            del st.session_state["ig"]
            del st.session_state["api_url_endpoint"]
            del st.session_state["instagram_user"]
            del st.session_state["instagram_password"]
            del st.session_state["agent"]
            st.rerun()

            
    if (st.session_state.ig != None) : 
        for message in st.session_state.chat_history :
            if isinstance(message, HumanMessage) :
                with st.chat_message("user") :
                    st.markdown(message.content)
            else :
                with st.chat_message("assistant") :
                    st.markdown(message.content)

        user_query = st.chat_input("Type your message here...")
            
        if (user_query is not None and user_query != "") and (chat_with_voice!=True):
            st.session_state.chat_history.append(HumanMessage(content=user_query))
        
            with st.chat_message("user") :
                st.markdown(user_query)

            with st.chat_message("assistant") :
                ai_response = get_agent_response(user_query)
                message_placeholder = st.empty()
                full_response = ""
                # Simulate a streaming response with a slight delay
                for chunk in ai_response.split():
                    full_response += chunk + " "
                    time.sleep(0.05)

                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")
                
                # Display the full response
                message_placeholder.info(full_response)

            st.session_state.chat_history.append(AIMessage(content=ai_response))
        elif (chat_with_voice) and (len(st.session_state.speech_to_text_history) > 0):
            user_query = st.session_state.speech_to_text_history[-1]
            st.session_state.chat_history.append(HumanMessage(content=user_query))
        
            with st.chat_message("user") :
                st.markdown(user_query)

            with st.chat_message("assistant") :
                ai_response = get_agent_response(user_query)
                message_placeholder = st.empty()
                full_response = ""
                # Simulate a streaming response with a slight delay
                for chunk in ai_response.split():
                    full_response += chunk + " "
                    time.sleep(0.05)

                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")
                
                # Display the full response
                message_placeholder.info(full_response)

            st.session_state.chat_history.append(AIMessage(content=ai_response))

if __name__ == "__main__" :
    main()