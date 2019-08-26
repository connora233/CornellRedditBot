# Import needed packages
import praw
import time
import re
import passwords # Custom file with the 3 variables specified below

# Create an instance of a reddit account
USERNAME = 'Cornell_Class_Bot'#'Cornell_class_Bot'

reddit = praw.Reddit(client_id=passwords.client_id,
                     client_secret=passwords.client_secret,
                     username=USERNAME,
                     password=passwords.password,
                     user_agent='Made by /u/DubitablyIndubitable')

subreddit = reddit.subreddit('Cornell') # is this ever used?

# Declare neccesary global variables
checked_posts = []
checked_comment = []
count = 0
comment_count = 0
output = ""

# Common 4-digit numbers mentioned in posts that could create a false-positive
invalid_nums = ['1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1999', '2000', '2001', '2002', '2003',
               '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016',
               '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '1000', '3000', '4000',
               '5000', '6000'] # turn into hashset!
# invalid_nums_dict = {class:1 for class in invalid_nums}

def remove_duplicates(x):
    """
    Removes duplicate numbers from lists. Used incase the class number is mentioned multiple times in a post
    Input:
    x - list of numbers
    Output:
    list of unique numbers
    """
    return list(set(x))


def filter_nums(x):
    """
    Removes the commonly mentioned 4-digit numbers listed above from the numbers detected to be classes
    Input:
    x - list of numbers
    Output:
    filtered list of numbers containing no elements that are in invalid_nums
    """
    # for num in x:
    #     if num in invalid_nums:
    #         x.remove(num) # don't remove while iterating over...
    return [num for num in x if num not in invalid_nums]


def find_posts(classes, url):
    """
    Finds posts containing the same class mentioned in the original post by ensuring
    the class number appears in the to-be recommended post's title and comment section
    Input:
    classes - list of class numbers
    url - url to the post being commented on as a string
    Output:
    ???
    """
    # global output #??
    response = ""
    num = 0
    print("Searching for related material")

    # Check all recent posts to see if any class in classes is mentioned in the
    # title or body. If it is, check the comments to make sure this post isn't
    # the original post the bot will eventually comment on nor is it a post already
    # checked (need this ??? try removing ??)
    for archive in reddit.subreddit('cornell').new(limit=None): # change this to top?
        for class_ in classes:
            if class_ in archive.title + " " + archive.selftext:

                for comment in archive.comments:
                    if class_ in comment.body and archive.url != url and archive.url not in response:
                        response = response + "[" + archive.title + "](" + archive.url + ")" + "\n\n"
                        num = num + 1
                        if num == 5:
                            return response
                        break
    return response


def hasCommented(post):
    """
    Function to check if the comments of a post contain a comment by this bot
    Input:
    post - a praw submission object to check
    """
    for comment in post.comments:
        if comment.author == USERNAME:
            return True
    return False


def hasReplied(comment):
    """
    Function to check if the bot has replied to a comment
    Input:
    comment - a praw comment object to check
    """
    for reply in comment.replies:
        if reply.author == USERNAME:
            return True
    return False


def reply_to_comment(debug_mode=False):
    """
    Reply to all comments invoking classbot
    Input:
    debug_mode - if True, doesn't reply to comments
    """
    global comment_count
    global output
    for submission in reddit.subreddit('cornell').new(limit=500):
        for comment in submission.comments:
            if "!classBot" in comment.body and (not hasReplied(comment)):
                classes = re.findall(r'\d{4}', comment.body)
                unique_classes = remove_duplicates(classes)
                filtered_classes = filter_nums(unique_classes)

                if len(filtered_classes):
                    output = find_posts(filtered_classes, submission.url)
                    if len(output) != 0:
                        if not debug_mode:
                            comment.reply(("I noticed you asked about a specific class! "
                            "Here are some possibly useful links: \n\n" + output))
                        else:
                            print(("I noticed you asked about a specific class! "
                            "Here are some possibly useful links: \n\n" + output))
                        comment_count = comment_count + 1
                        print("This is the " + str(comment_count) + "th comment!")
                    output = ""


def comment_on_post(debug_mode=False):
    """
    Comment on most recent posts containing a 4-digit number
    Input:
    debug_mode - if True, doesn't reply to comments
    """
    global checked_posts
    global checked_comment
    global comment_count
    global output

    for submission in reddit.subreddit('cornell').new(limit=25): # change to top?
        if not hasCommented(submission):
            classes = re.findall(r'\d{4}', submission.title + " " + submission.selftext)
            unique_classes = remove_duplicates(classes)
            filtered_classes = filter_nums(unique_classes)

            if len(filtered_classes) != 0 and submission.url not in checked_posts:
                checked_posts = [submission.url] + checked_posts
                # if (len(checkedPosts) > 30):
                #     del checkedPosts[-1]
                checked_posts = checked_posts[:30]
                output = find_posts(filtered_classes, submission.url)

            if len(output) != 0:
                if not debug_mode:
                    submission.reply(
                        "I noticed you asked about a specific class! Here are some possibly useful links: \n\n" + output)
                else:
                    print("I noticed you asked about a specific class! Here are some possibly useful links: \n\n" + output)
                comment_count = comment_count + 1
                print_num_comments(comment_count)
            output = ""

def print_num_comments(comment_count):
    """
    Print number of comments bot has made
    Input:
    Number of comments made so far
    """
    last_digit = comment_count % 10
    if last_digit == 1:
        print("This is the " + str(comment_count) + "st comment!")
    elif last_digit == 2:
        print("This is the " + str(comment_count) + "nd comment!")
    elif last_digit == 3:
        print("This is the " + str(comment_count) + "rd comment!")
    else:
        print("This is the " + str(comment_count) + "th comment!")

def remove_bad_comments(threshold=0, num_to_check=15):
    """
    Remove comments from the past num_to_check with a score below threshold.
    Set num_to_check to None to check all comments
    Input:
    threshold - minimum score needed to keep a comment
    num_to_check - check the most recent num_to_check comments' score
    """
    user = reddit.redditor(USERNAME)
    for comment in user.comments.new(limit=num_to_check):
        if comment.score < threshold:
            comment.delete()

# Loop to constantly check the most recent 25 posts to see if it's neccesary for the bot to comment
while True:
    comment_on_post(debug_mode=True)
    # reply_to_comment(debug_mode=True) #reduce number of comments scanned !!
    remove_bad_comments()
    print("Sleeping now")
    break
    time.sleep(300)