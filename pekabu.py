import streamlit as st
import requests
from datetime import datetime, timedelta

# YouTube API Key
API_KEY = "YOUR_API_KEY_HERE"

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"

# Streamlit App Title
st.title("YouTube Viral Topics Tool")

# Fixed Days to 15
DAYS = 15

# List of broader keywords
keywords = [
    "Chosen Ones", "Spiritual Awakening", "Spiritual Growth", "Manifestation", 
    "Law of Attraction", "Higher Consciousness", "Third Eye Awakening", "Energy Shift"
]

# Fetch Data Button
if st.button("Fetch Data"):
    try:
        # Calculate start date (15 days ago)
        start_date = (datetime.utcnow() - timedelta(days=DAYS)).isoformat("T") + "Z"
        all_results = []

        # Iterate over the list of keywords
        for keyword in keywords:
            st.write(f"Searching for keyword: {keyword}")
            
            search_params = {
                "part": "snippet",
                "q": keyword,
                "type": "video",
                "order": "viewCount",
                "publishedAfter": start_date,
                "maxResults": 10,
                "key": API_KEY,
            }

            response = requests.get(YOUTUBE_SEARCH_URL, params=search_params)
            data = response.json()
            
            if "items" not in data or not data["items"]:
                st.warning(f"No videos found for keyword: {keyword}")
                continue
            
            videos = data["items"]
            video_ids = [video["id"]["videoId"] for video in videos]
            
            if not video_ids:
                continue
            
            # Fetch video statistics
            stats_params = {"part": "statistics", "id": ",".join(video_ids), "key": API_KEY}
            stats_response = requests.get(YOUTUBE_VIDEO_URL, params=stats_params)
            stats_data = stats_response.json()
            
            if "items" not in stats_data:
                continue
            
            for video, stat in zip(videos, stats_data["items"]):
                title = video["snippet"].get("title", "N/A")
                description = video["snippet"].get("description", "")[:200]
                video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
                views = int(stat["statistics"].get("viewCount", 0))
                
                # Filter videos with more than 50,000 views
                if views >= 50000:
                    all_results.append({
                        "Title": title,
                        "Description": description,
                        "URL": video_url,
                        "Views": views
                    })
        
        # Display results
        if all_results:
            st.success(f"Found {len(all_results)} results with 50,000+ views!")
            for result in all_results:
                st.markdown(
                    f"**Title:** {result['Title']}  \n"
                    f"**Description:** {result['Description']}  \n"
                    f"**URL:** [Watch Video]({result['URL']})  \n"
                    f"**Views:** {result['Views']}"
                )
                st.write("---")
        else:
            st.warning("No videos found with more than 50,000 views in the last 15 days.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
