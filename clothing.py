import requests, json
import os
from dotenv import load_dotenv
 
load_dotenv()
 
api_key = os.getenv('API_KEY')
base_url = "http://api.openweathermap.org/data/2.5/weather?"
 
clothing_map = {}
outfits_map = {}
 
class clothing_weather:
    # Fetch weather data based on location
    def weather(city_name):
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
 
        # temp and conditions
        print("TEMP")
        response = requests.get(complete_url)
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
 
            current_temperature = y["temp"]
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            # if high humidity add 5 degrees to temp
            print(" Temperature (in kelvin unit) = " +
                            str(current_temperature) +
                "\n atmospheric pressure (in hPa unit) = " +
                            str(current_pressure) +
                "\n humidity (in percentage) = " +
                            str(current_humidity) +
                "\n description = " +
                            str(weather_description))
            return current_temperature+"/"+weather_description
 
    # pick clothes based on situation
    def clothing_selection(temp_weather):
        # previous clothing selected
        if temp_weather in outfits_map.values:
            for outfit in outfits_map.keys:
                if outfits_map[outfit] == temp_weather:
                    print(outfit)
                    response = input("Do you like this outfit?(y/n):")
                    if response == 'y':
                        return
 
        # Check our map for clothes fitting description
        for clothes in clothing_map.keys:
            # seperate temp_weather and clothing_map weather
           
            # compare first and second values ( if * ignore, else should equal)
 
            if clothing_map[clothes] == temp_weather:
                print(outfit)
                response = input("Do you like this outfit?(y/n):")
                if response == 'y':
                    return
        # save selected clothes:temperature+weather
        f = open('outfits.txt', 'a+')
        f.write(outfit+":"+temp_weather)
        f.close()
 
    # enter clothing selection
    def enter_wardrobe():
        clothing = input("Enter Item: ")
        temp_weather = input("Enter temp+weather: ")
        clothing_map[clothing] = temp_weather
        f = open('wardrobe.txt', 'a+')
        f.write(clothing+":"+temp_weather)
        f.close()
 
    def read_wardrobe():
        f = open("wardrobe.txt", "r")
        for x in f:
            print(x)
        f.close()
 
        f = open('outfits.txt', 'r')
        for x in f:
            print(x)
        f.close()
 
    if __name__ == '__main__':
        read_wardrobe()
        while(True):
            clothes = input("Would you like to add to your wardrobe?(y/n): ")
            if(clothes == 'y'):
                enter_wardrobe()
            else:
                break
        try:
            city_name = input("Enter city name: ")
            selection = clothing_selection(weather(city_name))
            print("Recommended clothing: "+ selection)
        except:
            print("ERROR")
 
 
    #to-do:
    # add db extension