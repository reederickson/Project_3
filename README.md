# George Washington University Bootcampspot - Project 3
Created by Breakout Room 1 Members:
- Andrew Kemp
- Bryan Johnson
- Reed Erickson
- Tom Regan

Our Project 3 presentation can be found [here](https://www.canva.com/design/DAF-BdQChmw/yEestTJYNk7lJpt7IPr76g/edit?utm_content=DAF-BdQChmw&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton).

## An overview of the project and its purpose


## How we handled the initial data and cleaning

### Data Cleaning
- Split blood pressure into systolic and diastolic columns, converting them to integers
- The BMI category listed both "Normal" and "Normal Weight" columns; we combined them.
- The Sleep Disorder column uses NULL values. We converted those values to "None" so that the data would be included in any joins.
- The Occupation column had two values, "Salesperson" and "Sales Representative". We discussed, at length, combining these two values based on smaller occurences, but determined these were separate roles and left them as is.

### Database Creation
Since the original CSV had string values for categorical columns, we split those up, replacing them by numerical values from the new tables we had created so that any joins done would be based on numerical primary keys.

## Instructions on how to use and interact with the project
The "Project3.ipynb" file in the repo is everything you will need to interact with our work. An outside script (in the "Setup_and_Organization" folder) is called to create the database and get the data into the current file.



## Ethical considerations made
In our analysis, we used a publicly accessible dataset in which participants were identified solely by "Person_IDs" to maintain anonymity. Due to the lack of racial or cultural descriptors within the dataset, it is challenging to ascertain the presence of any biases inherent in the data. Notably, the majority of occupations represented in the dataset are categorized as white-collar jobs, which typically entail professional, managerial, or administrative roles. This observation underscores a particular demographic focus within the dataset, potentially influencing the generalizability of our findings and warranting caution in their interpretation. Despite these limitations, the availability of such data provides valuable insights into certain aspects of societal trends and behaviors, albeit within specific contexts.

## References for the data source(s)
- We found our initial data set using [Kaggle](https://www.kaggle.com/datasets/uom190346a/sleep-health-and-lifestyle-dataset) can be found in the "Resources" folder.
- Our [project proposal](https://docs.google.com/document/d/1CoOXnwNHr9Z0zHisnk19jql2-3583IVBbd84mXM9NiQ/edit).
- All split data can be found in the "Resources/Datbase_CSVs" folder.

## References for any code used that is not your own
Seaborn: Building structured multi-plot grids using custom functions and plotting pairwise data relationships - https://seaborn.pydata.org/tutorial/axis_grids.html
