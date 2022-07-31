# フォーム

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
