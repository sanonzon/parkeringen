# parkeringen

## slö 'deploy'.
python parkering/manage.py runserver LOKALT_IP:PORT<br>
Forward:a PORT i din router till LOKALT_IP så folk kan använda det.


#/account
Everything related to user
#/main
Everything connected
#/kombo_parking
Everything related to the komboparking project

python manage.py runserver<br>
  starts local server.
  
python manage.py createsuperuser<br>
  Create your own local admin for your own database.

python manage.py makemigrations \<appname\><br>
  Creates helper-files for database.

python manage.py migrate<br>
  Creates / Edits the database with helper-files from above.
  
