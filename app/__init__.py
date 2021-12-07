from elasticsearch import Elasticsearch
from flask import Flask, render_template,request,redirect, url_for


app = Flask(__name__,  static_url_path='/static')
es = Elasticsearch(HOST="http://localhost", PORT=9200, timeout=30)
es = Elasticsearch()

from app import views
from app import search
