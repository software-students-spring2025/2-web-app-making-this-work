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

*Note: These instructions follow installation and running on Mac OSX.*

### Making sure Python is installed

1. Ensure you have Python installed. Instructions for that can be found [here](https://www.python.org/downloads/).

### Cloning

2. Click the green button above labeled `Code`.
3. Ensure you are on the `Local` tab.
4. This next step is up to you, but I prefer to use HTTPS and the instructions will follow that.
5. Copy the link in the window.
6. Open a Terminal window on your machine and navigate to the directory where you would like to house the project's codebase.
7. Type `git clone https://github.com/software-students-spring2025/2-web-app-making-this-work.git`.
8. Navigate into the newly cloned folder using CD.

### Installing MongoDB locally

9. No .env file is needed. We will be hosting the DB locally. Ensure you have MongoDB community version installed locally. Enterprise version will work too, but the commands below are for community. The instructions installing can be found [here](https://www.mongodb.com/docs/manual/installation/#mongodb-installation-tutorials).
10. Once it is installed, run `brew services start mongodb-community`.

### Setting up the Python environment & DB-state

11. Using Python, create a virtual environment with `python -m venv environment_name`.
12. Enter that environment with the commant `source environment_name/bin/activate`.
13. Once inside the environment, run `pip install flask flask-login pymongo werkzeug python-dotenv` to install all non-default dependencies.
14. Run `python CreateDB.py`. This will create & initialize the database locally. If you run into issues, it may be because your machine is already hosting something on port 27017. In that case, end whatever process is doing that.

### Running the web-app

15. Now, run `flask run`.
16. Browse to the web app at the link http://127.0.0.1:5000.
17. Open Developer Tools in your browser and activate mobile viewing.

```
The DB is initialized with two default accounts. Their credentials are as follows.  
Admin Username:         `admin@nyu.edu`  
Admin Password:         `password`  
Generic User Username:  `user@nyu.edu`  
Generic User Password:  `password`  

You can also create your own account and select your privelages. The email you use must end in `@nyu.edu`.
```

### Shutting it down

17. To terminate hosting the web-app, in your terminal, click Control and C at the same time.
18. We are still in the virtual environment, so type the command `deactivate`. This will exit the environment.
19. Run the comman `brew services stop mongodb-community`, and you're done!
   
## Task boards

[Broken-Down Tasks Board](https://github.com/orgs/software-students-spring2025/projects/36)

[Sprint 1 Project Link](https://github.com/orgs/software-students-spring2025/projects/140/views/1)

[Sprint 2 Project Link](https://github.com/orgs/software-students-spring2025/projects/141/views/1)

## Screens

### 6 different screens.

- 2 that must display data retrieved from the database: [admin dashboard page](http://127.0.0.1:5000/dashboard), [map page](http://127.0.0.1:5000/).
- 1 that must allow the user to add data to the database: [signup page](http://127.0.0.1:5000/signup).
- 1 that must allow the user to edit data in the database: [bathroom page](http://127.0.0.1:5000/bathroom/67c86d2c86ba06887925a9d8) (when logged in as Admin).
- 1 that must allow the user to delete data from the database: [user profile page](http://127.0.0.1:5000/profile).
- 1 that must allow the user to search for data in the database: [search page](http://127.0.0.1:5000/search).

Note: some screens have multiple features and therefore overlap in their functionality, but for this documentation here, we are pretending they are single-feature in regard to the CRUD process.