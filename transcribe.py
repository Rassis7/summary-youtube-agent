from langchain_community.document_loaders.blob_loaders.youtube_audio import (
    YoutubeAudioLoader,
)
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers.audio import (
    OpenAIWhisperParserLocal,
    # OpenAIWhisperParser
)


def transcribe_youtube_videos(url: str, files_folder_dir: str) -> str:
    loader = GenericLoader(
        YoutubeAudioLoader([url], f"{files_folder_dir}/audio"),
        OpenAIWhisperParserLocal(),
    )

    docs = loader.load()

    transcription = ""
    for doc in docs:
        transcription = transcription + doc.page_content

    return transcription
