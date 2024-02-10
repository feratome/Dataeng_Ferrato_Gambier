from flask import Flask, render_template, url_for
import csv
from pymongo import MongoClient
import pandas as pd

app = Flask(__name__)

#def get_products_from_csv():

    #return products

@app.route('/')
def home():
    client = MongoClient('mongo', 27017)
    db = client['mydatabase']

    collections = [
        db['collection_clearwheyisolate12081395'],
        db['collection_gainerprisedemasse10529988'],
        db['collection_impactwheyisolate10530911'],
        db['collection_impactwheyprotein10530943'],
        db['collection_melangeperformancetoutenun10530268'],
        db['collection_melangeproteinetotalprotein10529951'],
        db['collection_substitutderepasproteine11324199'],
        db['collection_thewhey12968603']
    ]

    products = []
    for collection in collections:
        for document in collection.find():
            product = {
                'product_id' : document['_id'],
                'product_name': document['product_name'],
                'product_price': document['product_price'],
                'size': document['size'],
                'weight_count': document['weight_count'],
                'arome_count': document['arome_count'],
                'nutrients': document['table_data']['Nutrient'],
                'per_100g': document['table_data']['Per 100g'],
                'per_portion': document['table_data']['Per Portion'],
                'product_grade': document['product_grade'],
                'image_src' : document['image_src']
            }
            products.append(product)
    #products = get_products_from_csv()
    return render_template('index.html', products=products)

@app.route('/product/<product_name>')
def product(product_name):
    #products = get_products_from_csv()
    client = MongoClient('mongo', 27017)
    db = client['mydatabase']

    collections = [
        db['collection_clearwheyisolate12081395'],
        db['collection_gainerprisedemasse10529988'],
        db['collection_impactwheyisolate10530911'],
        db['collection_impactwheyprotein10530943'],
        db['collection_melangeperformancetoutenun10530268'],
        db['collection_melangeproteinetotalprotein10529951'],
        db['collection_substitutderepasproteine11324199'],
        db['collection_thewhey12968603']
    ]

    products = []
    for collection in collections:
        for document in collection.find():
            product = {
                'product_id' : document['_id'],
                'product_name': document['product_name'],
                'product_price': document['product_price'],
                'size': document['size'],
                'weight_count': document['weight_count'],
                'arome_count': document['arome_count'],
                'nutrients': document['table_data']['Nutrient'],
                'per_100g': document['table_data']['Per 100g'],
                'per_portion': document['table_data']['Per Portion'],
                'product_grade': document['product_grade'],
                'image_src' : document['image_src']
            }
            products.append(product)
    product = next((p for p in products if p['product_name'] == product_name), None)
    if product:
        return render_template('product.html', product=product)
    else:
        return "Product not found", 404

if __name__ == "__main__":
    app.run(debug=True)
