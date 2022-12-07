import requests
import json
import os
#
#MIT License
#
#Get the weather from OpenWeathermap and display as text.
#requires a key from https://openweathermap.org/api  The api is free for use up to 1,000 api calls per day.
#We parse user input against a json list of airport codes. Users can search for weather by airport code, city or zip.
#
#Airport Codes came from https://github.com/Vertisize-Solutions/Airports-List  MIT license. You might want to get the latest.
#I've included it here for convenience
#
#Set path to airportcodes.json
airportcodes_path = '/home/pi/www/set-your-path-to/airportcodes.json'
#this is your OpenWeatherMap api key.  Won't work without it.
appid='your-open-wx-api-key'

def getWeather(local = 'fargo', *therest):
    units = 'imperial' #'metric'
    query = 'q='
    if len(local) == 3:
        try:
            airport = search(local.capitalize())
            local = str(airport[1] + ', ' + airport[3])
            query = 'q='

        except Exception as e:
            print('Error in getWeath > airportcodes call: ', e)
            
        
    #check for 5 digit U.S. zip code
    if len(local) == 5 and local.isdigit():
        query = 'zip='
            
    try:
        r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?{query}{local}&appid={appid}&units=imperial')
        d = r.json()
        return(d)

    except Exception as e:
        print('Error in getWeather: ', e)
        result = 'We could not find that city.\nTry again using this format: \nCity, Country Code. \n Example: Ottawa, CA\n'
        return(result)
    
def search(code, *therest):
    import json
    print('I am in openwx.search. ')
    code = code.upper()
    info = list()
    #print(os.chdir())
    try:
        with open(airportcodes_path) as ac:
            a = json.load(ac)

            for x in a:
                if x['AIRPORTCODE'] == code:     
                    info.append(x['AIRPORTNAME'])
                    info.append(x['CITY'])
                    info.append(x['COUNTRY'])
                    info.append(x['COUNTRYCODE'])
                    info.append(x['LAT'])
                    info.append(x['LONG'])
                    return(info)
                    break

    except Exception as e:
        print('error in search():  >>',e)
        return('Not Found')

if __name__ == '__main__':

    try:
        #wx =  getWeather('56560', 'alaska', 'Atlanta')
        a = input('Enter city, airport code or zip >')
        wx = getWeather(a)
        print(wx)

    except Exception as e:
        print ('Error in __main__ :', e)
