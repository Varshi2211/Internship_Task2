import requests
from bs4 import BeautifulSoup
import json

def extract_university_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    university = {
        'name': soup.find('h1', class_='uni_title').text,
        'logoSrc': soup.find('img', class_='university_logo')['src'],
        'type': soup.find('p', class_='uni_type').text.split(':')[1].strip(),
        'establishedYear': soup.find('p', class_='uni_founded').text.split(':')[1].strip(),
        'location': {
            'country': soup.find('p', class_='uni_country').text.split(':')[1].strip(),
            'state': soup.find('p', class_='uni_state').text.split(':')[1].strip(),
            'city': soup.find('p', class_='uni_city').text.split(':')[1].strip()
        },
        'contact': {
            'facebook': soup.find('a', href=lambda href: 'facebook' in href)['href'],
            'twitter': soup.find('a', href=lambda href: 'twitter' in href)['href'],
            'instagram': soup.find('a', href=lambda href: 'instagram' in href)['href'],
            'officialWebsite': soup.find('a', href=lambda href: 'uni-stuttgart.de/' in href)['href'],
            'linkedin': soup.find('a', href=lambda href: 'linkedin.com' in href)['href'],
            'youtube': soup.find('a', href=lambda href: 'youtube.com' in href)['href']
        }
    }

    return university

if __name__ == '__main__':

    response = requests.get('https://www.4icu.org/de/universities/')
    soup = BeautifulSoup(response.text, 'html.parser')
    university_urls = [a['href'] for a in soup.find_all('a', href=True) if '/de/university/' in a['href']]

    universities = []
    for url in university_urls:
        universities.append(extract_university_info(url))

    with open('universities.json', 'w', encoding='utf-8') as f:
        json.dump(universities, f, ensure_ascii=False, indent=4)
