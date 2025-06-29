import sys
import os
import logging
from typing import List, Optional

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.tools import tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_functions_agent

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from transcribe import (
    transcribe_youtube_videos,
)
from news import search_news
from llm import LLM
from transcribe_local_video import (
    extract_audio_from_video,
    transcribe_audio_to_text,
    get_local_file,
)


from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model_name = os.getenv("CONVERSATION_MODEL", "llama2")
FILES_FOLDER_PATH = "files"


@tool
def transcribe_local_video_tool(video_path: str, language="en-US") -> str:
    """
    This tool takes a local video file path as input and generates a full transcription of the video's content.

    This tool takes a local video file path as input and generates a full transcription of the video's content.
    It processes the video to extract spoken text and returns it as plain text. If the transcription fails
    or the input URL is invalid, an appropriate error message or fallback response is returned.

    Args:
        video_path (str): The path to the local video file to be transcribed. This should be a valid and accessible file path.
        language (str): The language of the audio in the video. Default is 'en-US' (Portuguese - Brazil).

    Returns:
        str: Return only the plain text of the video's transcription
    """
    try:
        print("🎧 Transcribing local video...")
        normalized_video_path = get_local_file(video_path)

        audio_path = os.path.join(FILES_FOLDER_PATH, "audio.wav")
        text_path = os.path.join(FILES_FOLDER_PATH, "transcription.txt")
        extract_audio_from_video(normalized_video_path, audio_path)
        transcribe_audio_to_text(audio_path, text_path, language=language)

        with open(text_path, "r", encoding="utf-8") as f:
            transcription = f.read()
        if not transcription:
            raise ValueError("Empty transcription received")
        print("✅ Transcription completed successfully.")
        return transcription
    except Exception as e:
        logger.error(f"Error in transcribe_tool: {e}")
        return "I don't know"


@tool
def transcribe_tool(url: str) -> str:
    """
    This tool takes a YouTube video URL as input and generates a full transcription of the video's content.

    This tool takes a YouTube video URL as input and generates a full transcription of the video's content.
    It processes the video to extract spoken text and returns it as plain text. If the transcription fails
    or the input URL is invalid, an appropriate error message or fallback response is returned.

    Args:
        url (str): The URL of the YouTube video to be transcribed. This should be a valid and accessible YouTube video link.

    Returns:
        str: Return only the plain text of the video's transcription
    """
    try:
        print("🎧 Transcribing video...")
        transcription = transcribe_youtube_videos(url, FILES_FOLDER_PATH)
        if not transcription:
            raise ValueError("Empty transcription received")
        print("✅ Transcription completed successfully.")
        return transcription
    except Exception as e:
        logger.error(f"Error in transcribe_tool: {e}")
        return "I don't know"


@tool
def summarize_tool(transcription: str) -> str:
    """
    Summarizes the provided video transcription concisely.

    This tool takes a video transcription as input and generates a concise summary using bullet points.
    The summary focuses on the key points and main ideas conveyed in the transcription, ensuring clarity
    and brevity.

    Args:
        transcription (str): The full transcription of the video to be summarized.
                             This should be a plain text representation of the video's content.

    Returns:
        str: A concise summary of the video transcription. If the transcription is empty or invalid, an
             appropriate error message or fallback response is returned.
    """
    try:
        if not transcription.strip():
            raise ValueError("No transcription provided")
        llm = LLM.load_ollama_model(model_name, temperature=0.5)
        messages = [
            SystemMessage(
                content="""
                Summarize the following video transcription concisely using bullet points:
                - A complete overview of the video's main subject.
                - A list of the primary themes covered in the video, with each bullet point containing a short explanation of the theme.
                - A final concluding bullet point that encapsulates the overall message or takeaway of the video.
                """
            ),
            HumanMessage(content=f"Transcription: {transcription}"),
        ]
        print("📝 Summarizing transcription...")
        summary = llm.invoke(messages)
        print("✅ Summary completed successfully.")
        return summary if summary else "I don't know"
    except Exception as e:
        logger.error(f"Error in summarize_tool: {e}")
        return "I don't know"


@tool
def search_news_tools(text: str, max_results: Optional[int] = None) -> List[dict]:
    """
    Searches for news articles related to the provided text.

    This tool extracts relevant keywords from the input text and uses them to query a news search engine.
    The keywords are generated by analyzing the text for technologies, tools, concepts, companies, or topics,
    and translating them into English. The tool ensures that only meaningful keywords are used by excluding
    verbs and generic words. The keywords are formatted as a lowercase, 'OR'-separated string.

    Args:
        text (str): The input text to analyze and extract keywords from. This text should describe the topic
                    or context for which related news articles are being searched.
        max_results (Optional[int]): The maximum number of news articles to return. If not provided, a default
                                     number of results will be returned.

    Returns:
        List[dict]: A list of dictionaries, where each dictionary represents a news article. Each dictionary
                    contains details such as the title, URL, and a brief description of the article.
    """
    try:
        if not text.strip():
            raise ValueError("No text provided")
        llm = LLM.load_ollama_model(model_name, temperature=0)

        message = [
            SystemMessage(
                content="""
                Extract up to 10 highly relevant keywords from the text below.
                Focus on names of technologies, tools, concepts, companies, or topics.
                Do not include verbs or generic words.
                Translate the keywords into English.
                Return ONLY a plain string of keywords in all lowercase, separated by 'OR'. Do not include any additional text, explanations, or formatting.
                Example Output: keyword1 OR keyword2 OR keyword3 OR keyword4 OR keyword5
                """
            ),
            HumanMessage(content=f"text: {text}"),
        ]

        print("🔑 Extracting keywords...")
        keywords = llm.invoke(message)
        print(f"🔠 Keywords extracted: {keywords.content}")
        print("🔍 Searching for news articles...")
        articles = search_news(query=keywords.content, max_results=max_results)
        print("✅ News search completed successfully.")
        return articles

    except Exception as e:
        logger.error(f"Error in search_news_tools: {e}")
        return []


@tool
def save_tool(response: str) -> None:
    """
    Saves the response to a file.

    This tool takes a response string as input and saves it to a file named 'agent_output.md'.
    The file is created in the current working directory, and if it already exists, it will be overwritten.

    Args:
        response (str): The response string to be saved to the file.

    Returns:
        None
    """
    try:
        with open("agent_output.md", "w") as f:
            f.write(response)
        print("✅ Response saved successfully.")
    except Exception as e:
        logger.error(f"Error in save_response: {e}")


toolkit = [
    transcribe_tool,
    transcribe_local_video_tool,
    summarize_tool,
    search_news_tools,
    save_tool,
]


def run_agent(user_prompt: str) -> None:
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are an AI assistant.
                Use your tools to complete the following task.
                You have access to the following tools: transcribe, summarize, search_news, save.
                You should response in markdown format.
                """,
            ),
            MessagesPlaceholder("history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

    agent_llm = LLM.load_open_ai_model(temperature=0)
    agent = create_openai_functions_agent(agent_llm, toolkit, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=toolkit, verbose=True)

    text_input = [user_prompt]
    response = agent_executor.invoke({"input": text_input})
    print(response["output"])


if __name__ == "__main__":
    print("Bem-vindo ao chat! Digite 'sair' para encerrar.")

    while True:
        prompt = input("Você: ")
        if prompt.lower() in ["sair", "exit", "quit"]:
            print("Chat encerrado. Até mais!")
            break

        run_agent(prompt)
