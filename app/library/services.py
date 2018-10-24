import re
from urllib import parse
import config
import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def url_encode(text):
    return parse.quote(text)


def url_decode(text):
    return parse.unquote(text)


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
                'url': url_encode(detail_url)
            }
            book_info.append(data)
        data = {'rows': book_info, 'total': num}
        return {'code': 200, 'msg': 'success', 'data': data}


def get_book_detail(endpoint):
    url = '%s%s' % (config.LIBRARY_HOST, url_decode(endpoint))
    try:
        res = requests.get(url, timeout=10)
    except Exception as e:
        logger.warning('图书馆检索图书失败，URL:%s，错误信息:%s' % (url, e))
        return {'code': 502, 'msg': '图书馆服务器连接出错，请重试'}
    else:
        book_info = []
        soup = BeautifulSoup(res.text, "html.parser")
        article = soup.body.find('article')
        catalog = article.find(class_="catalog").find_all('p')
        catalog_list = []
        for index in catalog:
            catalog_list.append(index.getText())
        list_book = article.find_all(class_="tableLib")
        for book in list_book:
            book_name = book.find(class_="titBox").find("p").getText()
            book_one = book.find(class_="tableCon").find_all("tr")
            # 索书号
            callno = book_one[0].find('td').getText()
            # 条码号
            barcode = book_one[1].find('td').getText()
            # 登录号
            access_num = book_one[2].find('td').getText()
            # 藏书部门
            collect_dept = book_one[3].find('td').getText()
            # 流通状态
            status = book_one[4].find('td').getText()
            # 应还日期
            deadline = book_one[5].find('td').getText()
            data = {
                "book_name": book_name,
                "callno": callno,
                "barcode": barcode,
                "access_num": access_num,
                "collect_dept": collect_dept,
                "status": status,
                "deadline": deadline
            }
            book_info.append(data)
        data = {'rows': book_info, "catalog": catalog_list}
        return {'code': 200, 'msg': 'success', 'data': data}
