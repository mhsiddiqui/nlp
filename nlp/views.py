# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import subprocess

from django.views.generic import TemplateView


def run_shell_command(command):
    return subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).stdout.read()


class IndexPage(TemplateView):
    template_name = 'index.html'
