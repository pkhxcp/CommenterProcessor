import praw

def getAllComments(seedComments):
	allComments = []
	for comment in praw.helpers.flatten_tree(seedComments):
		if type(comment) is praw.objects.MoreComments:
			nestedComments = []
			try:
				nestedComments = comment.comments()
			except AssertionError:
				print("Tried to scrape a MoreComments object with no mo comments")
			if(len(nestedComments) != 0):
				allComments += getAllComments(nestedComments)
		else:
			allComments.append(comment)
	return allComments

def main():
	subList = []
	keyList = []
	searchLimit = 0
	sortType = ""
	output = open('output.txt', 'w')
	with open('input.txt', 'r') as input:
		for line in input:
			category, contents = line.split(": ", 1)
			contents = contents.split("; ")
			contents[-1] = contents[-1].rstrip('\n')
			if category == "SUBREDDITS":
				subList = contents
				print("SUBREDDITS: %s" % contents)
			elif category == "KEYWORDS":
				keyList = contents
				print("KEYWORDS: %s" % contents)
			elif category == "LIMIT":
				searchLimit = contents
				print("LIMIT: %s" % contents)
			elif category == "TYPE":
				sortType = contents
				print("TYPE: %s" % contents)
	# Initialize the API wrapper
	r = praw.Reddit(user_agent='Commenter Processor')
	# This is how to query posts within a specific subreddit
	for subreddit in subList:
		for keyword in keyList:
			submissions = r.get_subreddit(subreddit).search(keyword,sort=sortType[0],limit=int(searchLimit[0]))
			userList = {}
			userCount = {}
			totalUsers = 0
			limTracker = 1
			# Loop through all the search results
			for post in submissions:
				print("SUBREDDIT: %s, KEYWORD: %s, COUNT: %d" % (subreddit, keyword, limTracker))
				limTracker += 1
				title = str(post).split(":: ", 1)[1]
				# For some reason my windows command prompt didn't agree with printing apostrophes.
				# My fix was to add the encode below. Apparently it's bad. ¯\_(ツ)_/¯
				# print(title.encode("utf-8"))
				userList.setdefault(title, [])
				# Loop through all the comments within a post
				post.replace_more_comments(limit=None, threshold=0)
				for comment in praw.helpers.flatten_tree(post.comments):
					# Get the Redditor's name and print it
					author = comment.author
					# Make sure the Redditor is not deleted
					if(author != None and author.name not in userList[title]):
							userList[title].append(author.name)
			for key,value in userList.items():
				for user in value:
					if user not in userCount:
						userCount[user] = 1
						totalUsers += 1
					else:
						userCount[user] += 1
			output.write("SUBREDDIT: %s\nKEYWORD: %s\nTOTAL USERS: %d\n" % (subreddit, keyword, totalUsers))
			for key,value in userCount.items():
				output.write("%20s: %2s\n" % (key, value))
	output.close()
if __name__ == "__main__":
	main()
