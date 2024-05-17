# Agri-Management System

Agri-Management System is a web application built with Flask that aims to provide a comprehensive platform for farmers and agricultural authorities to manage various aspects of agricultural operations. The application offers features such as user registration, profile management, land and cultivation details, insurance and compensation applications, subsidy management, soil testing, product listing, and administrative functionalities.

## Features

- User Registration and Authentication
- User Profile Management
- Land and Cultivation Details
- Insurance Application and Approval
- Compensation Application and Approval
- Subsidy Management
- Soil Testing
- Product Listing and Subsidy Application
- Admin Panel
  - User Management
  - Insurance and Compensation Approval
  - Notification Management
  - Product Management
  - Subsidy Approval

## Technologies Used

- Python
- Flask
- SQLite (SQLAlchemy ORM)
- HTML/CSS/JavaScript
- Docker

## Installation

1. Clone the repository:

```
git clone https://github.com/your-repo/agri-management-system.git
```

2. Navigate to the project directory:

```
cd agri-management-system
```

3. Install the required dependencies:

```
pip install -r requirements.txt
```

4. Set up the database:

```
python
from app import db
db.create_all()
exit()
```

5. Run the application:

```
python app.py
```

The application will be accessible at `http://localhost:5000`.

## Docker

This project includes a Dockerfile for easy deployment using Docker. To build and run the Docker image, follow these steps:

1. Build the Docker image:

```
docker build -t agri-management-system .
```

2. Run the Docker container:

```
docker run -p 5000:5000 agri-management-system
```

The application will be accessible at `http://localhost:5000`.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
