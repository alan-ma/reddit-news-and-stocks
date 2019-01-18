# Data Senior Thesis
### Activity in r/worldnews and the Stock Market
#### Alan Ma

## Abstract
The stock market is quite an enigma due to the complex relationships between events that occur in the world and the prices of different stocks. The purpose of this this report was to build a model to predict stock market indices such as the Dow Jones Industrial Average (Dow) and the Standard & Poor's 500 (S&P 500), which are often used as indicators of the general economy. The model was based off of trends in the activity on Reddit’s subreddit r/worldnews, which includes articles pertaining to the global population. The top 15 posts from each day (over three years) in r/worldnews were retrieved, including four pieces of information for each post: the number of upvotes, number of comments, percentage of upvotes (versus downvotes), and the sentiment of the article’s title. These factors were used to create a model through the process of multiple linear regression and also predict recent values of the analyzed stock market indices. The result was that the models created did not fit the training data and inaccurately predicted recent stock market indices.

### Visualization Tools

To get an idea of what the data looks like, the following tools were built (Vue.js, Chart.js):

Individual posts (original data): http://54.174.75.231:3000/visualization/individualPosts.html

Aggregate data (histograms): http://54.174.75.231:3000/visualization/aggregatePosts.html

## Procedure

### Determining Which Data to Use

The first step in the process was to choose sources of information and determine how to quantify world news and the stock market. The justification to use news posts from Reddit r/worldnews was primarily for convenience and diversity of data. It was infeasible to collect data from news sources from around the world and from a variety of topics, as well as the activity and user interactions on each article. Posts on /r/worldnews are articles and links shared by anyone around the world, which according to the subreddit description, make it "A place for major news from around the world, excluding US-internal news." This allows news from around the globe to gain traction and spread to a lot of users – r/worldnews currently has 18.8 million subscribers, making it the 6th most subscribed subreddit. Reddit also provides an application programming interface (API) to easily retrieve information such as the number of upvotes and comments on each post.

The stock market is not perfectly quantifiable, but there are a lot of attempts to do so using stock market indices. The scope of this report does not cover the underlying concepts of the different indices and benefits/drawbacks of each. Instead, 21 popular indices will be used as general indicators of the market (refer to the Appendices for the list).

### Features (Inputs)

The process of multiple linear regression requires input variables (features). There are multiple variables of concern when it comes to posts in r/worldnews. Creating an aggregate index from these variables could lead to bias when creating the index, so it is a better choice to leave the variables independent of each other. Each variable will be quantitative, and qualitative variables (such as sentiment) will require processing to turn into usable data.

For each day, there will be numerous posts submitted on that date. The primary control variable will be the number of posts chosen from each day; the top 15 posts – sorted by score – from each date were used in this report. The justification for sorting by score was that the most popular submissions would be the posts most capable of affecting the stock market. Each post included the following information:

- Score – the number of upvotes
- Number of Comments – number of comments on the post
- Upvote Ratio – the ratio of upvotes to downvotes on the post
- Title – the title of the post, typically the name or short description of the article that was posted

The Score, Number of Comments, and Upvote Ratio can be used directly as numerical data, but the Title of the post will be used to determine its Sentiment. The sentiment (positive, neutral, or negative) will be classified using TextBlob, a natural language processing library in Python.

The features derived from these will be the mean and standard deviation of each variable from all 15 posts. In total, there will be 8 input variables (4 base pieces of information with the mean and standard deviation of each). Each day will have these 8 input variables and one output variable (the stock market index on the given date). Submissions from the past 3 years (from January 1, 2015 to December 31, 2017) will be retrieved, meaning a sample size of 1095 days and collecting 16425 posts.

### Sampling Technique
The sampling strategy in this experiment was essentially convenience sampling since using Reddit as a source of world news was due to the ease of gathering data. Although convenience sampling is not the most effective type of sampling, the nature of posts in r/worldnews is a type of stratified sampling; r/worldnews aggregates articles from around the globe, attempting to represent many countries and not overrepresent certain countries (i.e. the United States). The top 15 posts on each day, sorted by score, creates a hint of random sampling in this process; it is unknown which posts will be submitted and which ones will gain the most upvotes, adding randomness to the sampling. Since 16425 posts were analyzed, the amount of information retrieved was a fairly representative sample of the population.

### Retrieving Data

The processing in this report was done through Python due to its wide range of applications and extensive use in data science. To retrieve information from Reddit, a Python library was used to access its posts – the Python Reddit API Wrapper (PRAW). An existing account on Reddit was used to authenticate the requests, and a developer app was created to generate the client id and client secret. The drawback to Reddit's API was that it is very difficult to sort posts by date and retrieve the top submissions. For this purpose, a very useful tool called Pushshift was used, which allowed complex queries on the entire Reddit database. This API allowed queries through HTTP requests, and the date was specified through Unix Epoch Time.

The Pushshift API sometimes experienced discrepancies in data between its own database and the actual submissions on Reddit. To overcome this challenge, the identification codes for the top posts from each day were retrieved through Pushshift. This was done using HTTP requests through a useful library called urllib in Python. The actual information for each post was retrieved through PRAW based on the submission ID of each post.

