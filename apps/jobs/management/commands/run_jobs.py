import time

from django.core.management.base import BaseCommand

from config.settings.env import GracefulShutdown


class Command(BaseCommand):
    help = "Run the background job worker (DB-backed outbox processor)"

    def handle(self, *args: object, **options: object) -> None:
        GracefulShutdown.register()
        self.stdout.write(self.style.SUCCESS("Job worker started. Waiting for jobs..."))
        # Stub: will be implemented in PR 7 (job runner + payment verification)
        while not GracefulShutdown.should_stop:
            time.sleep(10)
        self.stdout.write(self.style.WARNING("Job worker received shutdown signal. Exiting."))
