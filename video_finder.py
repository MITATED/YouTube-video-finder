#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 16:09:52 2020

@author: chrislovejoy & mitated
"""

import os
from datetime import datetime
from typing import List

from models import ResultItem
from youtube_api import YouTubeAPI

yt_driver = YouTubeAPI(os.environ.get('API_KEY', 'default api key'))


def search_each_term(
        search_terms: List[str],
        uploaded_in_last_days: int = 7,
        max_results: int = 50,
        views_threshold: int = 5000,
        num_to_print: int = 5) -> List[ResultItem]:
    items = get_all_results_for_search_terms(search_terms, uploaded_in_last_days, max_results)

    result_items = []
    for item in items:
        views_count = yt_driver.get_views_count_by_video_id(item['id']['videoId'])
        if views_count < views_threshold:
            continue
        subscribers_count = yt_driver.get_subscribers_count_by_channel_id(item['snippet']['channelId'])
        days_since_published = get_days_ago_last_publication(item)
        ratio = get_ratio(views_count, subscribers_count)
        channel_name = yt_driver.get_channel_name_by_channel_id(item['snippet']['channelId'])

        result_item = ResultItem(
            title=item['snippet']['title'],
            video_url=f"https://www.youtube.com/watch?v={item['id']['videoId']}",
            custom_score=custom_score(views_count, ratio, days_since_published),
            views=views_count,
            channel_id=item['snippet']['channelId'],
            channel_name=channel_name,
            num_subscribers=subscribers_count,
            view_subscriber_ratio=ratio,
            channel_url=f"https://www.youtube.com/channel/{item['snippet']['channelId']}"
        )
        result_items += [result_item]
    result_items.sort(reverse=True, key=lambda x: x.custom_score)

    # print("THE TOP VIDEOS OVERALL ARE:")
    # print_top_videos(result_items, num_to_print)
    # print("==========================\n")

    result_items_dict = [i.__dict__ for i in result_items]

    return result_items_dict


def get_all_results_for_search_terms(
        search_terms: List[str],
        uploaded_in_last_days: int = 7,
        max_results: int = 50,
) -> List[dict]:
    items = []
    for search_term in search_terms:
        items += yt_driver.find_videos(
            search_term=search_term,
            uploaded_in_last_days=uploaded_in_last_days,
            max_results=max_results
        )['items']
    return items


def print_top_videos(videos: List[ResultItem], num_to_print: int = 5):
    """Prints top videos to console, with details and link to video."""
    for i, video in enumerate(videos[:num_to_print]):
        title = video.title
        views = video.views
        subs = video.num_subscribers
        link = video.video_url
        print(
            f"Video #{i + 1}:\n"
            f"The video '{title}' has {views} views, from a channel "
            f"with {subs} subscribers and can be viewed here: {link}"
            f"\n"
        )
        print("==========================\n")


def get_custom_score(views_count: int, ratio: float, days_since_published: int) -> float:
    ratio = min(ratio, 5)
    score = (views_count * ratio) / days_since_published
    return score


def get_days_ago_last_publication(item: dict) -> int:
    when_published = item['snippet']['publishedAt']
    when_published_datetime_object = datetime.strptime(when_published, '%Y-%m-%dT%H:%M:%SZ')
    today_date = datetime.today()
    days_since_published = int((today_date - when_published_datetime_object).days)
    if days_since_published == 0:
        days_since_published = 1
    return days_since_published


def get_ratio(views_count: int, subscribers_count: int) -> float:
    if subscribers_count == 0:
        return 0
    ratio = views_count / subscribers_count
    return ratio


def custom_score(views_count: int, ratio: float, days_since_published: int) -> float:
    ratio = min(ratio, 5)
    score = (views_count * ratio) / days_since_published
    return score
