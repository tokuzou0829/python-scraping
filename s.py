# パッケージインポート関係
import warnings
warnings.simplefilter('ignore', FutureWarning)
import subprocess
import sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium", "-q"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "PySimpleGUI", "-q"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "pyfiglet" , "-q"])
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import requests
import json
import time
import datetime
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
import PySimpleGUI as sg
from pyfiglet import Figlet

# タイトル表示
f = Figlet(font="slant")
msg = f.renderText("PythonScraping")
print(msg)

#  セクション1 - オプションの設定と標準レイアウト
sg.theme('SystemDefault')

layout = [
    [sg.Text('何の画像が必要ですか?', text_color='#000', background_color='#fff', font=('Arial',20))],
    [sg.Text('検索内容', size=(15, 1), text_color='#000', background_color='#fff'), sg.InputText('キャラクターの名前とか(中野三玖)')],
    [sg.Text('最大検索回数', size=(15, 1), text_color='#000', background_color='#fff'), sg.InputText('1~400')],
    [sg.Text('ジャンル', size=(15, 1), text_color='#000', background_color='#fff'), sg.InputText('アニメ名とか?(五等分の花嫁)')],
    [sg.Text('ジャンルの中に作られるフォルダ名', size=(15, 1), text_color='#000', background_color='#fff'), sg.InputText('キャラクターの名前とか(中野三玖)')],
    [sg.Text("保存先フォルダ", text_color='#000', background_color='#fff'), sg.InputText(), sg.FolderBrowse()],
    [sg.Checkbox("TokuzouServerIMGに保存する", text_color='#000', background_color='#fff', default=False)],
    [sg.Submit(button_text='実行ボタン')]
]
# セクション 2 - ウィンドウの生成
window = sg.Window('スクレイピング準備', layout=layout, background_color='#fff')
# セクション 3 - イベントループ
while True:
    event, values = window.read()

    if event is None:
        print("入力完了")
        break

    if event == '実行ボタン':
        window.close()
        
        QUERY = values[0]
        search_count = str(values[1])
        title = values[2]
        charactername = values[3]
        savedir = values[4]

        server = str(values[5])
        if server == str("True"):
            servercheck = "保存されます"
        else:
            servercheck = "保存されません"
        
        show_message = "検索内容：" + QUERY + 'が入力されました。\n'
        show_message += "最大検索回数：" + search_count + 'が入力されました。\n'
        show_message += "ジャンル：" + title + 'が入力されました。\n'
        show_message += "ジャンルの中に作られるフォルダ名：" + charactername + "が入力されました。\n"
        show_message += "保存先フォルダ："+savedir+'/'+title +'/'+charactername+"に保存されます。\n"
        show_message += "スクレイピングした画像はサーバーに" + servercheck + "。\n"
        print(show_message)
        # ポップアップ
        sg.popup(show_message + 'ポップアウトを閉じるとスタートします。')

# セクション 4 - ウィンドウの破棄と終了
window.close()

tm_start = time.time()            #処理時間計測用
dt_now = datetime.datetime.now()  # 現在日時
dt_date_str = dt_now.strftime('%Y/%m/%d %H:%M')
print("開始時間:" + dt_date_str)
LIMIT_DL_NUM = int(search_count)                 # ダウンロード数の上限
SAVE_DIR = savedir + '/' + title + '/' + charactername                 # 出力フォルダへのパス（フォルダがない場合は自動生成する）
FILE_NAME = charactername                          # ファイル名（ファイル名の後ろに０からの連番と拡張子が付く）
TIMEOUT = 100                             # 要素検索のタイムアウト（秒）
ACCESS_WAIT = 5                             # アクセスする間隔（秒）
RETRY_NUM = 3                           # リトライ回数（クリック、requests）
DRIVER_PATH = './chromedriver'       # chromedriver.exeへのパス
reqUrl = "https://img.tokuzouserver.net/"
headersList = {
 "Content-Type": "application/json" 
}

# Chromeをヘッドレスモードで起動
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--start-fullscreen')
options.add_argument('--disable-plugins')
options.add_argument('--disable-extensions')
driver = webdriver.Chrome(DRIVER_PATH, options=options)
 
# タイムアウト設定
driver.implicitly_wait(TIMEOUT)
 
tm_driver = time.time()
print('WebDriver起動完了', f'{tm_driver - tm_start:.1f}s')

# Google画像検索ページを取得
url = f'https://www.google.com/search?q={QUERY}&tbm=isch'
driver.get(url)
 
tm_geturl = time.time()
print('Google画像検索ページ取得', f'{tm_geturl - tm_driver:.1f}s')
 
tmb_elems = driver.find_elements_by_css_selector('#islmp img')
tmb_alts = [tmb.get_attribute('alt') for tmb in tmb_elems]
 
count = len(tmb_alts) - tmb_alts.count('')
print(count)
 
while count < LIMIT_DL_NUM:
    # ページの一番下へスクロールして新しいサムネイル画像を表示させる
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(1)
 
    # サムネイル画像取得
    tmb_elems = driver.find_elements_by_css_selector('#islmp img')
    tmb_alts = [tmb.get_attribute('alt') for tmb in tmb_elems]
 
    count = len(tmb_alts) - tmb_alts.count('')
    print(count)  
 
# サムネイル画像をクリックすると表示される領域を取得
imgframe_elem = driver.find_element_by_id('islsp')
 
