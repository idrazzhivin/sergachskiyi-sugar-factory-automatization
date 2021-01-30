import requests
import json
import simplekml

def get_token(login, password):
    log_resp = requests.get('http://cloud.ckat-nn.ru/ServiceJSON/Login?UserName={}&Password={}'.format(login, password))
    if log_resp:
        token = log_resp.text
        return token
    else:
        print('Login error')
        return -1


def get_schemas(token):
    schemas_resp = requests.get('http://cloud.ckat-nn.ru/ServiceJSON/EnumSchemas?session={}'.format(token))
    if schemas_resp:
        schemas = schemas_resp.json()
        return schemas
    else:
        print('EnumSchemas error')
        return -1


def get_devices_id(token, schema_id):
    devices_resp = requests.get('http://cloud.ckat-nn.ru/ServiceJSON/EnumDevices?session={}&schemaID={}'.format(
        token, schema_id))
    if devices_resp:
        devices = devices_resp.json()
        devices_id = []
        for device in devices['Items']:
            devices_id.append(device['ID'])
        return devices_id
    else:
        print('EnumDevices error')
        return -1


def get_data_by_id(token, schema_id, device_id):  # на выходе - все данные
    online_info_resp = requests.get('http://cloud.ckat-nn.ru/ServiceJSON/GetOnlineInfo?session={}&schemaID={}&IDs={}'.format(
            token, schema_id, device_id))
    if online_info_resp:
        online_info_resp = online_info_resp.json()
        return online_info_resp
    else:
        print('GetOnlineInfo error')
        return -1


'''
def get_data_all(token, schema_id, all_ids):  # !
    max_req_size = 50  # максимальное количество id, которое подается на сервер при одном запросе
    req_size = 0
    ids_req_str = ''
    data_all = dict()
    for id in all_ids:
        if req_size == max_req_size - 1:
            ids_req_str += id + ','
            online_info = get_data_by_id(token, schema_id, ids_req_str)
            if online_info != -1:
                print('Retrieved the following ids (max {} per request): {}'.format(max_req_size, ids_req_str))
                for key in online_info:
                    if (online_info[key] != None):
                        if online_info[key]['LastPosition']['Lat'] != 0 and online_info[key]['LastPosition']['Lng'] != 0:
                            data_all[key] = online_info[key]['LastPosition']
                        else:
                            print('No coordinates for', key)
                    else:
                        print('No info about', key)
            ids_req_str = ''
            req_size = 0
        else:
            ids_req_str += id + ','
            req_size += 1

    # для оставшихся
    online_info_resp = requests.get(
        'http://cloud.ckat-nn.ru/ServiceJSON/GetOnlineInfo?session={}&schemaID={}&IDs={}'.format(
            token, schema_id, ids_req_str))
    online_info = online_info_resp.json()
    if online_info != -1:
        print('Retrieved the following ids (max {} per request): {}'.format(max_req_size, ids_req_str))
        for key in online_info:
            if (online_info[key] != None):
                if online_info[key]['LastPosition']['Lat'] != 0 and online_info[key]['LastPosition']['Lng'] != 0:
                    data_all[key] = online_info[key]['LastPosition']
                else:
                    print('No coordinates for', key)
            else:
                print('No info about', key)

    return data_all
'''


def get_data_all(token, schema_id):  # на выходе - словарь с координатами
    online_info_all_resp = requests.get('http://cloud.ckat-nn.ru/ServiceJSON/GetOnlineInfoAll?session={}&schemaID={}'.format(token, schema_id))
    if online_info_all_resp:
        online_info_all = online_info_all_resp.json()
        coords = dict()
        for key in online_info_all:
            if (online_info_all[key] != None):
                if online_info_all[key]['LastPosition']['Lat'] != 0 and online_info_all[key]['LastPosition']['Lng'] != 0:
                    coords[key] = online_info_all[key]['LastPosition']
                else:
                    print('No coordinates for', key)
            else:
                print('No info about', key)
        return coords
    else:
        print('GetOnlineInfoAll error')
        return -1


def add_data_to_kml(coordinates, filename):
    kml = simplekml.Kml()
    for key in coordinates:
        pnt = kml.newpoint()
        pnt.name = key
        pnt.description = 'There is supposed to be fuel level for ' + key
        pnt.coords = [(
            coordinates[key]['Lng'],
            coordinates[key]['Lat']
        )]
    kml.save(filename)


# ------------------------------------------------------------------#
login = 'Весна'
password = '912912913'
# token = GetToken(login, password)
token = '49FE5BA414AD84FACBD27EAA845EA440B7638E634CD265C09FAFB45B1121D06A'
if token != -1:
    schemas = get_schemas(token)
    schema_id = schemas[0]['ID']
    print('Token:', token)
    print('Schema ID:', schema_id)
    print('Sсhema name:', schemas[0]['Name'])
    devices_ids = get_devices_id(token, schema_id)
    print(devices_ids)
    coords = get_data_all(token, schema_id)
    #key = '12f35d7c-34e3-45f9-a25b-338925c839ad'
    #data = get_data_by_id(token, schema_id, key)
    #print(data[key]['LastPosition'])
    #coordinates = data[key]['LastPosition']
    add_data_to_kml(coords, 'Vehicles.kml')



