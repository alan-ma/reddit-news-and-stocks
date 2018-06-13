# retrieve submissions from reddit
# through pushshift.io and reddit praw

import praw, urllib.request, json
from os import listdir
from textblob import TextBlob
from datetime import datetime, time, timedelta
from math import floor


# return sentiment of string using textblob
def get_sentiment(title):
    analysis = TextBlob(title)
    return analysis.sentiment.polarity


# return string of rounded timestamp of datetime
def get_time(input_time):
  return str(floor(input_time.timestamp()))

reddit = praw.Reddit(client_id='x--wD8MK1ZD7NA',
                     client_secret='S2CsK_xAmKHq3_h0ZMB2Ejd6qhY',
                     user_agent='mac:dataseniorthesis:v1 (by /u/energywolf)')

subreddit = reddit.subreddit('worldnews')

# midnight = datetime.combine(datetime.today(), time.min) # 23:59:59 yesterday
midnight = datetime.fromtimestamp(1514764800) # january 1, 2018 midnight
completed_counter = 0

completed_days = listdir("parsed_dates")
print("currently " + str(len(completed_days)) + " days")

# retrieve submissions from pushshift.io
# r/worldnews, top 300 posts from specified date
# posts from one day before epoch_date
def retrieve_from(epoch_date):
  POSTS = 10 # number of top posts

  # 86400 seconds in a day
  before_time = epoch_date - timedelta(days = 1)

  request_string = "http://api.pushshift.io/reddit/submission/search/?after="
  request_string += get_time(before_time)
  request_string += "&before="
  request_string += get_time(epoch_date)
  request_string += "&sort_type=score&sort=desc&subreddit=worldnews&size="
  request_string += str(POSTS)

  print(request_string)
  
  contents = urllib.request.urlopen(request_string).read()
  contents_string = contents.decode("utf-8")
  contents_json = json.loads(contents_string)

  return contents_json


# parse the data in the json contents of a submission
def parse_data(submission_content):
  submission_list = submission_content["data"]
  parsed_info = {
    "data": []
  }

  counter = 0
  for submission in submission_list:
    submission_id = submission["id"]
    submission_score = submission["score"]
    submission_comments = submission["num_comments"]
    submission_title = submission["title"]
    reddit_submission = reddit.submission(id = submission_id)
    upvote_ratio = reddit_submission.upvote_ratio
    sentiment = get_sentiment(submission_title)

    parsed_info["data"].append(
      {
        "count": counter,
        "id": submission_id,
        "title": submission_title,
        "score": submission_score,
        "comments": submission_comments,
        "upvoteRatio": upvote_ratio,
        "sentiment": sentiment
      }
    )

    counter += 1
  
  return parsed_info


# main loop
while True:
  try:
    file_name = get_time(midnight) + ".json"

    if file_name not in completed_days:
      submission_list = retrieve_from(midnight)
      parsed_info = parse_data(submission_list)

      with open("parsed_dates/" + file_name, 'w') as outfile:
        json.dump(parsed_info, outfile)
      
      completed_counter += 1
      print("completed day " + get_time(midnight) + " total " + str(completed_counter))
    
    midnight -= timedelta(days = 1) # previous day
  except KeyboardInterrupt:
    print("completed " + str(completed_counter) + " by " + get_time(midnight))

