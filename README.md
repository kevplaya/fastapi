# Fastapi Application

## 개요
다국어 지원하는 회사 검색 및 태그명으로 검색, 태그 추가/삭제할 수 있는 API 서버 입니다.

## 시스템 요구 사항
- FastAPI
- SQLAlchemy
- MySQL
- Docker

## 기본 요구 사항
1. 회사명 자동완성 : 회사명 일부만으로도 회사명이 검색되어야 합니다.
2. 회사명으로 이름검색 : 회사명으로 Exact value 검색합니다.
3. 새로운 회사 추가
4. 태그명으로 회사검색 :
    - 관련된 회사가 검색되어야합니다.
    - 다국어로 검색이 가능해야합니다.
        - 일본어 및 다른 언어로 된 태그로 검색해도 회사가 노출되어야합니다.
    - 동일한 회사는 한번만 검색되어야 합니다.
5. 회사 태그 정보 추가 : 회사명에 태그 정보를 추가해야 합니다.
6. 회사 태그 정보 삭제 : 회사명에 태그 정보를 삭제해야 합니다.

## 서버 실행
아래 커맨드를 순서대로 실행합니다.

```bash
make build # 도커 이미지를 빌드합니다.
```

```bash
make setupdb # MySQL 데이터베이스를 생성합니다.
```

```bash
make up # 서버를 실행합니다.
```

## docker 용 make 커맨드 일람
```shell
make build # 도커 이미지를 빌드합니다.
make setupdb # MySQL 데이터베이스를를 생성합니다.
make up # 서버를 실행합니다.
make down # 컨테이너를 모두 중지합니다.
make shell # 쉘커맨드에 접근합니다.
make shell-mysql # MySQL 컨테이너 실행중 mysql shell에 접근합니다.
```

## .env 추가
root 폴더 하단에 아래 내용을 담은 env를 추가합니다.
```
DATABASE_URL=mysql+pymysql://root:root@{host_to_yourdb/container_name}:3306/wanted
```

## Test 방법

```shell
# 전체 테스트
python -m pytest tests/

# 개별 테스트
pytest -m pytest tests/{test_file_name}
pytest -m pytest tests/{test_file_name} -k {test_method}
```
