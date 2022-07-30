# Django

python：3.8.9  
Django：3.2.10

※ [仮想環境について](https://acokikoy.hatenablog.com/entry/2019/09/14/141128)

|よく使う|コマンド|
|---|---|
|仮想環境起動|source (仮想環境名)/bin/activate|
|仮想環境を抜ける|deactivate|

サーバーの実行方法については[下の方](#anc1)を読んでください  
Djangoの説明は`zexplainフォルダ`に書いています  

簡単なフォルダ説明
```
django_app [ディレクトリ（プロジェクト）]
∟django_app [プロジェクトフォルダ]
∟hello [アプリケーションフォルダ]
∟mahiro [仮想環境（.gitignoreで消した）]
∟db.sqlite3 [データベース（.gitignoreで消した）]
∟manage.py
∟requirements.txt
```

## Djangoプロジェクト作成方法（Macの場合）
pythonを入れている前提で話を進めます。  
1. 好きな場所にディレクトリを作成（念のためターミナルで作成）
1. 作成したディレクトリへ移動
1. 仮想環境(virtualenv)を作成  
`myenv`はお好きにどうぞ。仮想環境名です。  
`python3 -m venv myvenv`
1. 仮想環境を起動  
`source myvenv/bin/activate`  
もしくは`. myvenv/bin/activate`  

以下仮想環境が起動している状態で行う。  
1. pipを最新バージョンへ  
`python -m pip install --upgrade pip`
1. エディタで、作成したディレクトリを開き、一番上の階層に`requirements.txt`を作成
1. `requirements.txt`に`Django~=3.2.10`を記載
1. ターミナルに戻って以下を実行  
`pip install -r requirements.txt`  

これでDjangoのインストールは完了

作成したディレクトリにいること・仮想環境を動かしていることを確認して以下を実行  
`django-admin startproject プロジェクトフォルダ名 .`

<a id="anc1"></a>

## サーバー実行する方法
実行するディレクトリにいること・仮想環境を動かしていることを確認。  

### 初回実行時
`python manage.py migrate`を実行しましょう。  

（でないと、`Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.`と言われます）  

次回以降は以下だけで大丈夫です。  

### 2回目以降実行時
`python manage.py runserver`を実行しましょう。  

### 実行を止めるとき
MacであろうがWindowsであろうが`Control+C`です。  

### 仮想環境から抜けるとき
`deactivate`（たぶん）  
ターミナルを閉じたら勝手に仮想環境から抜けてしまう気もしますが...
