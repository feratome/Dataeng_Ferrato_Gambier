from pymongo.mongo_client import MongoClient
import scrapy
from bs4 import BeautifulSoup
import pandas as pd

class MyProteinSpider(scrapy.Spider):
    name = 'myprotein'

    start_urls = [
        'https://fr.myprotein.com/nutrition-sportive/impact-whey-protein/10530943.html',
        'https://fr.myprotein.com/nutrition-sportive/impact-whey-isolate/10530911.html',
        'https://fr.myprotein.com/nutrition-sportive/clear-whey-isolate/12081395.html',
        'https://fr.myprotein.com/nutrition-sportive/gainer-prise-de-masse/10529988.html',
        'https://fr.myprotein.com/nutrition-sportive/melange-performance-tout-en-un/10530268.html',
        'https://fr.myprotein.com/nutrition-sportive/melange-proteine-total-protein/10529951.html',
        'https://fr.myprotein.com/nutrition-sportive/the-whey/12968603.html',
        'https://fr.myprotein.com/nutrition-sportive/substitut-de-repas-proteine/11324199.html'

    ]


    def parse(self, response):
        # Extracting HTML content
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        product_prices = soup.find('p', class_='productPrice_price').text.strip()

        # Scraping product name
        product_name = soup.find('h1', class_='productName_title').text.strip()

        # Scraping table data
        table = soup.find('table')
        if table:
            data = self.parse_table(table)
        else:
            data = None

        # Scraping item list count
        item_list = soup.find('ul', class_='athenaProductVariations_list')
        weight_count = len(item_list.find_all('li'))

        # Scraping arome count
        select_dropdown = soup.find('select', class_='athenaProductVariations_dropdown')
        arome_count = len(select_dropdown.find_all('option'))

        product_grade = [grade.text.strip() for grade in soup.find_all('span', class_='athenaProductReviews_aggregateRatingValue')]

        product_default = soup.find_all('button', class_='athenaProductVariations_box default athenaProductVariationsOption') 
        image_src = soup.find('img', class_='athenaProductImageCarousel_image')['src']

        text_inside_button=None
        # Iterate through the list of button elements
        for button in product_default:
            # Check if the button contains the specified span with class 'srf-hide'
            if button.find('span', class_='srf-hide'):
                # Extract the text inside the button
                text_inside_button = button.get_text(strip=True)
                # Split the text based on 'Sélectionner' and take the first part
                text_inside_button = text_inside_button.split('Sélectionner')[0].strip()
        

        mongodatas = product_name, product_prices,text_inside_button, weight_count, arome_count, data , product_grade ,image_src

        # Pass response along with data to save_to_mongodb
        self.save_to_mongodb(mongodatas, response.url)


        yield {
            'product_name': product_name,
            'product_price': product_prices,
            'size' : text_inside_button,
            'weight_count': weight_count,
            'arome_count': arome_count,
            'table_data': data,
            'product_grade': product_grade,
            'image_src' : image_src
            
        }

    def parse_table(self, table):
        # Initialize lists to store data
        nutrients = []
        per_100g_values = []
        per_portion_values = []

        # Extract data from the table
        rows = table.find_all('tr')

        for row in rows[1:]:  # Skip the first row as it contains header information
            columns = row.find_all('td')
            nutrient = columns[0].text.strip()
            per_100g = columns[1].text.strip()
            per_portion = columns[2].text.strip()

            nutrients.append(nutrient)
            per_100g_values.append(per_100g)
            per_portion_values.append(per_portion)

        # Create a dictionary
        data_dict = {
            'Nutrient': nutrients,
            'Per 100g': per_100g_values,
            'Per Portion': per_portion_values
        }

        return data_dict

    def save_to_mongodb(self, data, url):
        try:
            # Connect to MongoDB
            client = MongoClient('mongo', 27017)

            # Specify the database and collection based on the URL
            db_name = 'mydatabase'
            collection_name = f'collection_{url.replace("https://fr.myprotein.com/nutrition-sportive/", "",).replace("/", "").replace(".html","").replace("-","").replace("_","")}'

            db = client[db_name]
            collection = db[collection_name]

            # Convert the tuple to a dictionary with meaningful keys
            keys = ['product_name', 'product_price','size' , 'weight_count', 'arome_count', 'table_data','product_grade','image_src']
            data_dict = dict(zip(keys, data))

            # Insert the dictionary into the MongoDB collection
            collection.insert_one(data_dict)

            print(f"Document inserted successfully into {db_name}.{collection_name}")
            print(db.list_collection_names())
        except Exception as e:
            print(f"Error inserting document: {e}")
        finally:
            # Close the MongoDB connection
            client.close()
