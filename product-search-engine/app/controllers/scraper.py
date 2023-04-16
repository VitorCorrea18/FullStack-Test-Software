from bs4 import BeautifulSoup
from selenium import webdriver


def define_url(category, site, query):
    switcher = {
        'mercado_livre': 'https://lista.mercadolivre.com.br/',
        'buscape': 'https://www.buscape.com.br/search?q=',
    }
    base_url = switcher.get(site)
    category_defined = define_category(category, site)
    if category_defined == None:
        return False
    else:
        if query == '':
            return base_url + category_defined + category_defined
        elif query != '' and site == 'mercado_livre':
            new_query = query + '_NoIndex_True#D[A:' + query + ',on]'
            return base_url + category_defined + new_query
        elif query != '' and site == 'buscape':
            return base_url + category_defined + query
        
def define_category(category, site):
    if site == 'mercado_livre':
        switcher = {
            'mobile': 'celulares-telefones/celulares-smartphones/',
            'refrigerator': 'eletrodomesticos/refrigeracao/geladeiras/',
            'tv': 'eletronicos-audio-video/televisores/',
        }
        print(category, switcher.get(category))
        return switcher.get(category)
    elif site == 'buscape':
        switcher = {
            'mobile': 'celular-e-smartphone/',
            'refrigerator': 'geladeira/',
            'tv': 'tv/',
        }
        return switcher.get(category)

def scrape_mercado_livre(soup):
    data = []
    for item in soup.find_all('div', class_='andes-card'):
        link = item.find('a', class_='ui-search-link')['href']
        image = item.find('img', class_='ui-search-result-image__element')['src']
        title = item.find('h2', class_='ui-search-item__title').text
        price = item.find_all('span', class_='price-tag-fraction')[0].text
        data.append({
            'link': link,
            'title': title,
            'image': image,
            'price': price,
        })
    return data

def scrape_buscape(soup):
    data = []
    for item in soup.find_all('a', class_='SearchCard_ProductCard_Inner__7JhKb'):
        link = 'http://www.buscape.com.br/' + item.get('href')
        title = item.find('div', class_='SearchCard_ProductCard_NameWrapper__Gv0x_').text
        image = item.find('div', class_='SearchCard_ProductCard_Image__ffKkn').find('img')['src']
        best_merchant = item.find('h3', class_='SearchCard_ProductCard_BestMerchant__f4t5p')
        if best_merchant:
            best_merchant = best_merchant.text
        else:
            best_merchant = ''
        best_price = item.find('p', class_='Text_Text__h_AF6').text
        installments = item.find('p', class_='SearchCard_ProductCard_Installment__tFssR').text
        data.append({
            'link': link,
            'title': title,
            'image': image,
            'best_merchant': best_merchant,
            'best_price': best_price,
            'installments': installments,
        })
    return data

def scrape_data(category, site, query):
    url = define_url(category, site, query)
    if url:
        # I had to use Selenium webdriver because these uses JavaScript to asynchronously decode the images URLs.
        driver = webdriver.Chrome()
        driver.get(url)
        driver.implicitly_wait(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        if site == 'mercado_livre':
            return scrape_mercado_livre(soup)
        elif site == 'buscape':
            return scrape_buscape(soup)
    else:
        return False