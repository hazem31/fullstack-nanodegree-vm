# Logs Analysis

This project is a part of Udacity's Full Stack Nanodegree Program. In this project, I had to use my SQL database knowledge in order to extract various data from the database. I practiced interacting with a live database both from the command line and from your code. I have explored a large database with over a million rows.

In this project, I have used PostgreSQL database. My task was to create a reporting tool that prints out reports (in plain text) based on the data in the database. This reporting tool is a Python program using the psycopg2 module to connect to the database.

The database contains newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. Using that information, code will answer questions about the site's user activity.

The database includes three tables:

    -The authors table includes information about the authors of articles.
    -The articles table includes the articles themselves.
    -The log table includes one entry for each time a user has accessed the site.

## So what are we reporting, anyway?

Here are the questions the reporting tool should answer. The example answers given aren't the right ones, though!

1. What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.


2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.

3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser.

