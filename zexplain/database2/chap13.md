# リレーションシップとForeignKey
本格的なWebアプリを作るようになってくると、「1つのWebアプリに1つのテーブルだけ」といったことでは済まなくなる。  
いくつものテーブルが組み合わせられて動くようなことになる。  
この際に考える必要があるのが、「テーブル同士の連携」である。  

例えば、簡単な掲示板のようなものを考える。これには、投稿するメッセージを管理するテーブルと、利用者を管理するテーブルがある、とする。そうすると、それぞれのメッセージは、「誰が投稿したか」という情報を利用者テーブルから持ってきて使うことになる。つまり、メッセージのテーブルにある1つ1つのレコードには、「これを投稿した利用者のレコード」が関連づけられていなければならない。  

Djangoでは、こうした関連付けを「リレーションシップ」と呼ぶ。  

## リレーションシップの種類
* 1対1対応  
テーブルAのレコード1つに対して、テーブルBのレコード1つが対応している。  

* 1対多対応  
テーブルAのレコード1つに対して、テーブルBのレコード複数が対応している。  

* 多対1対応  
逆から見れば、上記と同じ。  

* 多対多対応  
テーブルAの複数のレコードに対して、テーブルBの複数のレコードが対応している。  

## リレーションシップの設定方法
リレーションシップの設定は、モデルで行う。モデルの中に、関連づける相手のモデルに関する項目を用意することで、両者の関連がわかるようになる。  

### テーブルの「主従」
「どっちのテーブルが主体となって関連付けがされるか」を表す。関連付けするとき、「どちらがより重要か」ということである。わかりやすく言えば、これは「絶対にないと困るのが主テーブル」である。

### 1対多/多対1の関連付け
* 主モデル（「1」側）  
```py
class A(models.Model):
    ...項目...
```

* 従モデル（「多」側）  
```py
class B(models.Model):
    項目 = models.ForeignKey(モデル名)
    ...項目...
```

関連付けを考えるとき、「どちらが主で、どちらが従か」ということを頭に入れて考えるようにする。  
ポイントは「多」側のモデルに、models.ForeignKeyという項目を用意しておくこと。  
「ForeignKey」は外部キーのクラスである。外部キーというのは、このモデルに割り当てられているテーブル以外のテーブル用のキー、という意味。  
データベースのテーブルには、プライマリーキーが自動的に組み込まれる。プライマリーキーは、すべてのレコードに割り当てられる、値の重複していないID番号のようなもの。データベースは、プライマリーキーを使って個々のレコードを認識している。  
外部キーは、このプライマリーキーを保管するためのキー（テーブルに用意する項目）である。つまり、あるテーブルのレコードに関連する別のテーブルのレコードのプライマリーキーを、この外部キーに保管しておく、ということらしい。  

### 1対1の関連付け
* 主モデル（「1」側）  
```py
class A(models.Model):
    ...項目...
```

* 従モデル（「多」側）  
```py
class B(models.Model):
    項目 = models.OneToOneField(モデル名)
    ...項目...
```

### 多対多の関連付け
* 主モデル（「1」側）  
```py
class A(models.Model):
    ...項目...
```

* 従モデル（「多」側）  
```py
class B(models.Model):
    項目 = models.ManyToManyField(モデル名)
    ...項目...
```

## メッセージ投稿のシステムを考える
利用者のテーブルはFriendを流用する。あとは、投稿メッセージのテーブルを作成し、両者の関連付けを行えばよい。  
今回は「1対多」の関係で、投稿者が主テーブル、メッセージが従テーブルである。  

### メッセージテーブルを設計する

|項目|説明|
|---|---|
|タイトル|タイトルのテキスト|
|コンテンツ|これが投稿するメッセージ|
|投稿日時|投稿した日時|

## Messageモデルを作る

models.py  
```py
class Message(models.Model):
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=300)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '<Message: id=' + str(self.id) + ', ' + \
            self.title + '( ' + str(self.pub_date) + ' )>'
    
    class Meta:
        ordering = ('pub_date',)
```

on_deleteは削除する際の設定で、これはmodels.CASCADEを指定すると覚えてしまってOK。  
auto_now_addというのは、自動的に値を設定するためのもの。  
「'ordering' must be a tuple or list (even if you want to order by only one field).」とのことでした。  

## マイグレーションする
モデルをプロジェクトに反映させるには、「マイグレーション」。  
マイグレーションは、2段階の操作である。まずマイグレーションファイルを作り、それからそのファイルを適用する。  

### マイグレーションファイルを作る
ターミナルで以下を実行

```
python manage.py makemigrations hello
```

### マイグレーションを実行
ターミナルで以下を実行

```
python manage.py migrate
```

## admin.pyの修正
```py
from django.contrib import admin
from .models import Friend, Message

admin.site.register(Friend)
admin.site.register(Message)
```

これで、管理者ツールにMessageモデルクラスが追加された。  

