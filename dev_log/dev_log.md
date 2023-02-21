> django를 이용한 게시판 만들기  
> 정확히는 홈페이지 만들기, 기억력 저하로 인해 
> 기록을 남긴다(2023.2.21~)

# 가상환경
python = 3.9
django = 4.1

# 프로젝트 생성
```shell
(django_board) D:\workspace\django_board>django-admin startproject do_it_django_prj .
```

# 서버 실행
```shell
(django_board) D:\workspace\django_board>python manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions. 
Run 'python manage.py migrate' to apply them.
February 21, 2023 - 09:28:31
Django version 4.1, using settings 'do_it_django_prj.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.

```
# 관리자 계정 생성

## 마이그레이션
> 데이터베이스에 적용시켜야 하는 변화에 대한 기록
```shell
(django_board) D:\workspace\django_board>python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
```
> db.sqlite3 파일이 생성됨

## 관리자 계정 생성
```shell
(django_board) D:\workspace\django_board>python manage.py createsuperuser
Username (leave blank to use 'kcomwel'): kcwbig
Email address: kcwbig@comwel.or.kr
Password: 
Password (again):
This password is too short. It must contain at least 8 characters.
This password is too common.
This password is entirely numeric.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
```
서버 실행후 http://127.0.0.1:8000/admin/ 접속   
서버 실행시 migration 에러가 나타나지 않음

책에서는 .gitignore 파일에 db.sqlite3 도 추가   
집과 회사에서 동시 개발할때 필요할 듯 하여 추가하지 않음   

# APP 생성 (140p)
```shell
(django_board) D:\workspace\django_board>python manage.py startapp blog

(django_board) D:\workspace\django_board>python manage.py startapp single_pages
```



