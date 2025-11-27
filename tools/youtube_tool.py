import os
from googleapiclient.discovery import build

def search_youtube(query: str):
    """
    Searches YouTube for videos matching the query.
    """
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        return "Error: YOUTUBE_API_KEY not found."
        
    try:
        youtube = build("youtube", "v3", developerKey=api_key)
        request = youtube.search().list(
            part="snippet",
            maxResults=5,
            q=query,
            type="video"
        )
        response = request.execute()
        
        results = []
        for item in response.get("items", []):
            title = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            url = f"https://www.youtube.com/watch?v={video_id}"
            results.append(f"Title: {title}\nLink: {url}\n")
            
        return "\n".join(results) if results else "No videos found."
        return "\n".join(results) if results else "No videos found."
    except Exception as e:
        print(f"CRITICAL ERROR in search_youtube: {e}") # Print to stdout for terminal visibility
        return f"Error searching YouTube: {str(e)}"

def summarize_video(video_url: str):
    """
    Summarizes a YouTube video using Gemini's multimodal capabilities.
    """
    return f"Please watch and summarize this video: {video_url}"
