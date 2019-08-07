# CornellRedditBot
A bot that gives you extra info about classes you're interested in!

This bot uses a combination of RegEx and user-filtering to determine if a user of r/Cornell
is asking about a class. The bot is constantly checking the most recent 25 posts, it does this
every five minutes, to determine if a person is asking about a class. If a post has been previously
cached, then the bot will skip over it.

If the bot determines that a post is about a class, then it parses through the most recent 1000 posts
to the sub-reddit to determine if they are relvant to what the OP of the reddit post asked. The results
are appended to a string and automatically commented by the bot account on reddit!
