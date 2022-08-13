# データベース発展

## レコードの並び替え
多数のレコードを検索した時、基本的にはレコードの作成順（id純）に並んで表示される。  
レコードの並び替えは、Managerクラスの「order_by」というメソッドで行える。  

```py
<モデル>.objects.<allやfilterなど>.order_by(項目名)
```

引数は複数指定できる。  
例えば、('name', 'mail')と引数を指定すれば、まずname順に並び替え、同じnameのものがあった場合はそれらをmail順に並び替えるようにできる。  

### 年齢順に並び替える

#### views.py
```py
def index(request):
    data = Friend.objects.all().order_by('age')
    params = {
        'title': 'Hello',
        'message': '',
        'data': data,
    }
    return render(request, 'hello/index.html', params)
```

#### index.html
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
        </tr>
    {% for item in data %}
        <tr>
            <td>{{ item.id }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.age }}</td>
            <td>{{ item.mail }}</td>
            <td>{{ item.birthday }}</td>
        </tr>
    {% endfor %}
    </table>
</body>
```

### 逆順
```py
<モデル>.objects.<allやfilterなど>.order_by(項目名).reverse()
```

## 指定した範囲のレコードを取り出す
```
<QuerySet>[開始位置:終了位置]
```

位置は、最初のレコードの前がゼロとなり、1つ目と2つ目の間が1、2つ目と3つ目の間が2、と考えると良いらしい。 
つまり、1つ目から5つ目まで取り出したければ、[0:5]とすれば良い。  
**開始位置+1〜終了位置**が返ってくる。

### views.py
```py
def find(request):
    if (request.method == 'POST'):
        msg = 'serch result:'
        form = FindForm(request.POST)
        str = request.POST['find']
        list = str.split()
        data = Friend.objects.all()[int(list[0]:int(list[1]))]
    else:
        msg = 'serch words ...'
        form = FindForm()
        data = Friend.objects.all()
    params = {
        'title': 'Find',
        'message': msg,
        'form': form,
        'data': data,
    }
    return render(request, 'hello/find.html', params)
```

### find.html
```html
<body>
    <h1>{{ title }}</h1>
    <p>{{ message|safe }}</p>
    <table>
        <form action="{% url 'find' %}" method="post">
        {% csrf_token %}
        {{ form }}
        <tr>
            <th></th>
            <td>
                <input type="submit" value="click">
            </td>
        </tr>
    </table>
    <hr>
    <table>
        <tr>
            <th>id</th>
            <th>name</th>
            <th>age</th>
            <th>mail</th>
            <th>birthday</th>
        </tr>
    {% for item in data %}
        <tr>
            <td>{{ item.id }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.age }}</td>
            <td>{{ item.mail }}</td>
            <td>{{ item.birthday }}</td>
        </tr>
    {% endfor %}
    </table>
</body>
```

## レコードの集計
保存してあるデータを取り出すだけではなく、必要なレコードの値を集計処理することもある。  
こういう場合は、必要なレコードをallやfilterで取り出し、そこから値を順に取り出して集計し計算する、というのが一般的らしい。  
「合計」や「平均」などの一般的な集計ならば、もっと簡単な方法がある。  
集計用の関数を使い、「aggregate」というメソッドで集計を行わせる。  

```py
変数 = <モデル>.objects.aggregate(関数)
```

引数には、django.db.modelsに用意されている集計用の関数を記述する。  

|集計用関数|説明|
|---|---|
|Counter(項目名)|指定した項目のレコード数を返す|
|Sum(項目名)|指定した項目の合計を計算する|
|Avg(項目名)|指定した項目の平均を計算する|
|Min(項目名)|指定した項目から最小値を返す|
|Max(項目名)|指定した項目から最大値を返す|

### ageの集計
```py
from django.db.models import Count, Sum, Avg, Min, Max

def index(request):
    data = Friend.objects.all()
    re1 = Friend.objects.aggregate(Count('age'))
    re2 = Friend.objects.aggregate(Sum('age'))
    re3 = Friend.objects.aggregate(Avg('age'))
    re4 = Friend.objects.aggregate(Min('age'))
    re5 = Friend.objects.aggregate(Max('age'))
    msg = 'Count:' + str(re1['age__count'])\
        + '<br>Sum:' + str(re2['age__sum'])\
        + '<br>Average:' + str(re3['age__avg'])\
        + '<br>Min:' + str(re4['age__min'])\
        + '<br>Max:' + str(re5['age__max'])
    params = {
        'title': 'Hello',
        'message': msg,
        'data': data
    }
    return render(request, 'hello/index.html', params)
