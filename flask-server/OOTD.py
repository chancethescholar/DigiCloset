import geocoder
import python_weather
import asyncio
import random

class OOTD:
    # https://pypi.org/project/geocoder/
    def get_location(self):
        # use geocoder to get current location based on ip address
        g = geocoder.ip('me')
        location = {
            "city": g.city,
            "state": g.state
            }
        return location
    
    # https://pypi.org/project/python-weather/
    async def get_weather(self):
        location = self.get_location()
        city = location["city"]
        state = location["state"]

        async with python_weather.Client(format=python_weather.IMPERIAL) as client:

            # fetch a weather forecast from a city
            weather = await client.get(city + ", " + state)
        
            # returns the current day's forecast temperature (int)
            return {"temperature": weather.current.temperature}
        
    def get_all_clothing_type(self, type, closet):
        # returns list of all clothing of a specific type
        all_clothing = []
        for clothing in closet:
            if clothing["type"] == type:
                all_clothing.append(clothing)
        return all_clothing
    
    def get_clothing_from_colors(self, clothing, colors):
        # return list of all clothing of a specific type that includes the given colors
        poss_clothing = []
        for c in clothing:
            if c["colors"] is not None:
                c_colors_list = c["colors"].split(", ")
                for color in c_colors_list:
                    if color in colors:
                        poss_clothing.append(c)

        return poss_clothing
        
    # returns combination of clothing: "shorts, top, shoes" or "skirt, top, shoes" or "dress, shoes"
    def get_hot_ootd(self, closet):
        # store final outfit
        outfit = []

        # get all clothing relevant to this outfit
        tops = self.get_all_clothing_type("Top", closet)
        dresses = self.get_all_clothing_type("Dress", closet)
        shorts = self.get_all_clothing_type("Shorts", closet)
        skirts = self.get_all_clothing_type("Skirt", closet)
        shoes = self.get_all_clothing_type("Shoe", closet)

        # randomly pick a top or dress to start with
        top_or_dress = random.randint(0, 1)

        # if there are no tops in closet, choose a dress
        if len(tops) == 0:
            top_or_dress = 1

        # if there are no dresses in closet, choose a top
        elif len(dresses) == 0:
            top_or_dress = 0
        
        # if there are no tops or dresses, the user should add more clothing to closet
        elif len(tops) == 0 and len(dresses) == 0:
            return {"missing": "Top"} # need top or dresses

        # start with top
        if top_or_dress == 0:
            # pick a random top from closet and add it to outfit (we just need the image to display in UI)
            top = random.choice(tops)
            outfit.append(top["image"])

            # get all the colors from top
            top_colors = top["colors"]

            # get all possible bottoms (shorts and skirts from closet)
            bottoms = shorts + skirts

            # if there are no shorts or skirts, the user should add more clothing to closet
            if len(bottoms) == 0:
                return {"missing": "Bottom"} # need shorts or skirt 
            
            # if top is white or black, it will likely match with any bottom
            if top_colors == "white" or top_colors == "black":
                # so choose random bottom and add to outfit
                bottom = random.choice(bottoms)
                outfit.append(bottom["image"])     
            
            else:
                # if not, get all bottoms that include any colors in the top
                poss_bottoms = self.get_clothing_from_colors(bottoms, top_colors)
                # and bottoms that are black, white, blue, or light blue (assuming blues are denim), likely will match with the top
                poss_bottoms += self.get_clothing_from_colors(bottoms, "black, white, blue, light blue")
                
                # choose a random bottom from possible bottoms and add to outfit
                if len(poss_bottoms) != 0:
                    bottom = random.choice(poss_bottoms)
                    outfit.append(bottom["image"])     
                
                # if there are no bottoms that match the criteria, user should add more clothing
                if len(poss_bottoms) == 0:
                    return {"missing": "Bottom"} # need shorts or skirt 

        # start with dress, we only need a dress and shoes for this outfit
        elif top_or_dress == 1:
            # choose random dress and add to outfit
            dress = random.choice(dresses)
            outfit.append(dress["image"])

            # get dress colors
            dress_colors = dress["colors"]

        if top_or_dress == 0:
            base_colors = top_colors
        else:
            base_colors = dress_colors

        # get shoes to complete outfit in both scenarios
        # shoes should either match top colors or dress colors
        poss_shoes = self.get_clothing_from_colors(shoes, base_colors)

        # if no shoes match, with top or dress colors, get shoes that are either black or white (will likely match with any outfit)
        if len(poss_shoes) == 0:
            poss_shoes = self.get_clothing_from_colors(shoes, "black, white")     

        # choose random shoe and add to outfit
        if len(poss_shoes) != 0:
            shoe = random.choice(poss_shoes)
            outfit.append(shoe["image"])

        # if still no shoes match, we can still create outfit with what we have

        return outfit
    
    # returns combination of clothing: "sweater, pants, shoes" or "sweater, skirt, shoes"
    def get_warm_ootd(self, closet):
        outfit = []

        # get all clothing relevant to this outfit
        sweaters = self.get_all_clothing_type("Sweater", closet)
        pants = self.get_all_clothing_type("Pants", closet)
        skirts = self.get_all_clothing_type("Skirt", closet)
        shoes = self.get_all_clothing_type("Shoe", closet)

        # if there are no sweaters, the user should add more clothing to closet
        if len(sweaters) == 0:
            return {"missing": "Sweater"} # need sweater

        # start with sweater
        # get random sweater, add to outfit
        # get its colors
        sweater = random.choice(sweaters)
        outfit.append(sweater["image"])
        sweater_colors = sweater["colors"]

        # get all possible bottoms (pants and skirts from closet)
        bottoms = pants + skirts

        # if there are no pants or skirts, the user should add more clothing to closet
        if len(bottoms) == 0:
            return {"missing": "Bottom"} # need shorts or skirt 
        
        # if top is white or black, it will likely match with any bottom
        if sweater_colors == "white" or sweater_colors == "black":
            # so choose random bottom and add to outfit
            bottom = random.choice(bottoms)
            outfit.append(bottom["image"])     
        
        else:
            # if not, get all bottoms that include any colors in the top
            poss_bottoms = self.get_clothing_from_colors(bottoms, sweater_colors)
            # and bottoms that are black, white, blue, or light blue (assuming blues are denim), likely will match with the top
            poss_bottoms += self.get_clothing_from_colors(bottoms, "black, white, blue, light blue")
            
            # choose a random bottom from possible bottoms and add to outfit
            if len(poss_bottoms) != 0:
                bottom = random.choice(poss_bottoms)
                outfit.append(bottom["image"]) 
                    
            # if there are no bottoms that match the criteria, user should add more clothing
            if len(poss_bottoms) == 0:
                return {"missing": "Bottom"} # need pants or skirt 

        # shoes should either match sweater colors
        poss_shoes = self.get_clothing_from_colors(shoes, sweater_colors)
        
        # if no shoes match, with sweater colors, get shoes that are either black or white (will likely match with any outfit)
        if len(poss_shoes) == 0:
            poss_shoes = self.get_clothing_from_colors(shoes, "black, white")     
                
        # choose random shoe and add to outfit
        if len(poss_shoes) != 0:
            shoe = random.choice(poss_shoes)
            outfit.append(shoe["image"])

        return outfit
    
    # returns combination of clothing: "top, jacket, pants, shoes"
    def get_cold_ootd(self, closet):
        outfit = []

        # get all clothing relevant to this outfit
        tops = self.get_all_clothing_type("Top", closet)
        pants = self.get_all_clothing_type("Pants", closet)
        jackets = self.get_all_clothing_type("Jacket", closet)
        shoes = self.get_all_clothing_type("Shoe", closet)

        # if there are no tops or jackets, user should add more clothing
        if len(tops) == 0:
            return {"missing": "Top"} # need top
        
        elif len(jackets) == 0:
            return {"missing": "Jacket"} # need jacket

        # start with top, add random top and jacket to outfit
        top = random.choice(tops)
        outfit.append(top["image"])

        jacket = random.choice(jackets)
        outfit.append(jacket["image"])

        # get top and jacket colors
        top_colors = top["colors"]
        jacket_colors = jacket["colors"]

        # if there are no pants, user should add more clothing
        if len(pants) == 0:
            return {"missing": "Pants"} # need pants

        # if top and jacket are white or black, it will likely match with any bottom
        if (jacket_colors == "white" or jacket_colors == "black") and (top_colors == "white" or top_colors == "black"):
            bottom = random.choice(pants)
            outfit.append(bottom["image"])     
        
        else:
            # if not, get all bottoms that include any colors in the top or jacket
            poss_bottoms = self.get_clothing_from_colors(pants, jacket_colors + top_colors)
            # and bottoms that are black, white, blue, or light blue (assuming blues are denim), likely will match with the top
            poss_bottoms += self.get_clothing_from_colors(pants, "black, blue, white")

            # choose a random bottom from possible bottoms and add to outfit
            if len(poss_bottoms) != 0:
                bottom = random.choice(poss_bottoms)
                outfit.append(bottom["image"]) 
                    
            # if there are no pants, user should add more clothing
            if len(poss_bottoms) == 0:
                return {"missing": "Pants"} # need pants

        # shoes should either match top colors or jacket colors
        poss_shoes = self.get_clothing_from_colors(shoes, top_colors + jacket_colors)

        # if no shoes match, with top or jacket colors, get shoes that are either black or white (will likely match with any outfit)
        if len(poss_shoes) == 0:
            poss_shoes = self.get_clothing_from_colors(shoes, "black, white")     
                
        # choose random shoe and add to outfit
        if len(poss_shoes) != 0:
            shoe = random.choice(poss_shoes)
            outfit.append(shoe["image"])

        return outfit

    # returns combination of clothing: "sweater, jacket, pants, shoes"
    def get_very_cold_ootd(self, closet):
        outfit = []

        # get all clothing relevant to this outfit
        pants = self.get_all_clothing_type("Pants", closet)
        jackets = self.get_all_clothing_type("Jacket", closet)
        sweaters = self.get_all_clothing_type("Sweater", closet)
        shoes = self.get_all_clothing_type("Shoe", closet)
        
        # if there are no sweaters or jackets, user should add more clothing
        if len(sweaters) == 0:
            return {"missing": "Sweater"} # need sweater
        
        elif len(jackets) == 0:
            return {"missing": "Jacket"} # need jacket

        # start with sweater, get random sweater and jacket and add to outfit
        sweater = random.choice(sweaters)
        outfit.append(sweater["image"])

        jacket = random.choice(jackets)
        outfit.append(jacket["image"])

        # get sweater and jacket colors
        sweater_colors = sweater["colors"]
        jacket_colors = jacket["colors"]

        # if there are no pants, user should add more clothing
        if len(pants) == 0:
            return {"missing": "Pants"} # need pants

        # if jacket and sweater are white or black, it will likely match with any bottom
        if (jacket_colors == "white" or jacket_colors == "black") and (sweater_colors == "white" or sweater_colors == "black"):
            bottom = random.choice(pants)
            outfit.append(bottom["image"])     
        
        else:
            # if not, get all bottoms that include any colors in the jacket or sweater
            poss_bottoms = self.get_clothing_from_colors(pants, jacket_colors + sweater_colors)
            # and bottoms that are black, white, blue, or light blue (assuming blues are denim), likely will match with the top
            poss_bottoms += self.get_clothing_from_colors(pants, "black, blue, white, light blue")
                    
            # choose a random bottom from possible bottoms and add to outfit
            if len(poss_bottoms) != 0:
                bottom = random.choice(poss_bottoms)
                outfit.append(bottom["image"]) 
            
            # if there are no pants, user should add more clothing
            if len(poss_bottoms) == 0:
                return {"missing": "Bottom"} # need pants

        # shoes should either match top colors or jacket colors
        poss_shoes = self.get_clothing_from_colors(shoes, jacket_colors + sweater_colors)

        # if no shoes match, with jacket or sweater colors, get shoes that are either black or white (will likely match with any outfit)
        if len(poss_shoes) == 0:
            poss_shoes = self.get_clothing_from_colors(shoes, "black, white")     
                
        # choose random shoe and add to outfit
        if len(poss_shoes) != 0:
            shoe = random.choice(poss_shoes)
            outfit.append(shoe["image"])

        return outfit
    
    def get_ootd(self, closet):
        # get weather
        weather = asyncio.run(self.get_weather())

        # if temperature is above 77, get hot outfit
        if weather["temperature"] > 77: # hot
            return {"outfit": self.get_hot_ootd(closet)}
        
        # else if temperature is above 55, get warm outfit
        elif weather["temperature"] > 55: # warm
            return {"outfit": self.get_warm_ootd(closet)}
        
        # else if temperature is above 40, get cold outfit
        elif weather["temperature"] > 40: # cold
            return {"outfit": self.get_cold_ootd(closet)}
        
        # else, get very cold outfit
        else: # very cold
            return {"outfit": self.get_very_cold_ootd(closet)}