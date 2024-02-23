Python-Licenses
===============

A python library that help you to handle software licenses

Installation
------------

.. code:: bash

   pip install python_licenses==0.0.1

Usage
-----

.. code:: python

   from licenses import Licenses

   licenses = Licenses(path_folder="licenses")

   licenses.create_license(license_key="1234567890", expiration_date="2024-12-31")

   license = licenses.check_license("1234567890")

   print(license)

How to use
----------

Python Licenses is a library that helps you to handle software licenses.
It’s possible to create, update and delete licenses.

Example Create License
^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   from licenses import Licenses

   licenses = Licenses(path_folder="licenses")

   licenses.create_license(license_key="4312412341", expiration_date="2024-12-31")

Example Verify License
^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   from licenses import Licenses

   licenses = Licenses(path_folder="licenses")

   license = licenses.check_license(license_key="4312412341")

   print(license) # True

Example Delete License
^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   from licenses import Licenses

   licenses = Licenses(path_folder="licenses")

   licenses.delete_license(license_key="4312412341")
   license = licenses.check_license(license_key="4312412341")

   print(license) # False
