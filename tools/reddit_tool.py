import requests
from bs4 import BeautifulSoup

def scrape_reddit(query: str):
    """
    Searches Reddit for the query and returns post titles and content using JSON API.
    """
    # Search URL for reddit
    search_url = f"https://www.reddit.com/search.json?q={query}&sort=relevance&t=all"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(search_url, headers=headers)
        if response.status_code != 200:
            return f"Error scraping Reddit: Status {response.status_code}"
            
        data = response.json()
        posts = []
        
        # Navigate the JSON structure
        if 'data' in data and 'children' in data['data']:
            for child in data['data']['children'][:5]: # Top 5 posts
                post = child['data']
                title = post.get('title', 'No Title')
                selftext = post.get('selftext', '')[:200] + "..." if post.get('selftext') else ""
                url = post.get('url', '')
                posts.append(f"Title: {title}\nSummary: {selftext}\nLink: {url}\n")
                
        return "\n".join(posts) if posts else "No posts found."
    except Exception as e:
        return f"Error scraping Reddit: {str(e)}"
