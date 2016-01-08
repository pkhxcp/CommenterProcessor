import praw

def getAllComments(comments):
	allComments = []
	for comment in comments:
		if type(comment) is praw.objects.MoreComments:
			allComments += getAllComments(comment.comments())
		else:
			allComments.append(comment)
	return allComments

# Initialize the API wrapper
r = praw.Reddit(user_agent='Commenter Processor')

# This is how to query posts within a specific subreddit
submissions = r.get_subreddit('news').search("Iraq",sort="top",limit=10)

# Loop through all the search results
for post in submissions:

	allComments = getAllComments(post.comments)
	
	# Loop through all the comments within a post
	for comment in allComments:

		# Get the Redditor's name and print it
		author = comment.author
		# Make sure the Redditor is not deleted
		if(author != None):
			print(author.name)
		else:
			print("None")
