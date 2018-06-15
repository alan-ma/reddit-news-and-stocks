# aggregate data from individual posts
# output features
# scoreMean, scoreStdDev, commentsMean, commentsStdDev
# upvoteRatioMean, upvoteRatioStdDev, sentimentMean, sentimentStdDev
# also returns histogram data for distribution

# loop through data
# find the mean and standard deviation for each day
# separate variables for each mean and stddev for each day
# add that to the training set

import json, numpy
from os import listdir

files = sorted(listdir("new_parsed_dates"), reverse=True)

print("starting analysis of " + str(len(files)) + " posts")

score_means = []
score_std_devs = []
comments_means = []
comments_std_devs = []
upvote_ratio_means = []
upvote_ratio_std_devs = []
sentiment_means = []
sentiment_std_devs = []

for file_name in files:
  data = json.load(open("new_parsed_dates/" + file_name, 'r'))["data"]

  scores = [post["score"] for post in data]
  comments = [post["comments"] for post in data]
  upvote_ratios = [post["upvoteRatio"] for post in data]
  sentiments = [post["sentiment"] for post in data]

  score_means.append(numpy.mean(scores)) # add mean of scores
  score_std_devs.append(numpy.std(scores, ddof=1)) # add sample std dev of scores
  comments_means.append(numpy.mean(comments)) # add mean of comments
  comments_std_devs.append(numpy.std(comments, ddof=1)) # add sample std dev of comments
  upvote_ratio_means.append(numpy.mean(upvote_ratios)) # add mean of upvote ratios
  upvote_ratio_std_devs.append(numpy.std(upvote_ratios, ddof=1)) # add sample std dev of upvote ratios
  sentiment_means.append(numpy.mean(sentiments)) # add mean of sentiments
  sentiment_std_devs.append(numpy.std(sentiments, ddof=1)) # add sample std dev of sentiments

print("original data aggregated")

score_means_histogram, score_means_bin_edges = numpy.histogram(score_means, bins="auto")
score_std_devs_histogram, score_std_devs_bin_edges = numpy.histogram(score_std_devs, bins="auto")
comments_means_histogram, comments_means_bin_edges = numpy.histogram(comments_means, bins="auto")
comments_std_devs_histogram, comments_std_devs_bin_edges = numpy.histogram(comments_std_devs, bins="auto")
upvote_ratio_means_histogram, upvote_ratio_means_bin_edges = numpy.histogram(upvote_ratio_means, bins="auto")
upvote_ratio_std_devs_histogram, upvote_ratio_std_devs_bin_edges = numpy.histogram(upvote_ratio_std_devs, bins="auto")
sentiment_means_histogram, sentiment_means_bin_edges = numpy.histogram(sentiment_means, bins="auto")
sentiment_std_devs_histogram, sentiment_std_devs_bin_edges = numpy.histogram(sentiment_std_devs, bins="auto")

print("histogram values created")

total_score_means_mean = numpy.mean(score_means)
total_score_std_devs_mean = numpy.mean(score_std_devs)
total_comments_means_mean = numpy.mean(comments_means)
total_comments_std_devs_mean = numpy.mean(comments_std_devs)
total_upvote_ratio_means_mean = numpy.mean(upvote_ratio_means)
total_upvote_ratio_std_devs_mean = numpy.mean(upvote_ratio_std_devs)
total_sentiment_means_mean = numpy.mean(sentiment_means)
total_sentiment_std_devs_mean = numpy.mean(sentiment_std_devs)

total_score_means_std_dev = numpy.std(score_means, ddof=1)
total_score_std_devs_std_dev = numpy.std(score_std_devs, ddof=1)
total_comments_means_std_dev = numpy.std(comments_means, ddof=1)
total_comments_std_devs_std_dev = numpy.std(comments_std_devs, ddof=1)
total_upvote_ratio_means_std_dev = numpy.std(upvote_ratio_means, ddof=1)
total_upvote_ratio_std_devs_std_dev = numpy.std(upvote_ratio_std_devs, ddof=1)
total_sentiment_means_std_dev = numpy.std(sentiment_means, ddof=1)
total_sentiment_std_devs_std_dev = numpy.std(sentiment_std_devs, ddof=1)

print("mean and standard deviations calculated")

score_means_normalized = []
score_std_devs_normalized = []
comments_means_normalized = []
comments_std_devs_normalized = []
upvote_ratio_means_normalized = []
upvote_ratio_std_devs_normalized = []
sentiment_means_normalized = []
sentiment_std_devs_normalized = []

