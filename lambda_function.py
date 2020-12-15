"""
This module imports and calls the function to execute the API call
and print results to the console.
"""

import video_finder as vf


def lambda_handler(event, context):
    return vf.search_each_term(
        search_terms=event['search_terms'],
        uploaded_in_last_days=event['uploaded_in_last_days'],
        max_results=event['max_results'],
        views_threshold=event['views_threshold'],
        num_to_print=event['num_to_print']
    )


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Defining search parameters')
    parser.add_argument('search_terms', type=str, nargs='+',
                        help='The terms to query. Can be multiple.')
    parser.add_argument('--search-period', type=int, default=7,
                        help='The number of days to search for.')
    args = parser.parse_args()

    print(lambda_handler(
        {
            "search_terms": args.search_terms,
            "uploaded_in_last_days": args.search_period,
            "max_results": 50,
            "views_threshold": 5000,
            "num_to_print": 5,
        },
        None
    ))
