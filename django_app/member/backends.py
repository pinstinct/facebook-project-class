import os
import re

import requests
from django.core.files.base import File
from django.core.files.temp import NamedTemporaryFile

from member.models import MyUser


class FacebookBackend():
    # 있으면 가져오고 아니면 인증하는 과정을 작성
    def authenticate(self, facebook_id, extra_fields=None):
        # 프로필 이미지를 가져오는 기능 추가
        url_profile = 'https://graph.facebook.com/{user_id}/picture'.format(
            user_id=facebook_id,
        )
        params = {
            'type': 'large',
            'width': '500',
            'height': '500',
        }

        # 메모리상에 임시파일 생성
        temp_file = NamedTemporaryFile(delete=False)

        # stream=True는 조각단위로 다운받음
        r = requests.get(url_profile, params, stream=True)

        # 요청하는 URL에서 파일 확장자를 가져옴,
        # 확장자랑 앞에 있는 이름을 구분해줌
        _, file_ext = os.path.splitext(r.url)

        # 확장자 저장 , .과 ? 사이만 가져옴 = 확장자
        file_ext = re.sub(r'(\.[^?]+).*', r'\1', file_ext)
        file_name = '{}{}'.format(
            facebook_id,
            file_ext
        )
        for chunk in r.iter_content(1024):
            temp_file.write(chunk)

        # facebooi_id가 username인 경우 MyUser를 갖고 오거나
        # defaults값을 이용해서 지정
        defaults = {
            'first_name': extra_fields.get('first_name', ''),
            'last_name': extra_fields.get('last_name', ''),
            'email': extra_fields.get('email', ''),
        }
        user, user_created = MyUser.objects.get_or_create(
            defaults=defaults,
            username=facebook_id
        )
        user.img_profile.save(file_name, File(temp_file))
        return user

    def get_user(self, user_id):
        try:
            return MyUser.objects.get(id=user_id)
        except MyUser.DoesNotExist:
            return None
