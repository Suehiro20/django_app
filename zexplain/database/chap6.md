# 管理ツール
Djangoにはデータベースの管理ツールが用意されていて、それを使用してWeb上でテーブルなどの編集が行える

## 管理者の作成
ターミナルで行う  
プロジェクトのディレクトリにいること・仮想環境を動かしていることを確認して以下を実行  
`python manage.py createsuperuser`  

この後にターミナルで聞かれること

|聞かれること|説明|
|---|---|
|Username|管理者名を入力する。「admin」など|
|Email address|メールアドレスを入力する。|
|Password|パスワードを入力する。8文字以上|
|Password(Again)|もう一度パスワードを入力する。|

## モデルの登録
管理ツールは全てのモデルを編集できるわけではない。  
あらかじめ「このモデルは管理ツールで利用できる」というように登録したものだけが管理ツールで編集可能。  
アプリケーションの`admin.py`で行う。  

```py
from django.contrib import admin
from .models import Friend

admin.site.register(Friend)
```

`admin.site.register`が登録するメソッド  

## 管理ツールにログイン
1. Djangoプロジェクトを起動
1. `http://.../admin`にアクセス  
アクセスするとログインページに飛ばされる
1. 上記で登録したUsernameとPasswordでログイン

## 管理ツール画面について
利用可能なモデル（テーブル）が表示されている  

* 上部のリスト「AUTHENTICATION AND AUTHORIZATION」  
管理ツールであるadminアプリケーションが使用しているモデル  
「Groups」「Users」というモデルが用意されている  
* 下部のリスト「アプリ名」  
アプリの名前が見出し、その下にそのアプリで作成したモデルが表示されている  
モデルをクリックするとそのモデルのテーブルが見られる  
* 右側のリンク「Recent Action」  
最近移動したページへのリンクが表示されている  
「前に操作したページに戻りたい」というときに素早く移動できるよ！とのこと  

## テーブルの中身
管理ツール画面 > アプリケーションのモデル をクリックしてテーブルの中身を確認  

### レコードを作成する（ブラウザ上）
1. 右上「ADD モデル名 ＋」をクリック
1. 埋めていく
1. 右下「SAVE」をクリック

テーブルのレコード一覧に移動  
レコードのリスト部分に、`__str__`で用意した表示に則ってデータが出力されている

## Usersページ
管理ツール画面 > 「AUTHENTICATION AND AUTHORIZATION」> Users  

* 検索フィールド  
上部にある入力フィールド。レコードを検索する。  
利用者名を書いて「Search」をクリックすると、その名前の利用者レコードを検索して下に表示する。  
* Action  
チェックをつけたレコードに対して行う操作を、プルダウンメニューで選択し、「Go」で実行  
* Filter  
特定の条件に合うものだけを絞り込んで表示する機能  
ここにあるリンクをクリックすることで、管理者だけを表示したり、スタッフだけを表示したりできる  

### 利用者の追加（ブラウザ上）
Usersページで「ADD USER ＋」をクリック  
以下を入力して、新たな利用者を登録する  

|入力する内容|説明|
|---|---|
|Username|利用者の名前|
|Password|パスワード。8文字以上|
|Password(Again)|もう一度パスワードを入力|

「Save」をクリック  
追加の設定を行うページに移動する  
すでにある利用者の設定を変更する際にも表示されるページである  

* Change user  
登録されている利用者名とパスワードが表示される。  
パスワードは変更できないが、利用者名は変更できる。  
* Personal info  
利用者の個人情報を入力する。姓名、メアドなどの項目がある。  
* Permissions  
パーミッション（アクセス権）に関する項目  

|パーミッションの項目|内容|
|---|---|
|Active|アクティブ（利用中）か否か|
|Staff status|スタッフ権限を持っているかどうか|
|Superuser status|管理者権限を持っているかどうか|
|Groups|グループ（複数の利用者をまとめたもの）の所属の設定|
|User permmision|利用者に割り当てる権限のリスト。管理者の権限や登録してあるモデルの作成・削除などの権限を個別に割り当てられる|

* Important dates  
この利用者を追加した日時と、最後にログインした日時が設定されている。  
これらは変更することもできる。  

#### パスワードの変更について
パスワードの編集はできない。パスワードはデフォルトで暗号化されている。  
パスワードを変更する際は、以下。  

1. Change userのページのPasswordを確認
1. 「this form」と書かれている部分がある
1. このリンクをクリックすると、パスワードの変更フォームに移動する
1. フォームを送信すれば、パスワードを変更できる
