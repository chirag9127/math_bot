import json
import os
import requests

from apiclient.discovery import build


DEVELOPER_KEY = os.environ['YOUTUBE_DEVELOPER_KEY']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
DEEP_RELEVANCE_MODEL_SERVICE = os.environ['DEEP_RELEVANCE_MODEL_SERVICE']


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


def get_most_relevant_video(query, dl_gk=True):
    # TODO: Build GK service to toggle
    videos = YouTubeSearcher().search_for_videos(query)
    if dl_gk:
        if videos:
            data = {
                "query": [],
                "title": [],
                "description": [],
                "ids": [],
            }
            for video in videos:
                data["query"].append(query)
                data["title"].append(video['title'])
                data["description"].append(video['description'])
                data["ids"].append(video['video_id'])
            json_data = json.dumps(data)
            headers = {
                "Content-Type": "application/json"
            }
            r = requests.post(DEEP_RELEVANCE_MODEL_SERVICE,
                              headers=headers,
                              data=json_data)
            if r.status_code == 200:
                response = r.json()
                preds = response['preds']
                index = 0
                max_prob = 0.0
                for i, item in enumerate(preds):
                    prob = item[0]
                    if prob > max_prob:
                        max_prob = prob
                        index = i
                return data["ids"][index]
    else:
        if videos:
            return videos[0]['video_id']
