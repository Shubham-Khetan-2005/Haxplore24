## Requirement :-
* Xampp
* [wkhtmltox](https://wkhtmltopdf.org/downloads.html)
* Python

## How to run :-
1. `pip install -r requirement.txt`
2. start Xampp (Apache, mysql) server
3. Create database as shown in the video and main.py file
4. python main.py

## Features
* User can book and print tickets online for any temple listed on the website
* You can watch live darshan of the listed temple
* Temple Admins can get a through idea on past transaction through http://127.0.0.1:5000/admin
* Login credentials are highly encrypted through argon2 hashing
* All the transaction are stored securely in the form of blockchain where each transaction is stored in unique block
* Website is highly responsive suitable for any screen size
* Robust jinja templating has been employed for optimal performance with flask
