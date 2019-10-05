from news_app import NewsApp


if __name__ == "__main__":
    app = NewsApp()
    print('Started scraping from all sources.')
    app.accept()
    print('Scraping complete.')
