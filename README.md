
# tfjzl-final-cloud-app-with-database

Django Online Course final project.

## Required assessment files
- onlinecourse/models.py
- onlinecourse/admin.py
- templates/course_details_bootstrap.html
- onlinecourse/views.py
- onlinecourse/urls.py
- screenshots/03-admin-site.png
- screenshots/07-final.png

## Run
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Then create the course, lessons, instructors, learners, questions and choices in `/admin/`.
