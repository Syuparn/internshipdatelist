# internshipdatelist
リクナビの「気になる企業」登録企業のインターンシップ日程をリストアップ

## 概要
リクナビでは「気になる企業」のインターン日程を調べるために各企業ページで確認する必要があります。
そこで、~~無精者でも~~日程被りの確認や期限が迫ったものをひと目で把握できるよう、1つの表にまとめるツールを作りました。


## 使用方法
1. リクナビにログインし、「気になるリスト」ページのhtmlを"rikunabi.html"という名前でinterncalender.pyと同じディレクトリに保存します。(手抜き仕様なので要改善)

1. interncalender.pyを実行すると、interndate.csvにインターンの日程一覧の表が保存されます。

interndate.csvの形式

| |company|date|days|deadline|title|
|----|----|----|----|----|----|
|0|株式会社ホゲソリューションズ|12/24、12/31|1日|12月1日|ソフトウェア開発インターンシップ|
|...|...|...|...|...|...|

## 動作の流れ
1. 「気になる企業」リストページのhtmlをスクレイピングし各企業のページのURLを抽出

1. 各企業のインターンシップページのhtmlを取得しインターンシップ日程をスクレイピング

1. 日程データをpandasで表にまとめ.csv形式で保存

## 動作環境、必要ライブラリ
環境: Python3.6+

ライブラリ

-pandas

-BeautifulSoup4