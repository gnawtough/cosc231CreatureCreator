import requests
from bs4 import BeautifulSoup
import json

def fetch_page(url):
    response = requests.get(url)
    response.raise_for_status()  # Will raise an HTTPError for bad requests (400 or 500)
    return response.text

def extract_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    return [a['href'] for a in soup.select('div.entry-content a') if a['href'].startswith('https://factanimal.com')]


def extract_facts(url):
    html = fetch_page(url)
    soup = BeautifulSoup(html, 'html.parser')
    h1_tag = soup.find('h1')
    if h1_tag is None:
        print(f"No title found at {url}")
        return None  # Or you can return some default data structure

    title = h1_tag.get_text(strip=True)
    facts_section = soup.find('div', class_='entry-content')
    if facts_section is None:
        print(f"No facts section found at {url}")
        return None  # Or handle it in another suitable way

    facts = []

    for fact in facts_section.find_all('p'):
        next_title = fact.find_next_sibling('h2')
        if next_title and next_title.get_text(strip=True).startswith("Interesting"):
            break
        if fact.find('strong'):
            continue  # Skip headings within the content
        facts.append(fact.get_text(strip=True))

    return {
        'title': title,
        'url': url,
        'facts': facts
    }


def main():
    index_url = 'https://factanimal.com/animals/'
    index_html = fetch_page(index_url)
    animal_links = extract_links(index_html)

    all_animal_facts = []

    for link in animal_links:
        try:
            facts = extract_facts(link)
            if facts is not None:
                all_animal_facts.append(facts)
                print(f"Extracted facts for {facts['title']}")
            else:
                print(f"Skipped {link} due to missing data.")
        except requests.HTTPError as e:
            print(f"Failed to fetch {link}: {e}")

    with open('animal_facts.json', 'w') as f:
        json.dump(all_animal_facts, f, indent=4)


if __name__ == '__main__':
    main()