The final step in gathering preliminary data was to analyze the title's sentiment using TextBlob. TextBlob is a Python library for natural language processing, and part of its toolbox is a sentiment analysis which marks a text sample as negative, neutral, or positive. The specifics of the sentiment analysis tool is outside the scope of this report (see Errors and Omissions for drawbacks of TextBlob).
At this point, the four pieces of information were gathered and saved in individual files to prevent data loss. This was because each day took about 30 seconds to retrieve information for (due to restrictions of Reddit’s API), and network errors during the process of retrieval were bound to occur. A system was set in place to check which dates had been completed and which date to move onto.

The process of gathering data for the stock indices was much simpler: An API called Alpha Vantage was used to retrieve different stock indices for each date. These values will be written in files through a similar process.

Refer to the Appendices for the data retrieval scripts used in this report.

### Data Preprocessing

After the collection of data from Reddit and Pushshift, there were 1095 files with information from 15 posts in each (see Appendices for collected data). To aggregate the data, Python scripts were used to find the mean and standard deviation for each day. In addition to this, the mean and standard deviation of these means was taken in order to find the population mean according to the central limit theorem.
In multiple linear regression, a common preprocessing step is to normalize the data since there may be large inconsistencies between variables. The standardized value was calculated using the equation x-us, where x is original value, u is the mean, and s is standard deviation. The resulting information was stored in a training set file, which allowed models to be created off of the data.

## Analysis

### Data Visualization
Tools were created to help visualize the data from individual posts as well as the aggregated data. Examples of these tools are shown below (refer to the Appendices for links to these interactive tools). In the individual posts, the population mean is estimated according to the central limit theorem. Since only 15 posts were analyzed on each day, the confidence of each estimate was very low.
Histograms were generated to show the frequency distribution of each variable across all three years of data. The distribution of each feature turned out to resemble a normal distribution, with the calculated population mean and standard deviation for each of the 8 variables.


### Data Analysis

To build a model to predict the value of stock market indices, linear regression was used to fit a polynomial equation to the training set. The process used to create a model was with Python’s SciKit library, which has a linear regression module. The model that was created then allowed a coefficient of determination to be calculated as well as predict values for given inputs. A total of 21 different models were created for each stock market index. Refer to the Appendices for the Python scripts used in the analysis.

The mean coefficient of determination was 0.31, which shows that the models are able to predict the variance in the index based on the activity in r/worldnews 31% of the time. After the stock market index models were sorted by the coefficient of determination, an interesting result appears (refer to the Appendices for the entire list).

1. NASDAQ: (R2=0.6486)
2. S&P 500: (R2=0.6419)
3. DOW: (R2=0.6391)
19. Shanghai Stock Exchange (SSE) Composite: (R2=0.0822)
20. Nikkei (Japan) 225: (R2=0.0698)
21. ESTX50 EUR P (Zurich Stock Exchange): (R2=0.0649)

The indices that the model fit best were the indices in the North American market, while the Shanghai, Japanese, and Zurich markets had the worst models – almost no variance in the index could be predicted by the model.

### Predictions

Using the models, recent values of stock market indices were attempted to be predicted. Using r/worldnews activity in the past 24 hours in June 2018, values were predicted against the expected values of each index. For each model, the percentage error between the prediction and expected value ranged from 1% to 25%, on average 11%.

1. BEL 20 (1%)
2. ESTX50 EUR P (2%)
18. SSE Composite (18%)
19. DOW (18%)
20. Russell 2000 (22%)
21. NASDAQ (25%)

As expected, the predictions for the indices were highly varied and did not match any expected pattern. Interestingly enough, even though NASDAQ and DOW had the most accurate models, their predictions were the most erroneous. ESTX50 on the Zurich Stock Exchange had one of the most accurate predictions, even though its model was the least accurate.

## Conclusions

The conclusion from this report is that an accurate model cannot be built to predict stock market index values based on the selected variables in r/worldnews. Even the most accurate model only predicted 65% of the variance in the index, and the predictions were too varied to provide any sort of indication in the stock market.

However, the models created point towards a very interesting find: stock market indices based in American stock exchanges can be better predicted by activity in r/worldnews. This result could completely be a coincidence; perhaps stock exchanges in the United States behave differently than foreign exchanges, and such behaviour matches the model better. Another possibility is that activity in the subreddit is biased towards North American news, which then allows a more accurate model to be made for indices such as NASDAQ and DOW.

If the bias exists, the implication is that there is at least some sort of correlation between activity in r/worldnews and the accuracy of the model created. The data analyzed and the stock market indices could be much too broad for an accurate model; an alternative would be to focus on a niche topic. For example, activity in a subreddit dedicated towards a specific industry could be analyzed, building a model to predict a stock market index of a single industry.

# Errors and Omissions

Due to restrictions in time and resources, there were many shortcomings and changes in the report. The original goal was to use global stock market indices such as MSCI World and S&P Global 100 – this was because world news was being analyzed. However, very few stock market APIs exist to easily access the data for stock market indices, and none had the global indices. Thus, only local indices were analyzed, creating bias in the data.

