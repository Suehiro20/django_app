# CRUD
データベースを利用するための基本機能  

|機能|説明|
|---|---|
|Create|新たにレコードを作成しテーブルに保存する|
|Read|テーブルからレコードを取得する|
|Update|すでにテーブルにあるレコードの内容を変更し保存する|
|Delete|すでにテーブルにあるレコードを削除する|

これらが実装できれば、Djangoスクリプトからデータベースに保存されているレコードを操作できるようになる  
あくまで、これらは「必要最低限の機能」であって、実際には検索処理など必要  
アプリによってはこれらを用意する必要がない場合もある  

## Create
「モデルのインスタンスを用意し、保存のメソッドを実行する」  

```py
instance = Model()
...instanceに値を設定...
instance.save()
```

まずは、保存用のフォームから  

### forms.py
```py
class Friend(forms.Form):
    name = forms.CharField(label='Name')
    mail = forms.EmailField(label='Email')
    gender = forms.BooleanField(label='Gender', requeired=False)
    age = forms.IntegerField(label='Age')
    birthday = forms.DateField(label='Birth')
```

### create.html
```html
{% load static %}
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link rel="stylesheet" type="text/css" href="{% static 'hello/css/style.css' %}" />
</head>
<body>
    <h1>Hello/{{ title }}</h1>
    <table>
        <form action="{% url 'create' %}" method="post">
            {% csrf_token %}
            {{ form.as_table }}
            <tr>
                <td></td>
                <td><input type="submit" value="click"></td>
            </tr>
        </form>
    </table>
</body>
</html>
```

### index.html
テーブルの確認のために少し変更  

```html
{% load static %}
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link rel="stylesheet" type="text/css" href="{% static 'hello/css/style.css' %}" />
</head>
<body>
    <h1>Hello/Create/{{ title }}</h1>
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
</html>
```

### views.py
```py
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .forms import HelloForm
from .models import Friend

def index(request):
    data = Friend.objects.all()
    params = {
        'title': 'Hello',
        'data': data,
    }
    return render(request, 'hello/index.html', params)

def create(request):
    params = {
        'title': 'Hello',
        'form': HelloForm(),
    }
    if (request.method == 'POST'):
        name = request.POST['name']
        mail = request.POST['mail']
        gender = 'gender' in request.POST
        age = int(request.POST['age'])
        birth = request.POST['birthday']
        friend = Friend(name=name, mail=mail, gender=gender, age=age, birthday=birth)
        friend.save()
        return redirect(to='/hello')
    return render(request, 'hello/create.html', params)
```

インスタンスを作成後、一つ一つの値を設定していくのは面倒なので、インスタンス作成時に必要な値を引数で渡した  
`friend.save()`でインスタンスを保存  

`return redirect(to='/hello')`で`/hello`へリダイレクトしている
`from django.shortcuts import redirect`を忘れないこと  

### urls.py
```py
urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
]
```

## ModelFormの利用
上記のやり方では、受け取った値を一つずつ取り出してモデルインスタンスに設定している  
しかし、「request.POSTを丸ごと指定してモデルを作りたいところ」  
Djangoにはモデルのためのフォームを作成する「ModelForm」というクラスが用意されている！  

### forms.py
```py
from django import forms
from .models import Friend

class FriendForm(forms.ModelForm):
    class Meta:
        model = Friend
        fields = ['name','mail','gender','age','birthday']
```

このクラスは、ModelFormクラスを継承して作っている  
内部に「Meta」クラスを持っており、このクラスにはモデル用のフォームに関する情報が用意されている  
modelで使用するモデルクラス、fieldsで用意するフィールドをそれぞれ設定している  

### views.py
create関数を修正する  

```py
def create(request):
    if (request.method == 'POST'):
        obj = Friend()
        friend = FriendForm(request.POST, instance=obj)
        friend.save()
        return redirect(to='/hello')
    params = {
        'title': 'Hello',
        'form': FriendForm(),
    }
    return render(request, 'hello/create.html', params)
```

POST送信されたら、まずFriendクラスのインスタンスを作成する  
```py
obj = Friend()
```
これは、引数など指定していない「初期状態のインスタンス」  
続いて、FriendFormインスタンスを作成する  
```py
friend = FriendForm(request.POST, instance=obj)
```
FriendFormインスタンスを作成する際、引数に、POST送信されたフォームの情報が全てまとめてある「request.POST」を指定  
「instance」という引数では、先ほど作成したFriendインスタンスを指定する  

ModelFormの「save」メソッドを呼び出すと、ModelFormに設定された`request.POST`の値を`instance`に設定したFriendインスタンスに設定し、レコードが保存される  

## Update

