import unicodecsv as csv
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# user options
search_cutoff = 2000
site1 = "site1url"
site2 = "site2url"
site3 = "site3url"
site4 = "site4url"
# initialization
driver = webdriver.Chrome(executable_path=r'C:\Users\Jacob\Downloads\chromedriver_win32\chromedriver.exe')
driver.maximize_window()

# site1
driver.get(site1)
list_of_rows = []
while True:
    sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find('div', id='listing_container')
    if table == None:
        break
    for listing in table.findAll('div', attrs={'class': 'proplist-main'}):
        list_of_cells = []
        original_site = "site1"
        address = listing.find('div', attrs={'class': 'proplist-address'}).a.text.strip()
        price = listing.find('div', attrs={'class': 'listinglist_proplist_price'}).a.text.strip()
        price = price[:-1]
        price = price.replace(".", "")
        size = listing.findAll('span', attrs={'class': 'gallery-attr-item-value'})[3].text.strip()
        size = size.replace(",", ".")
        price_per_sq_meter = float(price)/float(size)
        link = listing.find('a', href=True)
        link = "site1domain" + link['href']
        if price_per_sq_meter <= search_cutoff:
            list_of_cells.extend((original_site, address, price, size, price_per_sq_meter, link))
            list_of_rows.append(list_of_cells)
    try:
        next_page_button = driver.find_element_by_class_name('page-next')
    except BaseException:
        break
    try:
        last_page = True
        last_page = driver.find_element_by_class_name('disablednav')
    except BaseException:
        last_page = False

    if last_page:
        break
    elif not last_page:
        next_page_button.click()
        sleep(1)

# site2
last_url = ""
driver.get(site2)
while True:
    url = driver.current_url
    if url == last_url:
        break
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find('div', id='divSearchPageResults')
    if table is None:
        break

    for listing in table.findAll('div', attrs={'class': 'searchResultProperty'}):
        list_of_cells = []
        original_site = "site2"
        address = listing.find('p', attrs={'class': 'searchPropertyLocation'}).text.strip()
        price = listing.find('div', attrs={'class': 'searchPropertyPrice'}).findAll('p')[1].text.strip()
        digits = []
        for i in price:
            if i.isdigit():
                digits.append(i)
        price = "".join(digits).strip()
        try:
            size = listing.find('div', attrs={'class': 'searchPropertyInfo'}).findAll('p')[3].text
            size = size[:-2].strip()
        except BaseException:
            size = listing.find('div', attrs={'class': 'searchPropertyInfo'}).findAll('p')[5].text
            size = size[-2].strip()
        try:
            price_per_sq_meter = float(price)/float(size)
        except ValueError:
            pass
        link = listing.find('a', href=True)
        link = "site2domain" + link['href']
        if size != "" and price_per_sq_meter <= search_cutoff:
            list_of_cells.extend((original_site, address, price, size, price_per_sq_meter, link))
            list_of_rows.append(list_of_cells)
    try:
        next_page_button = driver.find_element_by_class_name('paginadorNext')
    except BaseException:
        break
    last_url = url
    try:
        next_page_button.click()
        sleep(1)
    except BaseException:
        break


# site3
driver.get(site3)
cookies_bar = driver.find_element_by_class_name('cookiesBarClose')
cookies_bar.click()
while True:
    url = driver.current_url
    if url == last_url:
        break
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find('div', attrs={'class': 'col-md-content'})
    if table == None:
        break
    for listing in table.findAll('div', attrs={'class': 'offer-item-details'}):
        list_of_cells = []
        original_site = "ImoVirtual"
        address = listing.find('p', attrs={'class': 'text-nowrap'}).text.strip()
        address = address[25:]
        price = listing.find('li', attrs={'class': 'offer-item-price'}).text.strip()
        price = price[:-2]
        price = price.replace(" ", "")
        size = listing.find('li', attrs={'class': 'offer-item-area'}).text.strip()
        size = size[:-2]
        size = size.replace(",", ".")
        price_per_sq_meter = listing.find('li', attrs={'class', 'offer-item-price-per-m'}).text.strip()
        price_per_sq_meter = price_per_sq_meter[:-4]
        price_per_sq_meter = price_per_sq_meter.replace(" ", "").replace(",", ".")
        price_per_sq_meter = float(price_per_sq_meter)
        link = listing.find('a', href=True)
        link = link['href']
        if price_per_sq_meter <= search_cutoff:
            list_of_cells.extend((original_site, address, price, size, price_per_sq_meter, link))
            list_of_rows.append(list_of_cells)

    try:
        next_page_button = driver.find_element_by_class_name('pager-next')
    except NoSuchElementException:
        break

    next_page_button = next_page_button.find_element_by_tag_name('a')
    next_page_button.click()
    sleep(1)

# site4
driver.get(site4)
while True:
    url = driver.current_url
    if url == last_url:
        break
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    exist = soup.find('div', id='ctl00_ContentPlaceHolder1_div_imoveis')
    if exist == None:
        break
    table = soup.find('tbody')

    for row in table.findAll('tr'):
        for column in row.findAll('td'):
            list_of_cells = []
            original_site = "ERA"
            try:
                address = column.find('div', attrs={'class': 'titulo'}).findAll('span', recursive=False)
            except AttributeError:
                break
            first = address[0].text
            second = address[1].text
            address = first + second
            price = column.find('span', attrs={'class': 'preco'}).find('span')
            if price is None:
                break
            price = price.text
            price = price[:-2]
            price = price.replace(".", "")
            size = column.findAll('span', attrs={'class': 'num'})
            sqft = 0
            for option in size:
                try:
                    sqft = int(option.text)
                except ValueError:
                    sqft = option.text
            size = sqft
            price_per_sq_meter = 2001
            try:
                price_per_sq_meter = int(price)/int(size)
            except ValueError:
                pass
            link = column.find('a', href=True)
            try:
                link = "site4domain" + link['href']
            except TypeError:
                link = "none"
            if size != "N/D" and price_per_sq_meter <= search_cutoff:
                list_of_cells.extend((original_site, address, price, size, price_per_sq_meter, link))
                list_of_rows.append(list_of_cells)

    try:
        next_page_button = driver.find_element_by_id('ctl00_ContentPlaceHolder1_pnl_paginacao_setas2')
    except BaseException:
        break
    last_url = url
    next_page_button.click()
    sleep(1)

driver.close()

# Write Output to CSV
outfile = open("./data.csv", "wb")
writer = csv.writer(outfile, encoding="utf-8")
writer.writerow(["Original Site", "Address", "Price", "Square Meters", "Price/Square Feet", "Link"])
writer.writerows(list_of_rows)
