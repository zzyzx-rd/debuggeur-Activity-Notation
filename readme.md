##Intro

This module is an incomplete module of ```auto testing``` for the serpico app.
It is focused today on the grading functionality, and offer the possibility to create and grade activities, with limits.

Because of the complexity of the creation of activity in the app, you must only use the proposed function, and nothing else,
other wise the request will be incorrect.
## The connection/creation of a session
To work with the app, you need to be connected, and to have the sessions cookies set correctly.
To do this you must use a ```SerpicoSession```, with the  ```__init__``` function (see the documentation for usage).
A session must be used to create only one activity, otherwise there might be some issues.
## Create a activity
To create an activity, start with creating a DefaultData instance. It will provide the data for the different requests. 

   