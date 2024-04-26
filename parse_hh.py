import json

from bs4 import BeautifulSoup
from selenium import webdriver


def get_page_html(url=None):
    try:
        driver = webdriver.Edge()
        driver.get(url)
        page_html = driver.page_source
        driver.quit()

        return page_html
    except Exception as e:
        print(f"Ошибка при получении кода страницы: {e}")


def create_object_bs(html_content):
    return BeautifulSoup(html_content, features='lxml')


def get_max_num_page(soup):
    blocks = soup.find(class_="pager")

    page_list = [i.text for i in blocks.find_all(class_='bloko-button')]

    return page_list[-2]


def get_info_cards_page(soup):
    list_card_info = []

    cards = soup.find_all(class_='vacancy-serp-item__layout')

    for card in cards:
        try:
            link = card.find(class_='serp-item__title-link-wrapper').find(class_='bloko-link').get('href')
        except:
            link = None

        try:
            name_company = card.find(class_='bloko-link bloko-link_kind-tertiary').text
        except:
            name_company = None

        try:
            city = card.find(attrs={'data-qa': 'vacancy-serp__vacancy-address', 'class': 'bloko-text'}).text
        except:
            city = None

        try:
            salary_fork = card.find(class_='bloko-header-section-2').text
        except:
            salary_fork = None

        list_card_info.append([link, name_company, salary_fork, city])

    return list_card_info


def get_ingo_cards_pages(num_page=1):
    info_cards = []
    max_num_page = 0

    for i in range(0, num_page):
        html_content = get_page_html(
            url=f'https://spb.hh.ru/search/vacancy?L_save_area=true&text=Python%2C+django%2C+flask&search_field=name&search_field=company_name&search_field=description&excluded_text=&area=1&area=2&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=50&page={i}')
        soup = create_object_bs(html_content=html_content)

        if max_num_page == 0:
            max_num_page = int(get_max_num_page(soup=soup))
        list_card_info = get_info_cards_page(soup=soup)

        for card_info in list_card_info:
            info_cards.append(
                {
                    'card_link': card_info[0],
                    'name_company': card_info[1],
                    'salary_fork': card_info[2],
                    'city': card_info[3],
                }
            )

        info_cards.append(
            {
                'card_link': card_info[0],
                'name_company': card_info[1],
                'salary_fork': card_info[2],
                'city': card_info[3],
            }
        )

        if i >= max_num_page:
            break

    return info_cards


def write_contacts_to_csv(data, filename_write):
    with open(f'{filename_write}.json', 'w', encoding='utf-8') as f:
        for chunk in data:
            json.dump(chunk, f, ensure_ascii=False)
            f.write('')
