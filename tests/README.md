# 테스트 데이터 덤프
scripts의 커맨드 실행 이후 wanted 데이터베이스 덤프
```shell
mysqldump -h {host_to_db} -P {port} -u {user} -p'{password}' --column-statistics=0 app >'/{filename}'
```
이후 테스트 데이터 덤프
```shell
mysql -h 127.0.0.1 -P 3306 -u root -p'root' --default-character-set=utf8 mb4  app_test <'{filename}'
```
