# レコードの取得の基本

## レコードを全て表示する
基本的なアクセス「テーブルの全レコードを表示する」から行う  
データベースのアクセスも、アプリケーションごとの`views.py`を利用する　　

### views.py
```py
from django.shortcuts import render
from django.http import HttpResponse
from .models import Friend

def index(request):
    data = Friend.objects.all()
    params = {
        'title': 'Hello',
        'message': 'all freind',
        'data': data,
    }
    return render(request, 'hello/index.html', params)
```

`objects`とは...  
モデルクラスに用意されている属性  
Managerクラスのインスタンスが設定されている  
`all`メソッドによって、テーブルにある各レコードをモデルのインスタンスとし、インスタンスのセットとして出力する  

### index.html
```html
<body>
    <h1>{{ title }}</h1>
    <p>{{ message|safe }}</p>
    <table>
        <tr>
            <th>ID</th>
            <th>NAME</th>
            <th>GENDER</th>
            <th>MAIL</th>
            <th>AGE</th>
            <th>BIRTHDAY</th>
        </tr>
    {% for item in data %}
        <tr>
            <td>{{ item.id }}</td>
            <td>{{ item.name }}</td>
            <td>{% if item.gender == False %}male{% endif %}
                {% if item.gender == True %}female{% endif %}
                {% if item.gender == Unknown %}---{% endif %}
            </td>
            <td>{{ item.mail }}</td>
            <td>{{ item.age }}</td>
            <td>{{ item.birthday }}</td>
        </tr>
    {% endfor %}
    </table>
</body>
```

* id  
Djangoが自動的に追加する値  
データベースでは、テーブルの全てのレコードに対し「プライマリーキー」を用意する。これにより各レコードを識別している。

* forタグ  
```html
{% for item in data %}
    ...繰り返す内容...
{% endfor %}
```

* ifタグ
```html
{% if 条件 %}
    ...表示内容...
{% endif %}
```

## 指定のIDのレコードのみ取り出す
IDを入力するフォームが必要  

### forms.py
```py
from django import forms

class IdForm(forms.Form):
    id = forms.IntegerFeild(label='ID')
```

### index.html
以下を追加  

```html
<table>
<form action="{% url 'index' %}" method="post">
    {% csrf_token %}
    {{ form.as_table }}
    <tr>
        <td></td>
        <td><input type="submit" value="click"></td>
    </tr>
</form>
</table>
```

### views.py
```py
from django.shortcuts import render
from django.http import HttpResponse
from .forms import HelloForm
from .models import Friend

def index(request):
    params = {
        'title': 'Hello',
        'message': 'all friends.',
        'form': HelloForm(),
        'data': [],
    }
    if (request.method == 'POST'):
        num = request.POST['id']
        item = Friend.objects.get(id=num)
        params['data'] = [item]
        params['form'] = HelloForm(request.POST)
    else:
        params['data'] = Friend.objects.all()
    return render(request, 'hello/index.html', params)
```

```py
num = request.POST['id']
item = Friend.objects.get(id=num)
```
「IDの値がnumのレコードを一つだけ取り出す」  

テンプレート側で「セットから順にインスタンスを取り出して表示する」というように処理しているので  
```py
params['data'] = [item]
```
として、セットに入れて`params['data']`に代入している  
こうすることで、「項目が一つだけのセット」としてテンプレート側で処理できる  

## Managerクラス
Managerクラスとは、「データベースクエリ」を操作するための機能を提供するためのもの  
「データベースクエリ」とは、「データベースに対して、さまざまな要求をするためのもの」  
「クエリ」とは、テーブルへのアクセスや、取り出すレコードの条件などの指定のこと  

Managerクラスは、メソッドなどの内部から、SQLのクエリを作成してデータベースに問い合わせをし、その結果（レコードなど）を受け取る  
「Pythonのメソッドを、データベースクエリに翻訳して実行するもの」  

### モデルのリストを調べる

#### views.py
```py
def index(request):
    data = Friend.objects.all()
    params = {
        'title': 'Hello',
        'data': data,
    }
    return render(request, 'hello/index.html', params)
```

#### index.html
```html
<body>
    <h1>Hello/{{ title }}</h1>
    <p>{{ data }}</p>
    <table>
        <tr>
            <th>data</th>
        </tr>
    {% for item in data %}
        <tr>
            <td>{{ item }}</td>
        </tr>
    {% endfor %}
    </table>
</body>
```

{{ item }}で取り出すと、`.all()`によってQuerySetというクラスのインスタンスが取り出されていたとわかる  

### valuesメソッド
「レコードの値だけ欲しい」時に利用  
モデルに保管されている値を辞書の形にして取り出すことができる  

#### views.py
```py
def index(request):
    data = Friend.objects.all().values()
    params = {
        'title': 'Hello',
        'data': data,
    }
    return render(request, 'hello/index.html', params)
```

### 特定の項目のみ取り出す
`.values()`の引数に項目名を指定すると、その項目の値だけを取り出す  

#### views.py
```py
def index(request):
    data = Friend.objects.all().values('id', 'name')
    params = {
        'title': 'Hello',
        'data': data,
    }
    return render(request, 'hello/index.html', params)
```

### リストとして取り出す
「タプルとして」返ってきます

#### views.py
```py
def index(request):
    data = Friend.objects.all().values_list('id', 'name', 'age')
    params = {
        'title': 'Hello',
        'data': data,
    }
    return render(request, 'hello/index.html', params)
```

### その他のメソッド

|メソッド|内容|
|---|---|
|first|allなどで得られたレコードの内、最初のものだけを返すメソッド|
|last|allなどで得られたレコードの内、最後のものだけを返すメソッド|
|count|取得したレコードを返すメソッド|

#### views.py
```py
def index(request):
    num = Friend.objects.all().count()
    first = Friend.objects.all().first()
    last = Friend.objects.all().last()
    data = [num, first, last]
    params = {
        'title': 'Hello',
        'data': data,
    }
    return render(request, 'hello/index.html', params)
```

## QuerySetの表示をカスタマイズ

#### views.py
```py
def index(request):
    num = Friend.objects.all().count()
    first = Friend.objects.all().first()
    last = Friend.objects.all().last()
    data = [num, first, last]
    params = {
        'title': 'Hello',
        'data': data,
    }
    return render(request, 'hello/index.html', params)
```

クエリセットを変更すると全てのクエリセットに影響するので、気をつけましょう
