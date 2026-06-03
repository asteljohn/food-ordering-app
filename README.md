# Food Ordering App

## Project Overview

The Food Ordering App is a web-based application developed using Flask and SQLite. The system allows users to register, log in, browse food items, and place orders online. Administrators can manage food items and monitor orders through a dedicated admin dashboard.

The application is deployed on AWS EC2 using Docker and secured with HTTPS using SSL certificates.

---

## Features

### User Features

* User Registration
* User Login
* Browse Food Menu
* Place Orders
* Logout

### Admin Features

* Admin Login
* Add Food Items
* View Orders
* Manage Menu

### Security Features

* Password Hashing using bcrypt
* Session Management
* Rate Limiting using Flask-Limiter
* Security Headers
* HTTPS using SSL/TLS

### DevOps Features

* GitHub Version Control
* Docker Containerization
* GitHub Actions CI/CD
* Automated Backups using Cron Jobs

### Monitoring & Logging

* Application Logging (foodapp.log)
* Health Check Endpoint (/health)
* Metrics Endpoint (/metrics)
* CPU, Memory and Disk Monitoring using psutil

---

## Technology Stack

* Python
* Flask
* SQLite
* Docker
* GitHub
* GitHub Actions
* AWS EC2
* Nginx
* Certbot SSL
* DuckDNS
* bcrypt
* Flask-Limiter
* psutil

---

## Deployment Architecture

Users → DuckDNS Domain → HTTPS (SSL) → Nginx Reverse Proxy → Flask Application → SQLite Database

---

## Repository

GitHub Repository:
https://github.com/asteljohn/food-ordering-app

---

## Live Application

https://foodorderingapp.duckdns.org

---

## Backup Strategy

A cron job automatically executes backup.sh daily and creates compressed backups of the application.

---

## Monitoring

The application provides:

* /health endpoint
* /metrics endpoint
* Application log file (foodapp.log)

for monitoring application availability and server metrics.

---

## Author

Antony M.J
