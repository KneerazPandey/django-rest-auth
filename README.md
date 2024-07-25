# django-rest-auth
This application uses Django and Django Rest Framework Simple JWT Authentication to perform token-based user authentication.

# Functionality in the Project
- Custom User Model 
- JWT Authentication Scheme
- User Registration through email
- Email verification through OTP sent to an registered email address
- Used celery to send the email in background so that user get response very fast
- Validated user registration OTP
- Secure Login 
- Initiate forget password
- Validate forget password OTP
- Reset Forget Password
- Change Password
- Used of django signals to create the schedule task
- Automatically deletes the token from the database ones expired so, it is no longer in used using celery

***Summery: This project covers all the basic authentication any sysetem needs with the best tools and technology.***

# Language
    Python

# Framework
    Django
    Celery
    Django Rest Framework

# Python Packages
    corsheaders
    djangorestframework-simplejwt
    celery
    redis
    python-dotenv

# Steps of running Project
- [1]  **Note: When using docker its very easy as all the setups is already configures. You only need to run the container**
```bash
    docker-compose up
```

---

- [2]  **Note: First of all install python in your local machine and install the following packages using the below commands in your virtual environment. Also you need to make sure the redis is running in your system**

```bash
    pip install django
    pip install djangorestframework
    pip install corsheaders
    pip install djangorestframework-simplejwt
    pip install python-dotenv
    pip install celery[redis]
```

---

```bash
    cd rest_auth
    python manage.py runserver
```

---

```bash
    cd rest_auth
    celery -A rest_auth worker -l info
```


***Suggestion: Just install docker and run one line of command (docker-compose up) to run the project. Using the manual approach can be time consuming as it required a lot of time and efforts to setup the project.***

# About Django
Python-based Django is a free and open-source web application framework. Clean, practical design and quick web development are both possible with it. It was created by seasoned programmers to simplify repetitious chores so that we could concentrate on creating apps rather than inventing the wheel. Read more about django through [documentation](https://docs.djangoproject.com/en/4.0/)

# About Django Rest Framework
For creating Web APIs, the Django REST framework offers a potent and adaptable toolbox. The following are some motives for using the REST framework: For your developers, the Web browsable API is a major usability win. Read more about django rest framework through [documentation](https://www.django-rest-framework.org/)

# Abut Django Celery
Django Celery is an integration of Celery, a distributed task queue, with the Django web framework. It allows Django applications to handle asynchronous tasks, such as sending emails, processing background jobs, or scheduling periodic tasks. By leveraging Celery, Django can offload long-running tasks from web requests, improving performance and user experience. Celery's flexibility and scalability make it ideal for managing complex workflows and background processes in Django projects. [documentation](https://docs.celeryq.dev/en/stable/)