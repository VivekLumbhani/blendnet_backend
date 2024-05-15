﻿# blendnet_backend

# Django Server Setup Guide

This guide will walk you through the process of setting up and running a Django server with MySQL database. Follow the steps below to get started.

## Prerequisites
- Python installed on your system
- MySQL server installed and running
- MySQL client library for Python (you can install it via pip)

## Installation
1. Clone the repository:

2. Navigate to the project directory:

2. Navigate to the project directory:

## Activate Virtual Environment
1. Navigate to the `Scripts` directory inside the `env` folder:
2. Activate the virtual environment:
- On Windows:
  ```
  activate
  ```
- On macOS and Linux:
  ```
  source activate
  ```

## Install Dependencies
1. Navigate back to the project directory:
2. Install dependencies from `requirements.txt`:


python manage.py migrate


python manage.py runserver
