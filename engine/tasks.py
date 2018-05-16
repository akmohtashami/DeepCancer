import logging

from django.core.files import File
from django.db import transaction
from celery import current_app as app
from celery.signals import celeryd_init

from engine import models
from neural_net import Network
import shutil
import tempfile
import os


neural_net = None
logger = logging.getLogger(__name__)


@celeryd_init.connect
def load_network(**kwargs):
    global neural_net
    neural_net = Network()


@app.task
def run_model(id):
    with transaction.atomic():
        run = models.ModelRun.objects.select_for_update().get(id=id)
        if run.status != models.ModelRunStatus.PENDING:
            return
        run.status = models.ModelRunStatus.RUNNING
        run.save()
    logger.info("Started running request {}".format(id))
    run = models.ModelRun.objects.get(id=id)
    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_path = os.path.join(tmp_dir, "input")
            shutil.copy(run.input_file.path, input_path)
            logger.debug("Input file copied to {}\n".format(input_path))
            outputs = neural_net.run(tmp_dir)
            if outputs is None:
                logger.warning("No output provided")
            elif not isinstance(outputs, list):
                logger.error("Output should be a list. ")
            else:
                for tup in outputs:
                    if len(tup) == 2:
                        name, path = tup
                        link = True
                        incl = False
                    elif len(tup) == 4:
                        name, path, link, incl = tup
                    else:
                        logger.warning("Invalid output specification. Ignored")
                        continue
                    with open(path, 'rb') as file_:
                        run_output = models.ModelRunOutput(
                            run=run,
                            name=name,
                            show_download_link=link,
                            include_in_results_page=incl
                        )
                        run_output.file.save(name, File(file_))
                        run_output.save()
                        logger.debug("Output {} copied to storage from {}".format(name, path))
            run.status = models.ModelRunStatus.FINISHED
    except Exception as e:
        logger.exception(e)
        run.status = models.ModelRunStatus.FAILED
    run.task_id = None
    run.save()
    logger.info("Finished running request {}".format(id))
