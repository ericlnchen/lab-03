# Lab 3
[Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) this repo and clone it to your machine to get started!

## Team Members
- Eric Chen

## Lab Question Answers

Answer for Question 1:  

REST APIs scale efficiently because REST optimizes client-server interactions. Using REST the server completes every client request independently of all previous requests. Hence, the server does not have to retain past client request information, which reduces load. Additionally REST has 
well-managed caching that can partially or completely eliminates some client-server interactions. All these features help increase the scalability REST.  

Answer for Question 2:  

According to the list of resources given by the AWS article. Our mail server contains 3 methods: GET, POST, DELETE. GET corresponds to
the functions for getting an inbox, a sent-box, and a specific mail. POST corresponds to the add/send mail method. DELETE corresponds to the delete_mail method.  

Answer for Question 3:  

The common REST method that is not used our mail server is PUT. Since PUT is defined to update existing resources on the server, by using PUT, one extension could allowing the client to modify a specific mail entry.  

Answer for Question 4:  

API keys are used to identify and authenticate the client calling RESTFUL APIs. In addition, API keys allow the API provider to limit or control the usage of the client. API key are also very important security because the key acts as a unique identifier and secret token that verifies whether ot not the client has permission to access the data requested in the API call.

weather.py contains an additional API call for the bonus points!