import re
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_chroma import Chroma

def extract_video_id(url: str) -> str | None:
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def video_already_indexed(vectorstore: Chroma, video_id: str):
    """Check this video id is already has chunks in ChromaDB."""
    results = vectorstore.get(where={"video_id": video_id}, limit=1)
    return len(results['ids']) > 0

def fetch_transcript(vector_store: Chroma, video_id: str) -> str:
    try:
        if video_already_indexed(vector_store, video_id):
            return "exist"
        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(video_id, languages=['en'])
        transcript_list = fetched_transcript.to_raw_data()
        transcript = " ".join(chunk["text"] for chunk in transcript_list)
        return transcript.replace("\n", " ").strip()
    except TranscriptsDisabled:
        raise ValueError("Transcripts are disabled for this video")
    except Exception as e:
        raise RuntimeError(f"Transcript fetch failed: {e}")
