# Celery
from __future__ import absolute_import
from celery import shared_task

# Sticker Generator
from .scripts.StarStickerGenerator import StarStickerGenerator

# Twitter API
from .scripts.TwitterApi import TwitterAPI

# Reddit API
from .scripts.RedditApi import RedditAPI

# Email Utils
from .scripts.Utils import send_email_notification

# Date and time
from django.utils import timezone

# Models
from .models import GeneratedImage, CorpusRecord

# Shortcuts
from django.shortcuts import render

# Django views
from django.views.generic import TemplateView

# Threading
from threading import Thread

# Forms
from .forms import SecretCodeForm

# Site
from django.contrib.sites.models import Site


@shared_task
def test():
    print("666")
    return


@shared_task
def generate_upload_starsticker():
    """Main script

    Generates and uploads image"""
    # Image generation
    star_generator = StarStickerGenerator()
    generator_data = star_generator.Generate()
    if generator_data['saved']:
        # Tweet
        twitter_api = TwitterAPI()
        twitter_data = twitter_api.PostImage(
            status_text="#starstickersforeverything Markov state: " + str(generator_data['markov_state']))
        if twitter_data['posted']:
            data = {
                'date': str(timezone.now()),
                'user': twitter_data['user'],
                'sentence': generator_data['sentence'],
                'markov_state': generator_data['markov_state']
            }
            thread = Thread(target=send_email_notification, args=(data,))
            thread.start()
            GeneratedImage.objects.create(sentence=data['sentence'])
            return True
        else:
            False
    else:
        return False


@shared_task
def generate_corpus(reset=True):
    """Generates corpus.txt

    Reset True will clean corpus.txt otherwise downloaded comments will append"""
    a = RedditAPI()
    if a.SaveComments('toastme', 100, 'new', 'all', reset):
        return True
    else:
        return False


class IndexTemplateView(TemplateView):
    template_name = 'index.html'

    def get_domain(self):
        current_site_domain = Site.objects.get_current().domain
        return current_site_domain

    def get(self, request, *args, **kwargs):
        secret_code_form = SecretCodeForm()
        domain = self.get_domain()
        args = {
            'secret_code_form': secret_code_form,
            'domain': domain,
        }
        return render(request, self.template_name, args)

    def post(self, request):
        if 'secret_code-btn' in request.POST:
            secret_code_form = SecretCodeForm(request.POST)
            if secret_code_form.is_valid():
                secret_code = secret_code_form.cleaned_data['secret_code']
                if secret_code == 4.20:
                    thread = Thread(target=generate_upload_starsticker)
                    thread.start()
                    return render(request=self.request, template_name='successfully_posted.html')
        return render(request=self.request, template_name='oops.html')


class GenerateCorpusTemplateView(TemplateView):
    template_name = 'generate_corpus.html'

    def get_domain(self):
        current_site_domain = Site.objects.get_current().domain
        return current_site_domain

    def get(self, request, *args, **kwargs):
        secret_code_form = SecretCodeForm()
        domain = self.get_domain()
        last_corpus_record = None
        last_update = None
        comments_count = 0
        exception_count = 0
        try:
            last_corpus_record = CorpusRecord.objects.latest('created_at')
            comments_count = last_corpus_record.comments_count
            exception_count = last_corpus_record.exception_count
            last_update = last_corpus_record.updated_at
        except:
            pass
        args = {
            'secret_code_form': secret_code_form,
            'domain': domain,
            'last_update': str(last_update),
            'comments_count': comments_count,
            'exception_count': exception_count,
        }
        return render(request, self.template_name, args)

    def post(self, request):
        reset = False
        if 'reset-and-generate-btn' in request.POST:
            reset = True
        elif 'reset-btn' in request.POST:
            pass
        secret_code_form = SecretCodeForm(request.POST)
        if secret_code_form.is_valid():
            secret_code = secret_code_form.cleaned_data['secret_code']
            if secret_code == 4.20:
                thread = Thread(target=generate_corpus, args=(reset,))
                thread.start()
                return render(request=self.request, template_name='successfully_generated.html')
        return render(request=self.request, template_name='oops.html')
