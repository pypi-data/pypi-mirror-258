# Django Appointment 📦

![Tests](https://github.com/adamspd/django-appointment/actions/workflows/tests.yml/badge.svg)
![Published on PyPi](https://github.com/adamspd/django-appointment/actions/workflows/publish.yml/badge.svg)
[![Current Release Version](https://img.shields.io/github/release/adamspd/django-appointment.svg?style=flat-square&logo=github)](https://github.com/adamspd/django-appointment/releases)
[![pypi Version](https://img.shields.io/pypi/v/django-appointment.svg?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/django-appointment/)
[![PyPi downloads](https://static.pepy.tech/personalized-badge/django-appointment?period=total&units=international_system&left_color=grey&right_color=orange&left_text=pip%20downloads)](https://pypi.org/project/django-appointment/)
[![codecov](https://codecov.io/gh/adamspd/django-appointment/branch/main/graph/badge.svg?token=ZQZQZQZQZQ)](https://codecov.io/gh/adamspd/django-appointment)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/adamspd/django-appointment)](https://github.com/adamspd/django-appointment/commits/main)
[![GitHub last commit](https://img.shields.io/github/last-commit/adamspd/django-appointment)](https://github.com/adamspd/django-appointment/commit/main)
[![GitHub issues](https://img.shields.io/github/issues/adamspd/django-appointment)](https://github.com/adamspd/django-appointment/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/adamspd/django-appointment)](https://github.com/adamspd/django-appointment/pulls)
[![GitHub contributors](https://img.shields.io/github/contributors/adamspd/django-appointment)](https://github.com/adamspd/django-appointment/graphs/contributors)

⚠️ **IMPORTANT**: If upgrading from a version before 2.x.x, please note significant database changes were introduced in
Version 2.0.0 introduces significant database changes. Please read
the [migration guide](https://github.com/adamspd/django-appointment/tree/main/docs/migration_guides/v2_1_0.md) before
updating. Version 3.x.x introduces the ability to send email reminders for appointments using Django Q for efficient
task scheduling. It also allows clients to reschedule appointments if it is allowed by admins.

Django-Appointment is a Django app engineered for managing appointment scheduling with ease and flexibility. It enables
users to define custom configurations for time slots, lead time, and finish time, or utilize the default values
provided. This app proficiently manages conflicts and availability for appointments, ensuring a seamless user
experience.

For a detailed walkthrough and live example of the system, please refer to
[this tutorial](https://github.com/adamspd/django-appointment/tree/main/docs/explanation.md).

Detailed documentation can be found in
the [docs' directory](https://github.com/adamspd/django-appointment/tree/main/docs/README.md).
For changes and migration information, please refer to the release
notes [here](https://github.com/adamspd/django-appointment/releases)
and [here](https://github.com/adamspd/django-appointment/tree/main/docs/release_notes).

## Features ✨

1. Customizable time slots, lead time, and finish time.
2. Competent handling of appointment conflicts and availability.
3. Seamless integration with the Django admin interface for appointment management.
4. Custom admin interface for managing appointment/staff member editing, creation, availability, and conflicts.
5. User-friendly interface for viewing available time slots and scheduling appointments.
6. Capability to send email notifications to clients upon scheduling an appointment and email reminders for
   appointments, leveraging Django Q for task scheduling and efficiency.

## Key features introduced in previous versions.

- For more information, please refer to
  this [documentation](https://github.com/adamspd/django-appointment/tree/main/docs/history).

## Added Features and Bug Fixes in version 3.x.x

See the [release notes](https://github.com/adamspd/django-appointment/releases/tag/v3.2.0).
For older version,
see their [release notes](https://github.com/adamspd/django-appointment/tree/main/docs/release_notes).

## Quick Start 🚀

1. Add "appointment" to your `INSTALLED_APPS` setting like so:

   ```python
   INSTALLED_APPS = [
       # other apps
       'appointment',
       'django_q',
   ]
   ```

2. Incorporate the appointment URLconf in your project's `urls.py` like so:

   ```python
   from django.urls import path, include
   
   urlpatterns = [
       # other urls
       path('appointment/', include('appointment.urls')),
   ]
   ```
3. In your Django's `settings.py`, append the following:

   ```python
   AUTH_USER_MODEL = 'models.UserModel'  # Optional if you use Django's user model
   ```

   For instance, if you employ a custom user model:

   ```python
   AUTH_USER_MODEL = 'client.UserClient'
   ```

   If you're utilizing the default Django user model, there's no need to add this line since Django automatically sets
   it to:

   ```python
   AUTH_USER_MODEL = 'auth.User'
   ```

   Ensure your `create_user` function includes the following arguments, even if they are not all utilized:

   ```python
   def create_user(first_name, email, username, last_name=None, **extra_fields):
       pass
   ```

   This function will create a user with a password formatted as: f"{APPOINTMENT_WEBSITE_NAME}{current_year}"

   For instance, if you append this to your `settings.py`:

   ```python
   APPOINTMENT_WEBSITE_NAME = 'Chocolates'
   ```

   And the current year is 2023, the password will be "Chocolates2023". If `APPOINTMENT_WEBSITE_NAME` is not provided,
   the default value is "Website", rendering the password as "Website2023".

   This name is also utilized in the footer of the emails sent to clients upon scheduling an appointment:

   ```html
   <p>® 2023 {{ APPOINTMENT_WEBSITE_NAME }}. All Rights Reserved.</p>
   ```

   Configure `Q_CLUSTER` in your Django's `settings.py` to enable Django Q task scheduling:
   ```python
      Q_CLUSTER = {
        'name': 'DjangORM',
        'workers': 4,
        'timeout': 90,
        'retry': 120,
        'queue_limit': 50,
        'bulk': 10,
        'orm': 'default',
      }
    ```

4. Run `python manage.py migrate` to create the appointment models.

5. Start the Django Q cluster with `python manage.py qcluster`.

6. Launch the development server and navigate to http://127.0.0.1:8000/admin/ to create appointments, manage
   configurations, and handle appointment conflicts (the Admin app must be enabled).
7. You must create at least one service before using the application on the admin page. If your service is free, input 0
   as the price. If your service is paid, input the price in the price field. You may also provide a description for
   your service.
8. Visit http://127.0.0.1:8000/appointment/request/<service_id>/ to view the available time slots and schedule an
   appointment.

## Docker Support 🐳

Django-Appointment now supports Docker, making it easier to set up, develop, and deploy. With Docker and Docker Compose,
you can quickly get the project running in a consistent environment, streamline the development process, and simplify
deployment across different platforms.

### Getting Started with Docker for Development or Local Testing

Using Django-Appointment with Docker is primarily intended for development purposes or local testing. This means you'll
need to clone the project from the GitHub repository to get started.

Here's how you can set up Django-Appointment for local development or testing with Docker:

1. **Clone the Repository**: Clone the Django-Appointment repository to your local machine:

   ```bash
   git clone https://github.com/adamspd/django-appointment.git
   ```
   
   or using SSH:
   ```bash
   git clone git@github.com:adamspd/django-appointment.git
   ```

2. **Prepare .env File**: Create an `.env` file in the root directory of your project with your configuration settings.
   You should include your email host user and password for Django's email functionality:

   ```plaintext
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_password
   ```
3. **Build and Run the Docker Containers**: Run the following command to build and run the Docker containers:

   ```bash
   docker-compose up -d --build
   ```

4. **Create a Superuser**: After the containers are running, create a superuser to access the Django admin interface:

   ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

5. **Access the Application**: Once the containers are running, you can access the application at `localhost:8000`. The
   Django admin interface is available at `localhost:8000/admin`.
6. **Shut Down the Containers**: When you're finished, you can shut down the containers with the following command:

   ```bash
   docker-compose down
   ```
7. **(Optional) Run Migrations**: If you make changes to the models or database, you can run the migrations with the
   following command:

   ```bash
   docker-compose exec web python manage.py migrate
   ```

> **Note:** I use the default database settings for the Docker container. If you want to use a different database, you
> can
> modify the Dockerfile and docker-compose.yml files to use your preferred database.

## Customization 🔧

1. In your Django project's `settings.py`, you can override the default values for the appointment scheduler. More
   information regarding available configurations can be found in
   the [documentation](https://github.com/adamspd/django-appointment/tree/main/docs/README.md#configuration).
2. Modify these values as needed for your application, and the app will adapt to the new settings.
3. For further customization, you can extend the provided models, views, and templates or create your own.

## Support 💬

For support or inquiries regarding the Appointment Scheduler app, please refer to the documentation in the "docs"
directory or visit the GitHub repository for more information.

## Contributing 🤝

Contributions are welcome! Please refer to
the [contributing guidelines](https://github.com/adamspd/django-appointment/tree/main/CONTRIBUTING.md) for more
information.

## Code of Conduct 📜

Please refer to the [code of conduct](https://github.com/adamspd/django-appointment/tree/main/CODE_OF_CONDUCT.md) for
more information.

## Security policy 🔒

Please refer to the [security policy](https://github.com/adamspd/django-appointment/tree/main/SECURITY.md) for more
information.

## Notes 📝⚠️

I'm working on a testing website for the application
that is not fully functional yet, no hard feelings. But you can check it out
at [https://django-appt.adamspierredavid.com/](https://django-appt.adamspierredavid.com/). Ideas are welcome here since
I'm blocked on a few points.

## About the Author

Adams Pierre David - [Website](https://adamspierredavid.com/)