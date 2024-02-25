"""
Base Download runner

This module contains the DownloadRunnerBase class. 

The DownloadRunnerBase is responsible for running one of the downloader classes: JobDownloader or DaemonDownloader. If there are no jobids, then it runs the DaemonDownloader. 

It registers callbacks with the with the the Downloader that allow it to report "downloaded" or "pending" status back to the server.

Derived classses can avoid the complexities of threading contained in this class and the base downloader. They can register their own callbacks and know that they are running in the main thread. 

For an example of a derived class, see LoggingDownloadRunner.
"""

import json
import logging
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
 
from ciocore import api_client
from ciocore.downloader.job_downloader import JobDownloader
from ciocore.downloader.daemon_downloader import DaemonDownloader
from ciocore.downloader.log import LOGGER_NAME

STATUS_ENDPOINT = "/downloads/status"

STATUS_DOWNLOADED = "downloaded"
STATUS_PENDING = "pending"

logger = logging.getLogger(LOGGER_NAME)

callback_queue = Queue()


class DownloadRunnerBase(object):
    CLIENT_NAME = "DownloadRunnerBase"
 
    def __init__(self, jobids=None, location=None, **kwargs):

        if jobids:
            self.downloader = JobDownloader(jobids, **kwargs)
        else:
            self.downloader = DaemonDownloader(location, **kwargs)

        self.num_threads = kwargs.get("num_threads", 1)
        self.client = api_client.ApiClient()
        self.reporter = None

        # These callbacks are prefixed `base_` to avoid name collisions with derived classes.
        logger.debug("Assigning callbacks")
        self.downloader.on("start", self.base_on_start)
        self.downloader.on("start_task", self.base_on_start_task)
        self.downloader.on("file_done", self.base_on_file_done)
        self.downloader.on("task_done", self.base_on_task_done)
        self.downloader.on("done", self.base_on_done)

    def run(self):
        """
        Run the downloader.

        Start a reporter thread to report task status back to the server.
        """
        
        try:
            self.reporter = ThreadPoolExecutor(max_workers=self.num_threads)
            self.downloader.run()
        except Exception as exc:
            logger.exception("Error running downloader: %s", exc)
        finally:
            self.reporter.shutdown()

    def report_task_status(
        self, download_id, status=STATUS_DOWNLOADED, bytes_in_task=0
    ):
        # If the user interrupted the download, then we're just going to set the task status
        # back to pending to be safe. So what if they have to dl one or two files again?
        if self.downloader.interrupt_flag.is_set():
            status = STATUS_PENDING

        bytes_to_download = 0 if status == STATUS_DOWNLOADED else bytes_in_task

        data = {
            "download_id": download_id,
            "status": status,
            "bytes_downloaded": 0,
            "bytes_to_download": bytes_to_download,
        }
        json_data = json.dumps(data)

        self.client.make_request(STATUS_ENDPOINT, data=json_data, use_api_key=True)

        return data

    # Callbacks
    def base_on_start(self, evt):
        logger.debug("Starting download")

    def base_on_start_task(self, evt):
        logger.debug(
            "Starting task %s:%s",
            evt['job_id'],
            evt['task_id']
        )

    def base_on_file_done(self, evt):
        msg = f"File done {evt['job_id']}:{evt['task_id']}:{evt['filepath']}"
        if evt["error"]:
            msg += f" {evt['error']}"
        logger.debug(msg)

    def base_on_task_done(self, evt):
        if evt["preexisting"]:
            logger.debug(
                "Task already existed locally %s:%s",
                evt['job_id'],
                evt['task_id']
            )
            return
        future = self.reporter.submit(
            self.report_task_status,
            evt["download_id"],
            status=STATUS_DOWNLOADED,
            bytes_in_task=evt["size"],
        )
        future.add_done_callback(
            lambda f, job_id=evt["job_id"], task_id=evt["task_id"]: log_report_result(
                f.result(), job_id, task_id
            )
        )

    def base_on_done(self, evt):
        """
        When the job is done, check to see if any tasks were not completed.

        If we find any, then report them as pending.
        """
        logger.debug("Download done. Reporting remaining task statuses to server")
        with self.downloader.registry_lock:
            for job_id, job in evt["registry"].items():
                for task_id, task in job.items():
                    logger.debug("Checking registry task %s %s", job_id, task_id)
                    if task['completed_files'] < task['filecount']:
                        logger.warning(
                            "Task not completed %s:%s: %s/%s files.",
                            job_id,
                            task_id,
                            task['completed_files'],
                            task['filecount']
                        )

                        future = self.reporter.submit(
                            self.report_task_status,
                            task['download_id'],
                            status=STATUS_PENDING,
                            bytes_in_task=task['size'],
                        )
                        future.add_done_callback(
                            lambda f, job_id=job_id, task_id=task_id: log_report_result(f.result(), job_id, task_id)
                        )


def log_report_result(report_result, job_id, task_id):
    """Log the report.

    It's possible the report back to the server was changed by the report_task_status, for example
    if the user interrupted the download.

    For this reason we log the actual report result.
    """
    logger.info("Reported task to server: %s:%s %s (%s)", job_id, task_id, report_result["status"], report_result["download_id"])