# 出力フォルダ作成
os.makedirs(SAVE_DIR, exist_ok=True)
 
# HTTPヘッダ作成
HTTP_HEADERS = {'User-Agent': driver.execute_script('return navigator.userAgent;')}
print(HTTP_HEADERS)           
            
# ダウンロード対象のファイル拡張子
IMG_EXTS = ('.jpg', '.jpeg', '.png', '.gif')
 
# 拡張子を取得
def get_extension(url):
    url_lower = url.lower()
    for img_ext in IMG_EXTS:
        if img_ext in url_lower:
            extension = '.jpg' if img_ext == '.jpeg' else img_ext
            break
    else:
        extension = ''
    return extension
 
# urlの画像を取得しファイルへ書き込む
def download_image(url, path, loop):
    result = False
    for i in range(loop):
        try:
            r = requests.get(url, headers=HTTP_HEADERS, stream=True, timeout=10)
            r.raise_for_status()
            with open(path, 'wb') as f:
                f.write(r.content)

        except requests.exceptions.SSLError:
            print('***** SSL エラー')
            break  # リトライしない
        except requests.exceptions.RequestException as e:
            print(f'***** requests エラー({e}): {i + 1}/{RETRY_NUM}')
            time.sleep(1)
        else:
            result = True
            break  # try成功
    return result
 
tm_thumbnails = time.time()
print('サムネイル画像取得', f'{tm_thumbnails - tm_geturl:.1f}s')
 
# ダウンロード
EXCLUSION_URL = 'https://lh3.googleusercontent.com/'  # 除外対象url
count = 0
url_list = []
serverimg = []
for tmb_elem, tmb_alt in zip(tmb_elems, tmb_alts):
     
    if tmb_alt == '':
        continue
 
    print(f'{count}: {tmb_alt}')
 
    for i in range(RETRY_NUM):
        try:
            # サムネイル画像をクリック
            tmb_elem.click()
        except ElementClickInterceptedException:
            print(f'***** click エラー: {i + 1}/{RETRY_NUM}')
            driver.execute_script('arguments[0].scrollIntoView(true);', tmb_elem)
            time.sleep(1)
        else:
            break  # try成功
    else:
        print('***** キャンセル')
        continue  # リトライ失敗
         
    # アクセス負荷軽減用のウェイト
    time.sleep(ACCESS_WAIT)
     
    alt = tmb_alt.replace("'", "\\'")
    try:
        img_elem = imgframe_elem.find_element_by_css_selector(f'img[alt=\'{alt}\']')
    except NoSuchElementException:
        print('***** img要素検索エラー')
        print('***** キャンセル')
        continue
 
    # url取得
    tmb_url = tmb_elem.get_attribute('src')  # サムネイル画像のsrc属性値
 
    for i in range(RETRY_NUM):
        url = img_elem.get_attribute('src')
        if EXCLUSION_URL in url:
            print('***** 除外対象url')
            url = ''
            break
        elif url == tmb_url:  # src属性値が遷移するまでリトライ
            print(f'***** urlチェック: {i + 1}/{RETRY_NUM}')
            time.sleep(1)
            url = ''
        else:
            break
 
    if url == '':
        print('***** キャンセル')
        continue
 
    # 画像を取得しファイルへ保存
    ext = get_extension(url)
    if ext == '':
        print(f'***** urlに拡張子が含まれていないのでキャンセル')
        print(f'{url}')
        continue
 
    filename = f'{FILE_NAME}{count}{ext}'
    path = SAVE_DIR + '/' + filename
    result = download_image(url, path, RETRY_NUM)
    if result == False:
        print('***** キャンセル')
        continue
    if server == str("True"):
        payload = json.dumps({
        "url": url
        })
        response = requests.request("POST", reqUrl, data=payload,  headers=headersList)
        jsonData = response.json()
        serverimg.append(f'{filename}: {jsonData["url"]}')
        url_list.append(f'{filename}: {url}')
    else:
        url_list.append(f'{filename}: {url}')
 
    # ダウンロード数の更新と終了判定
    count += 1
    if count >= LIMIT_DL_NUM:
        break
 
tm_end = time.time()
print('ダウンロード', f'{tm_end - tm_thumbnails:.1f}s')
print('------------------------------------')
total = tm_end - tm_start
total_str = f'トータル時間: {total:.1f}s({total/60:.2f}min)'
count_str = f'ダウンロード数: {count}'
print(total_str)
print(count_str)
 
# urlをファイルへ保存
urldirpath = SAVE_DIR + '/url'
os.mkdir(urldirpath)
if server == str("True"):
    path = SAVE_DIR + '/url/' + 'Download-Url.txt'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(dt_date_str + '\n')
        f.write(total_str + '\n')
        f.write(count_str + '\n')
        f.write('\n'.join(url_list))

    path = SAVE_DIR + '/url/' + 'ShareUrl-TokuzouServerIMG.txt'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(dt_date_str + '\n')
        f.write(total_str + '\n')
        f.write(count_str + '\n')
        f.write('\n'.join(serverimg))
else:
    path = SAVE_DIR + '/url/' + 'Download-Url.txt'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(dt_date_str + '\n')
        f.write(total_str + '\n')
        f.write(count_str + '\n')
        f.write('\n'.join(url_list))

driver.quit()
