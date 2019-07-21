import praw
import datetime
import re

reddit = praw.Reddit(client_id = 'pVhsuEKtvSeNVQ',
                     client_secret ='y1slipowOeHK5UTjLvby26PKwnA',
                     username='Cornell_class_Bot',
                     password = 'moderation2019',
                     user_agent = 'Made by /u/DubitablyIndubitable')

subreddit = reddit.subreddit('Cornell')


def get_date(submission):
	time = submission.created
	return datetime.datetime.fromtimestamp(time)


for submission in reddit.subreddit('cornell').new(limit=25):
    keyphrase = re.findall(r'\d{4}', submission.title + " " + submission.selftext)
    print(keyphrase)
    print(submission.title)
    print(submission.score)
    print(get_date(submission))