```

aggregateメソッドの引数に、関数を指定してあげることで、値が取り出せる。  
ただし、得られるものは整数値ではなく、辞書型になっているので、そこから値を取り出す必要がある。  

例えば、`Count('age')`による値は、`'age__count'`という値として保管されている。  
得られる値は以下のような名前になっている。  

```
'項目名（アンダーバー二つ）関数名'
```

## SQlを実行する
Djangoでは、filterを使ってたいていの検索は行えるようになっているが、本格的なアプリ開発で非常に複雑な検索を行う必要があるような場合、filterを組み合わせてそれを実現するのはかなり大変であることがある。  
そういう場合、「SQLのクエリを直接実行する」という方法が用意されている。  
これには、Managerクラスに用意されている「raw」というメソッドを使う。  

```
変数 = <モデル>.objects.raw(クエリ文)
```

### views.py
```py
def find(request):
    if (request.method == 'POST'):
        msg = request.POST['find']
        form = FindForm(request.POST)
        sql = 'select * from hello_friend'
        if (msg != ''):
            sql += ' where ' + msg
            data = Friend.objects.raw(sql)
            msg = sql
        else:
            msg = 'serch words...'
            form = FriendForm()
            data = Friend.objects.all()
        params = {
            'title': 'Hello',
            'message': msg,
            'form': form,
            'data': data,
        }
        return render(request, 'hello/find.html', params)
```

まず、if文を使ってPOST通信されているのをチェックし、変数sqlにアクセスするSQLクエリ文を用意する。  
以下で全レコードを取り出す処理ができたと考えるそうです。

```py
sql = 'select * from hello_friend'
```

フォームから何かテキストが送信されてきた場合は、このSQLクエリの後に更に文を追加する。  
以下で検索の条件などを設定できるようにしている。  

```py
if (msg != ''):
    sql += ' where ' + msg
```

最後に、完成した変数sqlを引数にしてrawメソッドを呼び出せばそのSQLクエリが実行される。  

```py
data = Friend.objects.raw(sql)
```

## SQLクエリの初歩

### テーブル名
`hello_find`はテーブル名である。ここまで、「Friendのテーブル名はfriendsだ」と説明してきたそうです。  
adminによる管理ツールでも、friendsと表示されていた。  
しかし、実際にデータベースに作成されているテーブル名は「hello_friend」  
Djangoでは、マイグレーションを使ってテーブルの生成を行う場合、以下のような形でテーブルの名前が設定される。  

```
アプリ名_モデル名
```

### select文
SQLクエリでレコードを検索する際の基本は「select」文である。  

```
select 項目名 from テーブル名
```

selectの後には、値を取り出す項目の指定を用意する。全部の項目を取り出すなら、「*」という記号を指定する。  

```
select * from hello_friend
```

### 条件指定（where）
whereの後に、検索の条件を指定する。  

```
select 項目 from テーブル where 条件
```

### 基本的な検索条件

* 完全一致
```
項目名 = 値
```

* あいまい検索
```
項目名 like 値
```
テキストの前後に「%」という記号をつけて、「ここにはどんなテキストも入ってよし」ということを指定する。  
例えば、`mail like '%.jp'`とすれば、メールアドレスが.jpで終わるレコードを全て検索する。  

* 数字の比較
```
項目名 < 値
項目名 <= 値
項目名 > 値
項目名 >= 値
```

* AND/OR検索
```
式1 and 式2
式1 or 式2
```

* 並び替え
```
where 〇〇 order by 項目名
where 〇〇 order by 項目名 desc
```

* 範囲の指定
```
where 〇〇 limit 個数 offset 開始位置
```

## SQLは非常手段
SQLクエリはなるべく使用しない！！！  
Pythonのスクリプトの中にPython以外のコードが含まれてしまうとスクリプトの見通しが悪くなる。  
SQLクエリにも方言があるため、データベースを変更した途端に動かなくなる場合もある。
