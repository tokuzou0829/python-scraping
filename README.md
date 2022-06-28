# 簡単に画像をスクレイピングしましょう!
Google画像検索から好きな画像を大量に保存できます!!

できること
- 推し画像を大量に保存できます!
- 取得した画像をとくぞうサーバーIMGに保存できます!
- GUIで直感的に操作できます!

使用方法
- Windowsでは動作しないようです。
- mac(m1)ubuntu(intel)で動作確認済みです。
- python3 必要です。(テスト済みバージョン 3.7,3.8,3.10.4)
- 使用しているChromeに対応したChrome driverが必要です。
- chrome driverはs.pyと同じディレクトリに配置してください。

ターミナルなどで次のコマンドを実行します。
1. `git clone https://github.com/tokuzou0829/python-scraping`
2. `cd python-scraping`
3. `pip install request` or `pip3 install request`
4. `pip install selenium` or `pip3 install selenium`
5. `pip install pysimplegui` or `pip3 install pysimplegui`
6. `python s.py`

## macを使用している場合
実行した際のGUIが真っ暗で表示されなかった場合は次の記事を参考にしてください。
brewのpythonの場合=>https://zenn.dev/thanai/articles/60843ae33bd4e2745d56

pyenvの場合=>https://zenn.dev/spacegeek/articles/3f8db1ffcd401e

### こちらの記事のコードを元に作成しました.
https://sasuwo.org/get-images-automatically-for-python/