The initial process was to use the top 300 submissions on each day over a period of 5 years, meaning 1825 days and 547500 posts. However, Reddit’s API had limitations in the number of requests per minute, meaning that retrieving 15 posts required about 20 to 30 seconds. Due to the limited time to retrieve data, the sample size was reduced to 15 posts per day. The three year limit was chosen since Reddit’s user base had grown substantially between 2013 and 2015, and the number of interactions would vary too much between the past and present to create a reliable model.

While analyzing the data, the number of usable dates was limited since stock markets do not open on the weekends. Thus, only 760 (on average) data points were available to be used from the original 1095 days. This limited the training set for linear regression, and because having too few data points could create bias in the model, this reduced the accuracy of the models.

## Appendices

### Stock Market Indices

The stock market indices that were analyzed in this report were:

- GSPTSE
- GSPC
- DJI
- IXIC
- NYA
- XAX
- RUT
- VIX
- FTSE
- GDAXI
- FCHI
- STOXX50E
- N100
- BFX
- MICEXINDEXCF.ME
- N225
- HSI
- 000001.SS
- STI
- AXJO
- AORD

The indices can be looked up on Yahoo Finance to find more detailed descriptions.

### Software

The Python scripts can be found in this report’s GitHub repository: https://github.com/alan-ma/data-senior-thesis. Individual scripts are listed below:

Retrieving information for each day’s top posts: https://github.com/alan-ma/data-senior-thesis/blob/master/new_retrieve_submissions.py

Retrieving stock market indices: https://github.com/alan-ma/data-senior-thesis/blob/master/retrieve_indices.py

Aggregating and preprocessing data: https://github.com/alan-ma/data-senior-thesis/blob/master/aggregate_data.py

Analyzing data: https://github.com/alan-ma/data-senior-thesis/blob/master/analyze.py

### Data

The collected data are also accessible in the GitHub repository. Each day’s top posts are stored in individual JSON files, all 1095 accessible at https://github.com/alan-ma/data-senior-thesis/tree/master/new_parsed_dates.

The aggregate data and additional information such as histogram values can be viewed in JSON files at https://github.com/alan-ma/data-senior-thesis/tree/master/aggregate_data.

### Visualization Tools

The interactive visualization tools have been hosted on a web server. Vue.js and Chart.js were used to create the web pages.

Individual posts (original data): http://54.174.75.231:3000/visualization/individualPosts.html

Aggregate data (histograms): http://54.174.75.231:3000/visualization/aggregatePosts.html

### Coefficients of Determination
Index Name | Coefficient
--- | ---
Nasdaq | 0.64864692
S&P | 0.641884594
Dow | 0.639050999
Russell 2000 | 0.535851415
NYSE COMPOSITE (DJ) | 0.497047688
FTSE 100 | 0.441857608
S&P/TSX | 0.3609716
NYSE AMEX COMPOSITE INDEX | 0.332768328
CAC 40 | 0.29880777
EURONEXT 100 | 0.286005156
Vix | 0.260478676
ALL ORDINARIES | 0.254218051
BEL 20 | 0.252336265
DAX | 0.230086207
HANG SENG INDEX | 0.214669644
MICEX IND | 0.182238236
S&P/ASX 200 | 0.157266957
STI Index | 0.105682442
SSE Composite Index | 0.082211307
Nikkei 225 | 0.069837138
ESTX50 EUR P | 0.064934665
| | |
 Mean | 0.312231032

### Predictions

Index Name | Predicted | Expected | % Difference
--- | --- | --- | ---
BEL 20 | 3792.077543 | 3763.5701 | 1%
ESTX50 EUR P | 3389.410454 | 3441.6001 | 2%
Vix | 14.35276513 | 14.6 | 2%
STI Index | 3177.566259 | 3294.8401 | 4%
CAC 40 | 5007.472469 | 5389.3198 | 7%
EURONEXT 100 | 974.938858 | 1055.08 | 8%
DAX | 11590.16435 | 12579.7197 | 8%
FTSE 100 | 7002.272183 | 7689.3999 | 9%
S&P/TSX | 14899.30363 | 16489.5 | 10%
S&P/ASX 200 | 5628.858605 | 6243.3999 | 10%
ALL ORDINARIES | 5688.607077 | 6341.6001 | 10%
NYSE COMPOSITE (DJ) | 11371.61697 | 12677.7002 | 10%
NYSE AMEX COMPOSITE INDEX | 2459.385838 | 2779.3501 | 12%
HANG SENG INDEX | 25371.87046 | 29436.8398 | 14%
Nikkei 225 | 19221.17501 | 22535.6504 | 15%
MICEX IND | 1913.861386 | 2262.1799 | 15%
S&P | 2307.756607 | 2764.1699 | 17%
SSE Composite Index | 3400.23248 | 2891.969 | 18%
Dow | 20245.26656 | 24663.1797 | 18%
Russell 2000 | 1330.234408 | 1696.37 | 22%
Nasdaq | 5781.918812 | 7739.71 | 25%
 |  |  | 
 |  |  | Mean Difference | 11%
