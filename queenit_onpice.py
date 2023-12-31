from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time
import csv
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException

class QueenitCrawling:    
    @staticmethod
    def queenit_crawling(url, path_input):
        driver = webdriver.Chrome()
        path = os.path.join(path_input, 'result')

        if not os.path.exists(path):
            os.makedirs(path)


        driver.get(url)

        # 앱 다음에 받기 닫기 버튼 클릭
        try:
            close_iwillgetapplater_button = driver.find_element(By.XPATH, "/html/body/div/div/div[3]/button[1]")
            driver.execute_script("arguments[0].click();", close_iwillgetapplater_button)
            print("잠깐! 웹으로 보고 계신가요? 닫아짐.")
            time.sleep(10)
        except NoSuchElementException:
            print("앱 다음에 받기 버튼을 찾지 못함ㅠ")

        # 원피스 클릭
        upper_button = driver.find_element(By.XPATH, "/html/body/div/div/div/div/div/div/div[5]/div[2]/div")
        driver.execute_script("arguments[0].click();", upper_button)
        print("원피스 클릭.")
        time.sleep(10)


        for _ in range(200):
            driver.execute_script("window.scrollTo(10, document.body.scrollHeight);")
            time.sleep(7)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # 상품 저장할 리스트 생성
        products = []

        # 이미지 URL을 중복 없이 저장하기 위한 set
        image_urls = set()

        #찾을 div
        product_blocks = soup.find_all('div', class_='css-7ny53m')

        # 이미지 다운로드 횟수 제한
        max_images = 1100
        images_downloaded = 0

        for block in product_blocks:
            if images_downloaded >= max_images:
                break

            name_element = block.find('span', class_='MuiTypography-BodyS')
            name = name_element.find('div', class_='MuiBox-root').text.strip()
            
            price_element = block.find('span', class_='MuiTypography-LabelM')
            price = price_element.find('div', class_='MuiBox-root').text.strip()

            rating_element = block.find('span', class_='MuiTypography-LabelXS')
            rating = rating_element.find('div', class_='MuiBox-root').text.strip() if rating_element else ""
            

            # 이미지 URL 추출 - 두 번째 <img> 태그 선택
            img_elements = block.find_all('img')
            image_url = ""
            for img_element in img_elements:
                if "https://" in img_element['src']:
                    image_url = img_element['src']
                    break
            
            if not image_url:
                continue

            if image_url and image_url not in image_urls:
                products.append({
                    'Name': name,
                    'Price': price,
                    'Rating': rating,
                    'ImageURL': image_url
                })
                image_urls.add(image_url)
                images_downloaded += 1
                time.sleep(2)
            

        # CSV 파일로 상품 정보 저장
        csv_path = os.path.join(path, 'queenit_crawl_onpice.csv')
        with open(csv_path, 'w', newline='', encoding='cp949') as csvfile:
            fieldnames = ['Name', 'Price', 'Rating', 'ImageURL']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(products)


if __name__ == '__main__':
    url = 'https://web.queenit.kr/'
    path_input = r'C:\Users\kwon\Desktop\crawling_project'
    QueenitCrawling.queenit_crawling(url, path_input)
