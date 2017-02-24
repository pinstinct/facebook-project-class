from pprint import pprint

import requests
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect

from facebook import settings


def login_fbv(request):
    facebook_app_id = settings.config['facebook']['app_id']
    context = {
        'facebook_app_id': facebook_app_id,
    }
    return render(request, 'member/login.html', context)


def logout_fbv(request):
    logout(request)
    return redirect('index')


def login_facebook(request):
    APP_ID = settings.config['facebook']['app_id']
    SECRET_CODE = settings.config['facebook']['secret_code']
    REDIRECT_URI = 'http://localhost:8000/member/login/facebook/'
    APP_ACCESS_TOKEN = '{app_id}|{secret_code}'.format(
        app_id=APP_ID,
        secret_code=SECRET_CODE
    )

    if request.GET.get('code'):
        code = request.GET.get('code')

        # 전달받은 code 값을 이용해 user_access_token 요청
        url_request_access_token = 'https://graph.facebook.com/v2.8/oauth/access_token'
        params = {
            'client_id': APP_ID,
            'redirect_uri': REDIRECT_URI,
            'client_secret': SECRET_CODE,
            'code': code
        }
        r = requests.get(url_request_access_token, params=params)
        dict_access_token = r.json()
        # access token 중요, 일단 이것만 사용
        USER_ACCESS_TOKEN = dict_access_token['access_token']
        print('USER_ACCESS_TOKEN : {}'.format(USER_ACCESS_TOKEN))

        # user_access_token, app_access_token 사용해 토큰 검증
        url_debug_token = 'https://graph.facebook.com/debug_token'
        params = {
            'input_token': USER_ACCESS_TOKEN,
            'access_token': APP_ACCESS_TOKEN,
        }
        r = requests.get(url_debug_token, params=params)
        dict_debug_token = r.json()
        pprint(dict_debug_token)
        USER_ID = dict_debug_token['data']['user_id']
        print('USER_ID : {}'.format(USER_ID))

        # 해당 USER_ID로 그래프 API에 유저 정보 요청
        url_api_user = 'https://graph.facebook.com/{user_id}'.format(
            user_id=USER_ID
        )
        fields = [
            'id',
            'first_name',
            'last_name',
            'gender',
            'picture',
            'email',
        ]
        params = {
            'fields': ','.join(fields),
            'access_token': USER_ACCESS_TOKEN,
        }
        r = requests.get(url_api_user, params)
        dict_user_info = r.json()
        pprint(dict_user_info)

        # 페이스븍 USER_ID만으로 인증
        user = authenticate(facebook_id=USER_ID)
        login(request, user)
        return redirect('index')
