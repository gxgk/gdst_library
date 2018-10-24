from flask import request, jsonify
from . import library_mod
from .services import search_book, get_book_detail


@library_mod.route('/')
def get_search_book():
    keyword = request.args.get("keyword", None, type=str)
    book_type = request.args.get("book_type", 1, type=int)
    page = request.args.get("page", 1, type=int)
    if not keyword:
        return jsonify({'code': 404, "msg": 'keyword no find'})
    data = search_book(keyword, page, book_type)
    return jsonify(data)


@library_mod.route('/book_detail')
def book_detail():
    endpoint = request.args.get("url", None, type=str)
    if not endpoint:
        return jsonify({'code': 404, "msg": 'endpoint no find'})
    data = get_book_detail(endpoint)
    return jsonify(data)
