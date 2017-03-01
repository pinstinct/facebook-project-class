# 소개
구현한 주요 기능은 다음과 같다.

1. OAuth 인증 연동
2. 페이스북 ID로 인증할 수 있는 Beckend 인증 시스템 구축
3. 가입 시 프로필 이미지도 저장하는 기능 추가


# 프로젝트 관리

```shell
.
├── django_app
│   ├── facebook
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── manage.py
└── requirements.txt

```

## Requirements
- Python (3.4.3)
- Django (1.10.5)
- requests (2.13.0)


## Installation
```shell
$ pip install -r 'requierements.txt'
```