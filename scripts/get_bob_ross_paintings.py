# -*- coding: utf-8 -*-
# author: Jared Wilber
"""get_bob_ross_data.py

This script scrapes twoinchbrush.com for all available Bob Ross paintings from 'The Joy of Painting'.

Example:
    The function may be called from the cli with or without arguments:

        # call without arguments
        $ python get_bob_ross_data.py

        # call with arguments
        $ python get_bob_ross_paintings.py --csv_name bob_ross.csv --verbose 1
"""

import argparse
import re
import requests

import pandas as pd

from bs4 import BeautifulSoup

BASE_URL = "https://www.twoinchbrush.com/all-paintings?page={}"
IMAGE_URL = "https://www.twoinchbrush.com/{}"
INFO_URL = "https://www.twoinchbrush.com/painting/{}"
COLORS = ["Black_Gesso","Bright_Red","Burnt_Umber","Cadmium_Yellow","Dark_Sienna","Indian_Red","Indian_Yellow","Liquid_Black","Liquid_Clear","Midnight_Black","Phthalo_Blue","Phthalo_Green","Prussian_Blue","Sap_Green","Titanium_White","Van_Dyke_Brown","Yellow_Ochre","Alizarin_Crimson"]


def get_youtube_src(result):
    """Extract youtube link."""
    youtube_src = result.find_all('iframe')[0]['src']
    return youtube_src


def get_bob_ross_paintings(csv_name="get_bob_ross_paintings.csv", verbose=1):
    """
    Create dataset of Bob Ross paintings (& associated meta-data).

    Parameters
    ----------
    csv_name: str (default='get_bob_ross_paintings.csv')
        Name of file to save dataframe to. Should end with '.csv'.
    verbose: int (default=1)
        If > 0, print scraping progress.

    Returns
    -------
    all_painting_df: pandas.DataFrame
        DataFrame of Bob Ross paintings with associated meta-data.
    """
    all_paintings = []
    for page_index in range(1, 18):
        page = requests.get(BASE_URL.format(page_index))
        soup = BeautifulSoup(page.content, 'html.parser')

        paintings = soup.find_all('div', class_='bob-ross-painting-holder')

        for painting in paintings:
            season = painting['data-season']
            episode = painting['data-episode']
            sequential = (int(season) - 1) * 13 + int(episode)
            painting_dict = {
                'painting_index': painting['data-id'],
                'img_src': painting['data-img'],
                'painting_title': painting['data-title'],
                'season': season,
                'episode': episode,
                'num_colors': painting['data-colors-count']
            }

            index = painting['data-id']
            info_url = INFO_URL.format(index)
            info_page = requests.get(info_url)
            info_soup = BeautifulSoup(info_page.content, 'html.parser')
            colors = info_soup.find(id='color-list').find_all('li')
            color_names = [color['data-name'] for color in colors]
            color_hexes = [color['data-hex'] for color in colors]

            painting_dict['youtube_src'] = get_youtube_src(info_soup)
            painting_dict['colors'] = [color_names]
            painting_dict['color_hex'] = [color_hexes]

            for color in COLORS:
                painting_dict[color] = 1 if color.replace('_', ' ') in painting_dict['colors'][0] else 0

            if verbose > 0:
                print('collected data from painting {}'.format(index), flush=True)
            # create dataframe from dict
            painting_df = pd.DataFrame(painting_dict, index=[sequential])

            all_paintings.append(painting_df)

    # store all info to single dataframe
    all_painting_df = pd.concat(all_paintings)

    # save results to csv
    all_painting_df.to_csv(csv_name)

    return all_painting_df


def main(csv_name, verbose):
    """Run script conditioned on user-input."""
    print("Collecting Bob Ross paintings", flush=True)
    return get_bob_ross_paintings(csv_name=csv_name, verbose=verbose)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Scrape paintings from Bob Ross."
    )
    parser.add_argument('--csv_name', default='get_bob_ross_paintings.csv',
                        help="Name of csv file to save data to.")
    parser.add_argument('--verbose', type=int, default=1,
                        help="If > 0, print scraping progress..")

    args = vars(parser.parse_args())
    print(args)
    main(**args)
