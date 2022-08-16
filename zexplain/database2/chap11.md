# バリデーション
バリデーションは、フォームなどの入力項目に条件を設定し、その条件を満たしているかどうかを確認する機能である。  
条件を満たしていれば、そのままレコードを保存したり、フォームの内容をもとに処理を実行したりする。  
満たしていない場合は、再度フォームページに移動してフォームを再表示させる。  

## モデルを使わないバリデーション
Djangoでは、フォームはforms.Formというクラスの派生クラスとして作成をした。そこでは、CharFieldなど各種のフィールドクラスを使ってフォームの項目を作成していた。  
先に、Friendのレコード作成を行うために「HelloForm」を作成した。  

```py
class HelloForm(forms.Form):
    name = forms.CharField(label='Name')
    mail = forms.EmailField(label='Email')
    gender = forms.BooleanField(label='Gender', required=False)
    age = forms.IntegerField(label='Age')
    birthday = forms.DateField(label='Birth', required=False)
```

```py
required=False
```

これが「バリデーションの設定」である。  
requiredは、「必須項目」として設定するためのバリデーション機能。  
Djangoでは、forms.Formにフィールドの項目を用意すると。自動的にrequiredがTrueに設定されるので必要。  

## バリデーションのチェック
モデル用のフォーム（models.Form）であれば、saveするときにバリデーションのチェックを自動的に行うなどの想像ができるが、一般的なフォームの場合、送られたフォームの値を自分で取り出して利用するのが一般的である。  
バリデーションは「自分でやる」。自分で送られた値のチェックを行い、その結果に応じて処理をするようにスクリプトを組んであげる。  

```py
if (<Form>.is_valid()):
    ...エラー？時の処理...
else:
    ...正常時の処理...
```

このように、forms.Formの「is_valid」メソッドを使ってバリデーションのチェックを行う。  
このメソッドは、フォームに入力された値のチェックを行い、1つでもエラーがあった場合にはFalseを、全くなかった場合にはTrueをそれぞれ返す。  

## バリデーションを使ってみる
checkページを作ってバリデーションを試す。  

### check.html
「template」フォルダ => 「hello」フォルダ => check.html

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
    <p>{{ message }}</p>
    <table>
        <form action="{% url 'check' %}" method="post">
        {% csrf_token %}
        {{ form.as_table }}
        <tr>
            <td></td>
            <td>
                <input type="submit" value="click">
            </td>
        </tr>
    </table>
</body>
</html>
```

### urls.py
```py
path('check', views.check, name='check')
```

### forms.py
```py
class CheckForm(forms.Form):
    str = forms.CharField(label='Name')
```

これは、「とりあえず動くかどうかチェック」というものなので、1つのフィールドを用意しておくだけにしてある。  

### views.py
```py
from .forms import CheckForm

def check(request):
    params = {
        'title': 'Hello',
        'message': 'check validation',
        'form': CheckForm(),
    }
    if (request.method == 'POST'):
        form = CheckForm(request.POST)
        params['form'] = form
        if (form.is_vaild()):
            params['message'] = 'OK!'
        else:
            params['message'] = 'not good.'
    return render(request, 'hello/check.html', params)
```

エラーがあれば？、params['message'] = 'OK!'を実行する。そうでなければ、params['message'] = 'not good.'を実行する。  

## サンプルフォームでバリデーションのチェック
* 未入力で送信（Webブラウザ側でのチェック）  
フォームは送信されない。何も書いていない状態で送信ボタンを押すと、ブラウザの機能により送信そのものがキャンセルされる。  

* Django側でのバリデーションチェック  
半角スペースを1つだけ書いて送信すると、フォームは送信されるが、エラー時の言葉が表示される。  

## 使えるバリデーション

### CharFieldのバリデーション
* required  
Trueならば必須項目、Falseならばそうではない。  

* min_length, max_length  
入力するテキストの最小文字数、最大文字数を指定する。いずれも整数値で指定。  

* empty_value  
空の入力を許可するかどうか。  

```py
class CheckForm(forms.Form):
    empty = forms.CharField(label='Empty', empty_value=True)
    min = forms.CharFeild(label='Min', min_length=10)
    max = forms.CharFeild(label='Max', min_length=10)
```


### IntegerField/FloatFieldのバリデーション
* required  
Trueならば必須項目、Falseならばそうではない。  

* min_value, max_value  
入力するテキストの最小値、最大値を指定する。いずれも整数値で指定。  

```py
class CheckForm(forms.Form):
    required = forms.IntegerField(label='Required')
    min = forms.IntegerFeild(label='Min', min_value=100)
    max = forms.IntegerFeild(label='Max', min_value=1000)
