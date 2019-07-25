# StarStickersForEverythingBot
## Description
**Coded for Python 3.6**
#### Based on StarStickersForEverything <3: https://www.facebook.com/StarStickersforEverything/
This python script gets the latest comments from the subreddit r/toastme and generates a phrase with the same kind of writting or style of the comments using **Markov chains**.  Then it crops the text into an star template image and posts it to Facebook! 
**There is nothing too complitaced in this script, so any modifications should be easy to apply (owo)**
## Disclaimer
Unfortunately, due to new Facebook politics, post can't be auto-uploaded anymore (yikes). **The rest of the script still works!**
# Structure
Basic structure of the project. **AT THE END OF EVERY .py FILE THERE IS AN EXAMPLE FOR IMPLEMENTATION**
## Reddit api
Main functionality is to save subreddits comments to the 'corpus' text file
- A Reddit account and a Reddit app is nedeed
More info at: https://www.reddit.com/prefs/apps and https://praw.readthedocs.io/en/latest/
- Basic implementation:
```
a = RedditAPI()
a.SaveComments('toastme', 50, 'new', 'all', False)
```
## Facebook api
Automated posting: **Not allowed anymore since Facebook changed it's policy :(**
- Basic implementation
```PostImage(GetGraphInstance(), 'image_generated.png', '')```
## Star Sticker Generator
Generates sentences with similar styles based on comments at 'corpus.txt' and draw the generated phrase into a star template inside 'img' folder.
- Basic implementation:
```
a = StarStickerGenerator()
print(a.Generate())
```
## img folder
contains necessary images:
- star_template: template for drawing text on
- star_template_box_coordinates: contains information about coordinates for drawing the text in the correct place
- generated_image: generated image
## corpus.txt
here all the subreddit comments are saved with a break line at the end of each one of them.
## utils.py
Origianly thought for sending email alert everytime an automated post failed or succeeded
```SendEmailNotification("this is a message", 'aaa@gmail.com', 'bbb@gmail.com')```
## requirements.txt
necessary libraries for this project to work  You can install them with ```pip install -r requirements.txt```
# HUGE THANKS TO:
- markovify: https://github.com/jsvine/markovify
Without this library this project wouldn't even exist!
- StarStickersForEverything: https://www.facebook.com/StarStickersforEverything/
Of course, the people with the original idea!
## woops! Bugs...
For any questions or improvements you can send me a message to agmachiavello@gmail.com ! Have fun :)
