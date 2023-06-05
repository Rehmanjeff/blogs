import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from reword import RewordAPI
import re
from bs4 import BeautifulSoup

# API key for OpenAI
API_KEY = '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'

def home():
    return ''

def wordCounter(text):

    words = text.split()
    return len(words)

def textCleaner(text):

    textt = re.sub(r'[^a-zA-Z0-9\s.]', '', text)
    return textt

def scrape(data):
    
    text = ''
    options = Options()
    options.add_experimental_option("detach", True)
    options.add_argument('--headless')

    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=options)
    driver.get(data['url'])

    paras = driver.find_elements("xpath", "//div[contains(@class, 'djm8--paragraph')]//p")
    for para in paras:
        text += para.get_attribute("innerHTML")
    
    soup = BeautifulSoup(text, "html.parser")
    text = textCleaner(soup.get_text())
    text = text.strip()
    words = (wordCounter(text) * 2) + 50

    title = driver.find_element("xpath", "//div[contains(@class, 'field--name-field-headline')]")
    response = {
        'title' : title.get_attribute("innerHTML")
    }

    reword_api = RewordAPI(API_KEY)
    paragraph = 'use synonyms of all words possible and rephrase it so it does not sound plagiarised.'+text
    reworded_paragraph = reword_api.reword_paragraph(paragraph, words)

    if 'choices' in reworded_paragraph:
        response['description'] = reworded_paragraph['choices'][0]['text']
        return response
    elif 'error' in reworded_paragraph:
        return reworded_paragraph['error']['code']
    else:
        return 'Unknown error'