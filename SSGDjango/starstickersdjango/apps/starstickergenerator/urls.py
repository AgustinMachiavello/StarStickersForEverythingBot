from django.urls import path, include

# Views
from .views import IndexTemplateView,GenerateCorpusTemplateView

# Static
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('generateandupload/', IndexTemplateView.as_view(), name='index'),
    path('generatecorpus/', GenerateCorpusTemplateView.as_view(), name='generatecorpus')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
