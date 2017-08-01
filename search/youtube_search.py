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


if __name__ == '__main__':
    """
    queries = [
        'Algebra videos',
        'What are some SAT math hacks?',
        'I want to learn to solve complicated equations',
        'What do I need to know about geometry for SAT Math?',
        'Tutorial on slope intercept form of a line',
        'Can you show me a video on how to solve basic equations?',
        'circles videos',
        'Video on solving quadratic equations',
        "Let's study about polygons",
        "How to solve linear equations in two variables?",
        'How to solve complicated SAT Math questions?',
    ]"""
    queries = []
    with open('../misc/queries.txt') as f:
        for line in f:
            queries.append(line.strip())
    with open('../misc/dataset_2.tsv', 'w') as fo:
        fo.write('query\ttitle\tdescription\tid\n')
        for query in queries:
            search_results = YouTubeSearcher().search_for_videos(query)
            for res in search_results:
                fo.write('{0}\t{1}\t{2}\t{3}\n'.format(
                    query, res['title'], res['description'], res['video_id']))
