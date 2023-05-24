import json
import hmac
import hashlib
from urllib.parse import unquote

from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions

from src.account.models import TgUser


BOT_TOKEN = settings.BOT_TOKEN


def check_hash(tg_data):
    data_check_string = unquote(tg_data)

    data_check_arr = data_check_string.split('&')
    needle = 'hash='
    hash_item = ''
    telegram_hash = ''

    user_data = {}
    for item in data_check_arr:
        if item[0:len(needle)] == needle:
            telegram_hash = item[len(needle):]
            hash_item = item
        if item.startswith('user='):
            user_data = json.loads(item[5:])

    data_check_arr.remove(hash_item)
    data_check_arr.sort()
    data_check_string = "\n".join(data_check_arr)

    secret_key = hmac.new("WebAppData".encode(), BOT_TOKEN.encode(),  hashlib.sha256).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    return telegram_hash == calculated_hash, user_data


class TgAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        tg_data = request.META.get('HTTP_TG_DATA')

        if not tg_data:
            raise exceptions.AuthenticationFailed("tg-date is required!")
        
        if not BOT_TOKEN:
            raise exceptions.AuthenticationFailed("Bot token is not available!")
        
        is_authenticated, user_data = check_hash(tg_data)

        if not is_authenticated:
            raise exceptions.AuthenticationFailed("Authentication failed!")

        user_id = user_data.get('id')

        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')
        username = user_data.get('username')
        language_code = user_data.get('language_code')

        user = TgUser.objects.get_or_create(user_id=user_id, defaults={
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "language_code": language_code
        })[0]

        return (user, None) 
