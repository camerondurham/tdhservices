from flask import Flask, request
from bs4 import BeautifulSoup
from menu_scraper import MenuScraper
import json

app = Flask(__name__)

from flask import Response

@app.route('/getdate')
def get_date():
    ms = MenuScraper()

    try:
        yr = int(request.args.get('year'))
        mo = int(request.args.get('month'))
        dy = int(request.args.get('day'))
        print( 'Reading request year: {year}, month: {month}, day: {day}'.format(year=yr, month=mo, day=dy))
        ms.parse_menus(year = yr, month = mo, day = dy)
        return Response(ms.return_menus(), mimetype='application/json', status=202)
    except ValueError:
        ms.parse_menus()
        return Response(ms.return_menus(), mimetype='application/json', status=400)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
