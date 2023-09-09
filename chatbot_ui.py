# pylint: disable=line-too-long

import streamlit as st
from dotenv import load_dotenv
from PIL import Image
from streamlit_chat import message

from agents.agent import create_agent

load_dotenv('.env')

agent = create_agent()


def display_header_and_image():
    """
    Displays the header information for the chatbot and an image.
    """
    st.subheader('Chatbot powered by Langchain, ChatGPT, Chroma DB, and Streamlit')
    image = Image.open('images/chatbot_architecture.png')
    st.image(
        image,
        caption='Chatbot Architecture',
        use_column_width=True,
    )


def initialize_session():
    """
    Initializes or resets session variables.
    """
    if 'responses' not in st.session_state:
        st.session_state['responses'] = ['How can I assist you?']
    if 'requests' not in st.session_state:
        st.session_state['requests'] = []


def display_chat_history():
    """
    Displays the chat history.
    """
    for i, response in enumerate(st.session_state['responses']):
        message(response, key=str(i))
        if i < len(st.session_state['requests']):
            message(st.session_state['requests'][i], is_user=True, key=str(i) + '_user')


def main():
    display_header_and_image()
    initialize_session()
    # container for chat history
    response_container = st.container()
    # container for text box
    textcontainer = st.container()

    with textcontainer:
        query = st.text_input('Prompt: ', placeholder='Enter your prompt here..')
        if query:
            with st.spinner('Generating Response...'):
                result = agent(query)
                st.session_state.requests.append(query)

                st.session_state.responses.append(result['output'])

    with response_container:
        display_chat_history()


if __name__ == '__main__':
    main()
