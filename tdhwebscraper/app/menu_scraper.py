from bs4 import BeautifulSoup, NavigableString
from json import JSONEncoder
import requests
import json


class DictEncoder(JSONEncoder):
    """
    Using JSONEncoder to implement custom serialization for sending JSON responses
    """

    def default(self, o):
        return o.__dict__

class DiningHall:
    """ DiningHall class stores an array of menus, ordered by meal menus
        DiningHall:
             menus = [
                {
                    "name" : "Breakfast",
                    "dishes" : [
                                {dish1},
                                ...
                                ]
                },
                {
                    "name" : "Lunch",
                    "dishes" : [
                                {dish1},
                                ...
                                ]
                }
    """
    def __init__(self, dining_hall):
        self.dining_hall = dining_hall
        self.menus = [ ]

    def add_menu(self, menu):
        self.menus.append(menu)

    def toJSON(self):
        import json
        return json.dumps(self, default=lambda o: o.__dict__,
                sort_keys=True, indent=4)

class Menu:
    """ Menu class stores dictionary of kitchen names mapped to list of dishes
            kitchen: categories (i.e. Hot Line, Fresh from the Farm, ...)
            dishes: see Dish class

            kitchens =  {
                            "kitchen" : [
                                 dish1,
                                 dish2,
                                 ...
                                 ],
                            ...
                        }

            meal = "Breakfast/Brunch/Lunch/Dinner"

            dining_hall = "Parkside Restaurant & Grill/USC Village/..."


    """

    def __init__(self, dining_hall, meal):
        self.meal = meal

        # list of dishes kitchen tags
        self.dishes = []

    def print_menu(self):
        for dish in self.dishes:
            dish.print_item()


    def return_menu_string(self):
        ret_str = ""
        ret_str += "\n\nDINING HALL:"
        ret_str += "\n" + self.meal
        for dish in self.dishes:
            ret_str += "\nCATEGORY: " + dish.kitchen + "\n" + dish.ret_item()

        return ret_str

    def add_dish(self, dish):
        self.dishes.append(dish)

    def toJSON(self):
        import json
        return json.dumps(self, default=lambda o: o.__dict__,
                sort_keys=True, indent=4)

class Dish:
    def __init__(self, name, dietary_tags, kitchen):
        self.dish_name = name
        self.dietary_tags = dietary_tags
        self.kitchen = kitchen

    def print_item(self):
        print("\n" + self.dish_name + ", " + self.kitchen + ", dietary tags: ", end = " ")
        for tag in self.dietary_tags:
            print(tag,end=" ")

    def ret_item(self):
        ret_str = "\nNAME: " + self.dish_name + "\ndietary tags: \n" + self.kitchen

        for tag in self.dietary_tags:
            ret_str += "\n" + tag

        return ret_str

class MenuScraper:
    def __init__(self,  main_url = "https://hospitality.usc.edu/residential-dining-menus/"):
        self.main_url = main_url
        self.menus_by_dh = {}
        self.loaded = False

    def clear(self):
        self.menus = {}
        self.loaded = False

    def load_menus(self):
        self.loaded = True
        self.data = requests.get(self.this_url)
        self.soup = BeautifulSoup(self.data.text, 'html.parser')

    def return_menus(self):
        #return json.dumps(self.menus, cls=DictEncoder)
        return json.dumps(self.menus_by_dh, cls=DictEncoder)

    def return_menu(self):
        """
        Returns array of menu objects
        """
        return self.menus.values()


    def date_url_old(self, yr, mo, dy):
        """
        Do not use
        Makes get request to parse menu on specific date
        """
        import datetime
        #"https://hospitality.usc.edu/residential-dining-menus/?menu_date=March+23%2C+2019"
        year = int(yr)
        month = int(mo)
        day = int(dy)

        d = datetime.datetime(year, month, day)
        date = "?menu_date=" + d.strftime("%B") + "+" + d.strftime("%d") + "%2C+" + d.strftime("%Y")
        return self.main_url + date

    def date_url(self, yr, mo, dy):
        """
        Makes get request to parse menu on specific date
        example: "https://hospitality.usc.edu/residential-dining-menus/?menu_date=March+23%2C+2019"
        """
        import datetime
        print('generating date string ... for {year}, {month}, {day}'.format(year=yr, month=mo, day=dy))
        try:
            if int(dy) < 10 and len(dy) > 1:
                dy = dy[1:]
            d = datetime.datetime(int(yr), int(mo), int(dy))
            date = "?menu_date=" + d.strftime("%B") + "+" + str(dy) + "%2C+" + d.strftime("%Y")
        except:
            print("Error parsing date ")
            date = ""
        return self.main_url + date






    def parse_menus(self, year = None, month = None, day = None):
        """
        TODO: Parses string in YYYYMMDD format

        """

        if year != None:
            print('parsing menus... for {year}, {month}, {day}'.format(year=year, month=month, day=day))
            self.this_url = self.date_url(yr=year,mo=month,dy= day)
            print("Grabbing data for date" + self.this_url)


        else:
            self.this_url = self.main_url

        self.load_menus()

        for meal in  self.soup.find_all('div',{'class':'hsp-accordian-container'}):
            meal_title = meal.find('span',{'class':'fw-accordion-title-inner'}).text
            meal_name = meal_title.split(" ")[0]
            dining_hall = ""
            for item in meal.find_all('div',{'class':'col-sm-6 col-md-4'}):
                menu_items = item.find_all('ul')
                i = 0

                dining_hall = item.find('h3', {'class':'menu-venue-title'}).text

                try:
                    self.menus_by_dh[ dining_hall ]
                except:
                    self.menus_by_dh[ dining_hall ] = DiningHall(dining_hall)

                dhm = Menu(dining_hall, meal_name)
                for cat in item.find_all('h4'):
                    category = cat.text
                    if category == "No items to display for this date":
                        continue

                    if len(menu_items) > i:
                        for ul in menu_items[i].find_all('li'):
                            dish_name = ' '.join([x.strip() for x in ul if isinstance(x,NavigableString)])

                            dietary_tags = []

                            for tag in ul.span.find_all('span'):
                                dietary_tags.append(tag.text)

                            new_dish = Dish(dish_name, dietary_tags, category)
                            dhm.add_dish(new_dish)


                    i = i + 1

                if len(dhm.dishes) > 0:
                    self.menus_by_dh[dining_hall].add_menu(dhm)

