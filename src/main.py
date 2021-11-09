from bs4 import BeautifulSoup
from selenium import webdriver
from flask import Flask, request, jsonify, render_template
import requests
import psycopg2 as pos

app = Flask(__name__)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"}
chrome_driver = r'chromedriver\chromedriver.exe'

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path=chrome_driver, options=options)

app.config['SECRET_KEY'] = 'thisismyflasksecretkey'
connection=pos.connect("dbname=pyhhh user=postgres password=aldy258654")
cursor=connection.cursor()

@app.route('/coin', methods=['GET', 'POST'])
def coin():
    if request.method == 'POST':
        coin = request.form['coin']

        target = 'https://coinmarketcap.com/currencies/' + coin + '/news/'
        driver.get(target)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        title = []
        parag = [[],[],[],[],[],[]]
        a = 0
        for links in soup.find_all('a', class_="svowul-0 jMBbOf cmc-link"):
            id = 1

            if links['href'][0] != 'h':       
                page_link = 'https://coinmarketcap.com' + links['href']
            else:
                page_link = links['href']

            title.append(links.h3.text)

            r = requests.get(page_link).text
            soup_links = BeautifulSoup(r, 'lxml')
            k = 0
            for data in soup_links.find_all('p', class_=None):
                parag[a].append(data.text)              
                cursor.execute("""insert into paragraph(id, article, parags) values (%s,%s,%s);""", (id, title[a], parag[a][k]))
                k += 1

            id += 1
            a += 1
            connection.commit()

        return render_template('index.html', content = title, parag = parag)

    return '''
           <form method="POST">
               <div><label>Cryptocurrency: <input type="text" name="coin"></label></div>
               <input type="submit" value="Submit">
           </form>'''

if __name__ == '__main__':
    app.run(debug=True, port=5000)