import requests


def local_long_lat():
    try:
        response = requests.get('https://api64.ipify.org?format=json')
        ip = response.json()['ip']
        # print("ip :", ip)
        response = requests.get(f'http://ip-api.com/json/{ip}')
        data = response.json()
        return data['lon'], data['lat']
    except Exception as e:
        return f"An error occurred: {e}"


def send_met_request(parameters):
    forecast_endpoint = 'https://api.met.no/weatherapi/locationforecast/2.0/compact.json'
    MET_CLIENT_ID = '776726f4-ce8f-4670-8ec9-e0ba796082cd'
    MET_CLIENT_SECRET = 'cef0915c-2487-4dcd-bfba-4d338722c9ef'
    header = {'User-Agent': 'weather-data-for-voice-assistant'}

    response = requests.get(forecast_endpoint,
                            headers=header,
                            params=parameters,
                            auth=(MET_CLIENT_ID, MET_CLIENT_SECRET))

    return response


def local_forcast():
    lon, lat = local_long_lat()
    try:
        parameters = {'lat': str(lat), 'lon': str(lon)}
        response = send_met_request(parameters)
        return response.json()
    except Exception as e:
        return f"An error occurred: {e}"


def local_time_and_air_temperature():
    forcat_data = local_forcast()
    time_temp_data_dict = {}
    for timeserie in forcat_data['properties']['timeseries']:
        time_temp_data_dict[timeserie['time']] = timeserie['data']['instant']['details']['air_temperature']

    return time_temp_data_dict
