# FeeCalculatorAPI

This code produces a web application exposing an API that returns a fee for a given loan amount and repayment period. FastAPI, the web framework for building APIs with Python was used, along with PyTest for producing a corresponding test suite. These prerequisites can be installed with the following: 

`pip3 install fastapi[all] pytest` 

The application can be started by using the following command from within the root directory: 

`uvicorn main:app --reload` 

All tests can be run by using the following command from within the root directory:

`pytest` 

Development environment: 
 - OS: Ubuntu 20.04 
 - Python version: Python 3.8.5 
