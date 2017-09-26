import unicodecsv as csv
from bs4 import BeautifulSoup
from selenium import webdriver


# Browser
driver = webdriver.Chrome(executable_path="path")
driver.get('url')

# User credentials and login
username = driver.find_element_by_name('Login')
username.send_keys('username')
password = driver.find_element_by_name('Password')
password.send_keys('password')
login_button = driver.find_element_by_name('LoginButton')
login_button.click()

# navigate to the my communities page
page_drop_downs = driver.find_elements_by_class_name("dropdown-toggle")
communities_list_links = []
for element in page_drop_downs:
    if element.text == "Communities":
        element.click()
        my_communities_link = driver.find_element_by_link_text("My Communities")
        my_communities_link.click()
        break

# navigate to the meeting page
page_link = driver.find_element_by_id("MainCopy_ctl02_lstCommunityList_hlTitle_1")
page_link.click()

# Navigate to the members page
members_page_drop_down = driver.find_element_by_class_name("glyphicon-align-justify")
members_page_drop_down.click()
members_page_link = driver.find_element_by_id("MainCopy_ctl02_Tab6Link")
members_page_link.click()


# loop through all the pages
page_switcher = 1
page_count = 1
list_of_rows = []
while True:
    # get page source code and find member data table
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find('div', id='MainCopy_ctl11_DisplayContactsUpdatePanel')

    # scrape data
    for row in table.findAll('div', attrs={'class': 'row member-row'}):
        list_of_cells = []
        name = row.find('div', attrs={'class': 'member-name'}).a.string
        list_of_cells.append(name)
        company = row.find('div', attrs={'class': 'company-name'}).__str__()
        company = company[130:]
        company.strip()
        list_of_cells.append(company)

        # filter out schools
        if not ("University" in list_of_cells[1] or
                "School" in list_of_cells[1] or
                "College" in list_of_cells[1] or
                ("Institute" in list_of_cells[1] and "Technology" in list_of_cells[1]) or
                "Universidad" in list_of_cells[1] or
                ("Institute" in list_of_cells[1] and "Tech" in list_of_cells[1]) or
                "college" in list_of_cells[1] or
                "university" in list_of_cells[1] or
                "Virginia Tech" in list_of_cells[1] or
                "Georgia Tech" in list_of_cells[1] or
                "UC Berkeley" in list_of_cells[1] or
                list_of_cells[1] is None or
                list_of_cells[1] == ""):
            list_of_rows.append(list_of_cells)

    # check if all the pages are scanned
    if page_count == 247:
        break

    # page navigation
    # next page group
    if page_switcher > 4:
        page_switcher = 1
        page_count += 1
        next_section_button = driver.find_element_by_id("MainCopy_ctl11_Pager_NextSectionButton")
        next_section_button.click()
    # next page
    else:
        link_id = "MainCopy_ctl11_Pager_Repeater1_PageLink_" + page_switcher.__str__()
        page_switcher += 1
        page_count += 1
        next_page_button = driver.find_element_by_id(link_id)
        next_page_button.click()


# Write Output to CSV
outfile = open("./filtered_informs.csv", "wb")
writer = csv.writer(outfile, encoding='utf-8')
writer.writerow(["Name", "Company"])
writer.writerows(list_of_rows)
