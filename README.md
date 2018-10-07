# 广科图书馆爬虫项目

最小Flask服务器，提供广科图书馆图书爬虫，并作为项目演示使用

### 特性

- [x] 支持Docker
- [x] Flask工厂模式
- [x] gunicorn多进程部署
- [x] 仅提供API

### 部署方法

```
cp config.py.default config.py

pip install -r requirements.txt

export FLASK_APP=serve.py
export FLASK_ENV = development
flask run
```
