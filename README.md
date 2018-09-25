# Fast-Food-Fast

Fast-Food-Fast is a food delivery service app for a restaurant.

[![Build Status](https://travis-ci.com/mubstimor/fast-food-fast.svg?branch=api)](https://travis-ci.com/mubstimor/fast-food-fast)  [![Coverage Status](https://coveralls.io/repos/github/mubstimor/fast-food-fast/badge.svg?branch=api&service=github)](https://coveralls.io/github/mubstimor/fast-food-fast?branch=api&service=github)  [![Code Climate](https://codeclimate.com/github/codeclimate/codeclimate/badges/gpa.svg)](https://codeclimate.com/github/mubstimor/fast-food-fast)  [![Test Coverage](https://api.codeclimate.com/v1/badges/24230611fce8192b6279/test_coverage)](https://codeclimate.com/github/mubstimor/fast-food-fast/test_coverage)

## Required Features



### Template Link

[Home Page](https://mubstimor.github.io/fast-food-fast/ui/index.html)

### Heroku Link

[API Home Page](https://tims-fast-food.herokuapp.com/)

## Supported Functionality

## Orders
```
Get /orders
GET /orders/<orderId>

* The Admin user should be able to do the following: See a list of orders,Accept and decline orders and Mark orders as completed
PUT /orders/<orderId>

* A user should be able to order for food
POST /orders
```

## Users
```
Get /users
GET /users/<userId>
PUT /users/<userId>
PUT /users/orders/<order_id>

* Users can create an account and log in
POST /users
POST /users/login

* A user should be able to see a history of ordered food
GET /users/myorders/<user_id>
```

## Still to implement
```
* The admin should be able to add,edit or delete the fast-food items
* The admin should be able to see a list of fast-food items
```