# testing

from os import listdir

# import praw, urllib.request, json
# from textblob import TextBlob

# def get_sentiment(title):
#     analysis = TextBlob(title)
#     return analysis.sentiment.polarity

# reddit = praw.Reddit(client_id='x--wD8MK1ZD7NA',
#                      client_secret='S2CsK_xAmKHq3_h0ZMB2Ejd6qhY',
#                      user_agent='mac:dataseniorthesis:v1 (by /u/energywolf)')

# subreddit = reddit.subreddit('worldnews')

# contents = urllib.request.urlopen("http://api.pushshift.io/reddit/submission/search/?after=1506816000&before=1506902400&sort_type=score&sort=desc&subreddit=futurology&size=3").read()

# contents_string = contents.decode("utf-8")

# contents_json = json.loads(contents_string)

# for submission in contents_json["data"]:
#     submission_id = submission["id"]
#     submission_title = submission["title"]
#     reddit_submission = reddit.submission(id=submission_id)
#     upvote_ratio = reddit_submission.upvote_ratio
#     sentiment = get_sentiment(submission_title)

#     print(submission_title)
#     print(submission["score"])
#     print(submission["num_comments"])
#     print(upvote_ratio)
#     print(sentiment)
#     print('\n')

# print(get_sentiment("Brother-in-Law of Spain\u2019s King Must Go to Prison, Court Rules"))

print(sorted(listdir("parsed_dates")[0:], reverse=True))
