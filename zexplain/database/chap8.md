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
