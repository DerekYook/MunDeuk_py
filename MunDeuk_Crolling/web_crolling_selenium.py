# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
#
# # Chrome 브라우저를 사용한 Selenium
# driver = webdriver.Chrome()
# # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#
# # 웹 페이지 로드
# driver.get('https://emart.ssg.com/express/freqbuy.ssg')
#
# # JavaScript가 실행된 후의 페이지에서 요소 찾기
# # 사용안됨
# # unit_prices = driver.find_elements_by_class_name('unit-price')
#
# # unit_prices = driver.find_elements(By.CLASS_NAME, 'unit-price')
# # print(unit_prices)
# #
# # for price in unit_prices:
# #     print(price.text)
#
# # 페이지 로딩이 완료될 때까지 대기
# WebDriverWait(driver, 10).until(
#     lambda x: x.execute_script("return document.readyState") == "complete"
# )
#
# # JavaScript 코드 실행하여 freqBuyService 값을 가져옴
# freq_buy_service = driver.execute_script("return freqBuyService;")
#
# # freq_buy_service 내용 출력
# print(freq_buy_service)
#
#
# # 브라우저 닫기
# driver.quit()


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# 크롬 드라이버 설정
driver = webdriver.Chrome()
# service = Service(ChromeDriverManager(chrome_type="google").install())
# options = webdriver.ChromeOptions()
# driver = webdriver.Chrome(service=service, options=options)

try:

    # 웹페이지 로드
    # driver.get("https://emart.ssg.com/express/freqbuy.ssg")
    driver.get("https://emart.ssg.com/search.ssg?target=all&query=rice")

    # 페이지가 로드될 때까지 대기
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "emitem_info"))
    )

    # time.sleep(30)

    # 모든 `mnemitem_grid_lst` 요소 찾기
    grid_elements = driver.find_elements(By.CLASS_NAME, "mnemitem_grid_item")

    # 각 그리드 요소 내에서 필요한 정보 추출
    for grid in grid_elements:
        try:
            # 브랜드명 추출
            brand_element = grid.find_element(By.CLASS_NAME, 'mnemitem_goods_brand')
            brand = brand_element.text.strip()
            if brand == "":
                brand = "브랜드 정보 없음"

        except:
            brand = "브랜드 정보 없음"

        try:
            # 상품명 추출
            title_element = grid.find_element(By.CLASS_NAME, 'mnemitem_goods_tit')
            title = title_element.text.strip()
            if title == "":
                title = "상품명 정보 없음"
        except:
            title = "상품명 정보 없음"

        try:
            # 가격 추출
            price_element = grid.find_element(By.CLASS_NAME, 'ssg_price')
            price = price_element.text.strip()
            if price == "":
                price = "가격 정보 없음"
        except:
            price = "가격 정보 없음"

        try:
            # 단위 가격 추출
            unit_price_element = grid.find_element(By.CLASS_NAME, 'unit_price')
            unit_price = unit_price_element.text.strip()
            if unit_price == "":
                unit_price = "단위 가격 정보 없음"
        except:
            unit_price = "단위 가격 정보 없음"

        # 추출한 데이터 출력
        print(f"브랜드명: {brand}")
        print(f"상품명: {title}")
        if price == "가격 정보 없음":
            print(f"가격: {price}")
        else:
            print(f"가격: {price}원")
        print(f"단위 가격: {unit_price}")
        print("------------------------------")

finally:

    # 브라우저 닫기
    driver.quit()
