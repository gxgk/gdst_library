import re
import config
import logging
import base64
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def base64_encode(text):
    return bytes.decode(base64.b64encode(str.encode(text)))


def search_book(keyword, page, book_type=1):
    """
    图书馆找书
    :param keyword:
    :param page:
    :param book_type:  1.题名 4.作者 6.主题词 5.ISBN
    :return:
    """
    payloads = {
        "kw": keyword,
        "searchtype": book_type,
        "xc": 3,
        "page": page
    }
    try:
        res = requests.get(config.LIBRARY_SEARCH_URL, params=payloads, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        num_text = soup.find("header").getText().strip()
    except Exception as e:
        logger.warning(u'图书馆检索图书失败，关键词:%s，错误信息:%s' % (keyword, e))
        return {'code': 502, 'msg': '图书馆服务器连接出错，请重试'}
    else:
        # 正则匹配数字
        pattern = re.compile(r'共(.*)条搜索结果')
        num = re.search(pattern, num_text, flags=0).group(1)
        list_book = soup.find_all("li")
        book_info = []
        for book in list_book:
            detail_url = book.find("a")['href']
            title_text = book.find('span').getText().strip()

            # 正则匹配标题，去除列号
            pattern = re.compile('.*\.(.*)')
            title = re.search(pattern, title_text, flags=0).group(1)

            book_detail = book.find_all('p')
            author = book_detail[0].getText().strip()
            publishing_house = book_detail[1].getText().strip()
            index = book_detail[2].getText().strip()
            data = {
                'title': title,
                'author': author.replace("作者：", ""),
                'publishing_house': publishing_house.replace("出版社：", ""),
                'index': index.replace("索书号：", ""),
                'url': base64_encode(detail_url)
            }
            book_info.append(data)
        data = {'rows': book_info, 'total': num}
        return {'code': 200, 'msg': 'success', 'data': data}
