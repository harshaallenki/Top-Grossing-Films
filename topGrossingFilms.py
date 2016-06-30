from urllib2 import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from time import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')

BASE_URL = "http://www.wikipedia.org"
PAGE_URL = "https://en.wikipedia.org/wiki/List_of_highest-grossing_films"

FILMS_TABLE_TAG = "wikitable sortable plainrowheaders"
FILM_INFO_TABLE_TAG = "infobox vevent"
BUDGET_BOXOFFICE_TAG = "line-height:1.3em;"

def makeSoup(html_page):
	soup = BeautifulSoup(html_page,"lxml")
	return soup
t1 = time()


print("Getting page....")
page = urlopen(PAGE_URL).read()
print("Got page")
soup = makeSoup(page)

films_table = soup.find("table",class_ = FILMS_TABLE_TAG)
film_rows = films_table.find_all("tr")[1:]
print("Finding films")
th_all = films_table.find_all("th");
th_all = th_all[6:]
print(len(th_all))

top_films = []
top_films_urls = []
top_films_year = []

print("Finding films url")
for film in th_all:
	try:
		top_films.append(film.a.text)
		top_films_urls.append(BASE_URL+film.a['href'])
	except Exception, e:
		print(film)
	
print("Finding films years")
for row in film_rows:
	top_films_year.append(row.find_all("td")[3].string)


print("Getting Individual films budget and boxoffice details")
budget_for_films = []
boxoffice_for_films = []
count = 0
for url in top_films_urls:
	print str(count)+". Getting film page of "+top_films[count]+"...."
	count += 1
	film_page = urlopen(url).read()

	film_soup = makeSoup(film_page)

	info_table_rows = film_soup.find("table",class_ = FILM_INFO_TABLE_TAG).find_all("tr")
	try:
		budget_for_films.append(info_table_rows[-2].find("td").contents[0])
		boxoffice_for_films.append(info_table_rows[-1].find("td").contents[0])
	except Exception, e:
		print(info_table_rows[-2:])
	
print(time() - t1,"s")
print("Budget")
for budget in budget_for_films:
	print budget
print("Boxoffice")
for boxoffice in boxoffice_for_films:
	print boxoffice

d = {"Film":top_films,"Year":top_films_year}
df_films = pd.DataFrame(d)
df_films.to_csv('topGrossingFilms.csv')





