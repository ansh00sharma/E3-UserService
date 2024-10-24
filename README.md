### Project Name : Student Leaderboard
# This is a Student's Academic LearderBoard Project



Start Date : 1st November 2024 

Excepted Completion Date : ---

Completed On : 


---------------------------------------------------------------------------------------------------------

1. Create a virtual environment where you have Cloned the Repository, activate it and then start working on it (good practice)
 
   <b>python -m venv environment_name</b> (for example myenv, which i have used in the project)

2. Create Django-project, django-apps

   <b>django-admin createproject project_name</b> (for example project, which i have used in the project)

3. To collect staticfiles for production environment

   <b>python manage.py collectstatic</b>

4. Do migrations first (by default it will use sqlite, but you can always choose that like I am using Postgres, check project>settings.py>DATABASES)
 
   <b>python manage.py makemigrations</b> (this creates the migration file of your models)
   
   <b>python manage.py migrate</b> (this migrate the changes introduced through migration file into db)

6. Create a superuser for django-admin (using this superuser username and password you can access django-admin)

   <b>python manage.py createsuperuser</b>
