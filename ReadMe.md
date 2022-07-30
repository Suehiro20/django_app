# Django

python：3.8.9
Django：3.2.10

※ [仮想環境について](https://acokikoy.hatenablog.com/entry/2019/09/14/141128)

|よく使う|コマンド|
|---|---|
|仮想環境起動|source (仮想環境名)/bin/activate|
|仮想環境を抜ける|deactivate|

簡単なフォルダ説明
```
django_app [ディレクトリ（プロジェクト）]
∟django_app [プロジェクトフォルダ]
∟hello [アプリケーションフォルダ]
∟mahiro [仮想環境（.gitignoreで消した）]
∟db.sqlite3 [データベース（.gitignoreで消した）]
∟manage.py
∟requirements.txt
```

## Djangoプロジェクト作成方法（Macの場合）
pythonを入れている前提で話を進めます。  
1. 好きな場所にディレクトリを作成（念のためターミナルで作成）
1. 作成したディレクトリへ移動
1. 仮想環境(virtualenv)を作成  
`myenv`はお好きにどうぞ。仮想環境名です。  
`python3 -m venv myvenv`
1. 仮想環境を起動  
`source myvenv/bin/activate`  
もしくは`. myvenv/bin/activate`  

以下仮想環境が起動している状態で行う。  
1. pipを最新バージョンへ  
`python -m pip install --upgrade pip`
1. エディタで、作成したディレクトリを開き、一番上の階層に`requirements.txt`を作成
1. `requirements.txt`に`Django~=3.2.10`を記載
1. ターミナルに戻って以下を実行  
`pip install -r requirements.txt`  

これでDjangoのインストールは完了

作成したディレクトリにいること・仮想環境を動かしていることを確認して以下を実行  
`django-admin startproject mysite .`

## フォルダについて

```
ディレクトリ（プロジェクト）
∟プロジェクトフォルダ
∟アプリケーションフォルダ
∟仮想環境
∟データベース
∟manage.py
∟requirements.txt
```

### プロジェクトフォルダ
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

### manage.py
このプロジェクトで実行するさまざまな機能に関するプログラム。  
Djangoではコマンドでプロジェクトを色々操作するが、そのための処理がここに書かれている。  

## サーバー実行する方法
実行するディレクトリにいること・仮想環境を動かしていることを確認。  

### 初回実行時
`python manage.py migrate`を実行しましょう。  

（でないと、`Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.`と言われます）  

次回以降は以下だけで大丈夫です。  

### 2回目以降実行時
`python manage.py runserver`を実行しましょう。  

### 実行を止めるとき
MacであろうがWindowsであろうが`Control+C`です。  

### 仮想環境から抜けるとき
`deactivate`（たぶん）  
ターミナルを閉じたら勝手に仮想環境から抜けてしまう気もしますが...

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

## アプリケーションについて

### views.py
```
from django.shortcuts import render
from django.http import HttpResponse
```
※ HttpResponse(返送内容)

### urls.py（アプリケーションフォルダ）
```py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```
※ pathの(アクセスするアドレス)の部分は`http://〇〇/hello/`の後に続くアドレス

### urls.py（プロジェクトフォルダ）
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

### クエリパラメータ
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

#### エラー処置
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

## テンプレートの作成
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

## フォーム利用

### index.htmlの準備
```html
<body>
    <form action="{% url 'form' %}" method="post">
        {% csrf_token %}
        <label for="msg">message: </label>
        <input id="msg" type="text" name="msg">
        <input type="submit" value="click">
    </form>
</body>
```

`action`で`<form>`の送信先を指定

### CSFR対策
`{% csrf_token %}`の部分  
CSFR対策のために日tっようなトークンを表示している  

「Cross-Site Request Forgeries」（リクエスト強要）の略  
外部からサイトへのフォーム送信などを行う攻撃のこと  
フォーム送信の際に、CSFRによる攻撃で、外部から大量のフォームが送りつけられたりすることを防ぐために、「正しくフォームから送信されたアクセスかどうか」をチェックする仕組みが必要  

`{% csrf_token %}`はフォームに「トークン」項目を追加する  
トークン：ランダムに生成されたテキスト  
送信時にこのトークンの値をフォームと一緒に受け渡し、それが正しいものかどうかをチェックするようにしてある

### views.pyの準備
```py
def form(request):
    msg = request.POST['msg']
    params = {
        'title': 'Hello/Form',
        'msg': 'こんにちは、' + msg + 'さん。',
        'goto': 'index'
    }
    return render(request, 'hello/index.html', params)
```

`name="msg"`に記入された値を、`request.POST['msg']`で取り出している  

* GET：クエリパラメータなどを取り出すのに使用（GET通信の時）/ 用意されているデータをただ取り出すだけの処理
* POST：フォームから送信された値を取り出したりするのに使用（POST通信の時）/ 新しいデータを作って受け取るような処理

### urlpatternsの準備
```py
urlpatterns = [
    ...
    path('form', views.form, name="form"),
]
```

## Formクラス
Formは、Djangoに用意されているフォームのクラス  
これを使用して、フォームの内容をPythonのクラスとして定義する  
これをテンプレートに変数として渡す  
このFormをテンプレートで出力すると、クラスの内容を元にフォームが自動生成される

### forms.pyを作成
アプリケーションフォルダ内に作成する  
```
ディレクトリ（プロジェクト）
∟プロジェクトフォルダ
∟アプリケーションフォルダ
 ∟forms.py
∟仮想環境
∟データベース
∟manage.py
∟requirements.txt
```

中身は...クラスを書く  
```py
from django import forms

class HelloForm(forms.Form):
    name = forms.CharField(label='name')
    mail = forms.CharField(label='mail')
    age = forms.IntegerField(label='age')
```

* forms.CharField：テキストを入力する一般的なフィールドのクラス
* forms.IntegerField：整数の値を入力するためのフィールドクラス

引数は`label`  
これを設定すると、フィールドの手前にラベルのテキストが表示される

### views.pyの準備
```py
def index(request):
    params = {
        'title': 'Hello',
        'message': 'your data:',
        'form': HelloForm(),
    }
    if (request.method == 'POST'):
        params['message'] = '名前:' + request.POST['name'] + \
            '<br>メール:' + request.POST['mail'] + \
            '<br>年齢:' + request.POST['age']
        params['form'] = HelloForm(request.POST)
    return render(request, 'hello/index.html', params)
```

GETとPOSTを同時に行なっている  
最初に共通する内容を書く  
次にPOSTのみで実行する内容を書く

### 表示するための準備（index.html）
```html
<body>
    <h1>{{ title }}</h1>
    <p>{{ message|safe }}</p>
    <form action="{% url 'index' %}" method="post">
        {% csrf_token %}
        {{ form }}
        <input type="submit" value="click">
    </form>
</body>
```

`{{ message|safe }}`の`|safe`を書くことでhtmlタグがそのままダグとして処理される  
ここでは`<br>メール`の部分の`<br>`をhtmlのタグとして処理してほしいので使用している  

### urlpatternsの準備
いつも通りpathを整えてあげてください

### 表示を整える
|メソッド|説明|
|---|---|
|<Form>.as_table|ラベルとフィールドのタグを<tr><td>でくくって書き出す（<table>は自分で書く必要）|
|<Form>.as_p|ラベルとフィールド全体を<p>でくくる|
|<FOrm>.as_ul|ラベルとフィールド全体を<il>タグでくくる|

`.as_hoge`を付けることでFormクラスの範囲は勝手に整形してくれる

## view関数のクラス化（応用編）

### views.pyの準備
```py
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from .forms import HelloForm

class クラス名(TemplateView):
    def __init__(self):
        ...初期設定...
    
    def get(self, request):
        ...GETの時の処理...
    
    def post(self, request):
        ...POSTの時の処理...
```

### urlpatternsの準備
```py
from django.conf.urls import url
from .views import HelloView

urlpatterns = [
    url(r'', HelloView.as_view(), name="index")
]
```


