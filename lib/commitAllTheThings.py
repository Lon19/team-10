import os

def gitPush():
	os.system("git add .")
	os.system("git commit -m '#commitAllTheThings!'")
	os.system("git push")
	print("Pushed")

counter = 0
while True:
	counter += 1
	if os.path.exists("meme.meme"):
		os.system("rm meme.meme")
	else:
		os.system("touch meme.meme")
	if counter>100:
		gitPush()
		counter = 0
