#import requests python to get the URL to start scraping the items
page = requests.get(url)

#create a BeautifulSoup object to manage the HTML parsed page content
soup = BeautifulSoup(page.content, 'html.parser')


#functions

soup.find() #find the first instance of a tag or item
soup.find_all() #find all instances of a tag or item

#we can use re to create a regex string to find particular items