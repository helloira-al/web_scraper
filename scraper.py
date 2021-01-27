import requests
from bs4 import BeautifulSoup
import pprint

first_page_response = requests.get('https://news.ycombinator.com/news')
second_page_response = requests.get('https://news.ycombinator.com/news?p=2')
first_page_soup = BeautifulSoup(first_page_response.text, 'html.parser')
second_page_soup = BeautifulSoup(second_page_response.text, 'html.parser')
first_page_links = first_page_soup.select('.storylink')
first_page_subtext = first_page_soup.select('.subtext')
second_page_links = second_page_soup.select('.storylink')
second_page_subtext = second_page_soup.select('.subtext')

all_links = first_page_links + second_page_links
all_subtexts = first_page_subtext + second_page_subtext

def sort_stories(hnlist):
    return sorted(hnlist, key= lambda k:k['votes'], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    for i, link in enumerate(links):
        title = links[i].getText()
        href = links[i].get('href', None)
        vote = subtext[i].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ' '))
            if points >=200:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories(hn)

pprint.pprint(create_custom_hn(all_links, all_subtexts))
