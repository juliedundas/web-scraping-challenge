#Imports & Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
#pip install ipython
#pip install nbconver


#Site Navigation
executable_path = {"executable_path": "/Users/sharonsu/Downloads/chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)


# Defining scrape & dictionary
def scrape():
    final_data = {}
    output = marsNews()
    final_data["mars_news"] = mars_new()
    final_data["mars_image"] = mars_image()
    final_data["mars_facts"] = mars_facts()
    final_data["mars_hemisphere"] = mars_hem()

    return final_data

#Mars News scrape function
def mars_news():
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    # Retrieve page with the requests module
    response = requests.get(url)
     # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')
    # results are returned as an iterable list
    results = soup.find_all("div", class_="slide")
    # Loop through returned results
    article_list = []
    for result in results:
    # Error handling
        try:
        # Identify and return title of article
            time.sleep(3)
            news_title = result.find('div', class_="content_title")
            title = news_title.find('a').text
            # Identify and return description of article
            news_p = result.find('div', class_="rollover_description")
            description = news_p.find('div', class_="rollover_description_inner").text
        
        # Print results only if title, price, and link are available
            if (news_title and news_p):
                print('-------------')
                print(f'Article Title: {title}')
                article_list.append(result)
                print(f'Article Description: {description}')
                #description_list.append(result)
           
        except AttributeError as e:
            print(e)
    #Print the latest news title and description
    print(f'Latest News Title: {title}')
    print(f'Description of Latest News Title: {description}')


#Mars image scrape function Space Images - Featured Image
def mars_image():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    images = soup.find_all('article', class_='carousel_item')
    #Loop through images to get partial url
    for image in images:
        image_url = image.find('a')['data-fancybox-href']
    #create varible for featured image url
    main_url = 'https://www.jpl.nasa.gov/'
    featured_image_url = main_url + image_url
    print(f"Click this link to see the current featured image: {featured_image_url}")

#Mars  Weather - not required



# Mars Facts scrape function
def mars_facts():
    #Create link for pandas URL
    pandas_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(pandas_url)
    df = tables[0]
    df.columns = ['Topic', 'Data']
    df.set_index(['Topic'])
    #Create html table
    html_table = df.to_html()
    html_table.replace('\n', '')
    df.to_html('table.html')    

# Mars hemisphere scrape:
def mars_hem():  

    print(final_data)