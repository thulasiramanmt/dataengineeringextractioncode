python code

import time
import nltk
from newspaper import Article, ArticleException
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup


nltk.download('punkt')


base_url = 'https://www.dataengineeringweekly.com/data-engineering-weekly-'
num_pages = 2


blog_links = {}


for page_num in range(1, num_pages+1):
    url = base_url + str(page_num)


    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)


        if response.status_code != 200:
            print(f"Error: Could not retrieve {url}")
            continue


        soup = BeautifulSoup(response.content, 'html.parser')


        links = soup.select('a[href^="http://"], a[href^="https://"]')
        for link in links:
            blog_url = link['href']
            domain = urlparse(blog_url).netloc
            if domain == 'www.dataengineeringweekly.com':
                continue


            try:
                article = Article(blog_url)
article.download()
                article.parse()
                article.nlp()


                keywords = article.keywords if article.keywords else []
                authors = article.authors if article.authors else []
                title = article.title if article.title else ""
                summary = article.summary if article.summary else ""


                blog_links.setdefault(domain, [])
                blog_links[domain].append({
                    "link": blog_url,
                    "keywords": keywords,
                    "authors": authors,
                    "title": title,
                    "summary": summary
                })


            except ArticleException as e:
                print(f"Error: {e}")
                continue


    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        continue


    time.sleep(2)


for domain, links in blog_links.items():
    print(f"Domain: {domain}")
    print("Blogs:")
    for blog in links:
        print(f"   - Link: {blog['link']}")
        print(f"     Keywords: {blog['keywords']}")
        print(f"     Authors: {', '.join(blog['authors']) if blog['authors'] else ''}")
        print(f"     Title: {blog['title']}")
        print(f"     Summary: {blog['summary']}")
        print()


