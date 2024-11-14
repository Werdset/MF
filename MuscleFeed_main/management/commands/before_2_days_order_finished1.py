from django.core.management.base import BaseCommand

from MuscleFeed_main.models import Order
from MuscleFeed_main.views import send_whatsapp_message


class Command(BaseCommand):
    help = 'Sending info message to clients WhatsApp before 2 days when order finished'

    def handle(self, *args, **options):
        send_whatsapp_message('client_order_before_2_days_to_finish', '79032344882', Order.objects.filter(is_completed=True)[0])