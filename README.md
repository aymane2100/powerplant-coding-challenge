# powerplant-coding-challenge solution


## Setting up

1. Open Visual Studio Code
2. Select 'Open Folder' to open the repository
3. Once it is opened, open a terminal and execute 'pip install -r requirements.txt' to install the necessary libraries

## Running the application

1. Open a terminal and execute 'cd powerplant-coding-challenge' to make sure you are in the right directory
2. Execute the scripts by entering 'python aymane_main.py'. The application is now running
3. Send payloads by using the following curl command 'curl -X POST -d @example_payloads/payload1.json -H "Content-Type: application/json" http://localhost:8888/productionplan'. The output of the command will be shown in the terminal.