## PPHA 30538: Data and Programming for Public Policy II - Python Programming
### Aditi Shankar, Harish Sai, Shweta Kamath

## Crime and Safety Perceptions in Chicago

## Research Questions: 
Our final project centered around understanding trends related to crime and perception of crime in Chicago. More specifically, we looked to answer the following:
* How has crime in Chicago evolved overtime (2011 - 2021)? 
* How does it compare to other cities?
* How have people’s perceptions of safety changed over time?
* Is there any relationship between the movements in perceptions of safety and actual crime? 
* What are the trends in crime and safety scores within the city across districts? 
* Are crimes reported described in neutral language? 


## Logistics: 

* For this project, please access data at this link: https://drive.google.com/drive/folders/15ujjH69Z8ZDNAatU3YxF98owm14B4Hr_?usp=sharing and save to the data folder in the repository (these were the ones that were too big to upload to GitHub). 
* For the crimes data, we used data from 2011-2021, while the website had data from 2001 - this was too large to even upload to google drive and hence we’ve only provided the 2011-2021 data (Our code to create this is commented in the plot_and_model.py file). 
* For crime data from Boston and Detroit, we downloaded the data and have saved it in the Google drive. For this data, please load “RMS_Crime_Incidents.csv” into the “Data” folder directly. For the csv files under the Boston Data folder on drive, load all data files into “Data/Boston”.
* The path should be changed by the grader to where the final project repository is located on your local computer. 
* The order in which the code is to be run is - 1. plot_and_model.py, 2.app.py, 3.txtanalysis.py. 

## Approach

**How has crime in Chicago evolved overtime and how does it compare to other cities?**: For the purpose of our analysis, we only use 2011-2021 data. We cleaned the dataset to have clear year, month, date and time columns for ease of analysis. We created data aggregation and date conversion functions for this as we needed to do the same cleaning for multiple datasets (for other cities and metrics like sentiment) and for different conditions. (referred to later). For comparison, we chose Boston and Detroit given the completeness of their data (and similarity in terms of reporting). 

**How have people’s perceptions of safety changed over time?**: For this, we used a dataset provided by the CPD that captures self-reported citizen sentiment about safety and trust in police. A lower score on safety sentiment implies a citizen feels *less safe* and a lower score on trust in police implies *diminished trust in the police force*. The data is available from 2017 to 2022 and starting 2018 is disaggregated by race and sex. We used aggregate functions to explore the data. We created a plot that looks at sentiment over the months and years to understand if drops in trust and safety coincide with spikes in crimes. We also compare the numbers for each race group through bar plots.

**Is there any relationship between the movements in perceptions of safety and actual crime?**: To answer this, we regressed the average safety score for a particular police district and month on its corresponding crime count (OLS model). As mentioned earlier, we wrote a function, data_agg_three, for efficient aggregating. The arguments to be inputted are the data frame, the 3 aggregation characteristics (police district, year and month), the variable to be aggregated (actual crime and safety scores), and the operation (sum for crimes, and average for safety scores).  Using the function smf.ols from the statsmodel package we ran the required regression. To understand local trends, we wrote a function (reg_pd), where the police district is a key-word argument, which returns regression summary tables for each district.

**What are the trends in crime and safety scores within the city across districts?**: We first used the ‘group_by’ function to reorient the data with police districts and years as the points of reference and do some minor cleaning across both datasets. Finally, we merge the geopandas dataframe that has the police district coordinates with our two datasets, which we use for plotting in 2 shiny reactive functions. To consolidate the plot, we wrote two functions for each graph: one that creates the ultimate plot; another that is given variables from our data. We employ interactive elements and displays, ‘Ui.input_slide’: to vary the years, ‘Ui.input_select’: to vary the characteristics and (c)  Ui.input_switch: to toggle the L train map on and off. To substantiate our analysis, we also plotted the various combinations of monthly crime counts and mean safety scores by police districts on a scatter plot. We allow users to choose a district through ‘Ui.input_select’.

**Are crimes reported described in neutral language?**: For the text analysis portion of our project, we are looking at crime descriptions by the University of Chicago Police Department. We first used the BeautifulSoup package to automatically retrieve this data from the web. To ensure we are not using too much data, we decided to check the descriptions for the last month – November, 2022. We made a nested for loop that scans through multiple pages of the data, and creates a data set that records: the crime, location, date, description for the whole month. Since this is a nest-loop, the output is a nested-list. Hence, after the for-loop, we flatten the nest-list, split our data across these domains, and remerge them to get a clean pandas dataframe. Now, on this dataframe, we check the polarity and subjectivity of the descriptions using a function. To have a cleaner output, similar to the forth homework assignment, we plot the mean polarity and subjectivity of each crime description for each day as seaborn line plots. To ensure the code is general, we create a function and for-loop to retrieve the plots.

## Results

Crime in Chicago is a hotly debated topic. The first response to telling someone you live in Chicago is a comment about safety. Through our analysis we unpack the facts about crime in the city and contrast it with how “safe” people feel. 

Annually, Chicago sees 100 crimes committed per 1000 residents and has been reducing over time. To put this in context, Boston and Detroit report, on average, 125 and 130 crimes/1000 residents. We also see that crimes tend to happen mostly in summer months and gradually drop off around winter. However, contrary to what we expect, overall city safety perceptions have not gone up with the reduction in crime rate. People also “feel” less safe in the winter even though crime peaks in the summer months.

On a district level, crime and safety perceptions seem linked. Crime rates are worse in the South and West sides of the city and in these areas, safety perceptions are lower than the rest of the city as well. Black and Asian individuals feel the least safe in Chicago, especially in South, West and South-West areas. Historically, these are the areas that are known to be at the end of police brutality which could explain reduced safety perception. Districts in the North had comparatively low levels of crime, and higher safety scores across all communities. This is maintained across the years in our analysis, as well as for all the different kinds of crime. 

However, even on a district level, safety perceptions seem to be sticky, with change in crime not impacting change in safety perceptions. Many districts show scattered points, indicating weak correlation between movements in monthly crime counts and mean safety scores.

Statistically, we found a coefficient of -0.0077 when we regressed mean safety scores on actual crime counts for the month, which implies that a unit increase in the crime count is associated with almost a null change in the safety score. This would suggest, as also substantiated by the scatter plot, a lack of any causal effect of crime on safety perceptions. When we run the regression at individual police district levels, we do notice differences in values and signs, but they vary negligibly.

Moving closer to familiar territory, we decided to analyze UCPD crime descriptions around UChicago. We know that neutrality needs to be maintained when describing crime. To test this, we ran a sentiment analysis on descriptions for crimes in November, 2022. The analysis involves getting the average subjectivity and polarity of all the crime descriptions.The subjectivity refers to the degree to which the criminal or crime described is personally involved in an object. It can have a positive or negative score, but should lean towards 0 (or neutral, objective). In our text analysis, we see that crime descriptions are not too subjective, ranging from 0 to +0.2. However, the subjectivity is a lot more in the last couple of days, almost touching +0.8. Similar trends can be observed in the polarity scores.This outlines that the UCPD is fairly neutral.
