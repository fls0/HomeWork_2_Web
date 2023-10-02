import folium
import requests
import re
from prompt_toolkit import prompt
from Map.prompt_tool import RainbowLetter,Completer

def command_save(file_name, map_name):
    russia_map = folium.Map(location=[55.7558, 37.6176], zoom_start=5)

    with open(file_name, 'r') as file:
        for line in file:
            coordinates = line.strip().split(',')
            if len(coordinates) != 2:
                raise ValueError("Файл має містити координати,що складаються з двох чисел, розділені комою. Наприклад: 55.7558,37.6176")
            lat, lon = map(float, coordinates)

            folium.Marker(
                location=[lat, lon],
                icon=folium.DivIcon(
                    icon_size=(12, 12),
                    html='<div style="background-color: red; width: 12px; height: 12px;"></div>'
                ),
                tooltip=f'Координати: {lat}, {lon}'
            ).add_to(russia_map)

    russia_map.save(map_name)
    return map_name
    

def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except UnboundLocalError:
            return "Неправильна назва міста."
        except ValueError:
            return "Incorrect date format."
    return wrapper


@input_error
def get_coordinates(city_name):
    api_key = "5cef6f4446b24817a8ebc8c727403c0a" 
    base_url = "https://api.opencagedata.com/geocode/v1/json"
    
    params = { "q": city_name,"key": api_key}
    response = requests.get(base_url, params=params)
    data = response.json()
    if data.get("results") and data["results"][0]["geometry"]:
        lat = data["results"][0]["geometry"]["lat"]
        lng = data["results"][0]["geometry"]["lng"]
        coordinates = lat, lng
    
    if coordinates:
        return f"Координати міста {city_name}: \n Широта: {lat} \n Довгота: {lng}"  
    else:
        return f"Не вдалося знайти координати для міста {city_name}."


def check_coordinates(file_name, coordinates):
    with open(file_name, 'r') as file:
        existing_coordinates = file.readlines()
    if coordinates in existing_coordinates:
        return True
    else:
        return False


def add_coordinates(file_name, coordinates):
    if not check_coordinates(file_name, coordinates):
        pattern = r'^-?\d+(\.\d+)?,-?\d+(\.\d+)?$'
        if re.match(pattern, coordinates):
            with open(file_name, 'a') as file:
                file.write('\n'+ coordinates)
                return f"Координати {coordinates} були додані до файлу."
        else:

            return f"Координати {coordinates} мають неправильний формат."
    else:
        return f"Координати {coordinates} вже існують у файлі."

def main(): 
    print("Вітаю. Доступні команди:")
    print("Зберегти карту ядерних обєктів країни 404 - 'save_nuclear'")
    print("Додати кординати до файлу з ядерними обєктами -'add_nuclear'")
    print("Зберегти карту аеропортів країни 404 - 'save_air'")
    print("Додати кординати до файлу з аеропортами -'add_air'")
    print("Зберегти карту адміністративних обєктів країни 404 - 'save_admin'")
    print("Додати кординати до файлу з ядерними обєктами -'add_admin'")
    print("Отримати кординати за назвою міста -'coordinates'")
    print("Вийти - 'good bye','close','exit'") 
    
    while True:
      

        input_str = prompt("Enter command: ", completer = Completer , lexer = RainbowLetter())
        
        if  input_str.startswith("save_nuclear"):
            result =command_save('Personal_assistant\Map\coordinates_nuclear.txt','russia_map_nuclear.html')
            print(f"Карта з  прапорцями збережена у файлі {result}.")  
        elif input_str.startswith("save_air"):
            result = command_save('Personal_assistant\Map\coordinates_air.txt','russia_map_air.html')
            print(f"Карта з  прапорцями збережена у файлі {result}.") 
        elif input_str.startswith("save_admin"):
            result =command_save('Personal_assistant\Map\coordinates_admin.txt','russia_map_admin.html')
            print(f"Карта з  прапорцями збережена у файлі {result}.")   
        elif input_str == "add_nuclear":
            input_str = input("Приклад: 55.7558,37.6176. Введіть нові кординати:")
            print(add_coordinates('Personal_assistant\Map\coordinates_nuclear.txt', input_str))
        elif input_str == "add_air":
            input_str = input("Приклад: 55.7558,37.6176. Введіть нові кординати:")
            print(add_coordinates('Personal_assistant\Map\coordinates_air.txt', input_str))
        elif input_str == "add_admin":
            input_str = input("Приклад: 55.7558,37.6176. Введіть нові кординати:")
            print(add_coordinates('Personal_assistant\Map\coordinates_admin.txt', input_str))
        elif input_str == "coordinates":
            input_str = input("Приклад: Москва. Введіть назву міста:")
            print(get_coordinates(input_str))         
        elif input_str in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Невірно введена команда. Доступні команди:")
            print("Зберегти карту ядерних обєктів країни 404 - 'save_nuclear'")
            print("Додати кординати до файлу з ядерними обєктами -'add_nuclear'")
            print("Зберегти карту аеропортів країни 404 - 'save_air'")
            print("Додати кординати до файлу з аеропортами -'add_air'")
            print("Зберегти карту адміністративних обєктів країни 404 - 'save_admin'")
            print("Додати кординати до файлу з ядерними обєктами -'add_admin'")
            print("Отримати кординати за назвою міста -'coordinates'")
            print("Вийти - 'good bye','close','exit'") 



if __name__ == "__main__":
    main()