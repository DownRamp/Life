import requests, json
import os
from dotenv import load_dotenv
from pysondb import db

load_dotenv()
 
api_key = os.getenv('API_KEY')
base_url = "http://api.openweathermap.org/data/2.5/weather?"

# temp: clothing array
clothing_map = {}
# temp: outfit array
outfits_map = {}
 
# Fetch weather data based on location
def weather(city_name):
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    # temp and conditions
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]

        current_temperature = y["feels_like"]
        current_temperature -= 273.15
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        # if high humidity add 5 degrees to temp
        print(" Temperature (in celcius unit) = " +
                        str(current_temperature) +
            "\n atmospheric pressure (in hPa unit) = " +
                        str(current_pressure) +
            "\n humidity (in percentage) = " +
                        str(current_humidity) +
            "\n description = " +
                        str(weather_description))

        return str(current_temperature)+"/"+weather_description

# pick clothes based on situation
def clothing_selection(temp_weather):
    # previous clothing selected
    weather = temp_weather.split("/")
    today_temp = float(weather[0].strip())
    today_weath = weather[1].strip()

    for key, outfit in outfits_map.items():
        inner_list =key.split("/")
        weath_strip = inner_list[1].strip()
        temp_strip = inner_list[0].strip()

        if today_weath in weath_strip:
            print(outfit)
            response = input("Do you like this outfit?(y/n):")
            if response == 'y':
                return ", ".join(outfit)

        # above temp
        if "+" in temp_strip:
            plus_remove = temp_strip.replace("+","")
            t = float(plus_remove)
            if today_temp >= t:
                print(outfit)
                response = input("Do you like this outfit?(y/n):")
                if response == 'y':
                    return ", ".join(outfit)

        # check temp range
        elif "-" in inner_list[0].strip():
            # separate range
            nums = inner_list[0].split("-")
            front = nums[0].replace("!","-")
            front = float(front)
            back = float(nums[1])
            if front <= today_temp and back >= today_temp:
                print(outfit)
                response = input("Do you like this outfit?(y/n):")
                if response == 'y':
                    return ", ".join(outfit)

    fin_outfit = ""
    # Check our map for clothes fitting description
    for key, clothes in clothing_map.items():
        inner_list = key.split("/")
        weath_strip = inner_list[1].strip()
        temp_strip = inner_list[0].strip()

        if today_weath in weath_strip:
            print(clothes)
            response = input("Add to your outfit?(y/n):")
            if response == 'y':
                fin_outfit = ", ".join(clothes)
                break

        # above temp
        if "+" in temp_strip:
            plus_remove = temp_strip.replace("+","")
            t = float(plus_remove)
            if today_temp >= t:
                print(clothes)
                response = input("Add to your outfit?(y/n):")
                if response == 'y':
                    fin_outfit = ", ".join(clothes)
                    break

        # check temp range
        elif "-" in inner_list[0].strip():
            # separate range
            nums = inner_list[0].split("-")
            front = nums[0].replace("!","-")
            front = float(front)
            back = float(nums[1])
            if front <= today_temp and back >= today_temp:
                print(clothes)
                response = input("Add to your outfit?(y/n):")
                if response == 'y':
                    fin_outfit = ", ".join(clothes)
                    break

    # save selected
    b = db.getDb("Clothes/outfit.json")
    vals_list = temp_weather.split("/")
    b.add({"temp": vals_list[0].strip(), "weather":vals_list[1].strip(),"outfit": fin_outfit})
    return fin_outfit


# enter clothing selection
def enter_wardrobe():
    clothing = input("Enter Item: ")
    temp_weather = input("Enter temp+weather (separate with /): ")
    clothing_map[temp_weather] = clothing
    b = db.getDb("Clothes/clothes.json")
    vals_list = temp_weather.split("/")
    b.add({"temp": vals_list[0].strip(), "weather":vals_list[1].strip(),"cloth": clothing})

def read_wardrobe():
    cloth = db.getDb("Clothes/clothes.json")
    cloth_list = cloth.getAll()
    # clothing_map
    for c in cloth_list:
        key = c["temp"]+"/"+c["weather"]
        value = c["cloth"]
        if key in clothing_map:
            clothing_map.get(key).append(value)
        else:
            l = []
            l.append(value)
            clothing_map[key] = l

    # outfits_map
    outfit = db.getDb("Clothes/outfit.json")
    outfit_list = outfit.getAll()
    for o in outfit_list:
        key = o["temp"]+"/"+o["weather"]
        value = o["outfit"]
        if key in outfits_map:
            outfits_map.get(key).append(value)
        else:
            l = []
            l.append(value)
            outfits_map[key] = l
 
if __name__ == '__main__':
    read_wardrobe()
    while(True):
        clothes = input("Would you like to add to your wardrobe?(y/n): ")
        if(clothes == 'y'):
            enter_wardrobe()
        else:
            break

    city_name = input("Enter city name: ")
    weather = weather(city_name)
    selection = clothing_selection(weather)
    print("Recommended clothing: "+ selection)
