# db-class
example database wrapper class

This file is an example DB Table wrapper. It provides an entry point into a framework table record

It provides the following methods:
  
  * load - a static methods for loading data, and ensures the record can be loaded either via the record ID, the field 'name' or by its own class type, or from a dictionary
  * save - save the class data into a db record, which handles duplication checking, and updating if the record already exists.
  * delete - remove the record from the DB
  * to_json - Ill want to output the data consistantly   
  

So, I try to provide multiple ways to load the record, db id, name, class or dict.
I provide ways to save the record, and update the record and a way to delete the record, or display the record.

If I was to write a REST wrapper around this:

  * GET = load
  * POST = load(dict with params), then save
  * PUT = load(record id or name), set any class variables that require changing, then save
  * DELETE = load(record id or name), then remove


my queries will undoubtably be relational, and therefor have relational classes.
so, for example, if I had a sites table, i may want to represent that relationship with site id in devices table, and when I load device, perhaps optionally load a class to represent the sites table by adding a flag to load method and code at end of load_by_id method:

  ```python
  if self.load_site:
      self.site = Site.load(db_rec.site_id)
  ```
  
  I would then add site to the to_json() method:
    
    ```python
       site=site.to_json() is site else None
    ```
    
  this would allow me to dynamically load the entire record for a site, if required, which would might be an arg to my GET REST call.
  
  
