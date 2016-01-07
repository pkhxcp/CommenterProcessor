import praw

def main():
	# Initialize the API wrapper
	r = praw.Reddit(user_agent='Commenter Processor')
	# This is how to query posts within a specific subreddit
	submissions = r.get_subreddit('news').search("Iraq",sort="top",limit=10)
	userList = {}
	userCount = {}
	# Loop through all the search results
	for post in submissions:
		title = str(post).split(":: ", 1)[1]
		userList.setdefault(title, [])
		# Loop through all the comments within a post
		for comment in post.comments:
			# Check that a comment is not a MoreComments type
			if(type(comment) is not praw.objects.MoreComments):
				# Get the Redditor's name and print it
				author = comment.author
				# Make sure the Redditor is not deleted
				if(author != None):
					if (author.name not in userList[title]):
						userList[title].append(author.name)
	for key,value in userList.items():
		for user in value:
			if user not in userCount:
				userCount[user] = 1
			else:
				userCount[user] = userCount[user] + 1
	print(userCount)
if __name__ == "__main__":
	main()