import requests
from bs4 import BeautifulSoup
import csv

def scrape_douban_top10():
    url = "https://movie.douban.com/top250"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.content, "html.parser")

        movie_list = soup.find('ol', class_='grid_view')
        if not movie_list:
            print("Could not find the movie list on the page.")
            return

        movies = []
        for i, li in enumerate(movie_list.find_all('li')):
            if i >= 10:
                break
            try:
                title = li.find('span', class_='title').text
                rating_element = li.find('div', class_='star').find_all('span')[-1].text
                rating = rating_element.replace('人评价', '')
                movies.append({'title': title, 'rating': rating})
            except Exception as e:
                print(f"Error extracting data from movie {i+1}: {e}")
                continue

        return movies

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def save_to_csv(movies, filename="douban_top10_movies.csv"):
    if not movies:
        print("No movies to save.")
        return

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'rating']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for movie in movies:
                writer.writerow(movie)
        print(f"Saved movie data to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

if __name__ == "__main__":
    top_movies = scrape_douban_top10()
    if top_movies:
        save_to_csv(top_movies)
