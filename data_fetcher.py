import requests

def fetch_posts(limit: int = 10) -> list[dict]:
    """
    Pobiera najnowsze wpisy z serwisu społecznościowego Hacker News.
    Korzysta z darmowego i publicznego API (Firebase), które nie wymaga kluczy ani logowania.
    """
    # 1. Pobranie listy ID najnowszych postów
    url = "https://hacker-news.firebaseio.com/v0/newstories.json"
    
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Błąd połączenia z API (Kod statusu: {response.status_code})")
        
    # Wybieramy tylko określoną liczbę (limit) najnowszych ID
    post_ids = response.json()[:limit]
    
    post_data = []
    # 2. Pobranie szczegółów każdego posta na podstawie jego ID
    for pid in post_ids:
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{pid}.json"
        item_data = requests.get(item_url).json()
        
        if item_data:
            # Tworzymy ustandaryzowany słownik z danymi posta
            post_data.append({
                "id": pid,
                "title": item_data.get("title", ""),
                "text": item_data.get("text", ""),
                "score": item_data.get("score", 0),
                "url": item_data.get("url", f"https://news.ycombinator.com/item?id={pid}")
            })
            
    return post_data

if __name__ == "__main__":
    print("Pobieranie najnowszych wpisów z Hacker News API...")
    try:
        sample = fetch_posts(limit=3)
        for i, p in enumerate(sample, 1):
            print(f"\n[{i}] {p['title']}")
            print(f"    Punkty: {p['score']} | URL: {p['url']}")
    except Exception as e:
        print(f"Błąd podczas testu: {e}")