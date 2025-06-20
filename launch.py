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
import requests

userid = r'sstico0'
to_download = False
dirpath = Path(r'story_fragments')
download_dir = Path(r'downloads')
use_proxies = False
headless_flag = True

def mainparse(urlt : str, context, content,filepath) -> None:
    page = context.new_page()
    page.goto(urlt)
    sleep(3)
    page.get_by_role("radio", name="Lily कथा-वाचन").click()
    sleep(1)
    ttsbox = page.get_by_placeholder("ElevenLabs वॉइस जनरेटर 32 भाषाओं में हाई क्वालिटी वाली, इंसान जैसी आवाज़ प्रदान कर सकता है। ऑडियोबुक्स, वीडियो वॉइसओवर्स, विज्ञापनों और अन्य के लिए उपयुक्त")
    ttsbox.fill(content)
    # tts_content = ttsbox.input_value()
    # breakpoint()
    while(ttsbox.input_value() != content):
        sleep(1)
    # print(f"TTS Box Content: {tts_content}")
    # breakpoint()
    # ttsbox.click()
    # sleep(1)
    # ttsbox.press("Control+a")
    # sleep(1)
    # sleep(1)
    page.locator("[id^=\"radix-\"][id$=\"-content-tts\"]").get_by_role("button", name="Play").click()
    sleep(1)
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
                test_browser = playwright.firefox.launch(headless=headless_flag, proxy={"server": selected_proxy})
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
    proxies = []
    if proxies_file.exists():
        with proxies_file.open("r", encoding="utf-8") as f:
            proxies = [line.strip() for line in f if line.strip()]
    
    browser = None
    if use_proxies and proxies:
        proxy_server = get_working_proxy(playwright, proxies)
        browser = playwright.firefox.launch(headless=headless_flag, proxy={"server": proxy_server})
    else:
        browser = playwright.chromium.launch(headless=headless_flag, ignore_default_args=["--mute-audio"])
    
    url = "https://elevenlabs.io/hi"

    for subdir in dirpath.iterdir():
        if subdir.is_dir():
            frags = [file for file in subdir.iterdir() if file.suffix.lower() in ['.txt']]
            for i, texts in enumerate(frags):
                print(i)
                output_file = Path(str(download_dir / subdir.name / texts.stem) + '.mp3')
                if output_file.is_file():
                    continue
                if use_proxies and proxies and (i + 1) % 5 == 0:
                    browser.close()
                    proxy_server = get_working_proxy(playwright, proxies) if use_proxies else None
                    browser = playwright.firefox.launch(
                        headless=headless_flag, 
                        proxy={"server": proxy_server} if proxy_server else None,
                        ignore_default_args=["--mute-audio"]
                    )
                with texts.open('r', encoding='utf-8') as f:
                    content = f.read()
                    print(content)
                try:
                    mainparse(url, browser, content, str(output_file))
                except Exception as e:
                    browser.close()
                    requests.get("https://trigger.macrodroid.com/5dcb4727-67fd-4414-bb15-0e6020ee08e1/reseti")
                    print(f"Error processing {texts}: {e}")
                    sleep(50)
                    browser = playwright.chromium.launch(headless=headless_flag, ignore_default_args=["--mute-audio"])
                    try:
                        mainparse(url, browser, content, str(output_file))
                    except Exception as e:
                        pass
                    # if not use_proxies:
                    #     browser.close()
                    #     break
                        

    

with sync_playwright() as playwright:
    run(playwright)