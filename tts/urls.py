from django.conf.urls import url

from nlp.views import GenerateVoice, IndexPage, TTSPage

urlpatterns = [
    url(r'^$', IndexPage.as_view()),
    url(r'^tts/$', TTSPage.as_view()),
    url(r'^tts/demo/$', GenerateVoice.as_view()),
]
