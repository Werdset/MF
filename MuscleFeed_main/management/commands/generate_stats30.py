import os
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import Avg
from django.utils import timezone

from MuscleFeed_main.models import Profile, Order, StatsPeriod


class Command(BaseCommand):
    help = 'Generate stats for 30 days'

    def handle(self, *args, **options):
        for i in range(30):
            now = timezone.now()-timedelta(days=30)+timedelta(days=i)
            profiles = Profile.objects.filter(status='active', is_moderator=False)
            orders = Order.objects.filter(is_completed=True)
            avg_price = orders.aggregate(Avg('price'))['price__avg']
            if not avg_price:
                avg_price = 0
            income = avg_price*len(orders)
            last_stats = {
                'profiles': 0,
                'orders': 0,
                'income': 0,
            }
            if StatsPeriod.objects.all():
                last_stats_period = StatsPeriod.objects.all().order_by('-id')[0]
                last_stats = {
                    'profiles': last_stats_period.profiles,
                    'orders': last_stats_period.orders,
                    'income': last_stats_period.income,
                }
            StatsPeriod.objects.create(
                date=now,
                profiles=len(profiles),
                profiles_change=len(profiles)-last_stats['profiles'],
                orders=len(orders),
                orders_change=len(orders)-last_stats['orders'],
                avg_price=avg_price,
                income=income,
                income_change=income-last_stats['income']
            )

