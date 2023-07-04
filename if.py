from firebase import firebase
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

# Firebaseの設定
firebase = firebase.FirebaseApplication('https://www.gstatic.com/firebasejs/9.23.0/firebase-app.js', None)

# Seleniumの設定
options = Options()
options.headless = True  # ヘッドレスモードで実行（画面表示なし）
driver = webdriver.Firefox(options=options, executable_path='/opt/homebrew/bin/geckodriver')

# スケジュールページのURL
url = 'https://www.imageforum.co.jp/theatre/schedule/'

# ページを取得してHTMLを取得
driver.get(url)
html = driver.page_source

# BeautifulSoupでHTMLをパース
soup = BeautifulSoup(html, 'html.parser')

# スケジュール情報を抽出してFirebaseに送信
schedule_box = soup.find('div', class_='schedule-day-box')
schedule_day_title = schedule_box.find('h2', class_='schedule-day-title').text.strip()
theaters = schedule_box.find_all('div', class_='schedule-box')

for theater in theaters:
    theater_name = theater.find('caption').img['alt']
    units = theater.find_all('td', class_='schebox')

    for unit in units:
        start_time = unit.div.text.strip()
        movie_title = unit.p.text.strip()
        end_time = unit.span.text.strip()
        movie_link = unit.a['href']

        # Firebaseにデータを送信
        data = {
            'date': schedule_day_title,
            'theater': theater_name,
            'start_time': start_time,
            'end_time': end_time,
            'movie_title': movie_title,
            'movie_link': movie_link
        }
        result = firebase.post('/schedule', data)
        print('Data sent to Firebase:', result)

# ブラウザを終了
driver.quit()


