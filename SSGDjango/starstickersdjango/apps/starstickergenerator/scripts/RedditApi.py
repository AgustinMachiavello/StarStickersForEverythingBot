# Python Reddit API Wrapper: https://praw.readthedocs.io/en/latest/
import praw
# Os
import os

# Settings
from django.conf import settings

# Date and time
from django.utils import timezone

# Credentials
from ..credentials import REDDIT_CREDENTIALS

# Models
from ..models import CorpusRecord


class RedditAPI():
    def GetRedditInstance(self):
        """ Returns a reddit instance object

        Logs in with given credentials.A reddit account is required and a reddit app is required.
        Reddit app creation: https://www.reddit.com/prefs/apps
        """
        print("Login in...")
        reddit = praw.Reddit(
            client_id=REDDIT_CREDENTIALS['client_id'],
            client_secret=REDDIT_CREDENTIALS['client_secret'],
            user_agent=REDDIT_CREDENTIALS['user_agent'],
            username=REDDIT_CREDENTIALS['username'],
            password=REDDIT_CREDENTIALS['password'],)
        print("---\nUser:{0}\nRead only:{1}\n---".format(reddit.user.me(), reddit.read_only))
        return reddit
    
    def GetSubredditInstance(self, reddit_instance, subreddit_name='toastme'):
        """Reuturns a subreddit instance object

        Gets subreddit instance by it's name
        """
        subreddit_instance = reddit_instance.subreddit(subreddit_name)
        return subreddit_instance

    def GetSubmissionList(self, subreddit_instance, submissions_limit, filter='new'):
        """Returns a list of submission objects

        Returns a list of a filtered submissions. The list length is given by submissions_limit.
        """
        submission_id_list = []
        sub_instance = None
        if filter=='new':
            sub_instance = subreddit_instance.new(limit=submissions_limit)
        elif filter=='hot':
            sub_instance = subreddit_instance.hot(limit=submissions_limit)
        for submission in sub_instance:
            submission_id_list.append(submission.id)
        return submission_id_list

    def ResetCorpus(self):
        """Returns a Boolean

        Resets corpus
        """
        f = open(settings.STATIC_IMAGE_FOLDER + "corpus.txt", "w")
        f.close()
        print("Corpus reseted")
        return True

    def SaveSubmissionCommentsToCorpus(self, reddit_instance, submission_id_list, mode='top'):
        """Returns a Boolean

        Gets comments and adds a break line at the end. Then saves the comments to the 'corpus' text file.
        Comments get filtered by mode. Mode can be 'all' or 'top'.
        """
        print("Getting comments...")
        f = open(settings.STATIC_IMAGE_FOLDER + "corpus.txt", "a")
        comments_count = 0
        exception_count = 0
        submission_count = 1
        submission_list_length = len(submission_id_list)
        for submission_id in submission_id_list:
            submission = reddit_instance.submission(id=submission_id)
            submission_count += 1
            percentaje = ((submission_count * 100) / submission_list_length)
            if percentaje in [25, 50, 75, 100]:
                print(percentaje, "%")
            if mode == 'top':
                comments_list = list(submission.comments)
            elif mode == 'all':
                comments_list = submission.comments.list()
            else:
                print("Error at SaveSubmissionComments")
                return False
            submission.comments.replace_more(limit=None)  # Get rid of MoreComments objects
            comments_count += len(comments_list)
            for comment in comments_list:
                try:
                    f.write(comment.body+"\n")
                except:
                    exception_count += 1
                    pass
        f.close()
        data = {
            'comments_count': comments_count,
            'exception_count': exception_count
        }
        print("Comments count:", comments_count)
        print("Comment exceptions:", exception_count)
        return data

    def SaveComments(self, subreddit_name, submissions_limit, submission_filter='new', comments_filter='all',
                     reset_corpus=False):
        """Returns a Boolean

        Main script. Logs in and then saves comments to 'corpus' text file.
        Submission limit is the number of submussions to extract comments from.
        If reset_copus is False, comments will just append to the existing ones.
        """

        if not reset_corpus:
            pass
        else:
            self.ResetCorpus()
        reddit_instance = self.GetRedditInstance()
        subreddit_instance = self.GetSubredditInstance(reddit_instance, subreddit_name)
        submission_id_list = self.GetSubmissionList(subreddit_instance, submissions_limit, submission_filter)
        saved = False
        data = {
            'last_update': str(timezone.now()),
            'comments_count': 0,
            'exception_count': 0,
            'saved': saved
        }
        data_save = self.SaveSubmissionCommentsToCorpus(reddit_instance, submission_id_list, comments_filter)
        if data_save:
            data['comments_count'] = data_save['comments_count'],
            data['exception_count'] = data_save['exception_count'],
            data['saved'] = True,
        CorpusRecord.objects.create(
            comments_count=int(data_save['comments_count']),
            exception_count=int(data_save['exception_count'])),
        return data


# EXAMPLE:
# a = RedditAPI()
# a.SaveComments('toastme', 50, 'new', 'all', False)
