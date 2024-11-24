import os
import time
import requests
import concurrent.futures
from urls import urls as PAPER_URLS

PAPERS_DIR = "papers"

def download_paper(url):
    paper_id = url.split("/")[-2]
    pdf_path = os.path.join(PAPERS_DIR, f"{paper_id}.pdf")

    retries = 0
    max_retries = 5

    while retries < max_retries:
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(pdf_path, "wb") as f:
                f.write(response.content)
            print(f"Paper {paper_id} downloaded")
            return True
        except requests.RequestException:
            retries += 1
            wait_time = 2 ** retries
            print(f"Failed for paper : {paper_id}")
            time.sleep(wait_time)

    
    while True:
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(pdf_path, "wb") as f:
                f.write(response.content)
            return True
        except requests.RequestException:
            print(f"Retrying till downloaded for paper : {paper_id}")
            time.sleep(60)

def main():
    max_workers = 5

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        list(executor.map(download_paper, PAPER_URLS))

    print("All papers downloaded")

if __name__ == "__main__":
    main()
