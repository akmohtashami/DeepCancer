import os
import uuid
from enum import IntEnum
from enumfields import EnumField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from engine import tasks


class ModelRunStatus(IntEnum):
    PENDING = 0
    RUNNING = 1
    FINISHED = 2
    FAILED = 3


class ModelRun(models.Model):

    def get_input_file_name(instance, filename):
        return str(instance.uid)

    uid = models.UUIDField(verbose_name=_("uid"), default=uuid.uuid4, editable=False, unique=True, db_index=True)
    email = models.EmailField(verbose_name=_("email"))
    input_file = models.FileField(verbose_name=_("input file"), upload_to=get_input_file_name)
    task_id = models.CharField(verbose_name=_("celery task id"), max_length=100, null=True)
    status = EnumField(ModelRunStatus, verbose_name=_("status"), default=ModelRunStatus.PENDING)

    def execute(self):
        self.task_id = tasks.run_model.delay(self.id).id
        self.save()


class ModelRunOutput(models.Model):
    run = models.ForeignKey(ModelRun, related_name="outputs", verbose_name=_("run"), on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_("name"), max_length=255)
    file = models.FileField(verbose_name=_("file"))
    show_download_link = models.BooleanField(verbose_name=_("show download link"), default=True, null=False)
    include_in_results_page = models.BooleanField(verbose_name=_("include in results page"),default=False, null=False)

    class Meta:
        unique_together = (("run", "name"), )
        ordering = ("run", "name")

    def get_file_size(self):
        return os.path.getsize(self.file.path)