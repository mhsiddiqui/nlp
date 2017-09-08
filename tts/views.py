# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import subprocess
import os
import uuid
from ipware.ip import get_ip
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from tts.models import GeneratedVoice
from nlp.settings import BASE_DIR, FESTIVALDIR
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import TemplateView

from tts.text_processor.processor import get_processed_data


def run_shell_command(command):
    return subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).stdout.read()

#
# class IndexPage(TemplateView):
#     template_name = 'tts/index.html'


class TTSPage(TemplateView):
    template_name = 'tts/tts.html'


class GenerateVoice(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(GenerateVoice, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        uuid_str = str(uuid.uuid4())
        self.delete_old_generated_voice()
        text_input_file = self.save_input_in_file(request.POST.get('text'), uuid_str)
        generated_voice = self.generate_voice(text_input_file, uuid_str)
        saved_obj = self.save_file_to_db(generated_voice, request.POST.get('text'))
        self.delete_temp_files(text_input_file, generated_voice)
        return render(request, template_name='tts/voice_demo.html', context={'generated': saved_obj})

    def save_input_in_file(self, txt, uuid_str):
        file_with_path = '%s/input/input_%s.txt' % (os.path.join(BASE_DIR, 'tmp'), uuid_str)
        with open(file_with_path, 'w+') as f:
            txt = get_processed_data(txt)
            f.write(txt.encode('utf8'))
        return file_with_path

    def generate_voice(self, file_with_path, uuid_str):
        output_file = 'out_%s.wav' % uuid_str
        command_data = {
            'path': BASE_DIR,
            'output_file': output_file,
            'input_file': file_with_path
        }
        command = FESTIVALDIR + '/bin/text2wave -o {path}/tmp/output/{output_file} {input_file}'.format(**command_data)
        command_output = run_shell_command(command)
        return '%s/tmp/output/%s' % (BASE_DIR, output_file)

    def save_file_to_db(self, file_path, text):
        file = open(file_path)
        generated_voice = GeneratedVoice.objects.create(
            text=text,
            ip=get_ip(self.request)
        )
        generated_voice.file.save('out.wav', file)
        return generated_voice

    def delete_temp_files(self, input_file, output_file):
        os.remove(input_file)
        os.remove(output_file)

    def delete_old_generated_voice(self):
        GeneratedVoice.objects.filter(ip=get_ip(self.request)).delete()



