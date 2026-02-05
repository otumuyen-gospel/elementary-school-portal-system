# school-portal

### Introduction
this project is the design and implementation of a school web portal using python and javascript. Frameworks used include react and django. This appication helps to manage basic information of users in any primary or secondary school system.

### Project Features
* Users can signup and login to their account to access features that are specific to them.
* Only authenticated users can access features of the application.
* user Account includes: 
 -  Administrators Account
 -  Teachers Account
 -  Student Account
 -  Parent Account
* Only the admin can create a new user account while all others can signup to access their user-specific features.
* Non-authenticated users are not authorize or granted access to any application-features.
* The app is made of a django rest Api for the backend and react app for the frontend.



# Backend App

### Installation Guide
* Clone this repository (school-portal) [https://github.com/otumuyen-gospel/school-portal.git]
* for the backend install and configure Python, django and  your python virtual environment.
* navigate to the root folder of the backend app inside the folder of the cloned project.
* Install dependencies for the project using as stated below.
```cmd
  pip install -r requirements.txt
```
* Ensure to have postgresql database installed and have created the necessary database and database user account. Please see [database settings](backend/backend/settings.py) in the project settings for more information.
* then run django migrations to create database tables.
```cmd
  python manage.py makemigrations
  python manage.py migrate
```

### App usage
* navigate to the backend app root folder then run the code below to start django server.
```cmd
  python manage.py runserver
```
* You can access the API endpoints using postman or Curl or any other Rest client of own choosen on port 8000.

## API Endpoints

### Account API
| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |

| GET | /accounts/users-list/ | list all users account; access[admin] |
```cmd
  curl --request GET --url "http://127.0.0.1:8000/accounts/users-list/" --header "Authorization: Bearer yourToken"
```

| GET | /accounts/class-users/classId/ | users belonging to a class; access[Admin,Teacher] |
```cmd
  curl --request GET --url "http://127.0.0.1:8000/accounts/class-users/50/" --header "Authorization: Bearer yourToken"
```

| GET | /accounts/retrieve-user/userId/ | retrieve user's own account ; access[Any] |
```cmd
  curl --request GET --url "http://127.0.0.1:8000/accounts/retrieve-user/158/" --header "Authorization: Bearer yourToken"
```

| POST | /accounts/create-user/ | new user; access[admin] |
```cmd
  curl --request POST --url "http://127.0.0.1:8000/accounts/create-user/" --header "Authorization: Bearer yourToken" --data "key1=value1&key2=value2"
```
 - Note this method should not be accessed directly instead use the Auth API

| DELETE | /accounts/remove-user/userId/ | delete user; [access:admin] |
```cmd
  curl --request DELETE --url "http://127.0.0.1:8000/accounts/remove-user/158/" --header "Authorization: Bearer yourToken"
```

| PUT | /accounts/user-update/userId/ | update user own account; [access:Any] |
```cmd
  curl --request PUT --url "http://127.0.0.1:8000/accounts/user-update/158/" --header "Authorization: Bearer yourToken" --data "key1=value1&key2=value2"
```

| PATCH | /accounts/user-promotion/userId/ | update user's class; access[admin,teacher] |
```cmd
  curl --request PATCH --url "http://127.0.0.1:8000/accounts/user-promotion/158/" --header "Authorization: Bearer yourToken" --data "key1=value1&key2=value2"
```

| GET | /accounts/user-analytics/ | students distribution in various classess; access[any] |
```cmd
  curl --request GET --url "http://127.0.0.1:8000/accounts/user-analytics/" --header "Authorization: Bearer yourToken"
```

| GET | /accounts/export-users/ | users; access[admin] |
```cmd
  curl --request GET --url "http://127.0.0.1:8000/accounts/export-users/" --header "Authorization: Bearer yourToken"
```

| POST | /accounts/system-backup/ | db and file backup; access[admin] |
```cmd
  curl --request POST --url "http://127.0.0.1:8000 /accounts/system-backup/" --header "Authorization: Bearer yourToken" 
```

| POST | /accounts/system-restore/ | db and file restore; access[admin] |
```cmd
  curl --request POST --url "http://127.0.0.1:8000 /accounts/system-restore/" --header "Authorization: Bearer yourToken" 
```



### Attendance API
| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |

| GET | /attendance/attendance-list/ | list all attendance account; access[admin] |
```cmd
  curl --request GET --url "http://127.0.0.1:8000/attendance/attendance-list/" --header "Authorization: Bearer yourToken"
```

| GET | /attendance/class-attendance/classId/ | class attendance; access[Admin,Teacher] |
```cmd
  curl --request GET --url "http://127.0.0.1:8000/attendance/class-attendance/50/" --header "Authorization: Bearer yourToken"
```

| GET | attendance/user-attendance/userId/ | retrieve user's own attendance ; access[Any] |
```cmd
  curl --request GET --url "http://127.0.0.1:8000/attendance/user-attendance/158/" --header "Authorization: Bearer yourToken"
```

| POST | attendance/create-attendance/ | new attendance; access[admin,Teacher] |
```cmd
  curl --request POST --url "http://127.0.0.1:8000/attendance/create-attendance/" --header "Authorization: Bearer yourToken" --data "key1=value1&key2=value2"
```

| DELETE | attendance/delete-attendance/id/ | delete attendance; access[admin,Teacher] |
```cmd
  curl --request DELETE --url "http://127.0.0.1:8000/attendance/delete-attendance/158/" --header "Authorization: Bearer yourToken"
```

| PUT | attendance/update-attendance/id/ | update user attendance; access[Admin,Teacher] |
```cmd
  curl --request PUT --url "http://127.0.0.1:8000/attendance/update-attendance/158/" --header "Authorization: Bearer yourToken" --data "key1=value1&key2=value2"
```

| GET | /attendance/export-attendance/ | class attendance; access[Teacher] |
```cmd
  curl --request GET --url "http://127.0.0.1:8000/attendance/export-attendance/" --header "Authorization: Bearer yourToken"
```


### Auth API
| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |

| POST | auth/register/ | new account; access[admin] |
```cmd
  curl --request POST --url "http://127.0.0.1:8000/auth/register/" --header "Authorization: Bearer yourToken" --data "key1=value1&key2=value2"
```
| POST | auth/login/ | new login, new refresh & access token; access[Any] |
```cmd
  curl --request POST --url "http://127.0.0.1:8000/auth/login/"  --data "key1=value1&key2=value2" 
```
| POST | auth/refresh/ | refresh auth access token; access[Any] |
```cmd
  curl --request POST --url "http://127.0.0.1:8000/auth/refresh/"  --data "key1=value1&key2=value2" 
```
| POST | auth/logout/ | invalidate access token; access[Any] |
```cmd
  curl --request POST --url "http://127.0.0.1:8000/auth/logout/" --header "Authorization: Bearer yourToken" --data "key1=value1&key2=value2" 
```
- Note to completely logout stored authenticated user credentials in the frontend must be deleted.

| POST | auth/reset/request/ | request password reset token via email; access[Any] |
```cmd
  curl --request POST --url "http://127.0.0.1:8000/auth/reset/request/"  --data "key1=value1&key2=value2" 
```
| POST | auth/reset/verify/ | verify password reset token; access[Any] |
```cmd
  curl --request POST --url "http://127.0.0.1:8000/auth/reset/request/"  --data "key1=value1&key2=value2" 
```
| POST | auth/reset/password/ | reset password; access[Any] |
```cmd
  curl --request POST --url "http://127.0.0.1:8000/auth/reset/password/"  --data "key1=value1&key2=value2" 
```

| PUT | auth/update-password/userId/ | change password; access[Any] |
```cmd
  curl --request PUT --url "http://127.0.0.1:8000/auth/update-password/1/" --header "Authorization: Bearer yourToken"  --data "key1=value1&key2=value2" 
```

### Class API
| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |

| GET | classes/class-list/ | list all classes; access[admin,Teacher] |
```cmd
  curl --request GET --url "http://127.0.0.1:8000/classes/class-list/" --header "Authorization: Bearer yourToken"
```

| GET | classes/user-class/classId/ | users own class; access[student,parent] |
```cmd
  curl --request GET --url "http://127.0.0.1:8000/classes/user-class/50/" --header "Authorization: Bearer yourToken"
```

| POST | classes/create-class/ | new class; access[admin] |
```cmd
  curl --request POST --url "http://127.0.0.1:8000/classes/create-class/" --header "Authorization: Bearer yourToken" --data "key1=value1&key2=value2"
```

| DELETE | classes/delete-class/classId/ | delete attendance; access[admin] |
```cmd
  curl --request DELETE --url "http://127.0.0.1:8000/classes/create-class/158/" --header "Authorization: Bearer yourToken"
```

| PUT | classes/update-class/classId/ | update class; access[Admin] |
```cmd
  curl --request PUT --url "http://127.0.0.1:8000/classes/update-class/158/" --header "Authorization: Bearer yourToken" --data "key1=value1&key2=value2"
```


### Complaint API
| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |

| GET | complaints/complaint-list/ | list all user complaint; access[admin] |
```cmd
  curl --request GET --url "http://127.0.0.1:8000/complaints/complaint-list/" --header "Authorization: Bearer yourToken"
```

| GET | /complaints/class-complaint-list/classId/ | class complaint; access[Admin,Teacher] |
```cmd
  curl --request GET --url "http://127.0.0.1:8000/complaints/class-complaint-list/50/" --header "Authorization: Bearer yourToken"
```

| GET | complaints/user-complaint-list/userId/ | retrieve user's complaint ; access[Any] |
```cmd
  curl --request GET --url "http://127.0.0.1:8000/complaints/user-complaint-list/158/" --header "Authorization: Bearer yourToken"
```

| POST | complaints/create-complaint/ | new complaint; access[Admin,Parent,Student] |
```cmd
  curl --request POST --url "http://127.0.0.1:8000/complaints/create-complaint/" --header "Authorization: Bearer yourToken" --data "key1=value1&key2=value2"
```

| DELETE | complaints/delete-complaint/id/ | delete complaint; access[admin,Student,Parent] |
```cmd
  curl --request DELETE --url "http://127.0.0.1:8000/complaints/delete-complaint/158/" --header "Authorization: Bearer yourToken"
```

| PUT | complaints/update-complaint/id/ | update user complaints; access[Admin,Student,Parent] |
```cmd
  curl --request PUT --url "http://127.0.0.1:8000/complaints/update-complaint/1/" --header "Authorization: Bearer yourToken" --data "key1=value1&key2=value2"
```


### Homework API
| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |

| GET | homework/homework-list/ | list all user homework; access[admin] |
```cmd
  curl --request GET --url "http://127.0.0.1:8000/homework/homework-list/" --header "Authorization: Bearer yourToken"
```

| GET | /homework/class-homework-list/classId/ | class homework; access[Admin,Teacher] |
```cmd
  curl --request GET --url "http://127.0.0.1:8000/homework/class-homework-list/50/" --header "Authorization: Bearer yourToken"
```

| GET | homework/user-homework-list/userId/ | retrieve user's homework ; access[Admin,Student] |
```cmd
  curl --request GET --url "http://127.0.0.1:8000/homework/user-homework-list/158/" --header "Authorization: Bearer yourToken"
```

| POST | homework/create-homework/ | new homework; access[Admin,Student] |
```cmd
  curl --request POST --url "http://127.0.0.1:8000/homework/create-homework/" --header "Authorization: Bearer yourToken" --data "key1=value1&key2=value2"
```

| DELETE | homework/delete-homework/id/ | delete homework; access[admin,Student] |
```cmd
  curl --request DELETE --url "http://127.0.0.1:8000/homework/delete-homework/158/" --header "Authorization: Bearer yourToken"
```

| PUT | homework/update-homework/id/ | update user homework; access[Admin,Student] |
```cmd
  curl --request PUT --url "http://127.0.0.1:8000/homework/update-homework/1/" --header "Authorization: Bearer yourToken" --data "key1=value1&key2=value2"
  ```


### Marks API
| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |

| GET | /marks/mark-list/ | list all student marks; access[admin] |
```cmd
  curl --request GET --url "http://127.0.0.1:8000/marks/mark-list/" --header "Authorization: Bearer yourToken"
```

| GET | /marks/class-marks/classId/ | class marks; access[Admin,Teacher] |
```cmd
  curl --request GET --url "http://127.0.0.1:8000/marks/class-marks/50/" --header "Authorization: Bearer yourToken"
```

| GET | marks/user-marks/userId/ | retrieve user's own marks ; access[Student,Parent] |
```cmd
  curl --request GET --url "http://127.0.0.1:8000/marks/user-marks/158/" --header "Authorization: Bearer yourToken"
```

| POST | marks/create-marks/ | new marks; access[admin,Teacher] |
```cmd
  curl --request POST --url "http://127.0.0.1:8000/marks/create-marks/" --header "Authorization: Bearer yourToken" --data "key1=value1&key2=value2"
```

| DELETE | marks/delete-mark/id/ | delete marks; access[admin,Teacher] |
```cmd
  curl --request DELETE --url "http://127.0.0.1:8000/marks/delete-mark/158/" --header "Authorization: Bearer yourToken"
```

| PUT | marks/update-mark/id/ | update user marks; access[Admin,Teacher] |
```cmd
  curl --request PUT --url "http://127.0.0.1:8000/marks/update-mark/158/" --header "Authorization: Bearer yourToken" --data "key1=value1&key2=value2"
```

| GET | /marks/export-marks/ | User Marks; access[Student] |
```cmd
  curl --request GET --url "http://127.0.0.1:8000/marks/export-marks/" --header "Authorization: Bearer yourToken"
```


### Quiz API
| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |

| GET | quizzes/quiz-list/ | list all quizzes; access[admin] |
```cmd
  curl --request GET --url "http://127.0.0.1:8000/quizzes/quiz-list/" --header "Authorization: Bearer yourToken"
```

| GET | quizzes/class-quiz/classId/ | class specific quiz; access[Admin,Teacher] |
```cmd
  curl --request GET --url "http://127.0.0.1:8000/quizzes/class-quiz/50/" --header "Authorization: Bearer yourToken"
```

| GET | quizzes/user-quiz/classId/ | retrieve user's class active quizzes ; access[Student] |
```cmd
  curl --request GET --url "http://127.0.0.1:8000/quizzes/user-quiz/158/" --header "Authorization: Bearer yourToken"
```

| POST | quizzes/create-quiz/ | new quiz; access[admin,Teacher] |
```cmd
  curl --request POST --url "http://127.0.0.1:8000/quizzes/create-quiz/" --header "Authorization: Bearer yourToken" --data "key1=value1&key2=value2"
```

| DELETE | quizzes/delete-quiz/id/ | delete quiz; access[admin,Teacher] |
```cmd
  curl --request DELETE --url "http://127.0.0.1:8000/quizzes/delete-quiz/158/" --header "Authorization: Bearer yourToken"
```

| PUT | quizzes/update-quiz/id/ | update quiz; access[Admin,Teacher] |
```cmd
  curl --request PUT --url "http://127.0.0.1:8000/quizzes/update-quiz/158/" --header "Authorization: Bearer yourToken" --data "key1=value1&key2=value2"
```

### Schedule API
| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |

| GET | schedule/schedule-list/ | list all schedule; access[any] |
```cmd
  curl --request GET --url "http://127.0.0.1:8000/schedule/schedule-list/" --header "Authorization: Bearer yourToken"
```

| POST | schedule/create-schedule/ | new schedule; access[admin,Teacher] |
```cmd
  curl --request POST --url "http://127.0.0.1:8000/schedule/create-schedule/" --header "Authorization: Bearer yourToken" --data "key1=value1&key2=value2"
```

| DELETE | schedule/delete-schedule/id/ | delete schedule; access[admin,Teacher] |
```cmd
  curl --request DELETE --url "http://127.0.0.1:8000/schedule/delete-schedule/158/" --header "Authorization: Bearer yourToken"
```

| PUT |  schedule/update-schedule/id/ | update schedule; access[Admin,Teacher] |
```cmd
  curl --request PUT --url "http://127.0.0.1:8000/schedule/update-schedule/158/" --header "Authorization: Bearer yourToken" --data "key1=value1&key2=value2"
```


### Subjects API
| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |

| GET | subjects/subject-list/ | list all subject; access[admin] |
```cmd
  curl --request GET --url "http://127.0.0.1:8000/subjects/subject-list/" --header "Authorization: Bearer yourToken"
```

| GET | subjects/class-subject-list/classId/ | list all subject offered in a class; access[admin,teacher,student] |
```cmd
  curl --request GET --url "http://127.0.0.1:8000/subjects/class-subject-list/4/" --header "Authorization: Bearer yourToken"
```

| POST | subjects/create-subject/ | new subject; access[admin] |
```cmd
  curl --request POST --url "http://127.0.0.1:8000/subjects/create-subject/" --header "Authorization: Bearer yourToken" --data "key1=value1&key2=value2"
```

| DELETE | subjects/delete-subject/id/ | delete subject; access[admin] |
```cmd
  curl --request DELETE --url "http://127.0.0.1:8000/subjects/delete-subject/158/" --header "Authorization: Bearer yourToken"
```

| PUT |  subjects/update-subject/id/ | update subject; access[Admin] |
```cmd
  curl --request PUT --url "http://127.0.0.1:8000/subjects/update-subject/158/" --header "Authorization: Bearer yourToken" --data "key1=value1&key2=value2"
```




### Technologies
* Python Django and Django rest framework
* Postgresql database

### Authors
* [otumuyen-gospel](https://github.com/otumuyen-gospel)





# Frontend App

### Installation Guide
* for the frontend install and configure Node.js, NPM and YARN.
* navigate to the root folder of the react frontend app inside the folder of the cloned project.
* Install yarn globally.
```cmd
    npm install --global yarn
```
* Install dependencies for the react project as stated below.
```cmd
     yarn install
```
* Once the dependencies are installed, then run the following line of code to start the frontend server.
```cmd
     yarn start
```

### App usage

* You can access the frontend from any modern browser of your choosen on port 3000.
* For testing, users can login using any of the dummy accounts below for accessing the app.
* Admin(password:admin@123, username:admin)
* Teacher(password:teacher@123, username:teacher)
* Student(password:student@123, username:student)
* Parent(password:parent@123, username:parent)

### Authors
* [otumuyen-gospel](https://github.com/otumuyen-gospel)