
# HealthySwapper

Programmed for the project 5 of OpenClassrooms Python developper certificate.
Allows user to swap from junk to healthy food by being given alternatives sourced from OpenFoodFacts API.

## Getting Started

* MySQL DATABASE SERVER must be installed on your conputer.

* Clone this repository inside the same folder (please keep the same files structure).

* Install Python3 on your computer if you are running a Windows environment.

* Execute the command "pip install -r requirements.txt".

* Execute p5.sql scrip on the MySQL server to create p5oc database

* Execute data_import to fill up p5oc DB (please change the constants.py file according to your needs)

* Execute the command "python ImgoingGreen.py".

### Using

* From the main menu enter option "1" then press "enter" to make a new search, the program then displays a choice of food       categories.
    Enter the category number for the food that you want to swap with an healthier one, the program then displays a choice of food items.
    Enter the food item number choosen then press "enter", the program displays an alternate to the food item, its description and a store which sells it when available along with a hyperlink to Open Food Facts web page of the replacement item.
    Enter option "0" then press "enter" to save this search or option "1" to return to main menu.

* From the main menu, enter option "2" to consult previously saved searches, the program displays the list of saved             food items and their desription.
    Enter option "0" to return to main menu.

* From the main menu press "3" to quit.

## Authors

**Paul Girmes** - *Initial work*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
