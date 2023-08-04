from bson.objectid import ObjectId
from pymongo.errors import PyMongoError
from pymongo import UpdateOne
from db import get_connection


def update_data(property_search, vehicle_selected, all_data):
    if property_search in vehicle_selected and isinstance(vehicle_selected[property_search], ObjectId):
        for data in all_data:
            if vehicle_selected[property_search] == data['_id']:
                vehicle_selected[property_search] = data


def update_colors(vehicle_selected):
    colors = [{'value': 'blue', 'translate': 'azul'},
              {'value': 'red', 'translate': 'rojo'},
              {'value': 'black', 'translate': 'negro'},
              {'value': 'white', 'translate': 'blanco'},
              {'value': 'yellow', 'translate': 'amarillo'},
              {'value': 'graphite', 'translate': 'grafito'},
              {'value': 'gray', 'translate': 'gris'},
              {'value': 'green', 'translate': 'verde'},
              {'value': 'orange', 'translate': 'naranja'}]
    for color in colors:
        if 'color' in vehicle_selected and vehicle_selected['color'] == color['value']:
            vehicle_selected['color'] = color['translate']
        if 'secondaryColor' in vehicle_selected and vehicle_selected['secondaryColor'] == color['value']:
            vehicle_selected['secondaryColor'] = color['translate']


try:
    client, db = get_connection()

    vehicle_collection = db["vehicles"]
    vehicles = list(vehicle_collection.find())

    hub_collection = db["hubs"]
    hubs = list(hub_collection.find({}, {"name": 1}))
    brand_collection = db["brands"]
    brands = list(brand_collection.find({}, {"name": 1}))
    model_collection = db["vmodels"]
    models = list(model_collection.find({}, {"name": 1}))
    cylinders_capacity_collection = db["cylinderscapacities"]
    cylinders_capacities = list(cylinders_capacity_collection.find({}, {"value": 1}))
    country_collection = db["countries"]
    countries = list(country_collection.find({},
                                        {"createdAt": 0, "updatedAt": 0, "created_by": 0, "updated_by": 0, "__v": 0}))
    city_collection = db["cities"]
    cities = list(city_collection.find({}, {"name": 1}))

    updates = [{'name_property': 'hub', 'data_collection': hubs},
               {'name_property': 'brand', 'data_collection': brands},
               {'name_property': 'cylindersCapacity', 'data_collection': cylinders_capacities},
               {'name_property': 'model', 'data_collection': models},
               {'name_property': 'country', 'data_collection': countries},
               {'name_property': 'city', 'data_collection': cities}]

    updated_vehicles = 0
    operations = []
    for vehicle in vehicles:
        try:
            for one_update in updates:
                update_data(one_update['name_property'], vehicle, one_update['data_collection'])
            update_colors(vehicle)
            vehicle.pop('salePrice', None)
            vehicle.pop('oldPrice', None)
            op = UpdateOne(
                {'_id': vehicle['_id']},
                {'$set': vehicle, '$unset': {'salePrice': "", 'oldPrice': ""}}
            )
            operations.append(op)
            updated_vehicles += 1
            print("append vehicle #", updated_vehicles)
        except Exception as e:
            print(f"Error processing vehicle {updated_vehicles}: {e}")
    if operations:
        print('start bulk update!')
        print("Loading...")
        vehicle_collection.bulk_write(operations)
        print('end bulk update!')
    print("Updated vehicles: ", updated_vehicles)

except PyMongoError as e:
    print(f"An error occurred in PyMongo: {str(e)}")

finally:
    if 'client' in locals():
        print("Connection close!")
        client.close()
