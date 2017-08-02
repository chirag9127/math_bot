from search.youtube_search import YouTubeSearcher


if __name__ == '__main__':
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
