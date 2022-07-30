# アプリケーション

## アプリケーションフォルダ
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

## views.py
```
from django.shortcuts import render
from django.http import HttpResponse
```
※ HttpResponse(返送内容)

## urls.py（アプリケーションフォルダ）
```py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```
※ pathの(アクセスするアドレス)の部分は`http://〇〇/hello/`の後に続くアドレス

## urls.py（プロジェクトフォルダ）
```py
from django.contrib import admin
from django.urls import path,include
# import app名.views as app名

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('hello/', hello.index),
    path('hello/', include('hello.urls')),
]
```
※ path(アクセスするアドレス, 呼び出す処理)

## クエリパラメータ（補足）
`http://...普通のアドレス...?キー=値&キー=値&キー=値...`
e.g.  
```py
def index(request):
    msg = request.GET['msg']
    return HttpResponse('you typed: "' + msg + '".')
```
と書いて  
`http://localhost:8000/hello/?msg=hello`  
とアクセスすると  
`you typed: "hello".`と表示される  

### エラー処置
e.g.  
```py
def index(request):
    if 'msg' in request.GET:
        msg = request.GET['msg']
        result = 'you typed: "' + msg + '".'
    else:
        result = 'please send msg parameter!'
    return HttpResponse(result)
```

※ GET属性は辞書型配列  

|やりとり|管理クラス名|説明|
|---|---|---|
|リクエスト|HttpRequest|クライアントからWebアプリケーションへのアクセス。アクセスの際に送られる情報（アクセスしたアドレスやアクセス時のヘッダー情報など）を保管|
|レスポンス|HttpResponse|Webアプリケーションからクライアントへのアクセス。クライアントに返送するデータや、返送時のアクセス情報などを管理|

### クエリパラメータ改
`http://...普通のアドレス.../値/値`  
hello > urls.py > urlpatternsを修正するだけ  
```py
urlpatterns = [
    path('<int:id>/<nickname>/', views.index, name='index'),
]
```
indexの中身は...  
```py
def index(request, id, nickname):
    result = 'your id: ' + str(id) + ', name: "' + nickname + '".'
    return HttpResponse(result)
```

## テンプレート
Djangoに組み込まれているシステム  
→ アプリケーションの登録をする必要  
↓  
settings.py（プロジェクトフォルダ）を変更する  
```py
INSTALLED_APPS = [
    ...
    'django.contrib.staticfiles',
    'hello',
]
```

### テンプレートの作成
```
ディレクトリ（プロジェクト）
∟プロジェクトフォルダ
∟アプリケーションフォルダ
 ∟templates
  ∟(フォルダ)
   ∟index.html
∟仮想環境
∟データベース
∟manage.py
∟requirements.txt
```
テンプレートの読み込みの際は「templates」フォルダ内のパスで指定をする  
`フォルダ/index.html`をいう風に指定をしないと、自分が他アプリケーションと混同し混乱してしまう

### urlpatterns（アプリケーションフォルダ）
```py
urlpatterns = [
    path('', views.index, name='index')
]
```

### index関数
```py
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'hello/index.html')
```

※ render：テンプレートをレンダリングすることに使用する関数  
`render(<HttpRequest>, テンプレート)`  
* 第1引数：クライアントへの返送を管理するHttpRequestインスタンスを指定
* 第2引数：費用するテンプレートを指定（テンプレートフォルダからのパスで指定）

### 変数利用

#### templatesの変更
マスタッシュ（{{}}）を使用  
{{ 変数 }}で書きましょう  

#### index関数の変更
```py
def index(request):
    params = {
        'title': 'Hello/Index',
        'msg': 'これは、サンプルで作ったページです。',
    }
    return render(request, 'hello/index.html', params)
```

* 値を辞書型配列にまとめる
* render時に第3引数で辞書型配列を渡す
* テンプレート側で{{}}で値を埋め込む

という作業で、ビュー関数側からテンプレート側に値を受け渡すことができる

### 複数ページの移動
index.htmlに以下を追記
```py
<p><a href="{% url goto %}">{{ goto }}</a></p>
```

views.pyに以下を追記
```py
def index(request):
    params = {
        ...
        'goto': 'next',
    }

def next(request):
    params = {
        'title': 'Hello/Next',
        'msg': 'これは、もう一つのページです。',
        'goto': 'index',
    }
    return render(request, 'hello/index.html', params)
```

urlpatternsに以下を追記
```py
urlpatterns = [
    path('', views.index, name='index'),   # /hello/にindex関数を割り当て
    path('next', views.next, name="next"), # /hello/next/にnext関数を割り当て
]
```

#### テンプレートタグ
**{% %}**はDjangoのテンプレートに用意されている「テンプレートタグ」という  
{% url 名前 %}と書くことで、指定した名前のURLが書き出される  
ここでいう名前とは`path()`で指定した`name="hogehoge"`の部分である

## 静的ファイルの利用

### staticフォルダを作成する  
```
ディレクトリ（プロジェクト）
∟プロジェクトフォルダ
∟アプリケーションフォルダ
 ∟static
  ∟(フォルダ)
   ∟css
    ∟style.css
∟仮想環境
∟データベース
∟manage.py
∟requirements.txt
```

### index.htmlの修正
```html
{% load static %}
<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="{% static 'hello/css/style.css' %}" />
    </head>
    <body>
    </body>
</html>
```
