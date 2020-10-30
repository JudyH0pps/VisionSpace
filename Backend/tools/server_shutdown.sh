kill $(ps -ef | grep -v "grep" | grep "python manage.py" | awk '{ print $2 }')
