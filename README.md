# Mobile, Web, API Test Automation

A universal automation framework to handle mobile testing, web testing, api testing in a single powerful python package with capabilities like device farming.

## Features

- Web automation
- API automation
- Mobile automation
- Device farming
- ChatGpt integration
- Allure docker service integration

## Prerequisites
 - knowledge of appium
 - knowledge of selenium
 - knowledge of python
 - knowledge of api testing

## Installation

There are two ways in which the framework can be utilised:
- Build the package and install it to current working directory
- Or, utilise the framework as is by creating a testing layer

### Steps:
- **Prep the system:**
    - [Install docker](https://www.docker.com/products/docker-desktop/)
        - [Windows installation](https://docs.docker.com/desktop/install/windows-install/)
        - [Linux installation](https://docs.docker.com/desktop/install/linux-install/)
        - [Mac installation](https://docs.docker.com/desktop/install/mac-install/)
    - [Install appium](https://appium.io/downloads.html)
    - [Install appium inspector](https://github.com/appium/appium-inspector/releases)
    - [Install android studio](https://developer.android.com/studio)
        - cli tools and sdkmanager need to be properly installed and configured, as in the later part these are required in automatic creation of emulators for testing using device farming
        - avdmanager, sdkmanager command availability in the terminal/cmd/powershell
    - [Install xcode](https://apps.apple.com/us/app/xcode/id497799835?mt=12) - **Optional - applicable only to mac device users**
    - [Download python 3.11](https://www.python.org/downloads/release/python-3110/), **minimum requirement >= 3.11**
    - Install pipenv as, it is used as a defacto for the package manager
        ```bash
        pip install pipenv
        Note: based on the python installation or configuration, the keyword for pip can be either pip/pip3
        ```
- **Prep project:**
    - There is an inbuilt device farming capability and for this we need to execute below command
        - The below command invokes two dashboards and two databases to manage device farming activities
            - RabbitMQ 
                - username: admin
                - password: admin123
                - [url](http://localhost:15672/)
            - Mongo express
                - [url](http://localhost:8081/)
    ```bash
    sudo docker compose -f docker-compose-device-farm.yml up --build
    -or-
    sudo docker compose -f docker-compose-device-farm.yml up -d --build
    ```
    - Once the docker containers are up, next thing is to prep the mongodb and add few data so that it starts working
        - Create a database called **appium_device_stats**
        - In the database which has been created, create two collections
            - device_stats
                - Holds data pertaining to device availability
            - device_sessions
                - Holds data pertaining to device sessions
    - Now the MongoDb and RabbitMQ are configured, let's head further steps which lead us to completion
    - Install project dependencies
        ```bash
        pipenv run make install
        ``` 
    - Invoke celery, this is required for device farming to work
        ```bash
        pipenv run celery -A uaf.device_farming.device_tasks worker -B -E -O fair --loglevel=INFO
        ```
    - Build the package - **Optional**
        ```bash
        pipenv run make build
        ```
    - Install the package to current pipenv package manager - **Optional**
        ```bash
        pipenv run make install-package
        ```
        - Note: Once executed, all the tests should pass, otherwise please correct the mistakes and proceed further
    - To visualise the report through allure docker service, docker containers have to be invoked. Use the below commands for the same
        ```
        sudo docker compose -f  docker-compose-report.yml up -d --build
        ```
    Now the project setup is done, lets proceed to next step

## Encrypt/decrypt sensitive information
- Currently, the project hosts sensitive data, which is encrypted using in house encryption using cryptography lib and since the file is encrypted and will remain encrypted indefinetly. Below is the template that needs to be followed for the same, at least initially to make the scripts and the project work. Later it can be modified according to the taste of individuals/ teams
    ```
    info:
        name: Common

    ports:
        appipum_service_min_port_band: <min_port_number>
        appium_service_max_port_band: <max_port_number>

    appium:
        appium_base_url_local: http://localhost:${port}/wd/hub
        appium_base_url_remote: http://localhost:${port}/wd/hub

    celery:
        broker_url: amqp://<username>:<password>@localhost:5672
        result_backend: rpc://<username>>:<password>@localhost:5672

    mongodb:
        connection_string: mongodb://<username>>:<password>@localhost:27018/appium_device_stats?authSource=admin&authMechanism=SCRAM-SHA-256
        device_stat_collection: device_stats
        device_session_collection: device_sessions

    chatgpt:
        api_key: <chat_gpt_api_key>
        engine: <chat_gpt_model>
        max_tokens: <max_token>
        temperature: <temperature>

    waits:
        max_time_out: <max_time_out_time_in_seconds_for_webdriver_wait>
    ```
- To encrypt/decrypt sensitive information, use the generated AES-256 key
  - If there is no AES-256 key present or if it is the first time that a script is being run then follow the below steps
    - Open a python console which is pointing to project root and type the below
      ```
      python cli.py --mode generate_key
      ```
    - Copy the generated key and store it in the project directory inside a .env file for reference, create one if not present
  - Now that we have a key handy, we can proceed with the sensitive data file encryption or decryption depending on the scenario
    - To encrypt the data file
      ```
      python cli.py --mode encrypt --key <generated_secret_key> --data_file <relative_file_path>
      ```
    - To decrypt the data file
      ```
      python cli.py --mode decrypt --key <generated_secret_key> --data_file <relative_file_path>
      ```

## Running Tests
- Now everything is setup and running fine, one final thing to test if things are really working. To run tests, run the following command

    ```bash
        pytest
        -or-
        pytest -v <relative_path_testclass_py_file>
        -or-
        pytest -v <relative_path_testclass_py_file>::<testcase_method_name>
        -or-
        pytest -v -m <tag_name>
    ```
- To run the test in parallel
    ```
    pytest -n <number_of_parallel_threads>
    -or-
    pytest -v <relative_path_testclass_py_file> -n <number_of_parallel_threads>
    -or-
    pytest -v -m <tag_name> -n <number_of_parallel_threads>
    ```
- To run the test and visualise report using allure
  - The allure reports will be available in the allure-reports which can be found in the project root 
    ```
    pytest -n <number_of_parallel_threads> --alluredir=allure-results
    -or-
    pytest -v <relative_path_testclass_py_file> -n <number_of_parallel_threads> --alluredir=allure-results
    -or-
    pytest -v -m <tag_name> -n <number_of_parallel_threads> --alluredir=allure-results
    ```
 - For more information on pytest, feel free to read the [docs](https://docs.pytest.org/en/7.1.x/contents.html)
