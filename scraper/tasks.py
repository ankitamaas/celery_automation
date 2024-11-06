# Start of Selection
import logging

logger = logging.getLogger(__name__)

from celery import shared_task
from .models import Keyword, KeywordResult
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@shared_task
def fetch_results_task():
    keywords = Keyword.objects.filter(status='pending')
    if keywords.exists:
        for keyword in keywords:
            fetch_results(keyword)

def fetch_results(keyword):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    # chrome_driver_path = '/Users/harsimran/Desktop/celery automation/chromedriver.exe'  # Path to ChromeDriver
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://www.google.com")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(keyword.keyword)
        search_box.submit()

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.g"))
        )

        first_result = driver.find_element(By.CSS_SELECTOR, "div.g")
        link_element = first_result.find_element(By.CSS_SELECTOR, "a")
        url = link_element.get_attribute('href')

        if not KeywordResult.objects.filter(keyword=keyword, url=url).exists():
            KeywordResult.objects.create(
                keyword=Keyword.objects.get(keyword=keyword),
                url=url,
                position=1,
                page_number=1
            )
        keyword.status = 'completed'
        keyword.save()

    except Exception as e:
        logger.error(f"Error fetching result: {e}")

    finally:
        logger.info(f"Done fetching result")
        driver.quit()
