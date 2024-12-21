# 4EvaBraids-backend

## Contents

1. [Introduction](#introduction)
2. [About](#about)
3. [Features (implemented)](#implemented-features)
4. [Features (To be implemented](#yet-to-be-implemented-features)
5. [Technologies](#technologies)
6. [Folder structure](#folder-structure)
7. [Important Folders and Their Purpose](#important-folders-and-their-purpose)
8. [Algorithms for crucial parts](#algorithms-for-crucial-parts)
9. [Deployment](#deployment)
10. [Contributing](#contributing)
11. [Link to resources](#important-links)

<br>

## Introduction

4EvaBraids is an online hair braiding platform, where users can books appointments with with skilled braiders and get their hair made, either as home service or onsite braiding. While this is the core of it's purpose there are other functionalities and features developed to spice up the site - Read on and see more!
![Landing Page](docs/images/Hero%20Section.png "Landing Page")

<br>

## About

-   Purpose
    -   The purpose of this site is to make finding and making braiding appointments easier for clients and also to automate managing custormers for the braiders. It also improves visibility and professionalism.
-   Motivation
    -   Prior tonow, braiders use Instagram and Tiktok as their bassic platform for professional page and work gallery. while these platforms are very good when used as galleries, they have several disadvantages. Just to list a few
        -   Not flexible
        -   Zero Automation
        -   Less professional
        -   Poor data gathering capabilities
-   Solution
    -   We provide the solution to all the above stated problems, and even more. such solutions are stated below
        -   Great professional brand (using a .com site, cool!)
        -   Unlimited way to showcase your work (we even liked the gallery to both IG and Tiktok, so videos hosted there can be displayed nd showcased on the site while keepig our database lighter
        -   Premuim booking experience
        -   Blog to improve SEO and show Ads
        -   Massive data logging and gathering information
        -   Complex automation to ease both client and braider of stress

![Features Page](docs/images/Features%20Section.png "Features Section")

<br>

## Implemented Features

None Yet

## Yet To Be Implemented Features

1. Gallery: A video and photo library
    - Gallery from our local database
    - Gallery from Instagram
    - Gallery from Tiktok
2. Booking algorithm
    - Account is created automatically using booking information
    - Email is sent to the braiders for a booking appointment
    - SMS is sent to the braiders for a bookig appointment
    - The whatsapp contack and IG handle of braider is returned to client
3. Blog
    - Blog with title, body and images (with links to youtube videos if needed)
    - Comments and likes for a blog
4. Testimonials
    - Testimonials from Clients
    - Achievemens and certificates
5. Online Payment Platform
    - For approved appointments
    - For items bought from the e-store
6. E-Cormmerce
    - An e-store for hair accessories
    - And other fashion components

![How to Book Page](docs/images/How%20to%20Book.png "Booking Instruction")

<br>

## Technologies

The following technologies were used for this project
| Technology | Purpose | Documentation link |
|------------|------------|------------|
| FastAPI | we used Python FastAPI as the web framework | to be included |
| Mongodb | The distributed noSQL database for this site is MongoDB Atlas| To be included |
| Redis | Redis was used for efficient caching | To be included |
| Cloudfare R2 | Our site includes a gallery of images and videos, we used Cloudfare to store these dynamic contents | To be included |
| Pytest | For our robust unit and itegration test | To be updated |
| NextJS | To be updated | To be updated |
| Tailwind CSS | To be updated | To be updated |
| Shadcn UI | To be updated | To be updated |
| Playwright | To be updated | To be updated |
| Vi test | To be updated | To be updated |

<br>

## Folder Structure

```txt
.
├── app
│   ├── main.py
│   ├── src
│   │   ├── config
│   │   │   ├── __init__.py
│   │   ├── controllers
│   │   │   └── user
│   │   │       ├── create_user.py
│   │   │       ├── delete_user.py
│   │   │       ├── get_all_users.py
│   │   │       ├── get_user_by_email.py
│   │   │       ├── get_user_by_id.py
│   │   │       ├── get_user_by_phone_number.py
│   │   │       ├── __init__.py
│   │   │       └── update_user.py
│   │   ├── data
│   │   │   ├── __init__.py
│   │   │   └── user.py
│   │   ├── exceptions
│   │   │   ├── already_exists.py
│   │   │   ├── __init__.py
│   │   │   ├── not_found.py
│   │   ├── models
│   │   │   ├── blog.py
│   │   │   ├── comment.py
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   │   ├── __init__.cpython-312.pyc
│   │   │   │   └── user.cpython-312.pyc
│   │   │   └── user.py
│   │   ├── service
│   │   │   ├── __init__.py
│   │   │   └── user.py
│   │   ├── utils
│   │   │   ├── crypt.py
│   │   │   ├── __init__.py
│   │   └── web
│   │       ├── __init__.py
│   │       └── user.py
│   └── tests
│       └── test_user
│           ├── manual_test.py
│           ├── test.py
│           └── test_user_data.py
├── docs
│   └── images
│       ├── Book Service.png
│       ├── Features Section.png
│       ├── Hero Section.png
│       ├── How to Book.png
│       └── README.md
├── folder_tree.txt
├── LICENSE.md
├── poetry.lock
├── pyproject.toml
└── README.md
```

<br>

## Important Folders and Their Purpose

-   `docs` - This folder contains documentation for the api and the project
-   `tests` - This folder contains a comprehensive test suit for the project
-   `app` - The parent folder for the api
    -   `main.py` - This is the entry point for the project
    -   `src` - Parent folder for all source code
        -   `config` - Configures the api. Has things like database settings etc
        -   `models` - Models for all object in the api are stored here
            -   blog.py - The blog model
            -   comment.py - The comment model
            -   user.py - The user model
        -   `data` - Contains code that interact directly with the DB. It defines an asynchroneous interface for the database. and it does not validate/filter data
            -   user.py - Contains a class that performs all user operation on the database
        -   `service` - The code here runs on top of the `data` folder (it call the methods from there). It performs all the data filtering and routing
            -   user.py - middlemean between the data and the controllers. `controllers` make use of `data` via `service`
        -   `controllers` - This folder is one level below the web interface. it receives from the api routes in `web` and calls the required service
            -   user - This folder contains all the user controllers
                -   create_user.py - This file contains the controller for creating a user
                -   delete_user.py - This file contains the controller for deleting a user
                -   get_all_users.py - This file contains the controller for getting all users
                -   get_user_by_email.py - This file contains the controller for getting a user by email
                -   get_user_by_id.py - This file contains the controller for getting a user by id
                -   get_user_by_phone_number.py - This file contains the controller for getting a user by phone number
                -   update_user.py - This file contains the controller for updating a user
        -   `exceptions` - User defined exceptions used throughout the project
            -   already_exists.py - This file contains the exception for when a user already exists
            -   not_found.py - This file contains the exception for when a user is not found
        -   `utils` - Utility functions used throughout the project
            -   crypt.py - This file contains the functions for encrypting and decrypting data
        -   `web` - Web interface for the api (it defines all routes for handling requests)
            -   user.py - This file contains all the routes for the user

<br>

## Local Development

To run this project locally, follow the steps below

1. Clone the repository and `cd` into it

```bash
git clone https://github.com/VicTheM/4EvaBraids-backend.git
cd 4EvaBraids-backend
```

2. Install the dependencies using the command below

```bash
poetry install
```

3. Create a `.env` file in the root directory and add the following environment variables

```bash
DB_HOST=your_monogodb_host
DB_PORT=your_mongodb_port
DB_NAME_DEVELOPMENT=your_mongodb_database_name
DB_NAME_TEST=your_mongodb_database_name
DB_NAME_PRODUCTION=your_mongodb_database_name
SECRET_KEY=your_secret_key

# An enviroment variable called ENV will determine which database to use
# The test suit automatically sets this to test. Default is development
```

4. Run the project using the command below

```bash
# Make sure to start your mongodb server if you are running it locally
sudo systemctl start mongod

export PYTHONPATH=$PWD/app/src
poetry run uvicorn app.main:app --reload
```

<br>

## Running Tests

To run the tests, run the command below

```bash
poetry run pytest --cov=app
```

<br>

## Algorithms For Crucial Parts

{{ To be updated when code is ready }}

<br>

## Deployment

{{ To be updated after deploying site }}

<br>

## Contributing

Hi, we appreciate any contribution to this repository, kindly fork this repo, add your feature (or fixes) and create a pull request. You can start by implementing the [yet-to-be-implemented](#yet-to-be-implemented-features) above or check for any issue and solve it.

> [!TIP]
> You can also send a mail to us on [victorychibuike121@gmail.com](victorychibuike121@gmail.com)

<br>

## Important Links

1. [Google drive](https://drive.google.com/drive/folders/1nkLk7gpuJ2goUGwwKMx_iF3ZcW3887rJ?usp=sharing)
2. [Project pitch](https://docs.google.com/presentation/d/1FpoadYXboSWbsJNq1_Om3yOAnf_qRi40m4ICDwHJI_4/edit?usp=sharing)
3. Frontend Repository
