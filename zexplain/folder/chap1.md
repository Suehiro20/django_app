# フォルダ

```
ディレクトリ（プロジェクト）
∟プロジェクトフォルダ
∟アプリケーションフォルダ
∟仮想環境
∟データベース
∟manage.py
∟requirements.txt
```

## プロジェクトフォルダ
Djangoのプロジェクトでは、「プロジェクト名と同じ名前のフォルダ」に、プロジェクト全体で使うファイルが保存されている。  
e.g. `django-admin startproject django_app`とすると`django_app`フォルダに全体で使うファイルが保存される  

| ファイル名 | 説明 |  
|---|---|
| \_\_init__.py | Djangoプロジェクトを実行するときの初期化処理を行うスクリプト |  
| settings.py | プロジェクトの設定情報を記述したファイル |  
| urls.py |プロジェクトで使うURLを管理するファイル |  
| wsgi.py | Webアプリケーションのメインプログラムとなる部分 |  

### settings.py
設定変更を行う。  
1. タイムゾーン  
`TIME_ZONE = 'Asia/Tokyo'`  
1. 言語  
`LANGUAGE_CODE = 'ja'`  
1. 静的ファイルのパスを追加（ファイルの一番下に追記）  
`STATIC_URL = '/static/'`  
`STATIC_ROOT = os.path.join(BASE_DIR, 'static')`  
1. ALLOWED_HOSTSでどのホストに対してチェックを行うか定める  
`DEBUG`が`True`に設定されていて、`ALLOWED_HOSTS`が空のリストの時は、自動的に`['localhost', '127.0.0.1', '[::1]']`という3つのホストに対してチェックが行われる。  
1. データベースについて書かれているのは以下の場所  
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

おそらく、
```py
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```
ならば上記で良い  

私の場合は、以下であった
```py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
```
この場合、`DATABASES`は
```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
また、`STATIC_ROOT = os.path.join(BASE_DIR, 'static')`も異なると考えられる（が、そもそもこれを書くのは一番上の階層にstaticフォルダを作る時かな）

### manage.py
このプロジェクトで実行するさまざまな機能に関するプログラム。  
Djangoではコマンドでプロジェクトを色々操作するが、そのための処理がここに書かれている。  

## フォルダについてver.2
アプリケーションごとにフォルダを作成  
e.g. ユーザー管理アプリ / 在庫管理アプリ / カート管理アプリ  

アプリは**MVC**モデルで作る  

|MVC|説明|
|---|---|
|Model|データアクセス関係の処理を担当。データベースとのやりとり担当。|
|View|画面表示関係担当。|
|Controller|全体の制御を担当。|

### アプリケーションフォルダ
`python manage.py startapp 名前`で作成  
自動的にアプリケーションフォルダ内に作成されるのは以下  

|ファイルなど|説明|
|---|---|
|migrationsフォルダ|データベース関係の機能のファイルがまとめられる|
|\_\_init__.py|アプリケーションの初期化処理のためのもの|
|admin.py|管理者ツールのためのもの|
|apps.py|アプリケーション本体の処理をまとめる|
|models.py|モデルに関係する処理を記述する|
|tests.py|プログラムのテストに関係するもの|
|views.py|画面表示に関するもの|

追加するファイルなど  
|ファイルなど|説明|
|---|---|
|urls.py|アプリ内のurl管理|
|templatesフォルダ|Djangoのtemplateを使用するため|
|staticフォルダ|静的ファイルを置いておく|
|forms.py|フォームのためのスクリプトファイル|