import datetime as dt
import csv
from bs4 import BeautifulSoup
from lxml import html
from datetime import datetime
from multiprocessing import Pool
from random import uniform, choice
from time import sleep, time
import requests
import os.path
import re
import os
DATAST_FOLDER = 'input/test/'
IMGS_FOLDER  = 'input/images/search_thumbnails/'
DFILE_NAME    = 'recipe_details'  + '.csv'
PIC_LIST      = 'pic_list' + '.csv'



from IPython.display import Image
PATH = "./"
Image(filename = PATH + "burger.jpg", width='100%', height=140)


def get_list_of_recipes():
    recipe_links = []
    chef_file = DATAST_FOLDER + 'chefkoch.csv'
    chef_file
    #print(chef_file)
    with open(chef_file, 'r') as f:
        chefkoch = csv.reader(f)
        for row in chefkoch:
            try:
                recipe_links.append(row[-2])
            except: 
                continue 
    return(recipe_links)

def get_list_of_scraped_recipes():
    
    recipe_links = []
    recipes_file = DATAST_FOLDER + DFILE_NAME
    if os.path.isfile(recipes_file):
        with open(recipes_file, 'r') as f:
            chefkoch = csv.reader(f)
            for row in chefkoch:
                try:
                    recipe_links.append(row[0])
                except: 
                    continue
    print('**************')
    print(recipe_links)
    print('**************')
    return(recipe_links)


def list_to_scrape():
    
    l_scraped = get_list_of_scraped_recipes()
    #print('-----------')
    #print(l_scraped)
    l_all     = get_list_of_recipes()
    
    
    #print('-----------')
    
    l_to_scrape = list(set(l_all) - set(l_scraped))
    #print('Difference of sets:', len(l_to_scrape))
    
    return(l_to_scrape)
recipe_links = list_to_scrape()
#recipe_links
def write_recipe_details(data):
    
    dpath = DATAST_FOLDER + DFILE_NAME
   
    with open(dpath, 'a', newline='') as f:
        writer = csv.writer(f)
        try:
            writer.writerow((data['link'],
                             data['ingredients'],
                             '------------------------',
                             #data['zubereitung'],
                             #data['tags'],
                             #data['gedruckt:'],
                             #data['n_pics']
                             #data['reviews'],
                             #data['gespeichert:'],
                             #data['Freischaltung:'],
                             #data['author_registration_date'],
                             #data['author_reviews']
                            ))
        except:
            writer.writerow('')
def write_picture_list(pics):
    dpath = DATAST_FOLDER + PIC_LIST
    with open(dpath, 'a', newline='') as f:
        writer = csv.writer(f)
        try:
            writer.writerow(pics)
        except:
            writer.writerow('')
def get_stats(soup):
    stats = {}
    # DROPPED
    # anzahl bewertungen
    reviews = soup.find('div', id="recipe__rating").find('span', class_ = "rating__total-votes m-r-s").text
    #stats['reviews'] = reviews
    
    # andere statistiken
    if reviews != '(0)':
        stats_table = soup.find('div', id="recipe-statistic").find_all('table')[1].find_all('tr')[1:5]
    else:
        stats_table = soup.find('div', id="recipe-statistic").find_all('table')[0].find_all('tr')[1:5]
        
    for tr in stats_table:
        stat_name  = tr.find_all('td')[0].text.strip()
        stat_value = tr.find_all('td')[1].text.strip().split(' ')[0]
        stats[stat_name] = stat_value
    return(stats)

def get_n_pictures(html_text):
    tree = html.fromstring(html_text)
    # alle bilder links
    links_pics = tree.xpath('//div[contains(@id, "slider")]//img[@class="slideshow-image lazyload"]/@src')
    return links_pics

def get_zubereitung(soup):
    zuber = soup.find('div', id="rezept-zubereitung").text.strip()
    zuber = zuber.replace('\n', ' ').replace('\r', '')
    return zuber

def get_ingredients(soup):
    # liste von zubereitungen
    ingredient_list = []
    amounts_ingredients = soup.find('table', class_="ingredients table-header").find_all('tr')
    
    for tr in amounts_ingredients:
        am = tr.find_all('td')[0].text.strip() # amount
        td = tr.find_all('td')[1].text.strip().split(',')[0] # ingredient
        td = re.sub('\(.*?\)','', td)
        ingr = am + '@' + td
        ingredient_list.append(ingr)
    
    #print(str.join(',', ingredient_list))
    return(str.join(',', ingredient_list))

def get_tags(soup):
    tags = []
    tag_cloud = soup.find('ul', class_ = 'tagcloud').find_all('li')
    for li in tag_cloud:
        tags.append(li.find('a').text.strip())
        
    return(str.join(',', tags))

# DROPPED
#def get_author_info(soup):
#    author = {}
#    author['author_registration_date'] = soup.find('div', class_="user-details").find('p').find('br').previous_sibling.strip()
#    author['author_reviews'] = soup.find('div', class_="user-details").find('p').find('br').next_sibling.strip()
#    return(author)
desktop_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']

def random_headers():
    return {'User-Agent': choice(desktop_agents),'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
failed_urls = []
def get_html(url):
    
    i = 5
    while i > 0:
        try:
            page = requests.get(url, headers=random_headers())
            if page.status_code != requests.codes.ok:
                page.raise_for_status()
            else:
                print(url)
                return page.text        
        except requests.exceptions.RequestException as e:
            print("Could not fetch " + str(url))
            print(e)
            # sichere url zu einer Liste von fehlgeschlagenen Links
            failed_urls.append(url)
            sleep(5)
            i = i - 1
            continue

    #print("Link zum 5. Mal nicht abrufbar " + str(url) + " ,abbrechen")
    return None
def get_recipe_info(url):
   
    url=url[22:]
    
    sleep_time = uniform(2, 4)
    sleep(sleep_time)
    
    html_text = get_html(url)
    #print(url[22:])
    
    
   
    try:
        
        soup = BeautifulSoup(html_text, 'lxml')
        ingredient_list = get_ingredients(soup)
        list_pics = get_n_pictures(html_text)
        data = {'link' : url,
                'ingredients' : ingredient_list,
                }
        
        
    except:
      
        data = ''
        list_pics = ['error']
        
    
   
    
    write_recipe_details(data)
    
    #write_picture_list(list_pics)
#print(recipe_links)    
get_recipe_info(recipe_links[10])
get_recipe_info(recipe_links[20])
get_recipe_info(recipe_links[30])
start_time = datetime.now()
print(start_time)
with Pool(15) as p:
    p.map(get_recipe_info, recipe_links)
print("--- %s seconds ---" % (datetime.now() - start_time))

