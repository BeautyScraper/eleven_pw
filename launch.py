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
    

def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False)
    # user_data_dir = Path(rf'{profile_dir}\{userid}')
    

    url = "https://elevenlabs.io/hi"

    # browser = playwright.firefox.launch_persistent_context(user_data_dir,headless= not to_download)
    for subdir in dirpath.iterdir():
        if subdir.is_dir():
            frags = [file for file in subdir.iterdir() if file.suffix.lower() in ['.txt']]
            # video = next((file for file in subdir.iterdir() if file.suffix.lower() in ['.mp4', '.avi', '.mkv', '.gif']), None)
            for texts in frags:
                with texts.open('r', encoding='utf-8') as f:
                    content = f.read()
                    print(content)  # You can process the content as needed
                mainparse(url, browser, content,str(download_dir /subdir.name/ texts.stem)+'.mp3')

    

with sync_playwright() as playwright:
    run(playwright)