import requests
from bs4 import BeautifulSoup

# 크롤링할 웹페이지 URL
url = 'https://emart.ssg.com/express/freqbuy.ssg'

# 웹페이지 요청
response = requests.get(url)

# 요청이 성공했는지 확인
if response.status_code == 200:
    # HTML 파싱
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup)

    # soup 객체를 문자열로 변환
    html_str = str(soup)

    # 문자열을 텍스트 파일로 저장
    with open('output.html', 'w', encoding='utf-8') as file:
        file.write(html_str)

    # # 예시: 모든 <div> 태그를 찾고 출력하기
    # div_tags = soup.find_all('div')
    # for tag in div_tags:
    #     print(tag.get_text())

    # 'unit-price' 클래스를 가진 모든 요소 찾기
    # unit_price_elements = soup.find_all(class_='cdtl_txt_info hide_gl')
    #
    # # 찾은 요소의 텍스트 출력
    # for element in unit_price_elements:
    #     print(element.get_text())
    #
    # # 텍스트 파일 열기
    # with open('output.txt', mode='w', encoding='utf-8') as file:
    #     for tag in unit_price_elements:
    #         file.write(tag.get_text() + '\n')
    #
    # print("Data has been saved to output.txt")

else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")