# Result-Scanner

This is an application that can extract data from result PDF given by KTU.(*currently for Rajagiri IT students only*)

# Screenshot

<img src="https://i.imgur.com/gyaLdFK.png" alt="Screenshot" />

## Getting Started

1. Install python 2.7 

    ``` sudo apt install python```

2. Install python module PyPDF2 

    ```pip install PyPDF2 ```

3. Install python module Flask

    ```pip install flask```

4. Install python module pdfkit

    ```pip install pdfkit```

5. Install pdfkit dependency wkhtmltopdf

    ```sudo apt-get install wkhtmltopdf```
    
These instructions will get you a copy of the project up and running on your local machine for testing purposes.

1. To start the application, go to the source folder and run ```resultScanner.py```

2. Now open your web browser and type the url ```localhost:5000```

3. In the application, upload the `result_RET.pdf` file only.(file name is currently hardcoded.)

4. After using the application, don't forget to click `Delete Session`

## Built With

* [Python Flask](https://flask.palletsprojects.com/en/1.1.x/) - Flask is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications.
* [Bootstrap](https://getbootstrap.com/) - Bootstrap is a popular CSS Framework for developing responsive websites.

## Authors

[Thejus Paul](https://github.com/Thejus-Paul)

See also the list of [contributors](https://github.com/thejus-paul/nurse-call/graphs/contributors) who participated in this project.

## License

This project is licensed under the GNU AGPL License - see the [LICENSE.md](LICENSE.md) file for details
