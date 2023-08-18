# pylint: disable=line-too-long

import streamlit as st
from dotenv import load_dotenv
from langchain import SerpAPIWrapper
from langchain.agents import Tool, initialize_agent
from langchain.chains import RetrievalQA
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from PIL import Image
from streamlit_chat import message

load_dotenv('.env')

from constants import BOTO3, COMPANY_NAME, PERSIST_DIRECTORY_BOTO3_DB, PERSIST_DIRECTORY_COMPANY_DB


def create_agent():
    llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", verbose=True)

    # load from disk
    vectordb_boto3 = Chroma(
        persist_directory=PERSIST_DIRECTORY_BOTO3_DB,
        embedding_function=OpenAIEmbeddings(),
    )

    # retrieval qa chain
    qa_chain_boto3 = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectordb_boto3.as_retriever(search_kwargs={"k": 4}),
    )

    # load from disk
    vectordb_cyberark = Chroma(
        persist_directory=PERSIST_DIRECTORY_COMPANY_DB,
        embedding_function=OpenAIEmbeddings(),
    )

    # retrieval qa chain
    qa_cyberark = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectordb_cyberark.as_retriever(search_kwargs={"k": 4}),
    )

    # conversational memory
    conversational_memory = ConversationBufferWindowMemory(
        memory_key="chat_history",
        k=5,
        return_messages=True,
    )

    search = SerpAPIWrapper()

    tools = [
        Tool(
            name=f'{BOTO3.capitalize()} Knowledge Base',
            func=qa_chain_boto3.run,
            description=f'useful for when you need to answer questions about {BOTO3.capitalize()} documentation. Input should be a fully formed question.',
        ),
        Tool(
            name=f'{COMPANY_NAME.capitalize()} Knowledge Base',
            func=qa_cyberark.run,
            description=f'useful for when you need to answer questions about {COMPANY_NAME.capitalize()} documentation. Input should be a fully formed question.',
        ),
        Tool(
            name="Search",
            func=search.run,
            description="Useful for searching the web",
        ),
    ]

    return initialize_agent(
        agent="chat-conversational-react-description",
        tools=tools,
        llm=llm,
        verbose=True,
        max_iterations=3,
        early_stopping_method="generate",
        memory=conversational_memory,
    )


def main():

    agent = create_agent()

    st.subheader("Chatbot with Langchain, ChatGPT, Chroma DB, and Streamlit")

    image = Image.open('images/chatbot_architecture.png')

    st.image(
        image,
        caption="Chatbot Architecture",
        use_column_width=True,
    )

    if "responses" not in st.session_state:
        st.session_state["responses"] = ["How can I assist you?"]

    if "requests" not in st.session_state:
        st.session_state["requests"] = []

    # container for chat history
    response_container = st.container()
    # container for text box
    textcontainer = st.container()

    with textcontainer:
        query = st.text_input("Query: ", key="input")
        if query:
            result = agent(query)
            st.session_state.requests.append(query)

            st.session_state.responses.append(result["output"])

    with response_container:
        if st.session_state["responses"]:
            for i in range(len(st.session_state["responses"])):
                message(st.session_state["responses"][i], key=str(i))
                if i < len(st.session_state["requests"]):
                    message(st.session_state["requests"][i], is_user=True, key=str(i) + "_user")


if __name__ == "__main__":
    main()
