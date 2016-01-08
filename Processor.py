import praw

def getAllComments(seedComments):
	allComments = []
	for comment in praw.helpers.flatten_tree(seedComments):
		if type(comment) is praw.objects.MoreComments:
			allComments += getAllComments(comment.comments())
		else:
			allComments.append(comment)
	return allComments

def main():
	output = open('output.txt', 'w')
	subList = []
	keyList = []
	searchLimit = 0
	type = ""
	with open('input.txt', 'r') as input:
		for line in input:
			category, contents = line.split(": ", 1)
			contents = contents.split("; ")
			contents[-1] = contents[-1].rstrip('\n')
			if category == "SUBREDDITS":
				subList = contents
			elif category == "KEYWORDS":
				keyList = contents
			elif category == "LIMIT":
				searchLimit = contents
			elif category == "TYPE":
				type = contents
	# Initialize the API wrapper
	r = praw.Reddit(user_agent='Commenter Processor')
	# This is how to query posts within a specific subreddit
	for subreddit in subList:
		for keyword in keyList:
			submissions = r.get_subreddit(subreddit).search(keyword,sort=str(type[0]),limit=int(searchLimit[0]))
			userList = {}
			userCount = {}
			totalUsers = 0
			# Loop through all the search results
			for post in submissions:
				title = str(post).split(":: ", 1)[1]
				# For some reason my windows command prompt didn't agree with printing apostrophes.
				# My fix was to add the encode below. Apparently it's bad. ¯\_(ツ)_/¯
				# print(title.encode("utf-8"))
				userList.setdefault(title, [])
				# Loop through all the comments within a post
				for comment in getAllComments(post.comments):
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
			output.write("SUBREDDIT: " + str(subreddit) + "\n")
			output.write("KEYWORD: " + str(keyword) + "\n")
			for key,value in userCount.items():
				output.write(str(key) + ": " + str(value) + "\n")
			output.write(str(totalUsers) + "\n\n")
	output.close()
if __name__ == "__main__":
	main()
