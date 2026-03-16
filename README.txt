roey averbuch

# Roy Averbuch's project

The project is built in such a way that each service has children inside a class
And there is a main one that manages the system "manager"
The consumer receives a callback from the manager
And he passes the message received to him for further processing
If there was an error, he passes the error as above
I added pydantic validation
That checks if the fields exist
Two fields are added to messages that come from intel if they do not exist
The way the system works is that each message undergoes validation
If it passes, it is passed to the function that manages each message according to the topic it came from
If the intel has already been destroyed, it is not passed on
And every message from attack or damage affects what is written in intel
And is also saved to its own collection
I also added my own logger in addition to what we gave in the test that writes to the console