```

### 日時関連のバリデーション
DateField、TimeField、DateTimeFieldなどのフィールドは、requiredの他に、フォーマットに関するバリデーションが設定されている。日時の形式に合わない値が入力されるとエラーになる。  
日時のフォーマットは「input_formats」という引数で指定することができる。  
リストの形で値を指定し、フォーマット形式を表すテキストを必要なだけ用意する。  

```
input_formats=[フォーマット1, フォーマット2, ...]
```

フォーマットは日時の各値を表す記号を組み合わせて作成する。用意されている記号は以下。  

|記号|説明|
|---|---|
|%y|年を表す記号|
|%m|月を表す記号|
|%d|日を表す記号|
|%H|時を表す記号|
|%M|分を表す記号|
|%S|秒を表す記号|

例えば、'%y/%m/%d'とすれば、2022/8/2のような形式のフォーマットになる。  

```py
class CheckForm(forms.Form):
    date = forms.DateField(label='Date', input_formats=['%d'])
    time = forms.TimeFeild(label='Time')
    datetime = forms.DateTimeFeild(label='DateTime')
```

上記の場合、Timeならば「時:分」という形式、日付ならば「日/月/年」という形式でないとエラーになる。  

## バリデーションを追加する
Formクラスにメソッドを追加する。  

```py
class クラス名(forms.Form):
    ...項目の用意...

    def clean(self):
        変数 = super().clean()
        ...値の処理...
```

「clean」というメソッドは、用意された値の検証を行う際に呼び出される。  
このメソッドでは、最初にsuper().clean()というものを呼び出して、基底クラス（継承するもとになっているクラス）のcleanを呼び出す。戻り値には、チェック済みの値が返される。  
ここで、super().clean()で得られた値から値を取り出し、チェックを行えばよい。  
こういう場合をエラーにしよう、となったときには、エラーを発生させれば良い。  

### raise ValidationErrorの働き
エラーはわざと発生させることができる。Djangoにはエラーのクラスがあり、そのインスタンスを作って「raise」というキーワードでエラーを送り出せば、エラーを発生させることができる。  
バリデーションのエラーは「ValidationError」というクラスとして用意されている。  

```
raise ValidationError(エラーメッセージ)
```

値をチェックし、必要に応じてValidationErrorを発生させれば、独自のバリデーション処理ができる。  

### forms.py
「no」で始まるテキストを入力すると、「You input "NO"!」というエラーメッセージが表示される。  

```py
from django import forms

class CheckForm(forms.Form):
    str = forms.CharField(label='String')

    def clean(self):
        cleaned_data = super().clean()
        str = cleaned_data['str']
        if (str.lower().startswith('no')):
            raise forms.ValidationError('You input "NO"!')
```

## ModelFormでのバリデーション
ModelFormの振り返り  

models.py
```py
from django.db import models

class Friend(models.Model):
    name = models.CharField(max_length=100)
    mail = models.EmailField(max_length=200)
    gender = models.NullBooleanField()
    age = models.IntegerField(default=0)
    birthday = models.DateField()

    def __str__(self):
        return '<Friend: id=' + str(self.id) + ', ' + \
            self.name + '( ' + str(self.age) + ' )>'
```

forms.py
```py
from django import forms
from .models import Friend

class FriendForm(forms.ModelForm):
    class Meta:
        model = Friend
        fields = ['name','mail','gender','age','birthday']
```

views.py
```py
def create(request):
    if (request.method == 'POST'):
        obj = Friend()
        friend = FriendForm(request.POST, instance=obj)
        friend.save()
        return redirect(to='/hello')
    params = {
        'title': 'CreateMeta',
        'form': FriendForm(),
    }
    return render(request, 'hello/create.html', params)
```

バリデーションが実行されるのは「save」のとき。  
POST送信されたら、Friendインスタンスとrequest.POSTを引数に指定してFriendFormインスタンスを作っている。そして、このFriendFormのsaveメソッドを呼び出して保存を行なっている。  
FriendFormは、ModelFormを継承して作った派生クラスである。このModelFormにあるsaveでは、保存の命令がされると、用意されているフォームの項目と、モデルインスタンスの項目をそれぞれバリデーションチェックし、双方向に問題がなければモデルにフォームの値を設定して保存を実行している。  
つまり、モデルの保存や更新では、「バリデーションをいつ実行するか」は考えなくて良い。普通にインスタンスを作って保存しようとすれば、必ずどこかのタイミングでDjangoがバリデーションチェックをやってくれるようになっている。  

## checkでFriendモデルを利用する
save以外に、forms.Formと同様、「is_valid」メソッドを使ってチェックできる。  

### views.py
```py
def check(request):
    params = {
        'title': 'Hello',
        'message': 'check validation.',
        'form': FriendForm(),
    }
    if (request.method == 'POST'):
        obj = Friend()
        form = FriendForm(request.POST, instance=obj)
        params['form'] = form
        if (form.is_valid()):
            params['message'] = 'OK!'
        else:
            params['message'] = 'not good.'
    return render(request, 'hello/check.html', params)
