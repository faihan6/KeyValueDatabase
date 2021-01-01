# KeyValueDatabase
This is a Key-Value Database store for Python which can be used to store data in terms of key-value pairs.

## Usage :
1. import the KeyValueDatabase class from 'key_value_database.py' file into your code
    `from key_value_database import KeyValueDatabase`

## Documentation :
**1. `KeyValueDatabase.create_database(name, path =__default_path)`**

	This is a static function used to create database files. The path argument is optional. If 'path' is not specified, then the database will be created at a default directory(which is OS specific). If path is specified, then the database will be created at the specified path.
	**Note:** This function just creates the database in the desired location. It does not return any reference/connection to the database. Use the `KeyValueDatabase.connect()` method to get reference to database object.
	
**2. `KeyValueDatabase.connect(path)`** 

	This is a static method that establishes a connection to the database and returns the Object reference to the database. This reference can be used to perform read/write operations in the database.

    > db = KeyValueDatabase.connect("<path to database>")

**3. `KeyValueDatabase.delete_database(path)`** 

	This is a static method that deletes the database referenced by the `path` argument. This method throws an error if the specified path does not point to a valid `.kvd` database file.

    > db = KeyValueDatabase.delete_database("<path to database>")
    
**4. `put_data(key,value,ttl_duration=None)`**	

	This is an instance method of objects of `KeyValueDatabase` class.  This method associates the `key` with the `value` and inserts it into the database. The `ttl_duration` specifies the 'Time-to-live' duration of the specified key in **seconds**. That is, if a 'Time-to-live' duration has been specified, then the key can be queried for only until the specified 'Time-to-live' duration. After that, the key cannot be accessed and will be deleted automatically if called after the time limit.
	The `value` can only be Python Dictionaries and the size of the dictionary cannot exceed 16KB.
	The `key` argument can only be Strings and it's length cannot exceed 32 characters.
  

    > db = KeyValueDatabase.connect("<path to database>")
    > db.put_data('address',{'door-no':'17','city':'Madurai'})

**Note:** The total possible size of the database is limited to 1GB. Therefore, when the database reaches the 1GB limit, calling this method to insert new data throws an error.

**5. `get_data(key)`**	

	This is an instance method of objects of `KeyValueDatabase` class. This method returns the value associated with the key from the database. The key to be searched in the database should be supplied as an argument to this method.
```
> db = KeyValueDatabase.connect("<path to database>")
> db.put_data('address',{'door-no':'17','city':'Madurai'})
> db.get_data('address')
{'door-no':'17','city':'Madurai'}
```
This method returns `None` when the key is not found in the database.

When tried to access keys with expired Time-to-live durations, this method will not return any value. In addition to this, this method deletes the key-value pair from the database when an expired key is supplied as the argument.

**6. `delete(key)`**	
This is an instance method of objects of `KeyValueDatabase` class. This method deletes the key-value pair associated with the key given in the argument from the database. 
```
> db = KeyValueDatabase.connect("<path to database>")
> db.put_data('address',{'door-no':'17','city':'Madurai'})
> db.get_data('address')
{'door-no':'17','city':'Madurai'}
> db.delete('address')
> db.get_data('address')
None
```

**7. `disconnect()`**	
This is an instance method of objects of `KeyValueDatabase` class. This method disconnects the program and the database, and closes the database file. No operations can be performed further on the database object reference once this method was called on the object.
```
> db = KeyValueDatabase.connect("<path to database>")
> db.disconnect()
```

## Other information
1. The maximum size a database can be is 1GB.
2. The database will be stored with `.kvd` extension.
