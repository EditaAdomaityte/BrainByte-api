# BrainByte API

A Django-based backend API for BrainByte, an interactive quiz application designed for web developers to test and improve their knowledge.

## BrainByte Client Link:
https://github.com/EditaAdomaityte/BrainByte-client

## Features
<p>
• RESTful API: Resource-specific endpoints with appropriate CRUD operations<br>
• Authentication System: JWT token-based authentication for secure user access<br>
• Quiz Generation: Dynamically generate quizzes based on categories and question count<br>
• Result Tracking: Store and retrieve user quiz results<br>
• Question Management: API endpoints for creating, updating, and deleting questions<br>
• User Contributions: System for users to submit new questions<br>
• Admin Controls: Special endpoints for admin functionality<br>
• User Role Management: API for managing user permissions and roles<br>
• Database Integration: Efficient SQLite3 storage for all application data<br>
</p>

### ERD

<img src="./src/pages/ERD.png" alt="">

## Installation

### 1. Prerequisites

Before you begin, ensure you have the following installed:
Python (v3.8 or higher):
https://www.python.org/downloads/

### 2. Clone the repository
In your terminal run:
```sh
git clone git@github.com:EditaAdomaityte/BrainByte-api.git
cd BrainByte-api
```
### 3.Install dependencies
In your terminal run:
```sh
pipenv install
```

### 4. Set up a virtual environment
In your terminal run:
```sh
pipenv shell
```

### 5. Apply migrations
In your terminal run:
```sh
./seed_database.sh
```
### 6. Run the debugger in VSCode.
 Once running, API is available at: http://localhost:8000

## Contributing
<p> 
Fork the repository<br>
Create your feature branch (git checkout -b feature/amazing-feature)<br>
Commit your changes (git commit -m 'Add some amazing feature')<br>
Push to the branch (git push origin feature/amazing-feature)<br>
Open a Pull Request<br>
</p>

## Technologies Used
![Python](https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white) 
![Django](https://img.shields.io/badge/django%20-%23092E20.svg?&style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?&style=for-the-badge&logo=sqlite&logoColor=white)


#### Created by Edita Adomaityte
<a href="https://github.com/EditaAdomaityte" target="_blank"><img src="https://img.shields.io/badge/github%20-%23121011.svg?&style=for-the-badge&logo=github&logoColor=white" alt="Edita Adomaityte GitHub" style="height: auto !important;width: auto !important;" /></a> <a href="https://linkedin.com/in/edita-adomaityte" target="_blank"><img src="https://img.shields.io/badge/linkedin%20-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white" alt="Edita Adomaityte LinkedIn" style="height: auto !important;width: auto !important;" /></a>
