from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import *
from bs4 import BeautifulSoup
import time

# Maksymalny czas czekania na wczytanie strony (w sekundach)
czas_wczytania = 5

# filmy przesłane przez CNBC (20000 filmów) - wiele przewijań
link_playlisty="""https://www.youtube.com/playlist?list=UUrp_UI8XtuYfpiqluWLD7Lw"""
# Anime Openings - jedno przewinięcie
#link_playlisty="""https://youtube.com/playlist?list=PL2bz44SztFKfe1oxtJc02km-nfkk6VxNJ&si=rf3BRghX_nV55Hfr"""
# BotW - dwa przewinięcia
link_playlisty = """https://youtube.com/playlist?list=PLPQswGgsDXyMfbcBX4UgkWXR8LMwypi43&si=O1jqZAnjR91Q2PbV"""

# Ustaw język przeglądarki na angielski, żeby znajdować odpowiednie elementy po nazwie
options = ChromeOptions()
options.add_argument("--accept-lang=en-US")
# Użyj Chrome, żeby móc scrollować
driver = webdriver.Chrome(options)

# Rozpocznij wczytywanie strony
driver.get(link_playlisty)
wait = WebDriverWait(driver, czas_wczytania)
time.sleep(czas_wczytania)

# Pomiń wyskakujące okienko o plikach cookie
# Znajdź przycisk odrzucenia cookie
# atrybut aria-label zawiera słowo "Reject"
przycisk_odrzucenie_cookies = driver.find_element(By.CSS_SELECTOR, """[aria-label~="Reject"]""")
if przycisk_odrzucenie_cookies is not None:
    przycisk_odrzucenie_cookies.click()
wait = WebDriverWait(driver, czas_wczytania)
time.sleep(czas_wczytania)
# https://stackoverflow.com/a/48851166
# Przewiń stronę do końca, żeby wczytać wszystkie filmy
# TODO chcemy zeby rozszerzal sie tylko pojemnik z filmami z rozpatrywanej playlisty, a potem tylko te filmy analizowac
# TODO jak nazywa sie ten pojemnik? 
last_height = driver.execute_script("""return document.querySelector("#contents").scrollHeight""")
while True:
    # Scroll down to the bottom.
    ActionChains(driver).scroll_by_amount(0, last_height).perform()
    # Wait to load the page.
    wait = WebDriverWait(driver, czas_wczytania)
    time.sleep(czas_wczytania)
    # Calculate new scroll height and compare with last scroll height.
    new_height = driver.execute_script("""return document.querySelector("#contents").scrollHeight""")
    if new_height == last_height:
        break
    last_height = new_height

# Zapisz stronę do pliku .html
content = driver.page_source
soup = BeautifulSoup(content, "html.parser")
html = soup.prettify()
with open("strona.html", "w", encoding="utf-8") as file:
    file.write(soup.prettify()) 

# tytul
# a id="video-title" title=[1] href=[2]
klasa_nazwisko="video-title"
div_nazwisko = soup.find("a",{"id": klasa_nazwisko})
print(div_nazwisko)

driver.quit()