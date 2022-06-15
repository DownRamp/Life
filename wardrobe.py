from pysondb import db

a = db.getDb("Clothes/clothes.json")
a.addMany([{"temp": "21+", "weather":"NA", "cloth": "T-Shirt"},
            {"temp": "21+", "weather":"NA", "cloth": "Shorts"},
            {"temp": "NA", "weather":"Rain,Thunderstorm","cloth": "Rain Coat"},
            {"temp": "16+", "weather":"NA","cloth": "Dress shirt"},
            {"temp": "16+", "weather":"NA","cloth": "Khakis"},
            {"temp": "12-18", "weather":"NA", "cloth": "Sweater"},
            {"temp": "12+", "weather":"NA", "cloth": "Sweat pants"},
            {"temp": "8-21", "weather":"NA", "cloth": "Jeans"},
            {"temp": "8-12", "weather":"NA", "cloth": "Jacket"},
            {"temp": "!20-8", "weather":"NA", "cloth": "Winter Coat"},
            {"temp": "!20-8", "weather":"NA", "cloth": "Pants with under"}
           ])

b = db.getDb("Clothes/outfit.json")
b.addMany([{"temp": "21+", "weather":"NA","outfit": "T-Shirt,Shorts"},
            {"temp": "!20-8", "weather":"NA","outfit": "Winter Coat,Pants with under"}
           ])