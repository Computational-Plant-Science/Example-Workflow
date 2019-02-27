from django.http.response import HttpResponse

import workflows.views as views

from .forms import CreateJobForm

class Analyze(views.AnalyzeCollection):
    app_name = "count_objects"
    form_class = CreateJobForm
