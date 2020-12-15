from datetime import datetime, timedelta
from apiclient.discovery import build


class YouTubeAPI(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.youtube_api = build('youtube', 'v3', developerKey=api_key)

    @staticmethod
    def get_date_for_last_days(days: int = 7) -> datetime:
        date_for_last_days = datetime.today() - timedelta(days=days)
        return date_for_last_days

    def find_videos(self,
                    search_term: str,
                    uploaded_in_last_days: int = 7,
                    max_results: int = 50) -> dict:
        uploaded_since = self.get_date_for_last_days(uploaded_in_last_days)  # Last 7 days

        search_results = self.youtube_api.search().list(
            q=search_term,
            part='snippet',
            type='video',
            order='viewCount',
            maxResults=max_results,
            publishedAfter=uploaded_since.strftime('%Y-%m-%dT%H:%M:%SZ')
        ).execute()
        return search_results

    def get_views_count_by_video_id(self, video_id: str) -> int:
        video_statistics = self.youtube_api.videos().list(id=video_id, part='statistics').execute()
        view_count = int(video_statistics['items'][0]['statistics']['viewCount'])
        return view_count

    def get_channel_name_by_channel_id(self, channel_id: str) -> str:
        channel_name = self.youtube_api.channels().list(
            id=channel_id,
            part='brandingSettings'
        ).execute()['items'][0]['brandingSettings']['channel']['title']
        return channel_name

    def get_subscribers_count_by_channel_id(self, channel_id: str, default_value: int = 1_000_000) -> int:
        subs_search = self.youtube_api.channels().list(id=channel_id, part='statistics').execute()
        if subs_search['items'][0]['statistics']['hiddenSubscriberCount']:
            num_subscribers = default_value
        else:
            num_subscribers = int(subs_search['items'][0]['statistics']['subscriberCount'])
        return num_subscribers
