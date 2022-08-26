import re
import bs4
import requests


def remove_text_between_parens(text):
    regex = re.compile(r"(<[^<>]*>)|\([^()]*\)")
    return re.sub(regex, r'\1', text)


def find_first_link(url):
    response = requests.get(url)
    html = response.text
    soup = bs4.BeautifulSoup(html, "html.parser")

    # This div contains the article's body
    # (Sept 2017: Body nested in two div tags)
    content_div = soup.find(
        id="mw-content-text").find(class_="mw-parser-output")
    content_div = remove_text_between_parens(str(content_div))
    # stores the first link found in the article, if the article contains no
    # links this value will remain None
    # print(content_div)
    content_div = bs4.BeautifulSoup(content_div, "html.parser")
    article_link = None
    # print(type(content_div))
    # print(content_div.prettify())
    all_ps = content_div.find_all('p',recursive=True)

    for p in all_ps:
        if not p.find_all('a',recursive=True):
            continue
        else:
            atags = p.find_all('a',recursive=True)
            for a in atags:
                if '#' in a.get('href'):
                    continue
                else:
                    article_link = a.get('href')
                    break
            break

    # Build a full url from the relative article_link url
    # first_link = urllib.parse.urljoin(
    #     'https://en.wikipedia.org/', article_link)
    first_link = BASE_URL+article_link
    return first_link


def continue_crawl(search_history, target_url, max_steps=55):
    if search_history[-1] == target_url:
        print(target_url)
        print("Philosphy reached in {} steps!".format(len(search_history)))
        return False
    elif len(search_history) > max_steps:
        print("Maximum (55) searches reached, search aborted.")
        return False
    elif search_history[-1] in search_history[:-1]:
        print("Arrived at an article already seen, search aborted.")
        return False
    else:
        return True

if __name__ == "__main__":
    start_url = "https://en.wikipedia.org/wiki/Duke_Kunshan_University"
    # start_url = "https://en.wikipedia.org/wiki/Phenomenon"
    target_url = "https://en.wikipedia.org/wiki/Philosophy"
    BASE_URL = "https://en.wikipedia.org"
    article_chain = [start_url]

    while continue_crawl(article_chain, target_url):
        print(article_chain[-1])

        first_link = find_first_link(article_chain[-1])
        if not first_link:
            print("Arrived at an article with no links, search aborted.")
            break

        article_chain.append(first_link)