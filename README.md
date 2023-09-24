### Hexlet tests and linter status:
[![Actions Status](https://github.com/Troshchk/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/Troshchk/python-project-83/actions)

### Package tests, linter and test coverage status:
[![Actions Status](https://github.com/Troshchk/python-project-83/workflows/page_analyzer/badge.svg)](https://github.com/Troshchk/python-project-83/actions)

[![Maintainability](https://api.codeclimate.com/v1/badges/2939635f88987b4d26d8/maintainability)](https://codeclimate.com/github/Troshchk/python-project-83/maintainability)

[![Test Coverage](https://api.codeclimate.com/v1/badges/2939635f88987b4d26d8/test_coverage)](https://codeclimate.com/github/Troshchk/python-project-83/test_coverage)

## Service Link
You can access the service here: [Page Analyzer](https://python-project-83-cqa5.onrender.com/).

Note: This web application is hosted on Render using a free tier, and the instance may spin down after 15 minutes of inactivity. When a new request is received, the instance restarts, which may result in a slower initial response.

## Description
Page Analyzer is a web application designed to analyze web pages for [SEO](https://en.wikipedia.org/wiki/Search_engine_optimization) relevance, similar to the functionality offered by PageSpeed Insights.

On the homepage of the app, you can input a web address. After validating that it's a valid URL, it will be added to the database.

Valid URLs should not exceed 256 characters and should be in the correct format. Any additional string, such as a query string, will be omitted.

You can view a list of all URLs stored in the database along with the results of the latest analysis for each URL. Further details about the analysis will be described later.

Additionally, you can access detailed information for a specific URL. This information includes the URL's ID in the database, the URL itself, and the date it was added to the database. Next to the URL information, you'll find details about the SEO analysis, including the analysis ID, response status code, h1, title, description, and the date of the analysis.

To initiate an analysis, you can use the provided blue button. This button sends a request to the specified URL and parses the response to gather SEO-related data. Note that responses with errors are not added to the database.

## Technical Details
### Application
Page Analyzer is a comprehensive web application built using the Flask framework. It adheres to the principles of modern web development based on the MVC (Model-View-Controller) architecture. This includes handling routing, request handling, templating, and interaction with the database.

### Database
This project utilizes PostgreSQL as its database system. It comprises two tables: "urls" and "url_checks" to satisfy the requirements for the third normal form in relational databases. SQL queries against the database are performed using the psycopg2 library. The database for this application is hosted on [Render](https://render.com/).

### SEO-Related Data
The analysis of each URL involves a request and response interaction. A request is sent to the specified URL, and the response is parsed using the [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) package to extract SEO-related data.

### Frontend
For visual design, this project employs Bootstrap and its components to create an appealing user interface.

### Deployment
The project uses an automated deployment approach via the [Render](https://render.com/) service, a hosting platform operating on a Platform-as-a-Service (PaaS) model. [Render](https://render.com/) manages the underlying infrastructure.

### CI/CD
To maintain code quality, a GitHub workflow named [page_analyzer](https://github.com/Troshchk/python-project-83/actions/workflows/app.yml) has been incorporated into the project. This workflow automates the testing of code changes. During the setup of the workflow, a database for testing purposes is created, populated with data before each test, and cleaned after each test to ensure the integrity of each testing session.





