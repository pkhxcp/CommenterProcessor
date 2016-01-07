import praw

# Initialize the API wrapper
r = praw.Reddit(user_agent='Commenter Processor')

# This is how to query posts within a specific subreddit
submissions = r.get_subreddit('news').search("Iraq",sort="top",limit=10)

# Loop through all the search results
for post in submissions:
	
	# Loop through all the comments within a post
	for comment in post.comments:

		# Check that a comment is not a MoreComments type
		if(type(comment) is not praw.objects.MoreComments):

			# Get the Redditor's name and print it
			author = comment.author
			# Make sure the Redditor is not deleted
			if(author != None):
				print(author.name)
