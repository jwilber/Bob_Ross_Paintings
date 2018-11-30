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

BASE_URL = "https://www.twoinchbrush.com/all-paintings"
IMAGE_URL = "https://www.twoinchbrush.com/{}"
INFO_URL = "https://www.twoinchbrush.com/painting/{}"


def get_youtube_src(result):
    """Extract youtube link."""
    youtube_src = result.find_all('iframe')[0]['src']
    return youtube_src


def get_data_img(result):
    """Extract data-img attribute."""
    data_img = result.find_all('a')[0]['data-img']
    return data_img


def get_painting_number(result):
    """Extract index of painting."""
    data_img = get_data_img(result)
    painting_number = re.search(r'\d+', data_img).group()
    return int(painting_number)


def get_img_src(result):
    """Extract src of image."""
    data_img = get_data_img(result)
    img_src = IMAGE_URL.format(data_img[1:])
    return img_src


def get_painting_title(result):
    """Extract title of painting."""
    painting_title = result.find_all('p')[0].text
    return painting_title


def get_text_nums(result):
    """Extract all text content associated with painting."""
    text_data = result.find_all('p')[1].text
    text_nums = re.findall(r'\d+', text_data)
    return text_nums


def get_season(result):
    """Extract season (of show) in which the painting appeared."""
    text_nums = get_text_nums(result)
    return text_nums[0]


def get_episode(result):
    """Extract episode in which the painting appeared."""
    text_nums = get_text_nums(result)
    return text_nums[1]


def get_num_colors(result):
    """Extract the total number of colors used in painting."""
    text_nums = get_text_nums(result)
    return text_nums[2]


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
    page = requests.get(BASE_URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    paintings = soup.find_all('div', class_='painting-holder')

    for painting in paintings:
        painting_dict = {
            'painting_index': get_painting_number(painting),
            'img_src': get_img_src(painting),
            'painting_title': get_painting_title(painting),
            'season': get_season(painting),
            'episode': get_episode(painting),
            'num_colors': get_num_colors(painting)
        }

        index = get_painting_number(painting)
        info_url = INFO_URL.format(index)
        info_page = requests.get(info_url)
        info_soup = BeautifulSoup(info_page.content, 'html.parser')
        colors = info_soup.find_all('ul', attrs={'class': None})[0].find_all('li')
        color_names = [color.text for color in colors]
        color_hexes = [color['style'].split(': ')[1] for color in colors]

        painting_dict['youtube_src'] = get_youtube_src(info_soup)
        painting_dict['colors'] = [color_names]
        painting_dict['color_hex'] = [color_hexes]
        if verbose > 0:
            print('collected data from painting {}'.format(index))
        # create dataframe from dict
        painting_df = pd.DataFrame(painting_dict, index=[0])

        all_paintings.append(painting_df)

    # store all info to single dataframe
    all_painting_df = pd.concat(all_paintings)

    # save results to csv
    all_painting_df.to_csv(csv_name)

    return all_painting_df


def main(csv_name, verbose):
    """Run script conditioned on user-input."""
    print("Collecting Bob Ross paintings")
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
