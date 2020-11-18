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
``` docker-compose exec web python manage.py migrate```

## Setting Up The Aplication
Assuming that you have already the datasets downloaded in your computer, follow the steps to load the data and them be able the access it in the API.

1. Copying the datasets to the container:

```docker cp <local_path> dorothy-image-service_web_1:/imagesrep```

Example: docker cp "C:\Users\Desktop\MontgomerySet\" dorothy-image-service_web_1:\imagesrep"

For the curent datasets, Indian, Chinese and Montgomery, the paths should end in IndiaDataSet, ChinaSet_AllFiles or MontgomerySet, which are the usual folder names for those datasets. Depending on the size of the dataset, this might take a few minutes.

2. Enter the image service from inside the container:

```docker exec -it dorothy-image-service_web_1 bash```
```cd webserver/django```

3. Perform the load command:

```python manage.py load <dataset_name> <container_dataset_path>```

Example: python manage.py load montgomery /imagesrep/MontgomerySet

The container dataset path can be rewritten as /imagesrep/<dataset_folder_name>, as it should always start with "/imagesrep/".
