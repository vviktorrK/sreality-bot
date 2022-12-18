#! /bin/bash

cd scraper
echo "Started crawling..."
scrapy crawl sreality
cd ../server
echo "Starting server..."
python3 -m flask --app sreality run --host=0.0.0.0
