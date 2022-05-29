# lloyds_openweatherapi_task

* Openstreetmap api integration in python allows the user to query temperature, weather
for a given city.

* Potential use case: daily app reminder of the current temperature before a lloyds employee goes to work
so that they can be prepared e.g. bring an umbrella if rain is generated as the output for London
or whichever city they are in. 

* If the city does not exist (not found), an appropriate error is returned to the user

* In order to run the code, the user must create a file called api_secret.ini (emphasis on not storing this in version control software for security reasons) with the content:
> ; api_secret.ini
>  [openweathermap]
>  owm_api_key=<api-key>

* This gives the user access to the openweather api.