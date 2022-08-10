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

### urls.py
今回は編集用にedit.htmlを作成する。これは、/edit/1というように、ID番号をURLに含むようにしておく。  
こうしておくことで、どのレコードを編集するか指定できるようにする。  

```py
urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('edit/<int:num>', views.edit, name='edit'),
]
```

### index.html
レコード一覧に編集用のリンクを追記する。  

```html
{% for item in data %}
    <tr>
        <td>{{ item }}</td>
        <td><a href="{% url 'edit' item.id %}">Edit</a></td>
    </tr>
{% endfor %}
```

`{% url 'edit' item.id %}`とすることで、/edit/1というようにeditの後にID番号をつけてアクセスできるようにしている。

### edit.html
編集ページのhtmlを作成する  
以下はcreate.htmlと違う部分  

```html
<form action="{% url 'edit' id %}" method="post">
    {% csrf_token %}
    {{ form.as_table }}
    <tr>
        <td></td>
        <td><input type="submit" value="click"></td>
    </tr>
</form>
```

### views.py
```py
def edit(request, num):
    obj = Friend.objects.get(id=num)
    if (request.method == 'POST'):
        friend = FriendForm(request.POST, instance=obj)
        friend.save()
        return redirect(to='/hello')
    params = {
        'title': 'Update',
        'id': num,
        'form': FriendForm(instance=obj)
    }
    return render(request, 'hello/edit.html', params)
```

urlpatternsに用意したURLでは、`'edit/<int:num>'`というように設定していたので、アドレスのnumの値がそのまま引数numに渡される。  
このnumの値を使って、Friendインスタンスを取得する。  

インスタンスの取得は、getメソッドを使って行う。引数idに番号を指定すれば、そのID番号のインスタンスが取り出せる。  
あとは、このFriendインスタンスを使ってFriendFormインスタンスを作成し、保存するだけ。  

instance引数に、getで取得したインスタンスを指定している。フォームから送信された値(request.POST)は、createの時と同じように用意してある。  
インスタンスを作成し、saveを呼び出せば、取得したFriendインスタンスの内容が更新されレコードが保存される。  

## Delete
まず、ID番号などを使って、削除するレコードのモデルインスタンスを取得しておく。  
そして、そのインスタンスの「delete」メソッドを実行すれば、そのモデルに対応するレコードが削除される。  

### urls.py
```py
urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('edit/<int:num>', views.edit, name='edit'),
    path('delete/<int:num>', views.delete, name='delete')
]
```

### index.html
レコード一覧に削除用のリンクを追記する。  

```html
{% for item in data %}
    <tr>
        <td>{{ item }}</td>
        <td><a href="{% url 'edit' item.id %}">Edit</a></td>
        <td><a href="{% url 'delete' item.id %}">Edit</a></td>
    </tr>
{% endfor %}
```

### delete.html
create.htmlとの違いは以下。

```html
<body>
    <h1>Hello/CRUD/{{ title }}</h1>
    <p>※ 以下のレコードを削除します。</p>
    <table>
        <tr>
            <th>ID</th>
            <th>{{ obj.id }}</th>
        </tr>
        <tr>
            <th>Name</th>
            <td>{{ obj.name }}</td>
        </tr>
        <tr>
            <th>Gender</th>
            <td>
                {% if obj.gender == False %}male{% endif %}
                {% if obj.gender == True %}female{% endif %}
                {% if obj.gender == Unknown %}unknown{% endif %}
            </td>
        </tr>
        <tr>
            <th>Email</th>
            <td>{{ obj.mail }}</td>
        </tr>
        <tr>
            <th>Age</th>
            <td>{{ obj.age }}</td>
        </tr>
        <tr>
            <th>Birth</th>
            <td>{{ obj.birthday }}</td>
        </tr>
        <form action="{% url 'delete' id %}" method="post">
            {% csrf_token %}
            {{ form.as_table }}
            <tr>
                <td></td>
                <td><input type="submit" value="click"></td>
            </tr>
        </form>
    </table>
</body>
```

### views.py
```py
def delete(request, num):
    friend = Friend.objects.get(id=num)
    if (request.method == 'POST'):
        friend.delete()
        return redirect(to='/hello')
    params = {
        'title': 'Delete',
        'id': num,
        'obj': friend
    }
    return render(request, 'hello/delete.html', params)
```

## CRUDまとめ
「Read」についてはallやgetを使った処理でレコードを取り出しているので、すでにやっています。  

CRUDは、データベースアクセスの基本であって、「データベースを使ったアプリの基本機能」というわけではないそうです。  
データベースを使ったアプリを作ろうと思ったら、「検索」（いかに的確に必要なレコードを取り出すか）の方が重要だそうです。
