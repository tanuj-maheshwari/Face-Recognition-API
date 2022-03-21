# Face Recognition API

> Submitter name: Tanuj Maheshwari
>
> Roll No.: 2019CSB1125
>
> Course: CS305 (Software Engineering)

Python based API service that performs "facial search" on a database of images.


## What does this program do?

This is a Python API, built using [FastAPI](https://fastapi.tiangolo.com/), that can be used to perform "facial search" on images stored on the server in a Relational Database (specifically MySQL) to get the top-k matches for all the faces in an input image.

The application uses [ageitgey's facial recognition library](https://github.com/ageitgey/face_recognition) for facial matching.


## A description of how this program works (i.e. its logic)

### Multi-Processing

As the processing of images in batch upload is computationally a very heavy task, multiprocessing has been used.

The parent process creates a child process pool of 8 processes using the `multiprocessing.Pool()` Python API. Similar multiprocessing has also been used to retrieve top k image matches (which is further optimsed using min-heap instead of simple sorting).

The server runs on `gunicorn` (which is a wrapper for uvicorn), which supports a multithreaded server. Hence, simultaneous calls can be made to the endpoints. 

> In the command below, 4 workers have been used. Hence, upto 4 processes can run concurently (other processes will be queued until the outstanding requests are completed).

### SOLID principles applied

The application follows SOLID principles so that further extension is easy and intutive. Such principles have been used throughout the assignment, and some of the prime examples are explained below :-

#### Database

The database has been implemented through 4 classes :-

* `DatabaseCRUD` -> Contains an interface for CRUD operations (`create`, `select`, `update`, `delete`, `insert`) on any generic database (such as PostgreSQL, MySQL, etc).

* `MySQLDatabase` -> An implementation of `DatabaseCRUD` class for MySQL.

* `ImageDatabase` -> An interface for Image related operations on database. **This is separated from `DatabaseCRUD` so that low level abstractions are separaed from high level logic**.

* `MySQLImageDatabase` -> An implementation of `ImageDatabase` that extends `MySQLDatabase`.

#### Image

Image related operations are done using 4 classes :-

* `Image` -> An interface for representing images. This is done so that functions like `getMetadata()` can support various implementations.

* `AGTImage` -> An implementation of `Image` class.

* `ImageEncoder` -> An interface that defines functions for the encoder used for face recognition. This is done so that multiple face recognition libraries could be used. It is not implemented inside `Image` class because this makes every class have single functionality.

* `AGTEncoder` -> An implementation of `ImageEncoder` class that uses [ageitgey's facial recognition library](https://github.com/ageitgey/face_recognition) for facial matching.

#### API

The API functions are implemnted using two classes :-

* `API` -> An interface that defines API functions.

* `AGTAPI` -> An implementation of `API` class. This composes a `Database` and an `ImageEncoder` object each to implement the functioanlities.

### API endpoints

- `"/search_faces/"` -> A `POST` request to this endpoint with an image containing one or more faces return a list of top matches for all the faces in the image. It takes `k` and `tolerance` as parameters:

    - `k` - The *maximum* number of matches to be returned for each face in the image
    - `tolerance` - The value of tolerance for each face matching. **Smaller value implies stricter matching**. The most optimal performance is at tolerance = 0.6

    > Only those images will be sent whose euclidean distance from the image posted. In case the tolerance value limits the number of images to less than k, less than k images will be sent.

    > The endpoint takes `k` and `tolerance` as query parameters. For example, a `POST` request to **http://127.0.0.1:8000/search_faces/?k=5&tolerance=0.6/** will have `k` as 5 and `tolerance` as 0.6

- `"/add_face/"` -> A `POST` request to this endpoint with an image containing a face will add the face to the database (and returns an appropriate response).

    > * In case the image contains no face, an appropriate response will be sent.
    > * In case the image contains more than one face, only one of the faces will be inserted in the dataabase.

- `"/add_faces_in_bulk/"` -> A `POST` request to this endpoint with a zip file containing images (with faces) will add all the faces in the images to the database. Returns the number of faces inserted in the database.

    > * **The .zip file, when unzipped must give only the images to be added, and not any other folder/zipped files**
    > * In case an image doesn't contain a face, it won't be inserted.
    > * Only one face per image will be inserted in the database.

- `"/get_face_info/"` -> A `POST` request to this endpoint with `image_id` (and `api_key`) as form data will return the image metadata stored in the database (returns an appropriate message if no query_id).


## How to compile and run this program

### Prerequisites and Setup

* The application **can only run on Linux based systems**, as the face_recognition API uses `dlib` and `cmake` internally.

* This application is built in python using FastAPI, hence python 3.6+ (along with pip3) is required.

* The application uses `MySQL` as the database, hence MySQL must be installed on the system.

    1. After installation of MySQL, configure it using the following command :-

        ```
        sudo mysql_secure_installation
        ```

    2. Then, open an instance of MySQL on the terminal using `sudo mysql -u root -p mysql`, and then enter the following command :-

        ```
        ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '<new_password>';
        ```
        > Replace \<new_password> with a new password.

    3. Then, create a database where the `IMAGE_DATASET` table will be stored.

        > Make sure that there is no table in the database before running the server and/or tests.

* To install `dlib` and `cmake`, follow the instructions on [ageitgey's library GitHub page](https://github.com/ageitgey/face_recognition).

* Then, install all the dependencies (list given below)

    * face_recognition
    * 'fastapi[all]'
    * 'uvicorn[standard]'
    * gunicorn
    * mysql-connector-python-rf
    * pytest
    * coverage

* Finally, setup the `config.json` file in the same directory as that of `app.py`. This file contains the details for connecting to the MySQL database. A sample `config.json` is provided with the project.

    > Make sure to use the password setup using the `ALTER USER` command.


### To run the server

To run the server, open a terminal in the directory and run :-

```
python3 -m gunicorn app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000
```

Kill the server by pressing `Ctrl` + `C`.

> **NOTE**
>
> * It might be possible that MySQL server is failing to connect. The issue can be solved by **restarting the MySQL server** using :-
>
>   ```
>   sudo service mysql restart
>   ```
>
> * `gunicorn` might not be able to connect to the given port (as either there might already be some processes running on the port, or some other gunicorn forked processes might be active). To solve the issue, you can do the following :-
>
>   * **Kill all the running gunicorn services**, using :-
>
>       ```
>       killall gunicorn
>       ```
>
>   * **Kill the processes running on the port**, using :-
>
>       ```
>       sudo kill `sudo lsof -t -i:8000`
>       ```
>       > Make sure not to kill processes on well defined ports (such as port 3306 where MySQL runs)
>
>   * **Change the port where the app is to be deployed** in the `gunicorn` command


### To run pytests

To run the pytests provided within the implementation, open a terminal in the folder location and run :-

```
python3 -m pytest
```

> **NOTE**: To successfully run the tests (without failure), the `IMAGE_DATASET` table should not exist in the database. If it does, **drop the table and then run the tests**.

> **SIDENOTES** :-
>
> 1. To upload the LFW dataset, uncomment line 13, 14 and 16 in `test_app.py`, and comment line 15. Also download the LFW dataset, a copy of which is available [here](https://drive.google.com/file/d/1sXEXDnNGSJZ4CPecfQ6ka2BRUtFGTPRH/view?usp=sharing), and place it inside the `test_images` folder. (Note that the API will not work for the original LFW downloaded file because it contains a .tar file inside of a .zip file)
>
>       > Note that the test might fail, as the number of images inserted depends from system to system. But all the well defined images will be inserted in the database.
>
> 2. To test an image in LFW dataset, uncoment line 36 and 39, and comment line 35 and 38, **after ensuring that the LFW dataset is already inserted in the dataset**


### To generate code coverage report

Code coverage is implemented using `Coverage.py` module. To generate coverage report, do the follwoing steps :-

1. Run the pytest using `coverage run`
    ```
    python3 -m coverage run --source=. -m pytest
    ```

2. Generate coverage report
    ```
    python3 -m coverage report
    ```

3. To generate detailed coverage report with hit/miss sections, run :-
    ```
    python3 -m coverage html
    ```


## Snapshot of a sample run

### Pytest

Below is a snapshot of passed pytest tests.

![Pytest Report](./sample_run/pytest.png?raw=true "Pytest Report")

### Coverage report

The unit tests provided cover 87% of the code. Below is a snapshot of the code coverage report.

![Coverage Report](./sample_run/coverage.png?raw=true "Coverage Report")
