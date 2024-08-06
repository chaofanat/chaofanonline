python manage.py makemigrations
python manage.py migrate

python manage.py collectstatic

@REM 创建超级用户
python manage.py createsuperuser


python run.py

@REM 生成requirements.txt
pip freeze > requirements.txt