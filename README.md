# Digital Business Canvas

## Introduction

The Digital Business Canvas is a sophisticated web application aimed at helping entrepreneurs and small businesses strategically map out their business models. Unlike typical business tools, this application integrates advanced database interactions and dynamic web features to provide a comprehensive platform for business planning and analysis.

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
  - `styles.css`: Custom styles.
  - `script.js`: Core JavaScript functions for dynamic interactions.
- `templates/`: HTML files for rendering website content.
  - `base.html`: Base template including headers and footers.
  - `index.html`: Main canvas creation interface.

## How to Run the Application

1. Clone the repository to your local machine.
2. Install required Python packages with `pip3 install django` and `pip install python3`.
3. Run `python3 manage.py makemigrations` and `python3 manage.py migrate` to set up the database.
4. Start the server using `python3 manage.py runserver`.
5. Open `http://127.0.0.1:8000/` in your web browser to access the application.

## Additional Information

- The application uses Django’s session framework for managing user sessions and data.
- If encountering issues with static files not loading, ensure Django is configured to serve static files appropriately in your development environment.
