# TrendMicroAutomation
This repository is for any python automation I have written for Trend Micro's Vision One XDR platform.

So I've designed some automation to help get relevant data for Incident Response using the Trend Vision One XDR platform's API.
We'll start with EndpointActivityByUser.py, which is a python program that makes API calls querying the past half hour from runtime for events containing "endpointHostName: <user-input> and logonUser:*"
It'll repeat this query 48 times to equal an entire days worth of data, and then spit it out in an output.txt

UserActivityByEndpoint.py does the same thing, but instead queries "logonUser: <user-input> and endpointHostName:*"
This should give a good view of what machines a user has events on in the past 24 hours.

Quarantine.py quarantines emails given an EmailID as a string. It also supports message ids in a .txt file, one entry per new line. It'll sleep for 5 seconds before moving on to the next request to avoid rate limits.

Quarantine.py now reports it's output to a response.log for troubleshooting purposes.

Now we have torgal.py, which takes arguments in the below syntax to execute the programs contained in the plugins folder below torgal.py itself

Currently supported arguments:

torgal.py host --hostname [hostname]

torgal.py user --username [username]

torgal.py mail --messageid "`<example@example.example.example.outlook.com>`"

torgal.py mail -messageidslist /path/to/file 
