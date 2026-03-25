import time

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run the background job worker (DB-backed outbox processor)"

    def handle(self, *args: object, **options: object) -> None:
        self.stdout.write(self.style.SUCCESS("Job worker started. Waiting for jobs..."))
        # Stub: will be implemented in PR 7 (job runner + payment verification)
        while True:
            time.sleep(10)
