import os

from apiclient.discovery import build


DEVELOPER_KEY = os.environ['YOUTUBE_DEVELOPER_KEY']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


class YouTubeSearcher:

    def __init__(self):
        self._searcher = build(
            YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
            developerKey=DEVELOPER_KEY)

    def search_for_videos(self, query, max_results=10):
        search_response = self._searcher.search().list(
            q=query,
            part="id,snippet",
            maxResults=max_results
        ).execute()

        return self.__extract_videos(search_response)

    def __extract_videos(self, search_response):
        videos = []
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                videos.append(
                    {'title': search_result["snippet"]["title"],
                     'video_id': search_result["id"]["videoId"],
                     'description': search_result["snippet"]["description"]})
        return videos


def get_most_relevant_video(query):
    videos = YouTubeSearcher().search_for_videos(query)
    if videos:
        return videos[0]['video_id']
