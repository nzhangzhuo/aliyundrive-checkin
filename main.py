import datetime
import time

import requests

import aliyun_token


def get_access_token(token):
    url = 'https://auth.aliyundrive.com/v2/account/token'
    payload = {'grant_type': 'refresh_token', 'refresh_token': token}

    response = requests.post(url, json=payload, timeout=5)
    data = response.json()

    if 'code' in data and data['code'] in ['RefreshTokenExpired', 'InvalidParameter.RefreshToken']:
        return False, '', '', data['message']

    nick_name, user_name = data['nick_name'], data['user_name']
    name = nick_name if nick_name else user_name
    access_token = data['access_token']
    return access_token


def sign_in(user):
    access_token = get_access_token(aliyun_token.token[user])
    url = 'https://member.aliyundrive.com/v1/activity/sign_in_list'
    payload = {'isReward': False}
    params = {'_rx-s': 'mobile'}
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.post(url, json=payload, params=params, headers=headers, timeout=5)
    data = response.json()
    return data
def sign_in_reward(day, user):
    json_data = {
        'signInDay': str(day),
    }
    access_token = get_access_token(aliyun_token.token[user])
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.post('https://member.aliyundrive.com/v1/activity/sign_in_reward',
                             headers=headers,
                             json=json_data)
    return response.json()


if __name__ == '__main__':
    arr = ['13992772974', '17209072974', '17209073367', '17209073974',
           '17209070297', '19034640815', '17320526936']
    while True:
        print(datetime.datetime.fromtimestamp(time.time()))
        for x in arr:
            print(x, str(sign_in(x))[:40] + '}')
            time.sleep(1)
        time.sleep(24 * 60 * 60)
