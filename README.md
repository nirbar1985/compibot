# Compibot - Company Chatbot powered by Langchain, ChatGPT, Chroma DB, and Streamlit


## Motivation

Given that ChatGPT was trained using data only up to September 2021 and has a context limit of 4K tokens per call to the LLM, we encounter the following constraints:

 - It's not suitable for discussions based on content produced after this date, such as understanding a newly developed API or our company's updated documentation.
- Directly pasting extensive content is restricted due to the context limitation.
## Summary
Place your files of any format into the designated folder. Once there, the data will be processed and integrated into a vector database. You can then interact with the chatbot using the Streamlit web application framework. Notably, the chatbot is also equipped to answer queries based on data that can be sourced from a Google search.

The chatbot's capabilities are backed by an agent that utilizes several tools:

1. Company DB: Enables question-answering derived from the company's database embeddings.
1. Boto3 DB: Designed for question-answering using the provided Boto3 documentation, but can be adapted for other data sources.
1. Google Search Tool: Useful for fetching information from the web.


## Getting Started
Clone the repository, set up the virtual environment, and install the required packages

1. git clone git@github.com:nirbar1985/compibot.git

1. Install dependencies
    ```shell script
    poetry install
    ```

1. Enter virtual env by:
    ```shell script
    poetry shell
    ```

## Store your API keys
- Place your OPENAI_API_KEY into .env file
- Place your SERPAPI_API_KEY into .env file


## Index your documents
- Place the company documentation files into the designated directory inside documents directory
- Place the boto3 documentation files into the docs_boto3 directory inside documents directory
- run once the indexing script: 
    ```
    python indexing.py
    ```
- The vector database is now stored persistently in the "db" directory.



## Troubleshooting 
because a known bug in langchain output parser in some scenarios - 
please paste the following temporarily fix:
```
except Exception as e:
    # If any other exception is raised during parsing, also raise an
    # OutputParserException
    try:
        response = json.loads(text)
        return AgentFinish({"output": response["action_input"]}, text)
    except json.JSONDecodeError:
        # Handle JSON parsing error, if needed
        raise OutputParserException(f"Could not parse LLM output: {text}") from e

```

in this location - 
https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain/agents/conversational_chat/output_parser.py#L50
## Start chatting
Kick of the chatbot by running:
```
streamlit run chatbot.py
```
## Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". Don't forget to give the project a star! Thanks again!

Fork the Project
Create your Feature Branch (git checkout -b feature/AmazingFeature)
Commit your Changes (git commit -m 'Add some AmazingFeature')
Push to the Branch (git push origin feature/AmazingFeature)
Open a Pull Request
(back to top)

License
Distributed under the MIT License. See LICENSE.txt for more information.