for i in range(len(files)):
  score_means_normalized.append( (score_means[i] - total_score_means_mean) / total_score_means_std_dev )
  score_std_devs_normalized.append( (score_std_devs[i] - total_score_std_devs_mean) / total_score_std_devs_std_dev )
  comments_means_normalized.append( (comments_means[i] - total_comments_means_mean) / total_comments_means_std_dev )
  comments_std_devs_normalized.append( (comments_std_devs[i] - total_comments_std_devs_mean) / total_comments_std_devs_std_dev )
  upvote_ratio_means_normalized.append( (upvote_ratio_means[i] - total_upvote_ratio_means_mean) / total_upvote_ratio_means_std_dev )
  upvote_ratio_std_devs_normalized.append( (upvote_ratio_std_devs[i] - total_upvote_ratio_std_devs_mean) / total_upvote_ratio_std_devs_std_dev )
  sentiment_means_normalized.append( (sentiment_means[i] - total_sentiment_means_mean) / total_sentiment_means_std_dev )
  sentiment_std_devs_normalized.append( (sentiment_std_devs[i] - total_sentiment_std_devs_mean) / total_sentiment_std_devs_std_dev )

print("normalized values created")

training_set = {}

for i in range(len(files)):
  date_index = round(int(files[i].strip(".json")) / 86400) * 86400
  training_set[ str(date_index) ] = [
    score_means_normalized[i],
    score_std_devs_normalized[i],
    comments_means_normalized[i],
    comments_std_devs_normalized[i],
    upvote_ratio_means_normalized[i],
    upvote_ratio_std_devs_normalized[i],
    sentiment_means_normalized[i],
    sentiment_std_devs_normalized[i],
  ]

print("training set completed")

original_values = {
  "scoreMeans": score_means,
  "scoreStdDevs": score_std_devs,
  "commentsMeans": comments_means,
  "commentsStdDevs": comments_std_devs,
  "upvoteRatioMeans": upvote_ratio_means,
  "upvoteRatioStdDevs": upvote_ratio_std_devs,
  "sentimentMeans": sentiment_means,
  "sentimentStdDevs": sentiment_std_devs
}

histogram_values = {
  "scoreMeansHistogram": score_means_histogram.tolist(),
  "scoreStdDevsHistogram": score_std_devs_histogram.tolist(),
  "commentsMeansHistogram": comments_means_histogram.tolist(),
  "commentsStdDevsHistogram": comments_std_devs_histogram.tolist(),
  "upvoteRatioMeansHistogram": upvote_ratio_means_histogram.tolist(),
  "upvoteRatioStdDevsHistogram": upvote_ratio_std_devs_histogram.tolist(),
  "sentimentMeansHistogram": sentiment_means_histogram.tolist(),
  "sentimentStdDevsHistogram": sentiment_std_devs_histogram.tolist(),
  "scoreMeansBinEdges": score_means_bin_edges.tolist(),
  "scoreStdDevsBinEdges": score_std_devs_bin_edges.tolist(),
  "commentsMeansBinEdges": comments_means_bin_edges.tolist(),
  "commentsStdDevsBinEdges": comments_std_devs_bin_edges.tolist(),
  "upvoteRatioMeansBinEdges": upvote_ratio_means_bin_edges.tolist(),
  "upvoteRatioStdDevsBinEdges": upvote_ratio_std_devs_bin_edges.tolist(),
  "sentimentMeansBinEdges": sentiment_means_bin_edges.tolist(),
  "sentimentStdDevsBinEdges": sentiment_std_devs_bin_edges.tolist()
}

central_limit_values = {
  "totalScoreMeansMean": total_score_means_mean,
  "totalScoreStdDevsMean": total_score_std_devs_mean,
  "totalCommentsMeansMean": total_comments_means_mean,
  "totalCommentsStdDevsMean": total_comments_std_devs_mean,
  "totalUpvoteRatioMeansMean": total_upvote_ratio_means_mean,
  "totalUpvoteRatioStdDevsMean": total_upvote_ratio_std_devs_mean,
  "totalSentimentMeansMean": total_sentiment_means_mean,
  "totalSentimentStdDevsMean": total_sentiment_std_devs_mean,
  "totalScoreMeansStdDev": total_score_means_std_dev,
  "totalScoreStdDevsStdDev": total_score_std_devs_std_dev,
  "totalCommentsMeansStdDev": total_comments_means_std_dev,
  "totalCommentsStdDevsStdDev": total_comments_std_devs_std_dev,
  "totalUpvoteRatioMeansStdDev": total_upvote_ratio_means_std_dev,
  "totalUpvoteRatioStdDevsStdDev": total_upvote_ratio_std_devs_std_dev,
  "totalSentimentMeansStdDev": total_sentiment_means_std_dev,
  "totalSentimentStdDevsStdDev": total_sentiment_std_devs_std_dev
}

training_values = {
  "trainingSet": training_set
}

with open("aggregate_data/original_values.json", 'w') as outfile:
  json.dump(original_values, outfile)

with open("aggregate_data/histogram_values.json", 'w') as outfile:
  json.dump(histogram_values, outfile)

with open("aggregate_data/central_limit_values.json", 'w') as outfile:
  json.dump(central_limit_values, outfile)

with open("aggregate_data/training_values.json", 'w') as outfile:
  json.dump(training_values, outfile)

print("done.")

