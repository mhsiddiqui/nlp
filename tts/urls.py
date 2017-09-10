from django.conf.urls import url

from tts.views import GenerateVoice, TTSPage, DemoPage

urlpatterns = [
    # url(r'^$', IndexPage.as_view()),
    url(r'^$', TTSPage.as_view(), name='tts-page'),
    url(r'^demo/$', DemoPage.as_view(), name='tts-demo'),
    url(r'^generate/voice/$', GenerateVoice.as_view(), name='generate-tts-voice'),
]
