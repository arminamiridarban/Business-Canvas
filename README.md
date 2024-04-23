# Digital Business Canvas

## Introduction:

Welcome to the Digital Business Canvas, an innovative web application designed to empower entrepreneurs and small businesses with a deeper understanding of their products and the market landscape. By leveraging sophisticated database models and extensive JavaScript code, this project offers a dynamic platform for creating and analyzing business canvases.

## Distinctiveness and Complexity:

This project boasts a robust architecture with multiple database models, including one-to-many, many-to-many, and distinct models, totaling to 11 different models. The extensive JavaScript code drives the creation of an online Business Canvas Creator, aiding users in comprehensively mapping out their business strategies. In addition, Most of the CSS used in the application is created by the developer and the app is completly responsive.

## Description:

### Main Page:

The main page provides users with a visual schema of the canvas, offering a quick overview of the canvas structure.
You have access to Login/Register section or Tutorial without creating an account but to use the application features, you need to create an account which is free.

### Create Canvas:

The heart of the application lies in the Create Canvas section, where users are prompted to input information about their products and market positioning. A login/register mechanism ensures data security and personalized canvas creation. While this section primarily facilitates the creation of canvases, users can also modify, delete, or add to existing canvases.
In this section, if user needs to add another data which prompted previously, they can use expand button to add another data.

### Build Canvas:

In the Build Canvas section, users can view all their created canvases and make real-time updates using a full CRUD (Create, Read, Update, Delete) functionality. Leveraging JavaScript and fetch methods, users can seamlessly interact with the backend without page refreshes, enhancing user experience and efficiency.

### Tutorial:

The Tutorial section serves as a comprehensive guide to understanding the business canvas concept. Users can explore an interactive canvas model with detailed descriptions of each section, gaining valuable insights into business strategy formulation.

### Login/Register:

In this section, users are able to make their very own account or login to their previous built account. JavaScript handles the switch between the Login and Register section.

## Project Files:

- **manage.py**: Django application responsible for serving the website and managing the Django framework.
- **templates/**: Contains HTML templates for various sections of the website.
- **static/**: Houses CSS, images, and JavaScript files for styling and interactivity.
- **db.sqlite3**: The database storing dynamic information, ensuring real-time updates and responsiveness.

## Running the App:

To run the Digital Business Canvas app in VSCode:

1. Navigate to your digitalbusiness directory in VSCode.
2. Ensure you have the required packages installed (use `pip3 install django`).
3. Set up your Django environment variables by running `python3 manage.py runserver`.
4. Access the local server address provided (e.g., http://127.0.0.1:8000/) in your web browser to explore the app.
5. Dive into your personalized Business Canvas application, and unleash your entrepreneurial potential!
