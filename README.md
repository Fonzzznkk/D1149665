# D1149665
demo

基本資訊:
主要程式在views.py
myapp/template/myapp 裡面是html檔
myapp/urls.py 是URL配置

網站架設資訊:
安裝xampp
需要用到apache和mysql

下載整個software資料夾
mysite>setting.py
以下要改成自己的資料庫設定
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Course_selection_system',     # 創建的資料庫名稱
        'USER': 'root',           # 默認 MySQL 用戶名（XAMPP 默認是 root）
        'PASSWORD': '',           # XAMPP 默認 root 密碼是空的
        'HOST': '',      # 使用本地伺服器
        'PORT': '3306',           # MySQL 預設端口
    }
}

事前準備:
安裝django
pip install django

安裝 mysqlclient：
pip install mysqlclient
2.2.5似乎會有問題
要安裝2.2.4

開啟方式:

在mysite開啟terminal
第一次開啟或有更改models.py
輸入
python manage.py makemigrations
python manage.py migrate
將models中設計的資料表新增/更新在mysql

開啟網站
輸入python manage.py runserver

127.0.0.1/myapp/login

