import requests
import csv
from csv import DictReader

def extract_data():
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/39.0.2171.95 Safari/537.36'}
    api = "https://api.croma.com/product/allchannels/v1/category/999?currentPage=1&" \
          "query=:relevance:excludeOOSFlag&fields=FULL&sort=relevance"
    response = requests.get(api, headers=HEADERS)
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


def get_products():
    with open("product_data.csv", 'r', encoding='windows-1254') as f:
        dict_reader = DictReader(f)
        list_of_dict = list(dict_reader)
        return list_of_dict


def filtered_products(products_list, user_input):
    best = []
    temp = 0
    keywords = user_input.split()
    # print(products[1])
    for product in products_list:
        check = True
        product_name = product['Title'].lower()
        for i in keywords:
            if i.lower() not in product_name:
                check = False
        if check:
            temp += 1
            best.append(product)
    print(temp)
    return best


def top_positions(products_list):
    top_position = []
    if len(products_list) <= 3:
        for i in range(0, len(products_list)):
            top_position.append(products_list[i]['Title'])
    else:
        for i in range(0, 3):
            top_position.append(products_list[i]['Title'])
    return top_position


def lowest_price_products(products_list):
    # for product in products_list:
    low_price_products = []
    if len(products_list) <= 3:
        for i in range(0, len(products_list)):
            low_price_products.append(products_list[i]['Title'])
    else:
        new_products_list = sorted(products_list, key=lambda k: k['Price'])
        for i in range(0, 3):
            low_price_products.append(new_products_list[i]['Title'])
    return low_price_products


def highest_avg_rating(products_list):
    high_avg_rating_products = []
    if len(products_list) <= 3:
        for i in range(0, len(products_list)):
            high_avg_rating_products.append(products_list[i]['Title'])
    else:
        new_products_list = sorted(products_list, key=lambda k: k['Average Rating score'], reverse=True)
        for i in range(0, 3):
            high_avg_rating_products.append(new_products_list[i]['Title'])
    return high_avg_rating_products


if __name__ == "__main__":
    print("testing space for functions.py file")
    products_list = get_products()
    # print(products_list)
    user_input = input("enter keywords to search!")
    filtered_product = filtered_products(products_list, user_input)
    for product in filtered_product:
        print(product)
    # top_products = top_positions(filtered_product)
    # lowest_price = lowest_price_products(filtered_product)
    # highest_avg_rating = highest_avg_rating(filtered_product)
    # for product in top_products:
    #     print(product)
    # for product in highest_avg_rating:
    #     print(product)




