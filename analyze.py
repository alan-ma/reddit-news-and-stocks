# runs linear regression on the training set

import json, praw, numpy
from sklearn import linear_model
from textblob import TextBlob


training_data = json.load(open("aggregate_data/training_values.json", 'r'))["trainingSet"]
output_data = json.load(open("aggregate_data/training_output.json", 'r'))
central_limit_values = json.load(open("aggregate_data/central_limit_values.json", 'r'))

stock_indices = []


class trainingSet:
  def __init__(self, training_data, output_data):
    self.training_data = training_data
    self.output_data = output_data
    self.id = output_data["id"]
    self.name = output_data["name"]
    self.count = 0
    self.fails = 0
    self.input_features = []
    self.output_values = []
    self.clf = linear_model.LinearRegression()
    self.create_training_set()
    self.train()
  
  def create_training_set(self):
    for key, value in self.output_data["data"].items():
      try:
        self.input_features.append(self.training_data[key])
        self.output_values.append(value)
        self.count += 1
      except KeyError:
        self.fails += 1
    print("created index " + self.id + " with " + str(self.count) + " objects")
  
  def train(self):
    self.clf.fit(self.input_features, self.output_values)


# return sentiment of string using textblob
def get_sentiment(title):
    analysis = TextBlob(title)
    return analysis.sentiment.polarity


def get_current_posts():
  global reddit
  scores = []
  comments = []
  upvote_ratios = []
  sentiments = []
  
  print("\ngetting posts...\n")

  for submission in reddit.subreddit('worldnews').top('day', limit=10):
    scores.append(submission.score)
    comments.append(submission.num_comments)
    upvote_ratios.append(submission.upvote_ratio)
    sentiments.append(get_sentiment(submission.title))
    print(str(submission.score) + " - " + submission.title)
  
  scores_mean = (numpy.mean(scores) - central_limit_values["totalScoreMeansMean"]) / central_limit_values["totalScoreMeansStdDev"]
  comments_mean = (numpy.mean(comments) - central_limit_values["totalCommentsMeansMean"]) / central_limit_values["totalCommentsMeansStdDev"]
  upvote_ratios_mean = (numpy.mean(upvote_ratios) - central_limit_values["totalUpvoteRatioMeansMean"]) / central_limit_values["totalUpvoteRatioMeansStdDev"]
  sentiments_mean = (numpy.mean(sentiments) - central_limit_values["totalSentimentMeansMean"]) / central_limit_values["totalSentimentMeansStdDev"]

  scores_std_dev = (numpy.std(scores, ddof=1) - central_limit_values["totalScoreStdDevsMean"]) / central_limit_values["totalScoreStdDevsStdDev"]
  comments_std_dev = (numpy.std(comments, ddof=1) - central_limit_values["totalCommentsStdDevsMean"]) / central_limit_values["totalCommentsStdDevsStdDev"]
  upvote_ratios_std_dev = (numpy.std(upvote_ratios, ddof=1) - central_limit_values["totalUpvoteRatioStdDevsMean"]) / central_limit_values["totalUpvoteRatioStdDevsStdDev"]
  sentiments_std_dev = (numpy.std(sentiments, ddof=1) - central_limit_values["totalSentimentStdDevsMean"]) / central_limit_values["totalSentimentStdDevsStdDev"]

  return [scores_mean, scores_std_dev, comments_mean, comments_std_dev, upvote_ratios_mean, upvote_ratios_std_dev, sentiments_mean, sentiments_std_dev]  


reddit = praw.Reddit(client_id='x--wD8MK1ZD7NA',
                     client_secret='S2CsK_xAmKHq3_h0ZMB2Ejd6qhY',
                     user_agent='mac:dataseniorthesis:v1 (by /u/energywolf)')


for key in output_data:
  stock_indices.append(trainingSet(training_data, output_data[key]))

print("\ncoefficient of determinations:\n")

for training_set in stock_indices:
  print(training_set.name + " => " + str(training_set.clf.score(training_set.input_features, training_set.output_values)))

print("\npredicting for today\n")

new_input_set = [ get_current_posts() ]

print('\n\n')

for training_set in stock_indices:
  expected_output = 0
  for key in training_set.output_data["data"]:
    expected_output = [ training_set.output_data["data"][key] ]
    break
  print(training_set.name + " predicted value of " + str(training_set.clf.predict( new_input_set )) + " with coefficient of " + str(training_set.clf.score( new_input_set, expected_output)) + " (expected: " + str(expected_output) + ")")

print("\ndone")



