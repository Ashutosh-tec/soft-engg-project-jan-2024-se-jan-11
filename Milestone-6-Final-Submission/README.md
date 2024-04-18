# Instructions to run our application

1. Install and run Discourse for development using Docker:
* Use the following link for installation and to run the discourse:
    https://meta.discourse.org/t/install-discourse-for-development-using-docker/102009

2. To run our application:
*  Clone the repository using: 
    `git clone https://github.com/Ashutosh-tec/soft-engg-project-jan-2024-se-jan-11.git`
* Change the directory to the “backend” directory inside the “Milestone-6-Final-Submission” directory using the command:
    Linux: `cd Milestone-6-Final-Submission/Code/backend`, Windows: `cd .\Milestone-6-Final-Submission\Code\backend`
* Create a Python virtual environment using the command:
    Linux: `python3 -m venv .venv`, Windows: `python -m venv .venv`
* Activate the virtual environment using the command:
    Linux: `source .venv/bin/activate`, Windows: `.\.venv\Scripts\activate`
* Install the requirements using the command:
    `pip install -r requirements.txt`
* Now, on the terminal, type the following command to start the Flask server:
    Linux: `python3 main.py`, Windows: `python main.py`
* In the same “backend” directory, in a new terminal inside the virtual environment, start the redis server by typing:
    `redis-server`
* Similarly, start the celery worker in the “backend” directory inside the virtual environment by typing:
    `celery -A main.celery worker -l info`
* Furthermore, start the celery beat in the “backend” directory inside the virtual environment by typing:
    `celery -A main.celery beat --max-interval 1 -l info`
* For the frontend of the application, we would require Node.js and npm. We recommend installing the latest LTS version of Node.js from the following link:
    https://nodejs.org/en
* Once Node.js is installed and npm is working, open a new terminal and change the directory to the “Code” folder inside the “Milestone-6-Final-Submission” directory, which we saw earlier.
* Once inside the directory, change the directory to “frontend” by using the command: 
    `cd frontend`
* Now, run the following command to install the necessary packages for the frontend: 
    `npm install`
* After successful installation of the required packages, serve the frontend using the command:
    `npm run serve`
* The frontend server would be available at the following URL: 
    http://localhost:8080


Please note that for the email functionality and search functionality to work, you would need API keys. To secure these API keys, they aren’t part of the repository. You would need to request the keys from us.
