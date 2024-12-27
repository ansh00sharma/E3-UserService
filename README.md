### Project Name : Student users
# This is a Student's Academic LearderBoard Project



Start Date : 1st November 2024 

Excepted Completion Date : ---

Completed On : 


---------------------------------------------------------------------------------------------------------

1. Create a virtual environment where you have Cloned the Repository, activate it and then start working on it (good practice)
 
   <b>python -m venv environment_name</b> (for example myenv, which i have used in the project)

2. Activate the Environment you created in step 1
 
   <b>.\myenv\Scripts\activate</b> (your cmd should change from C:\ to (myenv) C:\ )

3. To Install requirements for the Project use

   <b> pip install -r requirements.txt </b>
   
4. To Create Django-project from scratch 

   <b>django-admin startproject project_name</b> (for example users, which I have used in the project)

5. To collect staticfiles for production environment

   <b>python manage.py collectstatic</b>

6. For migrations first (by default it will use sqlite db, but you can always choose like I am using Mongodb, check project > settings.py > DATABASES)
 
   <b>python manage.py makemigrations</b> (this creates the migration file of your Models)
   
   <b>python manage.py migrate</b> (this migrate the changes introduced through migration file into db)

7. To Create a superuser for django-admin (using this superuser username and password you can access django-admin)

   <b>python manage.py createsuperuser</b>

8. To Run django server

   <b>python manage.py runserver </b>
