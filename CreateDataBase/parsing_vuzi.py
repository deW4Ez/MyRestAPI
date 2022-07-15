# Создание базы данных из данных о поступлении в ВУЗы из сервиса Postupi.online

from requests import Session
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# Создаем класс для БД
 
Base = declarative_base()

class University(Base):
    __tablename__ = "university"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    avg_rate_free = Column(Integer)
    avg_rate_paid = Column(Integer)
    count_free_place = Column(Integer)
    count_paid_place = Column(Integer)
    city = Column(String(128))

    def __repr__(self):
        return f"{self.name} | Ср. балл на бюджет - {self.avg_rate_free} | Ср. балл на платное {self.avg_rate_paid} | Кол-во бюджет. мест {self.count_free_place} | Кол-во плат. мест {self.count_paid_place}"



#Парсим сайт postupi.online, используя Selenium, чтобы получить данные о ВУЗах

PRODUCT_URL = "https://postupi.online/vuzi/?utm_source=yandex.ru&utm_medium=organic&utm_campaign=yandex.ru&utm_referrer=yandex.ru"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36 OPR/88.0.4412.65"    
}
driver = webdriver.Firefox(executable_path="./geckodriver")
driver.get(PRODUCT_URL)
sleep(5) # Для обхода защиты. На сайте перед входом стоит начальная загрузка, которая мешает обычному парсингу.
page = driver.page_source
soup = BeautifulSoup(page,"lxml")
driver.close()
driver.quit()


#Собираем данные с сайта

titles = soup.find_all(class_="list__h")
scores = soup.find_all(class_="list__score-wrap")
cities = soup.find_all(class_="list__pre")


#Создаем БД

engine = create_engine("sqlite:///../database.sqlite")
Base.metadata.create_all(engine)
sess = Session(bind=engine)


#Добавляем записи, учитывая специфику используемых данных (Если у ВУЗа нет бюджетных мест, то баллы упускаются, а в количестве мест пишется `нет`)

for i in range(len(scores)):
    numbers = [s.get_text() for s in scores[i].find_all("b")]
    curr_city = cities[i].find_all("span")
    this_city = curr_city[len(curr_city)-2].get_text()
    if numbers[1] == "нет":
        sess.add(
            University(                
                name = titles[i].get_text(), 
                avg_rate_free = 0, 
                avg_rate_paid = float(numbers[0]), 
                count_free_place = 0, 
                count_paid_place = float("".join(numbers[2].split())),
                city = this_city)
        )
        sess.commit()
    else:        
        sess.add(
            University(name = titles[i].get_text(), 
                avg_rate_free = float(numbers[0]), 
                avg_rate_paid = float(numbers[1]), 
                count_free_place = float("".join(numbers[2].split())), 
                count_paid_place = float("".join(numbers[3].split())),
                city = this_city)
        )
        sess.commit()
        
    
    
        
