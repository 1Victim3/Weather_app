# Weather_app
TechAssesment
Weather_app
TechAssesment

This is a simple Django-based weather app that fetches and displays the current weather for a city provided by the user.

Prerequisites
Make sure you have the following installed on your machine:

Python 3.x or higher
pip (Python package installer)
Setup

1. Clone the repository: Clone the repository to your local machine using the following command: ->
git clone

2. cd weather-app

3. Create a virtual environment: 
->venv\Scripts\activate (for windows) 
->source venv/bin/activate ( For Macos)

4. Install the required dependencies: 
pip install -r requirements.txt

5. Apply database migrations: 
python manage.py migrate

6. Start the development server: 
python manage.py runserver

NOTE 1: ## Get Your OpenWeatherMap API Key

To use this weather app, you will need an API key from OpenWeatherMap.

1. Go to the OpenWeatherMap website.
2. Sign up for a free account if you don’t already have one.
3. Once logged in, navigate to the "API keys" section of your account dashboard.
4. Generate a new API key (if you haven't done so already).
5. Replace the API_KEY file in your project with the generated API key.
6. Now you can fetch the weather data using your personal API key.


NOTE 2:

I am using One more Api key of Timezone db for fetching the timezone of the particular City
1. Go to this page and get your account started https://timezonedb.com/
2. You will get the API key directly
3. If it did not work check your mail for activation
4. GEt the key and store it in the views section Function with comment of Timezone Db api key
