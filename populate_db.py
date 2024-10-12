# from APIKeys import MONGO_URI
# from flask import Flask, jsonify, request
# from pymongo import MongoClient
# import json
#
#
# app = Flask(__name__)
#
# mongo_uri = MONGO_URI
# client = MongoClient(mongo_uri)
#
# db = client["mydatabase"]
# rec_collection = db["rec"]
# company_collection = db["company"]
#
#
# def insert_companies():
#     company_logos = {
#         "Amazon": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg",
#         "Walmart": "https://upload.wikimedia.org/wikipedia/commons/c/ca/Walmart_logo.svg",
#         "Apple": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg",
#         "Netflix": "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg",
#         "Airbnb": "https://upload.wikimedia.org/wikipedia/commons/6/69/Airbnb_Logo_Bélo.svg",
#         "Nike": "https://upload.wikimedia.org/wikipedia/commons/a/a6/Logo_NIKE.svg",
#         "Adidas": "https://upload.wikimedia.org/wikipedia/commons/2/20/Adidas_Logo.svg",
#         "Samsung": "https://upload.wikimedia.org/wikipedia/commons/2/24/Samsung_Logo.svg",
#     }
#     for company, logo_url in company_logos.items():
#         company_collection.insert_one({"name": company, "price": })