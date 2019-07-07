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
        self.dining_hall = dining_hall
        self.meal = meal
        #self.kitchens = {}

        # list of dishes kitchen tags
        self.dishes = []

    def print_menu(self):
        print("\nDINING HALL:" + self.dining_hall + " - "+ self.meal)
        for dish in self.dishes:
            #print("CATEGORY: " + dish.kitchen)
            dish.print_item()


    def return_menu_string(self):
        ret_str = ""
        ret_str += "\n\nDINING HALL:"
        ret_str += self.dining_hall
        ret_str += "\n" + self.meal
        for dish in self.dishes:
            ret_str += "\nCATEGORY: " + dish.kitchen + "\n" + dish.ret_item()

        return ret_str

    def add_dish(self, dish):
        self.dishes.append(dish)

#    def add_kitchen(self, name, items):
#        print("ADDING AN ITEM NAME: " + name)
#        self.kitchens[name] = items
#        print("Len of kichen is: "  + str(len(self.kitchens)))

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
        self.menus = {}
        self.loaded = False

    def clear(self):
        self.menus = {}
        self.loaded = False

    def load_menus(self):
        self.loaded = True
        self.data = requests.get(self.this_url)
        self.soup = BeautifulSoup(self.data.text, 'html.parser')

    def print_all_menus(self):
        print("\n")
        for k,v in self.menus.items():
            print("\nMeal:  " + k + "  ", end=" ")

            for x in v:
                x.print_menu()
        print("\n")

    def return_menus(self):
        return json.dumps(self.menus, cls=DictEncoder)

    def return_all_menus(self):
        ret_str = ""

        for k,v in self.menus.items():
            ret_str += "\nMeal:  " + k

            for x in v:
                ret_str += x.return_menu_string()
        return ret_str

#    def dump_json(self):
#        """
#        Writes json objects of individual menu objects to menu-output.json file
#        """
#        import json
#        f = open("menu-output.json","a+")
#        f.write("{")
#
#        for key, value in self.menus.items():
#            for v in value:
#                f.write("\n")
#                f.write(v.toJSON())
#                f.write(",")
#        f.write("}")
#        f.close()

    def return_menu(self):
        """
        Returns array of menu objects
        """
        return self.menus.values()


    def return_menu_json(self):
        """
        Returns json array of menu objects
        """
        import json

        ret_str = "["

        for value in self.menus.values():
            #for v in value:
            for i in range(len(value)):
                ret_str += "\n" + value[i].toJSON()
                if i < len(value) - 1:
                    ret_str += ","
        ret_str += "]"

        return ret_str


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
            self.menus[ meal_name ] = []
            for item in meal.find_all('div',{'class':'col-sm-6 col-md-4'}):
                menu_items = item.find_all('ul')
                i = 0

                dining_hall = item.find('h3', {'class':'menu-venue-title'}).text
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

                self.menus[meal_name].append(dhm)

