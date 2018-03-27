# Bookworm
## Installation
You'll need to make sure that you have [Python 3+](http://python.org/) installed to be able to run this.


Firstly, clone the repository:

```
$ git clone https://github.com/VladasX/Bookworm.git
$ cd Bookworm
```

Then, it is recommended that you create a virtual environment to hold the Python dependencies:

**Linux and MacOS:**
```
$ virtualenv Bookworm
$ source Bookworm/bin/activate
```

**Windows:**
```
$ python -m venv Bookworm
$ Bookworm\Scripts\activate.bat
```

Next, you'll want to install the Python dependencies into your virtual environment using pip.

```
$ pip install -r requirements.txt
```

You can now run the migrations:

```
$ python manage.py makemigrations
$ python manage.py migrate
```

Optionally, if you wish to populate the application:

```
$ python population_script.py
```

Finally, you can run the application:

```
$ python manage.py runserver
```