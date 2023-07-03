# TrendMicroAutomation
This repository is for any python automation I have written for Trend Micro's Vision One XDR platform.

So I've designed some automation to help get relevant data for Incident Response using the Trend Vision One XDR platform's API.
We'll start with EndpointActivityByUser.py, which is a python program that makes API calls querying the past half hour from runtime for events containing "endpointHostName: <user-input> and logonUser:*"
It'll repeat this query 48 times to equal an entire days worth of data, and then spit it out in an output.txt

UserActivityByEndpoint.py does the same thing, but instead queries "logonUser: <user-input> and endpointHostName:*"
This should give a good view of what machines a user has events on in the past 24 hours.


Now we have torgal.py, which takes arguments in the below syntax to execute the programs contained in the plugins folder below torgal.py itself

Currently supported arguments:
torgal.py host --hostname <hostname>
torgal.py user --username <username>
