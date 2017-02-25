Fyndiq UrlShortner
------------------

A new, robust and flexible urlshortner.


How to use?
---------------

You should have installed Python 3.X and then create a new virtualenv.

Now you need to clone this project to your computer and the install requirements with
the following command:

    make create_virtualenv  # This command is optional is you already has a virtualenv
    make setup-dev


The 'setup-dev' command will install all python requirements for this project.

Once you have installed all requirements, you can run the devserver and see it online:

    make run-dev

Now access your browser in the url http://localhost:8002/ and you will see the running project.


Tests
-----

To execute tests, run the following command:

    make test


F.A.Q
------

How to use a new backend?

    Change your settings file to set the new backend:

    # settings.py
    URLSHORTNER_CONFIGS = {
        'backend': 'urlshortner.backends.random_hash'
    }


How to insert a new wordlist in database?

    Execute the following command:

        python manage.py load_words --wordlist <PATH>
