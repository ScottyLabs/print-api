import requests, bs4
from api import app
from flask import request, redirect, render_template, jsonify
from api.printer import Printer
import random

# Get all printer statuses
@app.route("/status", methods=["GET"])
def get_status():
  printers = get_printer_statuses()
  printers = list(map(get_printer_dict, printers))
  return jsonify(printers)

# Get available printers (green signal)
@app.route("/status/available", methods=["GET"])
def get_available():
  printers = get_printer_statuses()
  printers = filter(lambda printer: printer.signal == "GREEN", printers)
  printers = list(map(get_printer_dict, printers))
  return jsonify(printers)

def get_printer_dict(printer):
  return {
      "name": printer.name,
      "signal": printer.signal,
      "lcd_message": printer.lcd_message,
      "status": printer.status,
      "tray_statuses": printer.tray_statuses,
      "timestamp": printer.as_of,
      "color": printer.color,
      "coordinates": printer.coordinates,
    }

def get_printer_statuses():
  url = "https://clustersweb.andrew.cmu.edu/PrinterStats/All/"

  content = requests.get(url).content

  soup = bs4.BeautifulSoup(content, features="html.parser")

  table = soup.findAll("table")[1].findAll("tr")

  col_tag = ["name", "signal", "lcd_message", "status", "tray_status", "as_of"]

  printers = []

  for row in table[2:]:
      columns = row.find_all("td")
      kwargs = {}
      for c, tag in zip(columns, col_tag):
          if tag == "signal":
              data = c.img["alt"]
          else:
              data = c.get_text()
          kwargs[tag] = data
        
      TLLAT = 40.44811
      TLLNG = -79.944967
      kwargs['coordinates'] = {
        'lat': round(TLLAT - (0.002 * random.random()), 5),
        'lng': round(TLLNG - (0.002 * random.random()), 5),
      }

      printers.append(Printer(**kwargs))

  return printers