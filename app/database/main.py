import time
from data_crawling import crawl_rss
from data_ingestion import ingest_data
from database_api import sync_to_database

def main():
    while True:
        print("Bắt đầu chu kỳ đồng bộ...")
        
        # Bước 1: Data Crawling
        print("Thực hiện Data Crawling...")
        crawl_rss()

        # Bước 2: Data Ingestion
        print("Thực hiện Data Ingestion...")
        data = ingest_data()

        # Bước 3: Database API
        print("Thực hiện Database API...")
        sync_to_database(data)

        # Chờ 5 phút trước khi kiểm tra lại
        print("Chờ 5 phút để chu kỳ tiếp theo...")
        time.sleep(300)

if __name__ == "__main__":
    main()