## 管理者ツールでMessageを使う
管理者ページにアクセス。  
HELLO => Messageの右側にある「Add」をクリックして、Messageの作成ページに移動する。  
Friend、Title、Contentの3つの項目が表示されている。プライマリーキーのidや、自動設定されるpub_dateなどは表示されないようになっている。  
また、Friendはフィールドではなくポップアップメニューになっており、現在Friendに登録されている利用者が項目として表示される。  

## Messageページを作る

### urls.py
```py
path('message/', views.message, name='message'),
path('message/<int:page>', views.message, name='message'),
```

### forms.py
```py
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['title', 'content', 'friend']
```

### views.py
```py
from .models import Friend, Message
from .forms import FriendForm, MessageForm

def message(request, page=1):
    if (request.method == 'POST'):
        obj = Message()
        form = MessageForm(request.POST, instance=obj)
        form.save()
    data = Message.objects.all().reverse()
    paginator = Paginator(data, 5)
    params = {
        'title': 'Message',
        'form': MessageForm(),
        'data': paginator.get_page(page),
    }
    return render(request, 'hello/message.html', params)
```

### message.html
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
    <h1>{{ title }}</h1>
    <table>
        <form action="{% url 'message' %}" method="post">
            {% csrf_token %}
            {{ form.as_table }}
            <tr>
                <td></td>
                <td><input type="submit" value="send"></td>
            </tr>
        </form>
    </table>
    <hr>
    <table>
        <tr>
            <th>title</th>
            <th>name</th>
            <th>datetime</th>
        </tr>
    {% for item in data %}
        <tr>
            <td>{{ item.title }}</td>
            <td>{{ item.friend.name }}</td>
            <td>{{ item.pub_date }}</td>
        </tr>
    {% endfor %}
    </table>
    <div class="pagination">
        {% if data.has_previous %}
            <a href="{% url 'message' %}/{{ data.previous_page_number }}">&laquo;prev</a>
        {% endif %}
        {% if data.has_next %}
            <a href="{% url 'page' %}/{{ data.next_page_number }}">next&raquo;</a>
        {% endif %}
    </div>
</body>
</html>
```

## indexに投稿メッセージを表示する
```html
<body>
    <h1>{{ title }}</h1>
    <p>{{ message|safe }}</p>
    <table>
        <tr>
            <th>id</th>
            <th>name</th>
            <th>age</th>
            <th>mail</th>
            <th>birthday</th>
            <th>Message</th>
        </tr>
    {% for item in data %}
        <tr>
            <td>{{ item.id }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.age }}</td>
            <td>{{ item.mail }}</td>
            <td>{{ item.birthday }}</td>
            <td>
                <ul>
                {% for ob in item.message_set.all %}
                    <li>{{ ob.title }}</li>
                {% endfor %}
                </ul>
            </td>
        </tr>
    {% endfor %}
    </table>
    <div class="pagination">
        {% if data.has_previous %}
            <a href="{% url 'index' %}">&laquo;first</a>
            <a href="{% url 'index' %}/{{ data.previous_page_number }}">&laquo;prev</a>
        {% endif %}
        <span class="current">
            [{{ data.number }}/{{ data.paginator.num_pages }}]
        </span>
        {% if data.has_next %}
            <a href="{% url 'index' %}/{{ data.next_page_number }}">next&raquo;</a>
            <a href="{% url 'index' %}/{{ data.paginator.num_pages }}">last&raquo;</a>
        {% endif %}
    </div>
</body>
</html>
```

Friendインスタンスから、それに関連するMessageを取り出すには、  

```
{% for ob in item.message_set.all %}
    <li>{{ ob.title }}</li>
{% endfor %}
```

「message_set」は、関連するテーブルモデルであるMessageが保管されている属性である。  
「〇〇_set」は、逆引き名として扱われる。「逆引き名」とは、ForeignKeyのような関連項目がない主テーブルのモデルクラス側から従テーブル側を取り出すための項目。  

「〇〇_set」には、相手側のモデルクラスの「RelatedManager」というものが設定されている。普通、モデルにはobjects属性があって、そこにManagerというクラスのインスタンスが設定されていた。そこにあるallなどを呼び出すことで、レコードを取り出したりできた。RelatedManagerは、このManagerの仲間である。  
ただし、RelatedManagerは相手側テーブルの関連するレコードだけを操作する。  
Managerでは、allメソッドで全レコードを取り出せたが、RelatedManagerは、allメソッドでそのレコードに関連する相手側テーブルのレコードだけが取り出せる。  

## 相手側テーブルへのアクセスの基本

* ForeignKeyなどを指定したテーブル（従テーブル）のモデルでは、相手のテーブル名の属性が用意されていて、それで相手のレコードを取り出せる。
* ForeignKeyなどがない側のテーブル（主テーブル）のモデルでは、「〇〇_set」という逆引き名の属性にあるRelatedManagerを使って、相手側のレコードを取り出せる。
