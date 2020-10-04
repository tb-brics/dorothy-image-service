# Dorothy-image-service
Web service for managing x-ray databases,
    
## Requirements
 You must have Docker Desktop installed to run this application in your computer.
        
## Webserver
The image service builds the data base  that will be filled with the data from multiple datasets, and them rearrange and display them to users in a more accessible way.
        
## Running the Webservice
After cloning this repository, via command line, cd into the project root folder and start the containers by running:
``` cd dorothy-image-service ```
``` docker compose up ```

## Setting Up The Aplication
After loading the web server and the DB server for the very first time, you must create the project related database structure and a django superuser for the admin site.

From your terminal/DOS/Powershell window, connect to the web server by typing:

```docker container exec -it dorothy_web_1 bash```

Once inside the running container, type the commands bellow to create the database structure and create a DJango superuser to have access to the admin page.

