# db-class
example database wrapper class

This file is an example DB Table wrapper. It provides an entry point into a framework table record

It provides the following methods:
  
  * load - a static methods for loading data, and ensures the record can be loaded either via the record ID, the field 'name' or by its own class type, or from a dictionary
  * save - save the class data into a db record, which handles duplication checking, and updating if the record already exists.
  * delete - remove the record from the DB
  * to_json - Ill want to output the data consistantly   
  