```

これは送信時にエラーとなるか否かである。保存はしていないので新しいレコードは追加されない。  

## モデルのバリデーション設定
forms.FormとModelFormのバリデーションは違う。  

### バリデーションルールの組み込み

models.py
```py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Friend(models.Model):
    name = models.CharField(max_length=100)
    mail = models.EmailField(max_length=200)
    gender = models.NullBooleanField()
    age = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(150)])
    birthday = models.DateField()

    def __str__(self):
        return '<Friend: id=' + str(self.id) + ', ' + \
            self.name + '( ' + str(self.age) + ' )>'
```

```py
IntegerField(validators=[])
```

validatorsという引数に、リストが設定されている。このリストには、「バリデータ」と呼ばれるクラスのインスタンスが用意されている。  
バリデータは、バリデーションルールを実装するクラス。  

## モデルで使えるバリデータ
* MinValueValidator/MaxValueValidator  
入力可能な最小値と最大値を指定する

* MinLengthValidator/MaxLengthValidator  
入力するテキストの最小文字数・最大文字数を指定する

* EmailValidator/URLValidator  
一般的なCharFieldなどを使ってメールアドレスやURLを入力させる場合、書かれた値がメールアドレスやURLの形式になっているかチェックする必要がある。  
こういった場合に使用する。引数などは必要ない。  

* ProhibitNullCharactersValidator  
null文字を禁止するためのもの。  

* RegexValidator  
正規表現パターンを使って、パターンに合致する値かどうかをチェックするためのもの。引数には、正規表現パターンを指定する。  

```py
from django.db import models
from django.core.validators import RegexValidator

class Friend(models.Model):
    name = models.CharField(max_length=100, validators=[RegexValidator(r'^[a-z]*$')])
    mail = models.EmailField(max_length=200)
    gender = models.NullBooleanField()
    age = models.IntegerField(default=0)
    birthday = models.DateField()

    def __str__(self):
        return '<Friend: id=' + str(self.id) + ', ' + \
            self.name + '( ' + str(self.age) + ' )>'
```

## バリデータ関数を作る
モデルクラスでもcleanメソッドを使ったやり方は利用できる。  
今回は、バリデーション処理を関数として用意しておき、それをバリデータとして組み込む。  

```py
def 関数名(value):
    ...処理...
```

valueに、チェックする値が保管される。この値を調べて、何か問題があれば、先にやった「raise ValidationError」を使ってエラーを発生させれば良い。  

### 数字バリデータ関数

models.py
```py
import re
from django.db import models
from django.core.validators import ValidationError

def number_only(value):
    if (re.match(r'^[0-9]*$', value) == None):
        raise ValidationError(
            '%(value)s is not Number!',
            params={'value': value}
        )

class Friend(models.Model):
    name = models.CharField(max_length=100, validators=[number_only])
    mail = models.EmailField(max_length=200)
    gender = models.NullBooleanField()
    age = models.IntegerField(default=0)
    birthday = models.DateField()

    def __str__(self):
        return '<Friend: id=' + str(self.id) + ', ' + \
            self.name + '( ' + str(self.age) + ' )>'
```

reというのが、Pythonの正規表現モジュール。この中にある「match」という関数は、引数に指定したテキストとパターンがマッチするかを調べるもの。これで指定のパターンとマッチする場合、その情報をまとめたオブジェクトが得られる。マッチしない場合は、Noneが返される。  

## フォームとエラーメッセージを個別に表示
個々のフィールドやエラーメッセージを個別に表示させる場合。  

```html
<body>
    <h1>{{ title }}</h1>
    <p>{{ message }}</p>
    <hr>
    <ol>
    {% for item in form %}
    <li>
        {{ item.name }} ({{ item.value }}) : {{ item.errors.as_text }}
    </li>
    {% endfor %}
    </ol>
    <table>
        <form action="{% url 'check' %}" method="post">
        {% csrf_token %}
        <tr>
            <th>名前</th>
            <td>{{ form.name }}</td>
        </tr>
        <tr>
            <th>メール</th>
            <td>{{ form.mail }}</td>
        </tr>
        <tr>
            <th>性別</th>
            <td>{{ form.gender }}</td>
        </tr>
        <tr>
            <th>年齢</th>
            <td>{{ form.age }}</td>
        </tr>
        <tr>
            <th>誕生日</th>
            <td>{{ form.birthday }}</td>
        </tr>
        <tr>
            <td></td>
            <td>
                <input type="submit" value="click">
            </td>
        </tr>
    </table>
</body>
```

### エラーメッセージの出力
フォーム全体のエラーメッセージを丸ごと取り出すには、formの「error」という属性を使う。  

```
{{ form.errors }}
```

1つ1つのフォームの項目を取り出して、そこからerrorsの値を取り出す、という場合。  

```
{% for item in form %}
...個々の処理...
{% endfor %}
```

個々の処理は、例えば、  

```
<li>
    {{ item.name }} ({{ item.value }}) : {{ item.errors.as_text }}
</li>
```

errorsは、「as_text」というのをつけることで、テキストとして値を取り出せる。
