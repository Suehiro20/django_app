# formsモジュール
```
formsモジュール
∟Formクラス
∟CharFieldクラス
∟IntegerFieldクラス
∟...他のクラス...
```
## 入力フィールド
* CharField
* EmailField
* IntegerField
* FloatField
* URLField

それぞれ、`required`、`min_length`、`max_length`などの引数をとる

## 日時に関するフィールド
|クラス|説明|
|---|---|
|DateField|日付の形式のテキストのみ受け付ける（2001-01-23 01/23/2001 01/23/01）|
|TimeField|時刻の形式のテキストのみ受け付ける（12:34 12:34:56）|
|DateTimeField|日付と時刻を続けて書いたテキストのみ受け付ける|

## チェックボックス
`BooleanFeild`を使用  

### forms.py
```py
class HelloField(forms.Form):
    check = forms.BooleanField(label='Checkbox', required=False)
```

※ チェックボックスはOFFだと値が送信されないため、`required='True'`だと、チェックボックスがOFFの状態を送信できない  

### テンプレート
```html
<body>
    <h1>{{ title }}</h1>
    <p>{{ result|safe }}</p>
    <table>
    <form action="{% url 'index' %}" method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <tr>
            <td>
            </td>
            <td>
                <input type="submit" value="click">
            </td>
        </tr>
    </form>
    </table>
</body>
```

### views.py
```py
class HelloView(TemplateView):
    def __init__(self):
        self.params = {
            'title': 'Hello',
            'form': HelloForm(),
            'result': None,
        }
    
    def get(self, request):
        return render(request, 'hello/index.html', self.params)
    
    def post(self, request):
        if ('check' in request.POST):
            self.params['result'] = 'Checked!'
        else:
            self.params['result'] = 'not checked...'
        self.params['form'] = HelloForm(request.POST)
        return render(request, 'hello/index.html', self.params)
```

※ チェックがONの時は`'check': ['on']`が送られる

## 3択のNullBooleanField
ONでもOFFでもない状態（intermediate）を扱う  
「Yes」「No」「Unknown」の三項目を持ったプルダウンメニューとして用意されている  

### forms.py
```py
class HelloForm(forms.Form):
    check = forms.NullBooleanField(label='Checkbox')
```

### views.py
```py
...
def post(self, request):
        chk = request.POST['check']
        self.params['result'] = 'you selected: "' + chk + '".'
        self.params['form'] = HelloForm(request.POST)
        return render(request, 'hello/index.html', self.params)
```

## プルダウンメニュー
`ChoiceField`を利用する  
`choices`という引数を持つ  
→ `choices`は「タプルのリスト」

### forms.py
```py
class HelloForm(forms.Form):
    data = [
        ('値', 'ラベル')
        ('one', 'item 1'),
        ('two', 'item 2'),
        ('three', 'item 3')
    ]
    choice = forms.ChoiceField(label='Choice', choices=data)
```

### views.py
```py
...
def post(self, request):
        ch = request.POST['choice']
        self.params['result'] = 'you selected: "' + ch + '".'
        self.params['form'] = HelloForm(request.POST)
        return render(request, 'hello/index.html', self.params)
```

※ 最初エラーが出たが、なぜか直った。残っていたキャッシュのせいか？  
もしエラーが出たら、`self.params['result'] = ch`として、`ch`に何が渡されているかを確認する  

## ラジオボタン
引き続き`ChoiceField`を利用する  
変更点は、引数`widget`を使うところ  

### forms.py
```py
class HelloForm(forms.Form):
    data = [
        ('値', 'ラベル')
        ('one', 'item 1'),
        ('two', 'item 2'),
        ('three', 'item 3')
    ]
    choice = forms.ChoiceField(label='radio', choices=data, widget=forms.RadioSelect())
```

※ `widget`は「Webページに表示されるhtmlタグを管理数る」  

## 選択リスト
引き続き`ChoiceField`を利用する  
変更点は、引数`widget`の値  

### forms.py
```py
class HelloForm(forms.Form):
    data = [
        ('値', 'ラベル')
        ('one', 'item 1'),
        ('two', 'item 2'),
        ('three', 'item 3'),
        ('four', 'item 4'),
        ('five', 'item 5'),
    ]
    choice = forms.ChoiceField(label='radio', choices=data, widget=forms.Select(attrs={'size': 6}))
```

※ `attrs={'size': 項目数}`で表示する項目数を設定している  

## 複数選択
`MultipleChoiceField`を利用  
`widget`の値も変更  

### forms.py
```py
class HelloForm(forms.Form):
    data = [
        ('値', 'ラベル'),
        ('one', 'item 1'),
        ('two', 'item 2'),
        ('three', 'item 3'),
        ('four', 'item 4'),
        ('five', 'item 5'),
    ]
    choice = forms.MultipleChoiceField(label='radio', choices=data, widget=forms.SelectMultiple(attrs={'size': 6}))
```

### views.py
```py
def post(self, request):
        ch = request.POST.getlist('choice')
        self.params['result'] = 'you selected: "' + str(ch) + '".'
        ...
```

`ch`の値をリストにしたい（送られてきた値を一つにして取り出したい）  
→ `.getlist()`を使用する  
→ `str(ch)`として、リストを文字として表示するようにする（でないと、`+`でつなげない！と言われる）

※ commandキーを押して複数選択しないといけないことに驚き  

リストの値を利用したいときは...   
例えば  
```py
def post(self, request):
        ch = request.POST.getlist('choice')

        result = '<ol><b>selected:</b>'

        for i in ch:
            result += '<li>' + i + '</li>'
        
        result += '</ol>'

        self.params['result'] = result
        self.params['form'] = HelloForm(request.POST)
        return render(request, 'hello/index.html', self.params)
```
