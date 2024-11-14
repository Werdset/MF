import datetime

from django.core.management.base import BaseCommand

from MuscleFeed_main.models import Order
from MuscleFeed_main.views import send_whatsapp_message


class Command(BaseCommand):
    help = 'Sending info message to clients WhatsApp before 2 days when order finished'

    def handle(self, *args, **options):
        two_days_after_today = datetime.date.today() + datetime.timedelta(days=2)
        for order in Order.objects.filter(last_date=two_days_after_today):
            frozen_from = False
            frozen_to = False
            if order.freezes.filter(finished=False):
                freeze_last = order.freezes.get(finished=False)
                frozen_from = freeze_last.frozen_from
                if freeze_last.frozen_to:
                    if freeze_last.frozen_to <= datetime.date.today():
                        freeze_last.finished = True
                        freeze_last.save()
                        order.save()
                        frozen_from = False
                        frozen_to = False
                    else:
                        frozen_to = freeze_last.frozen_to
            frozen = False
            if frozen_from:
                if datetime.date.today() >= frozen_from:
                    frozen = True
            if not frozen:
                send_whatsapp_message('client_order_before_2_days_to_finish', order.phone, order)