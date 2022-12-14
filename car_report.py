#!/usr/bin/env python3

import os
import json
import locale
import sys
from report_pdf_generator import generate as pdf_generate
from report_pdf_emailer import generate as email_generate
from report_pdf_emailer import send as email_send

def load_data(filename):
  """Loads the contents of filename as a JSON file."""
  with open(filename) as json_file:
    data = json.load(json_file)
  return data

def format_car(car):
  """Given a car dictionary, returns a nicely formatted name."""
  return "{} {} ({})".format(car["car_make"], car["car_model"], car["car_year"])

def process_data(data):
  """Analyzes the data, looking for maximums,
  Returns a list of lines that summarize the information/
  """
  sorted_data = sorted(data, key=lambda i:i['total_sales'])
  max_revenue = {"revenue": 0}
  max_sales = {"total_sales": 0}
  most_popular_year = {}
  for item in sorted_data:
    # Calculate the revenue generated by this model (price * total_sales)
    # We need to convert the price from "$1234.56" to 1234.56
    item_price = locale.atof(item["price"].strip("$"))
    item_revenue = item["total_sales"] * item_price
    if item_revenue > max_revenue["revenue"]:
      item["revenue"] = item_revenue
      max_revenue = item
    # TODO: also handle max sales
    if item["total_sales"] > max_sales["total_sales"]:
      max_sales = item
    # TODO: also handle most popular car_year
    if item["car"]["car_year"] not in most_popular_year.keys():
      most_popular_year[item["car"]["car_year"]] = item["total_sales"]
    else:
      most_popular_year[item["car"]["car_year"]] += item["total_sales"]                   
    
    all_values = most_popular_year.values()
    max_value = max(all_values)
    max_key = max(most_popular_year, key=most_popular_year.get)
    
    summary = [
      "The {} generated the most revenue: ${}".format(format_car(max_revenue["car"]), max_revenue["revenue"]),
      "The {} had the most sales: {}".format(max_sales["car"]["car_model"], max_sales["total_sales"]),
      "The most popular year was {} with {} sales".format(max_key, max_value)
    ]
    
def cars_dict_to_table(car_data):
  """Turns the data in car_data into a list of lists."""
  table_data = [["ID", "Car", "Price", "Total Sales"]]
  for item in car_data:
    table_data.append([item["id"], format_car(item["car"]), item["price"], item["total_sales"]])
  return table_data

def main(argv):
  """Process the JSON data and generate a full report out of it."""
  data = load_data("car_sales.json")
  summary = process_data(data)
  pdf_formatted_summary = '<br/>'.join(summary)
  email_formatted_summary = '\n'.join(summary)
  print(summary)
  # TODO: turn this into a PDF report
  pdf_generate("/tmp/cars.pdf", "Cars report", pdf_formatted_summary, cars_dict_to_table(data))
  # TODO: send the PDF report as an email attachment
  sender = "automation@example.com"
  receiver = "{}@example.com".format(os.environ.get('USER'))
  subject = "Sales summary for last month"
  body = email_formatted_summary
  message = email_generate(sender, receiver, subject, body, "/tmp/cars.pdf")
  email_send(message)
  
if __name__ == "__main__":
  main(sys.argv)
