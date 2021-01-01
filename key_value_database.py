
import os
import sys
import io
import json
from pympler import asizeof
import datetime

class KeyValueDatabase:
	__database_path = os.path.join(os.path.expanduser("~"),"Databases")
	__database_extension = '.kvd'
	__database = None

	def __init__(self,file):
		if(file.name[len(file.name)-4:len(file.name)] != KeyValueDatabase.__database_extension):
			raise Exception("Specified file is not a valid Database file")
		self.__database = file

	@staticmethod
	def __create_database_directory(path):
		try:
			if not os.path.exists(path):
				print(f"Creating a default directory for databases at {path}")
				os.mkdir(path)
		except:
			raise Exception("An Error occured when accessing Database location")
			exit()

	@staticmethod
	def create_database(name,path = __database_path):
		try:
			if(path!= None and not os.path.exists(path)):
				KeyValueDatabase.__create_database_directory(path)

			file = open(os.path.join(path,name+ KeyValueDatabase.__database_extension),'x')
			if(file != None):
				print(f"Database created Successfully: {file.name}")
				file.close()
		except FileExistsError:
			raise Exception("Error: A database with the name specified already exists. Please specify a different name.")
			exit()
		except:
			raise Exception("An Error occured when creating Database")
			exit()

	@staticmethod
	def delete_database(path):
		if (path[len(path)-4:len(path)] != KeyValueDatabase.__database_extension):
			raise Exception("Specified file is not a valid Database file")
		if not os.path.exists(path):
			raise Exception("Database File does not exist")

		os.remove(path)

	@staticmethod
	def connect(path):
		return KeyValueDatabase(open(path,'r+'))	

	def __find_occurance(self,key):
		curr_pos = 0
		lines = self.__database.readlines()
		for line in lines:
			data = KeyValueDatabase.__parse_line(line)
			if key in data:
				return curr_pos
			curr_pos+=1
		return -1	

	@staticmethod
	def __parse_line(line):
		return json.loads("{"+line+"}")
		

	def get_data(self,key):
		self.__database.seek(0,io.SEEK_SET)
		data = self.__database.readlines()
		for line in data:
			data = KeyValueDatabase.__parse_line(line)
			if key in data:
				
				ttl_duration = data[key]['ttl']['ttl_duration']
				elapsed_time = None
				if(ttl_duration != None):
					created_time = data[key]['ttl']['created_time']
					ct_obj = datetime.datetime(
						created_time['year'], 
						created_time['month'], 
						created_time['day'],
						created_time['hour'], 
						created_time['minute'], 
						created_time['second'],
						created_time['microsecond'], 
						created_time['tzinfo'], 
						)
					elapsed_time = (datetime.datetime.now() - ct_obj).seconds

				if(ttl_duration == None or elapsed_time < ttl_duration):
					return data[key]['value']
				else:
					print('Access time limit set for this field exceeded! Deleting this field.')
					self.delete(key)
					break
		return None

	def put_data(self,key,value,ttl_duration = None):
		size_of_key = sys.getsizeof(key)
		size_of_value = asizeof.asizeof(value)

		if(os.stat(self.__database.name).st_size > 1000000000 - (size_of_key+size_of_value)):
			raise Exception("Database size has reached the maximum size(1GB). Cannot add any more data into this database.")
		if(self.get_data(key) != None):
			raise Exception("Given key is already present in the database")
		if(len(key) > 32):
			raise Exception("Length of key should not exceed 32 Characters")
		if(type(value) != dict or size_of_value > 16000):
			raise Exception("Size of value(data) should not exceed 16KB")
		if(ttl_duration != None and ttl_duration < 0):
			raise Exception("Time-to-live property must be greater than or equal to 0")

		d = datetime.datetime.now()
		created_time = None
		if(ttl_duration != None):
			created_time = {
				'day' : d.day,
				'month': d.month,
				'year':d.year,
				'hour':d.hour,
				'minute':d.minute,
				'second':d.second,
				'microsecond':d.microsecond,
				'tzinfo':d.tzinfo
			} 



		data = {
			"value" : value,
			"ttl" : {
				'ttl_duration':ttl_duration,
				'created_time':created_time
			}
		}
		self.__database.seek(0,io.SEEK_END)
		self.__database.write(f'"{key}"' + ':' + json.dumps(data)+'\n')

	def delete(self,key):
		self.__database.seek(0,io.SEEK_SET)
		lines = self.__database.readlines()
		key_found = False
		pos = 0
		remaining_lines = ''
		for line in lines:
			if not key_found:
				data = KeyValueDatabase.__parse_line(line)
				if key in data:
					key_found = True
					continue
				else:
					pos += len(line)
				pos+=1
			if key_found:
				remaining_lines += line

		self.__database.seek(pos,io.SEEK_SET)
		self.__database.write(remaining_lines)
		self.__database.truncate()


	def disconnect(self):
		self.__database.close()
