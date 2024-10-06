import requests

# you can get the api_key from https://openweathermap.org/ and sign in to the website
api_key = open('api_key.txt', 'r').read() # if you have a file containing the api key 
# api_key = 'you can paste your api_key too in here'

while True:
    location = input("Location: ")

    result = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={api_key}')
    if result.json()['cod'] == '404':
        print("Invalid location!")
        continue
    else:
        description = result.json()['weather'][0]['description']
        temperature = round(result.json()['main']['temp'])
        feels_like = round(result.json()['main']['feels_like'])
        high = round(result.json()['main']['temp_max'])
        low = round(result.json()['main']['temp_min'])

        print(f"\nThe weather in {location[0].upper()}{location[1:]} is {temperature}° C with {description}.")
        print(f"It feels like {feels_like}° C.")
        print(f"Today's high is {high}° C and today's low is {low}° C.")

        choose = str(input("\nDo you want to check other location? (y/n):"))

        if choose.lower() == 'y':
          continue
        elif choose.lower() == 'n':
          print("\nProgram exit!")
          break
    break
