# 注意事項

### 基本資訊
主程式 views.py  
html myapp/template/myapp  
URL myapp/urls.py

### 網站架設資訊
安裝 XAMPP（需要用到 apache 和 mysql）  
下載整個 software 資料夾  
mysite > setting.py 要改成自己的資料庫設定
```py
DATABASES = { 
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Course_selection_system', # 創建的資料庫名稱
        'USER': 'root', # 默認 MySQL 用戶名（XAMPP 默認是 root）
        'PASSWORD': '', # XAMPP 默認 root 密碼是空的
        'HOST': '', # 使用本地伺服器
        'PORT': '3306', # MySQL 預設端口
    }
}
```

### 事前準備
```shell
# 安裝 django  
pip install django
# 安裝 mysqlclient
pip install mysqlclient
# 2.2.5似乎會有問題，要安裝2.2.4
pip install mysqlclient==2.2.4
```

### 開啟方式
在 mysite 開啟 terminal  
第一次開啟或有更改 models.py
```shell
# 將 models 中設計的資料表更新在 mysql
python manage.py makemigrations
python manage.py migrate
```
開啟網站
```shell
python manage.py runserver 
``` 