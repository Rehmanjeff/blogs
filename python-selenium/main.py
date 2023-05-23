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

    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=options)
    driver.get(data['url'])

    paras = driver.find_elements("xpath", "//div[contains(@class, 'djm8--paragraph')]//p")
    for para in paras:
        text += para.get_attribute("innerHTML")
    
    soup = BeautifulSoup(text, "html.parser")
    text = textCleaner(soup.get_text())
    words = (wordCounter(text) * 2) + 50

    reword_api = RewordAPI(API_KEY)
    paragraph = 'use synonyms of all words possible and rephrase it so it does not sound plagiarised.'+text
    reworded_paragraph = reword_api.reword_paragraph(paragraph, words)
    return reworded_paragraph['choices'][0]['text']