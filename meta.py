import requests
from urllib.parse import quote
import json
import numpy as np

def format_cookies(unformatted_cookies):
    cookies = unformatted_cookies.split(';')
    cookies = [cookie.split('=', 1) for cookie in cookies]
    for i in range(len(cookies)):
        cookies[i] = [cookie.strip() for cookie in cookies[i]]
    cookies = np.array(cookies)
    cookies = dict(zip(cookies[:,0],cookies[:,1]))
    return cookies


act_id = ''
access_token = ''
cookies = ''

headers = {
    'authority': 'adsmanager-graph.facebook.com',
    'accept': '*/*',
    'accept-language': 'en;q=0.9',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://adsmanager.facebook.com',
    'referer': 'https://adsmanager.facebook.com/',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
}

goals={
    'CPM':['IMPRESSIONS','impressions'],
    'CPC':['LINK_CLICKS','actions']
}

def get_interest_id(interest):
    url=f'https://graph.facebook.com/v18.0/act_{act_id}/targetingsearch?access_token={access_token}&q={quote(interest)}'
    response = requests.get(url,cookies=format_cookies(cookies),timeout=30,headers=headers)
    response = json.loads(response.text)
    result = []
    for data in response['data']:
        result.append({'platform': 'facebook', 'id': data['id'], 'name' : data['name'], 'metadata': { 'type' : data['type']}})
    return result

def retrieve_cost_audience(interests,goal,currency,age=0,gender=0,country='',platform='',rel_status=0):
    begining_part='https://adsmanager-graph.facebook.com/v18.0/act_'
    logging_part= act_id+'/delivery_estimate?access_token='+access_token
    Goal_part='&method=get&optimization_goal='+goals[goal][0]+'&'
    agemax_part='"age_max":'+str(age)+',' if age!=0 else ''
    agemin_part='"age_min":'+str(age)+',' if age!=0 else ''
    gender_part=f'"genders":[{gender}],'
    if(country == ''):
        geolocation_part='"geo_locations":{"country_groups":["worldwide"],"location_types":["home"]},'
    else:
        geolocation_part='"geo_locations":{"countries":["'+country+'"],"location_types":["home"]},'
    if(platform == 'instagram'):
        platform_part = '"publisher_platforms":["instagram"],"instagram_positions":["stream","story","explore","reels"],"device_platforms":["mobile","desktop"],'
    elif(platform == 'facebook'):
        platform_part = '"publisher_platforms":["facebook"],"facebook_positions":["feed","instant_article","instream_video","video_feeds","marketplace","story","facebook_reels_overlay","search","groups_feed","facebook_reels"],"device_platforms":["mobile","desktop"],'
    else:
        platform_part = ''

    interest_part='"flexible_spec":['

    for i in interests:
        interest_part +='{"interests":[{"id":"' +i+'"}]},'


    relstatus_part = '{"relationship_statuses":["'+rel_status+'"]}' if rel_status!=0 else ''
    interest_part = interest_part + relstatus_part if relstatus_part != '' else interest_part[:-1] #to trim the last comma
    interest_part += ']'

    link=begining_part+logging_part+Goal_part+'targeting_spec={'+geolocation_part+gender_part+agemin_part+agemax_part+platform_part+interest_part+'}'+'&currency='+currency
    response = requests.get(link,cookies=format_cookies(cookies),timeout=30,headers=headers)
    response = json.loads(response.text)
    r=response["data"][0]["daily_outcomes_curve"]
    return [r[len(r)-1]['spend']*1000/r[len(r)-1][goals[goal][1]],response['data'][0]['estimate_mau']] if r[len(r)-1][goals[goal][1]]!=0 else [0,response['data'][0]['estimate_mau']]


print(get_interest_id('football'))
interest = get_interest_id('football')[1]['id']
print(retrieve_cost_audience(interests=[interest],goal='CPM',country='ES',currency='EUR')) 
