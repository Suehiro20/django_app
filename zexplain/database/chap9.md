# 検索
Djangoでは、モデルにはobjectsという属性があり、この中にManagerというクラスのインスタンスが入っていた。  
検索関係も、このManagerに用意されている「フィルター」機能を使う。  
フィルターは、たくさんあるデータの中から必要なものを絞り込むためのもの。  

```
変数 = <Model>.objects.filter(フィルターの内容)
```

フィルターの内容をどう設定するかが、検索のテクニックとも言える部分だそうです。  

## 検索とフィルター

### urls.py
```py
urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('edit/<int:num>', views.edit, name='edit'),
    path('delete/<int:num>', views.delete, name='delete'),
    path('find', views.find, name='find')
]
```

### forms.py
```py
class FindForm(forms.Form):
    find = forms.CharField(label='Find', required=False)
```

### find.html
```html
<body>
    <h1>Hello/CRUD/{{ title }}</h1>
    <p>{{ message|safe }}</p>
    <table>
        <form action="{% url 'find' %}" method="post">
            {% csrf_token %}
            {{ form.as_table }}
            <tr>
                <td></td>
                <td><input type="submit" value="click"></td>
            </tr>
        </form>
    </table>
    <hr>
    <table>
        <tr>
            <th>data</th>
            <th></th>
            <th></th>
        </tr>
    {% for item in data %}    
        <tr>
            <td>{{ item }}</td>
            <td><a href="{% url 'edit' id %}">Edit</a></td>
            <td><a href="{% url 'delete' id %}">Delete</a></td>
        </tr>
    {% endfor %}
    </table>
</body>
```

### views.py
```py
def find(request):
    if (request.method == 'POST'):
        msg = 'serch result:'
        form = FindForm(request.POST)
        str = request.POST['find']
        data = Friend.objects.filter(name=str)
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

## あいまい検索

* 値を含む検索
```
項目名（アンダーバー二つ）contains=値
```
* 値で始まるものを検索
```
項目名（アンダーバー二つ）startswith=値
```
* 値で終わるものを検索
```
項目名（アンダーバー二つ）endswith=値
```

### （例）__contains
```py
def find(request):
    if (request.method == 'POST'):
        msg = 'serch result:'
        form = FindForm(request.POST)
        str = request.POST['find']
        data = Friend.objects.filter(name__contains=str)
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

## 大文字小文字を区別しない

* 大文字小文字を区別しない検索
```
項目名（アンダーバー二つ）iexact=値
```
* 大文字小文字を区別しないあいまい検索
```
項目名（アンダーバー二つ）icontains=値
項目名（アンダーバー二つ）istartswith=値
項目名（アンダーバー二つ）iendswith=値
```

## 数値の比較

* 値と等しい
```
項目名=値
```
* 値よりも大きい
```
項目名（アンダーバー二つ）gt=値
```
* 値と等しいか大きい
```
項目名（アンダーバー二つ）gte=値
```
* 値よりも小さい
```
項目名（アンダーバー二つ）lt=値
```
* 値と等しいか小さい
```
項目名（アンダーバー二つ）lte=値
```

### （例）__lte
```
data = Friend.objects.filter(age__lte=int(str))
```

## 〇〇歳以上〇〇歳以下
複数の条件を設定する場合、「両方の条件に合うものを探す」or「どちらか一つでもあえば全部探す」  
AND検索（論理積）or OR検索（論理和）

### 両方の条件に合うものを探す
```py
変数 = <Model>.objects.filter(1つ目の条件, 2つ目の条件)
```

以下が変更点  
```py
str = request.POST['find']
val = str.split()
data = Friend.objects.filter(age__gte=val[0], age__lte=val[1])
```

splitメソッドは、テキストを決まった文字や記号で分割したリストを返す。  
引数を省略すると、半角スペースや改行でテキストを分割する。  

#### 別の書き方
```py
変数 = <Model>.objects\
        .filter(1つ目の条件)\
        .filter(2つ目の条件)\
        .filter(3つ目の条件)\
        .filter(4つ目の条件)\
        ...略...
```

### どちらか一つでもあえば全部探す
```py
変数 = <Model>.objects.filter(Q(1つ目の条件)|Q(2つ目の条件))
```

以下が変更点  
```py
from django.db.models import Q

def find(request):
    if (request.method == 'POST'):
        msg = 'serch result:'
        form = FriendForm(request.POST)
        str = request.POST['find']
        data = Friend.objects.filter(Q(name__contains=str)|Q(mail__contains=str))
...略...
```

## リストを使って検索
```py
変数 = <Model>.objects.filter(項目名__in=リスト)
```

以下が変更点  
```py
str = request.POST['find']
list = str.split()
data = Friend.objects.filter(name__in=list)
```

