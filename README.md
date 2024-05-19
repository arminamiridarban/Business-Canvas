# Digital Business Canvas

## Introduction

The Digital Business Canvas is a sophisticated web application aimed at helping entrepreneurs and small businesses strategically map out their business models. Unlike typical business tools, this application integrates advanced database interactions and dynamic web features to provide a comprehensive platform for business planning and analysis. By using this web-application, user would be allowed to map all his/her business and have a better understanding of each layer of their project. Moreover, the user is allowed to map their adverseries in the market and understand the underlining and briliance of their project among their opponents.

## Distinctiveness and Complexity

Unlike typical project templates that revolve around straightforward CRUD operations or simple data displays, this project integrates complex database relationships and real-time data manipulation using AJAX. The application features:
- An intricate model structure with 11 different Django models, including complex relationships like many-to-many links for user collaboration on projects.
- Advanced JavaScript functionalities for dynamic content updates without reloading the page, enhancing user interaction and efficiency.
- Custom-built CSS for responsiveness, ensuring the application is fully functional on both desktop and mobile devices.

## Description of Project Files

- `manage.py`: Entry point for Django commands.
- `db.sqlite3`: Database file containing all application data.
- `requirements.txt`: Lists all Python packages needed to run the application.
- `static/`: Contains CSS, JavaScript, and image files.
  - `picture`: The static pictures of the website is located in this folder.
  - `fontawesome`: This is the Font Awesome Library for icons.
  - `styles.css`: Custom styles.
  - `script.js`: Core JavaScript functions for dynamic interactions.
- `templates/`: HTML files for rendering website content.
  - `base.html`: Base template including headers and footers.
  - `index.html`: Main canvas creation interface.

## How to Run the Application

1. Clone the repository to your local machine.
2. Install required Python packages with `pip3 install django` and `pip install python3`.Alternatively, you can install all dependencies at once by running `pip3 install -r requirements.txt` in your terminal.
3. Run `python3 manage.py makemigrations` and `python3 manage.py migrate` to set up the database.
4. Start the server using `python3 manage.py runserver`.
5. Open `http://127.0.0.1:8000/` in your web browser to access the application.

## Usage

- Tutorial: To user this application, you are free to use Tutorial tab, on the right-top corner of the screen in the nav bar. In the tutorial section, you will have a clear understanding of how to use each section and what are the sections. By clicking of each item, the section expands ith more detail and the question you need to ask your self to fill each section. 
- Login/Register: In order to use the application, you need to Login/Register. you can navigate to this section which is located in the nav bar and easily by providing a username and password, you would be allowed to use all the features of the app.
- Create Business Canvas: In this section, you can make your Business Canvas. Feel free to first use toturial of the app and then loop through each part of this section.
- Your Canvas: This is the section that you can see all the models which you've built before. you have full access to Edit, Add, Remove and update each section of the Canvas.
- Compare Canvas: This section, allowes user to compare Business Canvas of their own projects with other projects. If user is not logged in, they can benefit from comparing all current saved canvas.

## Additional Information

- The application uses Django’s session framework for managing user sessions and data.
- If encountering issues with static files not loading, ensure Django is configured to serve static files appropriately in your development environment.
