# yourapp/management/commands/scrape_keywords.py
from django.core.management.base import BaseCommand
from scraper.views import fetch_all_keywords  # Update with your actual app name

class Command(BaseCommand):
    help = 'Fetch keywords and their results'

    def handle(self, *args, **kwargs):
        fetch_all_keywords()
