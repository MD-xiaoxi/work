import requests
from bs4 import BeautifulSoup
import csv

def scrape_github_trending():
    url = "https://github.com/trending"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        repo_list = soup.find_all('article', class_='Box-row')
        if not repo_list:
            print("Could not find the repository list on the page.")
            return

        repos = []
        for i, repo in enumerate(repo_list):
            if i >= 10:
                break
            try:
                title_element = repo.find('h2', class_='h3 lh-condensed')
                if title_element:
                    title = title_element.find('a').text.strip()
                    repos.append({'title': title})
                else:
                    print(f"Could not find title for repo {i+1}")
                    continue
            except Exception as e:
                print(f"Error extracting data from repo {i+1}: {e}")
                continue

        return repos

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def save_to_csv(repos, filename="github_top10_repos.csv"):
    if not repos:
        print("No repositories to save.")
        return

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for repo in repos:
                writer.writerow(repo)
        print(f"Saved repository data to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

if __name__ == "__main__":
    top_repos = scrape_github_trending()
    if top_repos:
        save_to_csv(top_repos)
