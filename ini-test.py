from flask import Flask, request, render_template
import pygsheets
import random
import json
import urllib
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

print(config)


print(config.sections())
print(section.name())
'''
def fetch_source_data(source="OPENTDB"):
  question_source = []
  for each_section in config.sections():
    question_source.append({"name" : config[each_section]['name'], 
        "category" : config[each_section]['category'], 
        "summary" : config[each_section]['summary'], 
        "url" : config[each_section]['url'], 
        "info" : config[each_section]['info']})
  #return render_template('index.html', base_url=request.base_url, product=product, logo=logo, categories=categories, applist=applist)
  return question_source
'''
