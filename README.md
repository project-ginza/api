# Ginza API
For English, please [click here](/README_en.md).

## 1. 소개
Project Ginza에서 다음 기능을 담당하는 API.
* 회원 가입, 로그인, 정보변경 및 회원 탈퇴 등
* 상품 검색 및 주문
* 배송 처리

## 2. 실행방법
최초로 실행하는 경우, 먼저 마이그레이션을 통해 데이터베이스 세팅을 해주어야 합니다. 다음과 같이 진행합니다.
```shell
$python manage.py makemigrations
$python manage.py migrate
$python manage.py createsuperuser
```

그 다음에 실행 환경에 맞는 값을 입력하여 애플리케이션을 실행해 줍니다. 환경 변수 값은 다음과 같습니다.

* `local`: 각자 로컬 환경에서 실행
* `dev`: 개발 서버에서 실행시
* `staging`: 스테이징 서버에서 실행시
* `release`: 운영 서버에서 실행시

위의 환경변수 중 상황에 맞는 하나를 선택, 다음과 같이 실행해 주면 됩니다.
```shell
$python manage.py runserver 8000 --settings=ginza.settings.{env}
```

## 3. 로깅 (이세영 의견)
로그를 남기는 방법에 대해서 다음과 같은 여러 방식이 있지 않을까 생각이 들더라구요
* 파일에 로그 남기기
* DB에 로그 쌓기

현 단계에서는 전자와 같이 특정 디렉토리 내의 특정 파일에 쓰는 방식으로 처리합니다.

나중에 프로덕트 레벨에는 아파치 카프카를 적용하여 카프카에 로깅 메시지를 던지는 쪽으로 아키텍처를 고도화 해보는 쪽으로도 일단 생각은 해보고 있습니다. 물론 이렇게 하려면 카프카에서 로그를 받아와서 기록하는 로거를 따로 또 개발해야 하겠지만요.

### Simple Docker Command
* > docker-compose up -d
* > docker ps 
* > docker-compose down 