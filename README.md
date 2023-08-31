# Nearest-Neighbor Recommender Documentation

## Introduction:

This is a linear euclidean distance nearest-neighbor implementation for finding businesses which are most similar to any given client’s businesses. This will be used to provide a front-end display for clients to compare their waste-generation to other clients.

## Project Structure:

*Pipeline.ipynb* is a jupyter notebook used mainly for experimentation and research during development. It is included in the structure only for future iterative development. 

The *Data* folder contains two .csv files, *distances.csv* which holds the calculated euclidean distances between all businesses, and *List_B2B* which holds the relevant data of all B2B clients. Namely, this holds used data like the number of employees, the waste streams, the sector which the clients work in and the number of serviced facilities.

*Distances.csv* is generated during script execution, and contains a “distance” score between two different organizations, the lower the number the more similar the businesses are.

For example:

| , | from | to | distance |
| ----------- | ----------- | ----------- | ----------- |
| 0 | Diana Shipping | HOWDEN | 2.265509404818966 |

So the distance between “Diana Shipping” and “Howden” is around 2.27. This means that the two businesses are somewhat dissimilar. A distance of 0 means that the two organizations are identical.

The *main.py* python script is used for running the algorithm. 

## Technical Details:
The algorithm applied was linear nearest-neighbor search. It is a euclidean distance-based algorithm, which works effectively for the relatively small dataset. Later on this can be changed for some probabilistic model if the calculations ever become too time-prohibitive.

## Quick Start

For help with the script, execute

```console
foo@bar:~$ python3 main.py -h
```

To use the script, execute

```console
foo@bar:~$ main.py -c <recalculate distance matrix T/F> -b <business name> -n <number of similar businesses>
```

Specifying True for the -c parameter does the data processing and euclidean calculations again, outputting a new distances.csv file. This is good for when new data is introduced and the calculations must be done again. Specifying False skips this step.

-b accepts a string input business name, which is used to look up the distance on distances.csv. No identifying keys were used since they will most likely not work with the systems currently in place, though this is usually not a good implementation.

-n an integer specifying how many most similar businesses to return. Must be length - 2 of the available dataset.

##Main.py

Data Loading and Processing:

###complete_pipeline()

This function specifies the three steps of loading, cleaning and preprocessing the data. Each of these steps has its own function.

###load_in_dataset()

Loads the csv files into pandas Dataframes.

###process_data()

This step takes in the primary dataframe and transforms the String type waste streams of the “MATERIAL GROUP” column into lists. Next, it combines and counts the individual occurrences of each waste stream. Waste streams that have appeared less than once are discarded from the data as they would lead to excess dimensionality, making the calculations unreliable. Then, the numeric data is linearly scaled to values between 0 and 1. The categorical “MATERIAL GROUP” and “SECTOR” variables are one-hot-encoded, meaning that they have been transformed into a binary format. The columns which are no longer useful in the data are dropped. Finally, find_similar(pd Dataframe df1) is called on the dataframe to calculate the euclidean feature distances between each pairwise combination of the businesses. The distances are saved in a csv in the project domain.

Next, find_n_similar(String business, Int n) is called. This takes in our business of choice represented as a string, and from the distances.csv, finds the top n businesses with the lowest distances. This can then be returned as output of any sort. Currently it prints out the dataframe and returns the top n businesses, though this can be easily adjusted to save this information somewhere.


