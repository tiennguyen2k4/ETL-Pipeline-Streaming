import requests
import json

def Get_API_User():
    url = 'https://randomuser.me/api/'
    response = requests.get(url)
    result = response.json()
    if 'results' in result and result['results']:
        return result['results'][0]
    else:
        raise Exception("No results found in API response")

def Transform_Data_User():
    try:
        res_user = Get_API_User()
        index_in_phone = res_user['phone'].find(')')
        phone = res_user['phone'][index_in_phone+1:].replace("-", "")
        date_registered = res_user['registered']['date'][0:10]
        location = res_user['location']
        user = {
            'first_name': res_user['name']['first'],
            'last_name': res_user['name']['last'],
            'gender': res_user['gender'],
            'street': f"{location['street']['number']} {location['street']['name']}",
            'city': location['city'],
            'country': location['country'],
            'postcode': str(location['postcode']),
            'latitude': float(location['coordinates']['latitude']),
            'longitude': float(location['coordinates']['longitude']),
            'email': res_user['email'],
            'phone': str(phone),
            'username': res_user['login']['username'],
            'password_hash': res_user['login']['md5'],
            'date_registered': str(date_registered),
        }
    except Exception as e:
        print(f"Error fetching data: {e}")
    json_data = json.dumps(user, indent=4)
    return json_data

if __name__ == '__main__':
    Transform_Data_User()
