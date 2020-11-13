# Dorothy-image-service
X-ray Image web service for managing x-ray databases,exporting the TB tagged images for machine learning related activities.
    
## Requirements
 You must have Docker Desktop installed to run this application in your computer.
        
## Webserver
The image service builds the data base  that will be filled with the data from multiple datasets, and them rearrange and display them to users in a more accessible way.
        
## Running the Web Service
Once inside the running container, type the commands bellow to create the database structure and create a Django superuser to have access to the admin page. After cloning this repository, via command line, cd into the project root folder and start the containers by running:

``` cd dorothy-image-service\webserver\django ```
     ```docker-compose up -d```
``` docker-compose exec dorothy-image-service_web_1 python manage.py migrate```

## Setting Up The Aplication
After loading the web server and the DB server for the very first time, you must create the project related database structure and a django superuser for the admin site.

1. From your terminal/DOS/Powershell window, connect to the web server by typing:

```docker cp <path_local> dorothy-image-service_web_1:/imagesrep```

Example: docker cp "C:\Users\Desktop\Maria\Project\MontgomerySet\Dorothy-image-service_web:\imagesrep"

For the curent datasets, Indian, Chinese and Montgomery the paths should end in IndiaDataSet, ChinaSet_AllFiles or MontgomerySet, which are the usual folder names for the those datasets. Depending on the size of the dataset, this might can take a few minutes.

2. Enter the image_service from inside the container:

```docker exec -it dorothy-image-service_web_1 bash```

3. Perform the load command:

```python manage.py load<dataset_name> <container_dataset_name>```

Example: python manage.py load montgomery/imagesrep/MontgomerySet

The inside container dataset_path can be rewritten as /imagesrep/<dataset_folder_name>.






