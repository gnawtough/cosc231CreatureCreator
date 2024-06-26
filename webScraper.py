import requests
from bs4 import BeautifulSoup
import json

def fetch_page(url):
    response = requests.get(url)
    response.raise_for_status()  # Will raise an HTTPError for bad requests (400 or 500)
    return response.text

# self explanatory
def extract_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    return [a['href'] for a in soup.select('div.entry-content a') if a['href'].startswith('https://factanimal.com')]

# parses html for titles and tables for names and attributes
def extract_facts(url):
    html = fetch_page(url)
    soup = BeautifulSoup(html, 'html.parser')
    h1_tag = soup.find('h1')
    if h1_tag is None:
        print(f"No title found at {url}")
        return None

    title = h1_tag.get_text(strip=True)
    facts_section = soup.find('div', class_='entry-content')
    if facts_section is None:
        print(f"No facts section found at {url}")
        return None

    # I guess I can remove facts but it works and i dont want to
    facts = []

    for fact in facts_section.find_all('p'):
        next_title = fact.find_next_sibling('h2')
        if next_title and next_title.get_text(strip=True).startswith("Interesting"):
            break
        if fact.find('strong'):
            continue  # Skip headings within the content
        facts.append(fact.get_text(strip=True).lower())

    # these are the real facts, beautiful soup searches for table and returns all data in key:[key:value] format
    animal_attributes = {}
    info_tables = soup.find('tbody')
    if info_tables:
        rows = info_tables.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 2: # each row needs 2 columns
                key = cols[0].get_text(strip=True).strip(':').lower()
                value = cols[1].get_text(strip=True)
                animal_attributes[key] = value.lower()

    return {
        'title': title[:-6].lower(), #remove ' facts'
        'url': url,
        'facts': facts,
        'attributes': animal_attributes
    }


def main():
    index_url = 'https://factanimal.com/animals/'
    index_html = fetch_page(index_url)
    animal_links = extract_links(index_html)

    all_animal_facts = []

    # console logging and monitoring while scraping, takes a few minutes to complete.
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

