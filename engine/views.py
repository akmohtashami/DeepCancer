from Bio.PDB.Model import Model
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views import View

from engine.forms import RequestRunForm
from engine.models import ModelRun, ModelRunStatus, ModelRunOutput

__all__ = ["RequestRun", "RunResult", "RunOutputDownload"]


class RequestRun(View):
    def render_form(self, request, form):
        return render(request, "engine/request_run.html", context={
            "form": form
        })

    def get(self, request):
        form = RequestRunForm()
        return self.render_form(request, form)

    def post(self, request):
        form = RequestRunForm(request.POST, request.FILES)
        if form.is_valid():
            run = form.save()
            run.execute()
            return HttpResponseRedirect(reverse("engine:run_result", kwargs={
                "uid": run.uid
            }))
        return self.render_form(request, form)


class RunResult(View):
    def get(self, request, uid):
        run = ModelRun.objects.get(uid=uid)
        downloadable_outputs = run.outputs.filter(show_download_link=True)
        include_outputs = run.outputs.filter(include_in_results_page=True)
        included_data = ""
        for output in include_outputs:
            included_data += output.file.read().decode("utf-8")
        return render(request, "engine/run_result.html", context={
            "run": run,
            "statuses": ModelRunStatus,
            "downloadable_outputs": downloadable_outputs,
            "included_data": included_data,
        })


class RunOutputDownload(View):
    def get(self, request, uid, filename):
        output_file = get_object_or_404(ModelRunOutput, run__uid=uid, name=filename)
        # TODO: Use nginx sendfile
        response = HttpResponse(output_file.file)
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        return response