# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

To help university students filter, search for, and find campus bathrooms.

## User Stories

[User Stories Project Link](https://github.com/orgs/software-students-spring2025/projects/13/views/1)
1. As an user, I want to be able to delete my account so that I can completely leave the service at any time. 
2. As an admin, I'd like a dashboard so that I can view overall information.
3. As an admin, I want to be able to edit the bathroom's information so that the DB can be as accurate as possible.
4. As an user/admin, I want to be able to control wether or not I have admin privelages so that I can choose my correct role.
5. As a user, I want to be able to sign in to a personal account so that I can have my own data.
6. As a user I want to be able to open restroom location of choice in Google Maps so that I can navigate there quickly.
7. As a user, I want others to be able to leave reviews on bathrooms so that I can see public sentiment.
8. As a user, I want to be able to view the details of a certain bathroom so that I can compare them.
9. As a user, I want to be able to share bathrooms so that I can let a friend know about one if I so desire.
10. As a user, I want to filter bathrooms so that I can find one I'd prefer.


## Steps necessary to run the software

1. Ensure you have Python installed.
2. Click the green button above labeled `Code`.
3. Ensure you are on the `Local` tab.
4. This next step is up to you, but I prefer to use HTTPS and the instructions will follow that.
5. Copy the link in the window.
6. Open a Terminal window on your machine and navigate to the directory where you would like to house the project's codebase.
7. Type `clone https://github.com/software-students-spring2025/2-web-app-making-this-work.git`.
8. Navigate into the newly cloned folder using CD.
9. Place your credentials in the .env file.
10. Using Python, create a virtual environment with `python -m venv environment_name`
11. Enter that environment with the commant `source environment_name/bin/activate`
12. Once inside the environment, run `pip install flask flask-login pymongo werkzeug python-dotenv` to install all non-default dependencies.
13. Now, run app.py.
4. Browse to the web app at the link 127.0.0.1:5000.
*Note!* Your IP MUST BE WHITELISTED on the MongoDB in order to access it.
   
## Task boards

[Broken-Down Tasks Board](https://github.com/orgs/software-students-spring2025/projects/36)

[Sprint 1 Project Link](https://github.com/orgs/software-students-spring2025/projects/140/views/1)

[Sprint 2 Project Link](https://github.com/orgs/software-students-spring2025/projects/141/views/1)
