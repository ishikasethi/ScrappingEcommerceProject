import requests
import csv

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'}
url = 'https://www.croma.com/televisions-accessories/led-tvs/4k-ultra-hd-tvs/c/999'

"""Scrape the page source from the URL"""

# baseurl = "https://www.croma.com"
api = "https://api.croma.com/product/allchannels/v1/category/999?currentPage=1&" \
      "query=:relevance:excludeOOSFlag&fields=FULL&sort=relevance"
response = requests.get(
    api,
    headers=HEADERS)
data = response.json()
total_pages = data['pagination']['totalPages']
product_no = 0

with open('product_data.csv', 'w') as file:
    # Create a CSV writer object
    writerObj = csv.writer(file)
    # Add header row as the list
    writerObj.writerow(
        ['Sr No.', 'Title', 'Brand', 'MRP', 'Price', 'Count of Ratings',
         'Count of Reviews', 'Average Rating score', 'Product URL', 'Image URL'])
    for i in range(0, total_pages):
        response = requests.get(
            f"https://api.croma.com/product/allchannels/v1/category/999?currentPage={i}&"
            f"query=:relevance:excludeOOSFlag&fields=FULL&sort=relevance",
            headers=HEADERS)
        data = response.json()
        for product in data['products']:
            product_no += 1
            title = product['name']
            brand = product['manufacturer']
            # mrp = product['mrp']['formattedValue'].encode('utf-8')
            # price = product['price']['formattedValue'].encode('utf-8')
            mrp = round(product['mrp']['value'], 2)
            price = round(product['price']['value'], 2)
            try:
                ratingsCount = round(product['onlyRatingCount'], 2)
            except:
                ratingsCount = "N/A"
            try:
                reviewCount = round(product['finalReviewRatingCount'], 2)
            except:
                reviewCount = "N/A"
            try:
                avgRatingScore = round(product['averageRating'], 2)
            except:
                avgRatingScore = "N/A"
            product_url = product['url']
            image_url = product['plpImage']
            row_data = [product_no, title, brand, mrp, price, ratingsCount,
                        reviewCount, avgRatingScore, product_url, image_url]
            # Append the list as a row to the csv file
            writerObj.writerow(row_data)
