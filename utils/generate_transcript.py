from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled


def fetch_video_transcript(video_id):
    try:
        fetched_transcript = YouTubeTranscriptApi().fetch(video_id, languages=['en'])
        transcript_list = fetched_transcript.to_raw_data()
        transcript = " ".join(chunk["text"] for chunk in transcript_list)
        return transcript
    
    except TranscriptsDisabled:
        return None
    except Exception as e:
        raise RuntimeError(f"Transcript fetch failed: {e}")