from django.conf.urls import url

from tts.views import GenerateVoice, TTSPage

urlpatterns = [
    # url(r'^$', IndexPage.as_view()),
    url(r'^$', TTSPage.as_view()),
    url(r'^demo/$', GenerateVoice.as_view()),
]
