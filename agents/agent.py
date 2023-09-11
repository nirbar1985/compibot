from langchain import SerpAPIWrapper
from langchain.agents import Tool, initialize_agent
from langchain.chains import RetrievalQA
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from constants import BOTO3, COMPANY_NAME, PERSIST_DIRECTORY_BOTO3_DB, PERSIST_DIRECTORY_COMPANY_DB


def create_agent():
    llm = ChatOpenAI(temperature=0.7, model_name='gpt-3.5-turbo', verbose=True)

    # load from disk
    vectordb_boto3 = Chroma(
        persist_directory=PERSIST_DIRECTORY_BOTO3_DB,
        embedding_function=OpenAIEmbeddings(),
    )

    # retrieval qa chain
    qa_chain_boto3 = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=vectordb_boto3.as_retriever(search_kwargs={'k': 4}),
    )

    # load from disk
    vectordb_company = Chroma(
        persist_directory=PERSIST_DIRECTORY_COMPANY_DB,
        embedding_function=OpenAIEmbeddings(),
    )

    # retrieval qa chain
    qa_company = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=vectordb_company.as_retriever(search_kwargs={'k': 4}),
    )

    # conversational memory
    conversational_memory = ConversationBufferWindowMemory(
        memory_key='chat_history',
        k=5,
        return_messages=True,
    )

    search = SerpAPIWrapper()

    tools = [
        Tool(
            name=f'{BOTO3.capitalize()} Knowledge Base',
            func=qa_chain_boto3.run,
            description=(f'useful for when you need to answer questions about '
                         f'{BOTO3.capitalize()} documentation. Input should be a fully formed question.'),
        ),
        Tool(
            name=f'{COMPANY_NAME.capitalize()} Knowledge Base',
            func=qa_company.run,
            description=(f'useful for when you need to answer questions about '
                         f'{COMPANY_NAME.capitalize()} documentation. Input should be a fully formed question.'),
        ),
        Tool(
            name='Search',
            func=search.run,
            description='Useful for searching the web',
        ),
    ]

    return initialize_agent(
        agent='chat-conversational-react-description',
        tools=tools,
        llm=llm,
        verbose=True,
        max_iterations=3,
        early_stopping_method='generate',
        memory=conversational_memory,
    )
