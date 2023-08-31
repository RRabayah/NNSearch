### Nearest-Neighbor Recommender Documentation

## Introduction:

This is a linear euclidean distance nearest-neighbor implementation for finding businesses which are most similar to any given client’s businesses. This will be used to provide a front-end display for clients to compare their waste-generation to other clients.

## Project Structure:

*Pipeline.ipynb* is a jupyter notebook used mainly for experimentation and research during development. It is included in the structure only for future iterative development. 

The *Data* folder contains two .csv files, *distances.csv* which holds the calculated euclidean distances between all businesses, and *List_B2B* which holds the relevant data of all B2B clients. Namely, this holds used data like the number of employees, the waste streams, the sector which the clients work in and the number of serviced facilities.

*Distances.csv* is generated during script execution, and contains a “distance” score between two different organizations, the lower the number the more similar the businesses are.

For example:

,from,to,distance
0,Diana Shipping,HOWDEN,2.265509404818966

So the distance between “Diana Shipping” and “Howden” is around 2.27. This means that the two businesses are somewhat dissimilar. A distance of 0 means that the two organizations are identical.

The *main.py* python script is used for running the algorithm. 
