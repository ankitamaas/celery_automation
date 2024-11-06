import csv
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import Keyword, KeywordResult
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, LoginForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')  # Redirect to your home page
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('index.html')  # Redirect to your home page

def index(request):
    if request.method == "POST":
        fetch_all_keywords()  # Fetch keywords from the database
        return redirect('results')
    return render(request, 'index.html')

def fetch_all_keywords():
    keywords = Keyword.objects.all()  # Fetch all keywords from the database
    for keyword in keywords:
        if timezone.now() >= keyword.scheduled_time:
            keyword.status = "Completed"  # Update status to "in progress"
            keyword.save()  # Save status to the database
            fetch_results(keyword.keyword)  # Fetch results for each keyword
        else:
            keyword.status <= "Progress"  # Update status to "pending"
            keyword.save()  # Save status to the database

def fetch_results(keyword):
    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_driver_path = 'chromedriver.exe'  # Path to ChromeDriver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://www.google.com")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(keyword)
        search_box.submit()
        
        # Wait for results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.g"))
        )

        # Fetch only the first search result
        first_result = driver.find_element(By.CSS_SELECTOR, "div.g")
        
        try:
            link_element = first_result.find_element(By.CSS_SELECTOR, "a")
            url = link_element.get_attribute('href')
            position = 1  # First position
            page_number = 1  # Assuming we're only fetching the first page

            # Save the result in the database if it doesn't already exist
            if not KeywordResult.objects.filter(keyword__keyword=keyword, url=url).exists():
                KeywordResult.objects.create(
                    keyword=Keyword.objects.get(keyword=keyword), 
                    url=url, 
                    position=position, 
                    page_number=page_number
                )

        except Exception as e:
            print(f"Error fetching first result for {keyword}: {e}")

    finally:
        driver.quit()

def results(request):
    results = []
    seen_urls = set()
    for result in KeywordResult.objects.all():
        if result.url not in seen_urls:
            seen_urls.add(result.url)
            results.append(result)
    
    # Get the status of keywords
    keyword_statuses = {keyword.keyword: keyword.status for keyword in Keyword.objects.all()}

    return render(request, 'results.html', {'results': results, 'keyword_statuses': keyword_statuses})

def download_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="keyword_results.csv"'

    writer = csv.writer(response)
    writer.writerow(['Keyword', 'URL', 'Position', 'Page Number'])

    seen_urls = set()
    for result in KeywordResult.objects.all():
        if result.url not in seen_urls:
            seen_urls.add(result.url)
            writer.writerow([result.keyword.keyword, result.url, result.position, result.page_number])

    return response

def delete_all(request):
    KeywordResult.objects.all().delete()
    return redirect('results')


def check_and_send_true(request):
    # Iterate over all Keyword objects
    for keyword in Keyword.objects.all():
        # Check if the keyword status is 'completed' and scheduled time is in the past
        if keyword.status == 'completed' and keyword.scheduled_time < timezone.now():
            # Return a response indicating the task is complete
            return JsonResponse({'status': True})
        else:
            return JsonResponse({'status': False})

