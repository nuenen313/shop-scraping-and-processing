from playwright.sync_api import sync_playwright
import playwright
from datetime import datetime
import os
import requests
import re
import time


def scrapeImages(base_url, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(base_url)
        page_number = 1
        previous_page_content = None
        identical_page_count = 0
        downloaded_images = set()
        offers_processed=0
        hrefs=[]
        links_with_images = page.locator("a:has(img)")
        for i in range(links_with_images.count()):
            href = links_with_images.nth(i).get_attribute("href")
            hrefs.append(href)
        for href in hrefs:
            if href and ",biedronkowe-oszczdnoci" in href:
                print(f"Found offer link: {href}")
                date = re.findall(r'oferta-od-([\d-]+)', href)[0]
                date_range = "od-"+date
                datetime_object = datetime.strptime(date, '%d-%m')
                datetime_object = datetime_object.replace(year=datetime.now().year, hour=23, minute=59, second=59)
                date_range_shop = date_range + "-biedronka"
                specific_output_folder = os.path.join(output_folder, date_range_shop)
                os.makedirs(specific_output_folder, exist_ok=True)
                if offers_processed <= 2:
                    print("Accessing link")
                    page.wait_for_selector('body')
                    offers_processed += 1
                    while True:
                        if href.endswith("page=1"):
                            pagination_url = f"{href[:-1]}{page_number}"
                        else:
                            pagination_url = f"{href}#page{page_number}"
                        print(f"Attempting to scrape: {pagination_url}")
                        page.goto(pagination_url)
                        time.sleep(1)
                        page_number += 1
                        page.reload()
                        current_page_content = page.locator("div.embla_main").first.inner_html()

                        if previous_page_content and current_page_content == previous_page_content:
                            identical_page_count += 1
                            print(f"Identical content detected. Count: {identical_page_count}")
                        else:
                            identical_page_count = 0

                        if identical_page_count >= 2:
                            print("No new content found for 3 consecutive pages. Stopping.")
                            break

                        page.wait_for_selector("img.flex:not(.h-full)")
                        img_elements = page.locator('img.flex:not(.h-full)')
                        count = img_elements.count()
                        previous_page_content = current_page_content

                        for i in range(count):
                            img_url = img_elements.nth(i).get_attribute("src")
                            page_img = browser.new_page()
                            page_img.goto(img_url)
                            page_img.wait_for_selector("img")
                            time.sleep(1)
                            image_url = page_img.locator("img").get_attribute("src")
                            try:
                                if image_url not in downloaded_images:
                                    print(f"Downloading image {i + 1}: {image_url}")
                                    img_data = requests.get(image_url).content
                                    img_filename = os.path.join(specific_output_folder,
                                                                f'page_{page_number}_image_{i + 1}.jpg')

                                    with open(img_filename, 'wb') as img_file:
                                        img_file.write(img_data)
                                    print(f"Image {i + 1} saved successfully at {img_filename}")
                                    downloaded_images.add(image_url)

                            except Exception as e:
                                print(f"Failed to download {image_url}: {e}")

                            page_img.close()


def scrapeTaniWeekendImages(base_url, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(base_url)
        page_number = 1
        previous_page_content = None
        identical_page_count = 0
        downloaded_images = set()
        offers_processed=0
        hrefs=[]
        links_with_images = page.locator("a:has(img)")
        for i in range(links_with_images.count()):
            href = links_with_images.nth(i).get_attribute("href")
            hrefs.append(href)
        for href in hrefs:
            if href and ",tani-weekend" in href:
                print(f"Found offer link: {href}")
                date = re.findall(r'od-([\d-]+)', href)[0]
                date_range = "od-"+date
                datetime_object = datetime.strptime(date, '%d-%m')
                datetime_object = datetime_object.replace(year=datetime.now().year, hour=23, minute=59, second=59)
                date_range_shop = date_range + "-biedronka"
                specific_output_folder = os.path.join(output_folder, date_range_shop)
                os.makedirs(specific_output_folder, exist_ok=True)
                if offers_processed <= 2:
                    print("Accessing link")
                    page.wait_for_selector('body')
                    offers_processed += 1
                    while True:
                        if href.endswith("page=1"):
                            pagination_url = f"{href[:-1]}{page_number}"
                        else:
                            pagination_url = f"{href}#page{page_number}"
                        print(f"Attempting to scrape: {pagination_url}")
                        page.goto(pagination_url)
                        time.sleep(1)
                        page_number += 1
                        page.reload()
                        current_page_content = page.locator("div.embla_main").first.inner_html()

                        if previous_page_content and current_page_content == previous_page_content:
                            identical_page_count += 1
                            print(f"Identical content detected. Count: {identical_page_count}")
                        else:
                            identical_page_count = 0

                        if identical_page_count >= 2:
                            print("No new content found for 3 consecutive pages. Stopping.")
                            break

                        page.wait_for_selector("img.flex:not(.h-full)")
                        img_elements = page.locator('img.flex:not(.h-full)')
                        count = img_elements.count()
                        previous_page_content = current_page_content

                        for i in range(count):
                            img_url = img_elements.nth(i).get_attribute("src")
                            page_img = browser.new_page()
                            page_img.goto(img_url)
                            page_img.wait_for_selector("img")
                            time.sleep(1)
                            image_url = page_img.locator("img").get_attribute("src")
                            try:
                                if image_url not in downloaded_images:
                                    print(f"Downloading image {i + 1}: {image_url}")
                                    img_data = requests.get(image_url).content
                                    img_filename = os.path.join(specific_output_folder,
                                                                f'page_{page_number}_image_{i + 1}.jpg')

                                    with open(img_filename, 'wb') as img_file:
                                        img_file.write(img_data)
                                    print(f"Image {i + 1} saved successfully at {img_filename}")
                                    downloaded_images.add(image_url)

                            except Exception as e:
                                print(f"Failed to download {image_url}: {e}")

                            page_img.close()


def scrapeAlcoholImages(base_url, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(base_url)
        page_number = 1
        previous_page_content = None
        identical_page_count = 0
        downloaded_images = set()
        offers_processed = 0
        hrefs = []
        links_with_images = page.locator("a:has(img)")
        for i in range(links_with_images.count()):
            href = links_with_images.nth(i).get_attribute("href")
            hrefs.append(href)
        for href in hrefs:
            if href and ",alkohole" in href:
                print(f"Found offer link: {href}")
                date = re.findall(r'alkohole-p-([\d-]+)', href)[0]
                date_range = "od-" + date
                date_range_shop = "alkohole-" + date_range + "-biedronka"
                specific_output_folder = os.path.join(output_folder, date_range_shop)
                os.makedirs(specific_output_folder, exist_ok=True)
                if offers_processed <= 2:
                    print("Accessing link")
                    page.wait_for_selector('body')
                    offers_processed += 1
                    while True:
                        if href.endswith("page=1"):
                            pagination_url = f"{href[:-1]}{page_number}"
                        else:
                            print(href, "doesntendwith")
                            pagination_url = f"{href}#page={page_number}"
                        print(f"Attempting to scrape: {pagination_url}")
                        page.goto(pagination_url)
                        try:
                            if page.locator("button:has-text('Accept')").is_visible():
                                print("Cookie consent detected. Clicking 'Accept Cookies' button.")
                                page.locator("button:has-text('Accept')").click()
                                page.wait_for_timeout(1000)
                        except Exception as e:
                            print(f"Cookie consent form not found or failed to click: {e}")
                        try:
                            if page.locator("input#yes").is_visible():
                                print("Consent form detected. Clicking the 'Yes' button.")
                                page.locator("input#yes").click()
                                page.wait_for_timeout(1000)
                        except Exception as e:
                            print(f"Consent form not found or failed to click: {e}")
                        time.sleep(1)
                        page_number += 1
                        page.reload()
                        try:
                            current_page_content = page.locator("div.embla_main").first.inner_html()
                        except playwright._impl._errors.TimeoutError:
                            break
                        if previous_page_content and current_page_content == previous_page_content:
                            identical_page_count += 1
                            print(f"Identical content detected. Count: {identical_page_count}")
                        else:
                            identical_page_count = 0

                        if identical_page_count >= 3:
                            print("No new content found for 3 consecutive pages. Stopping.")
                            break

                        page.wait_for_selector("img.flex:not(.h-full)")
                        img_elements = page.locator('img.flex:not(.h-full)')
                        count = img_elements.count()
                        previous_page_content = current_page_content

                        for i in range(count):
                            img_url = img_elements.nth(i).get_attribute("src")
                            page_img = browser.new_page()
                            page_img.goto(img_url)
                            page_img.wait_for_selector("img")
                            time.sleep(1)
                            image_url = page_img.locator("img").get_attribute("src")
                            try:
                                if image_url not in downloaded_images:
                                    print(f"Downloading image {i + 1}: {image_url}")
                                    img_data = requests.get(image_url).content
                                    img_filename = os.path.join(specific_output_folder,
                                                                f'page_{page_number}_image_{i + 1}.jpg')

                                    with open(img_filename, 'wb') as img_file:
                                        img_file.write(img_data)
                                    print(f"Image {i + 1} saved successfully at {img_filename}")
                                    img_file.close()
                                    downloaded_images.add(image_url)

                            except Exception as e:
                                print(f"Failed to download {image_url}: {e}")
                            page_img.close()


output_directory = "C:\\Users\\Marta\\Desktop\\scrape"
base_url = "https://www.biedronka.pl/pl/gazetki"
scrapeImages(base_url, output_directory)
scrapeTaniWeekendImages(base_url, output_directory)
scrapeAlcoholImages(base_url, output_directory)
