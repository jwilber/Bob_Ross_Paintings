# Bob_Ross_Paintings

This repo stores data from [the paintings of Bob Ross](https://www.twoinchbrush.com/all-paintings) featured in the TV Show 'The Joy of Painting':

![Bob Ross Image](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS117A8XFP17_8SGyMZ_k8ne_nS1Ls0nqXagUc_F2lgbxilRYZqQQ&s)

 
The following data is provided in this repo:

## data/bob_ross_paintings.csv

Csv file containing metadata for each painting.

| Column | Description | Data Type |
|---|---|---|
| `painting_index` | Painting number as enumerated in collection. | number |
| `img_src` | Url path to image. | text |
| `painting_title` |  Title of the painting. | text |
| `season` | Season of 'The Joy of Painting' in which the painting was featured. | number |
| `episode` | Episode of 'The Joy of Painting' in which the painting was featured. | number |
| `num_colors` | Number of unique colors used in the painting. | number |
| `youtube_src` | Youtube video of episode featuring the painting. | text |
| `colors` | List of colors used in the painting. | list |
| `colors_hex` | List of colors (hexadecimal code) used in the painting. | list |


## data/paintings/

Directory with a `png` image for each painting.


## scripts/get_bob_ross_paintings.py

Python script used to scrape the paintings.

Example use:

```
# call without arguments
$ python get_bob_ross_paintings.py

# call with arguments
$ python get_bob_ross_paintings.py  --csv_name bobross.csv --verbose 1
```


## scripts/dl_images.sh

Shell script that, when run, will download a `png` for each painting and save it in `data/paintings/`.

Example use:

```
# call without arguments
$ bash dl_images.sh
```
