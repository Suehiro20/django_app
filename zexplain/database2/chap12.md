# ページネーション
ページネーションとは、「ページ分け」のための機能。  
テーブルに保管されているレコードを一定数ごとに分け（これが「ページ」）、それを順に取り出して表示していく。  

## Paginatorクラスの使い方
ページネーションは、Djangoでは「Paginator」というクラスとして用意されている。  

* インスタンスの作成  
```
変数 = Paginator(コレクション, レコード数)
```

Paginatorのインスタンスを作成するには、まず「レコード全体をまとめたコレクション」と「1ページあたりのレコード数」の2つを引数として用意しなければならない。  
「レコード全体をまとめたコレクション」というのは、わかりやすく言えば、allやfilterメソッドで得られるオブジェクト（QuerySet）と考えて良い。  

* 指定ページのレコードを取り出す  
```
変数 = <Paginator>.get_page(番号)
```

Paginatorインスタンスから、特定のページのレコードを取り出すには、「get_page」というメソッドを利用する。引数にページ番号の整数を指定すれば、そのページのレコードをまとめて取り出す。  
この場合のページ番号は、「1」から始まり、指定のページ番号のレコードが見つからない場合は、最後のページのレコードを返す。  
「get_page」で得られるのは、「Page」というクラスのインスタンスである。これは、コレクションになっていて、ここからforなどを使用し、リストやセットと同じ感覚でレコードを取り出して処理することができる。  

## Friendをページごとに表示する

### urls.py
```py
path('<int:num>', views.index, name='index'),
```

### views.py
```py
from django.core.paginator import Paginator

def index(request, num=1):
    data = Friend.objcets.all()
    page = Paginator(data, 3)
    params = {
        'title': 'Hello',
        'message': '',
        'data': page.get_page(num),
    }
    return render(request, 'hello/index.html', params)
```

## ページ移動

### index.html
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
```

### 前のページに移動
```
{% if data.has_previous %}
    ...ここにリンクを用意...
{% endif %}
```

「has_previous」というメソッドを呼び出している。これは、前のページがあるかどうかをチェックするものである。   
前にページがあればTrue、一番前のページでもう前にページがなければFalseとなる。  

```html
<a href="{% url 'index' %}">&laquo;first</a>
<a href="{% url 'index' %}/{{ data.previous_page_number }}">&laquo;prev</a>
```

トップページは、ページ番号をつけず、ただ/helloだけでアクセスできる。  
前のページは、{% url 'index' %}の後に、{{ data.previous_page_number }}というものをつけて作成している。  
「previous_page_number」というメソッドは、前のページ番号を返す。  

### 現在のページの表示
```
[{{ data.number }}/{{ data.paginator.num_pages }}]
```

現在のページは、「number」という属性で得ることができる。  
アクセスして取得したレコードが全部で何ページ分あるかは、.paginatorの「num_pages」という属性で得られる。  
data.paginatorというのは、dataに収められているPaginatorインスタンスである。dataは、Paginatorのget_pageメソッドで取り出したセットであるが、その中にも使ったPaginatorインスタンスが収められている。  

### 次のページへ移動
```
{% if data.has_next %}
    ...ここにリンクを用意...
{% endif %}
```

「has_next」は、次のページがあるかどうかを示すメソッド。  
次のページが残っていたらTrue、最後のページであればFalseとなる。  

```html
<a href="{% url 'index' %}/{{ data.next_page_number }}">next&raquo;</a>
<a href="{% url 'index' %}/{{ data.paginator.num_pages }}">last&raquo;</a>
```

次のページに移動するリンクでは、「next_page_number」というメソッドを使用している。  
最後のページ番号に関しては、先ほど扱った「.paginator.num_pages」を使用している。  
