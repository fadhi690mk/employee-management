# Create a file named update_notifications.py in your app's management/commands directory
# app_name/management/commands/update_notifications.py

from django.core.management.base import BaseCommand
from manager.models import Notifications
from django.utils import timezone

class Command(BaseCommand):
    help = 'Update outdated status of notifications based on auto_delete option'

    def handle(self, *args, **options):
        notifications = Notifications.objects.all()

        for notification in notifications:
            notification.set_outdated_status()
            notification.save()

        self.stdout.write(self.style.SUCCESS('Successfully updated outdated status for notifications.'))
