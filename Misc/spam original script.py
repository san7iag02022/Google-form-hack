import requests
import concurrent
from concurrent.futures import ThreadPoolExecutor
characters = range(1, 10000)
base_url = 'https://docs.google.com/forms/d/e/1FAIpQLSeWkzPM9hLmOGOZz_MahUNvvPOKhHH8YOqeszl5KuvTKDDKuA/formResponse?&pageHistory=0&entry.2092238618=name&entry.1556369182=a@gmail.com&entry.479301265=1&entry.1753222212=Day 1&entry.588393791=None&entry.2109138769=Yes'
threads = 2000
def get_character_info(character):
    r = requests.get(base_url)
    return r.json()
with ThreadPoolExecutor(max_workers=threads) as executor:
    future_to_url = {executor.submit(get_character_info, char)
    for char in characters}
    for future in concurrent.futures.as_completed(future_to_url):
        try:
            data = future.result()
            print(data)
        except Exception as e:
            print('Looks like something went wrong:', e)
