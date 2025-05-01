import random
import shutil
from playwright.sync_api import Playwright, sync_playwright, expect
from pathlib import Path
from scrapy.http import HtmlResponse
from time import sleep
import re
import json
from os import listdir
from os.path import isdir, join

userid = r'sstico0'
to_download = False
dirpath = Path(r'story_fragments')
download_dir = Path(r'downloads')

def mainparse(urlt : str, context, content,filepath) -> None:
    page = context.new_page()
    page.goto(urlt)
    
    # breakpoint()
    page.get_by_placeholder("ElevenLabs वॉइस जनरेटर 32 भाषाओं में हाई क्वालिटी वाली, इंसान जैसी आवाज़ प्रदान कर सकता है। ऑडियोबुक्स, वीडियो वॉइसओवर्स, विज्ञापनों और अन्य के लिए उपयुक्त").click()
    page.get_by_placeholder("ElevenLabs वॉइस जनरेटर 32 भाषाओं में हाई क्वालिटी वाली, इंसान जैसी आवाज़ प्रदान कर सकता है। ऑडियोबुक्स, वीडियो वॉइसओवर्स, विज्ञापनों और अन्य के लिए उपयुक्त").press("Control+a")
    page.get_by_placeholder("ElevenLabs वॉइस जनरेटर 32 भाषाओं में हाई क्वालिटी वाली, इंसान जैसी आवाज़ प्रदान कर सकता है। ऑडियोबुक्स, वीडियो वॉइसओवर्स, विज्ञापनों और अन्य के लिए उपयुक्त").fill(content)
    page.locator("[id^=\"radix-\"][id$=\"-content-tts\"]").get_by_role("button", name="Play").click()
    with page.expect_download() as download_info:
        page.get_by_label("Download generated speech").click()
    download = download_info.value
    download.save_as(filepath)
    page.wait_for_timeout(10000)
    page.close()

def get_working_proxy(playwright,proxies):
        while True:
            selected_proxy = random.choice(proxies)
            print(f"Testing proxy: {selected_proxy}")
            try:
                test_browser = playwright.firefox.launch(headless=True, proxy={"server": selected_proxy})
                test_context = test_browser.new_context()
                test_page = test_context.new_page()
                test_page.goto("https://httpbin.org/ip", timeout=10000)
                print("Proxy is working:", test_page.content())
                test_browser.close()
                return selected_proxy
            except Exception as e:
                print(f"Proxy {selected_proxy} failed: {e}")
                print("Trying a new proxy...")

def run(playwright: Playwright) -> None:
    # Load proxies from a file
    proxies_file = Path("proxies")
    with proxies_file.open("r", encoding="utf-8") as f:
        proxies = [line.strip() for line in f if line.strip()]
    
    # Select a random proxy
    selected_proxy = random.choice(proxies)
    print(f"Using proxy: {selected_proxy}")
    # Test if the proxy is working
    
    browser = playwright.firefox.launch(headless=False, proxy={"server": get_working_proxy(playwright,proxies)})
    # user_data_dir = Path(rf'{profile_dir}\{userid}')
    

    url = "https://elevenlabs.io/hi"

    # browser = playwright.firefox.launch_persistent_context(user_data_dir,headless= not to_download)
    for subdir in dirpath.iterdir():
        if subdir.is_dir():
            frags = [file for file in subdir.iterdir() if file.suffix.lower() in ['.txt']]
            # video = next((file for file in subdir.iterdir() if file.suffix.lower() in ['.mp4', '.avi', '.mkv', '.gif']), None)
            for i,texts in enumerate(frags):
                output_file = Path(str(download_dir /subdir.name/ texts.stem)+'.mp3')
                if output_file.is_file():
                    continue
                if (i+1)%5 == 0:
                    browser.close()
                    browser = browser = playwright.firefox.launch(headless=False, proxy={"server": get_working_proxy(proxies)})
                with texts.open('r', encoding='utf-8') as f:
                    content = f.read()
                    print(content)
                    # You can process the content as needed
                mainparse(url, browser, content,str(output_file))

    

with sync_playwright() as playwright:
    run(playwright)