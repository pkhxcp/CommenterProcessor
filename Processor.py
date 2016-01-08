import praw
import pickle

def getAllComments(seedComments):
	allComments = []
	for comment in praw.helpers.flatten_tree(seedComments):
		if type(comment) is praw.objects.MoreComments:
			allComments += getAllComments(comment.comments())
		else:
			commentCount += 1
			allComments.append(comment)
	return allComments

def main():
	# Initialize the API wrapper
	r = praw.Reddit(user_agent='Commenter Processor')
	# This is how to query posts within a specific subreddit
	submissions = r.get_subreddit('news').search("Iraq",sort="hot",limit=1)

	userList = {}
	userCount = {}
	totalUsers = 0
	# Loop through all the search results
	for post in submissions:
		print(post)
		title = str(post).split(":: ", 1)[1]
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
	with open('output.txt', 'w') as output:
		pickle.dump(userCount, output)

if __name__ == "__main__":
	main()
