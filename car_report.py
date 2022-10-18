#!/usr/bin/env python3

import json
import locale
import sys
from report_pdf_generator import generate as report_generate
from report_pdf_emailer import generate as email_generate
from report_pdf_emailer import send as email_send

def load_data(filename):
  """Loads the contents of filename as a JSON file."""
  with open(filename) as json_file:
    data = json.load(json_file)
    data = sorted(data, key=lambda i:i['total_sales'])
  return data

def format_car(car):
  """Given a car dictionary, returns a nicely formatted name."""
  return "{} {} ({})".format(car["car_make"], car["car_model"], car["car_year"])

def process_data(data):
  """Analyzes the data, looking for maximums,
  Returns a list of lines that summarize the information/
  """
  max_revenue = {"revenue": 0}
  max_sales = {"total_sales": 0}
  most_popular_year = {}
  for item in data:
    # Calculate the revenue generated by this model (price * total_sales)
    # We need to convert the price from "$1234.56" to 1234.56
    item_price = locale.atof(item["price"].strip("$"))
    item_revenue = item["total_sales"] * item_price
    if item_revenue > max_revenue["revenue"]:
      item["revenue"] = item_revenue
      max_revenue = item
    # TODO: also handle max sales
    # TODO: also handle most popular car_year
    
    summary = [
      "The {} generated the most revenue: ${}".format(format_car(max_revenue["car"]), max_revenue["revenue"])
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
  print(summary)
  # TODO: turn this into a PDF report
  # TODO: send the PDF report as an email attachment
  
if __name__ == "__main__":
  main(sys.argv)
