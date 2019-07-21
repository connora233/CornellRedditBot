#import needed packages
import praw
import datetime
import re
from concurrent.futures import ThreadPoolExecutor

#
reddit = praw.Reddit(client_id = 'pVhsuEKtvSeNVQ',
                     client_secret ='y1slipowOeHK5UTjLvby26PKwnA',
                     username='Cornell_class_Bot',
                     password = 'moderation2019',
                     user_agent = 'Made by /u/DubitablyIndubitable')

subreddit = reddit.subreddit('Cornell')

invalidNums = ['1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1999', '2000', '2001', '2002', '2003',
               '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016',
               '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '1000', '3000', '4000',
               '5000', '6000']

def get_date(submission):
	time = submission.created
	return datetime.datetime.fromtimestamp(time)

def remove_duplicates(x):
    return list(set(x))

def remove_nums(x):
    for num in x:
        if num in invalidNums:
            x.remove(num)
    return x

def find_posts(classes):
    output = ""
    for archive in reddit.subreddit('cornell').new(limit=2000):
        check = archive.title + " " + archive.selftext()
        for classNums in classes:
            if classNums in check:
                output = output + archive.url + "\n"
    return output


for submission in reddit.subreddit('cornell').new(limit=25):
    keyphrase = remove_nums(remove_duplicates(re.findall(r'\d{4}', submission.title + " " + submission.selftext)))
    if keyphrase:
        with ThreadPoolExecutor(max_workers = 3) as executor:
            thread1 = executor.submit(find_posts(keyphrase))