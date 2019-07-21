import praw

reddit = praw.Reddit(client_id = 'pVhsuEKtvSeNVQ',
                     client_secret ='y1slipowOeHK5UTjLvby26PKwnA',
                     username='Cornell_class_Bot',
                     password = 'moderation2019',
                     user_agent = 'Made by /u/DubitablyIndubitable')

subreddit = reddit.subreddit('Cornell')

keyphrase = '!CornellBot'

