import psycopg2
from datetime import datetime # used for the timestamps
import random # used for rng

def Create_table():
	conn = psycopg2.connect("dbname='revlo' user='j'")
	cursor = conn.cursor()
	cursor.execute("""CREATE TABLE players (id SERIAL PRIMARY KEY   NOT NULL, username TEXT, points INT, lasttransaction TIMESTAMP WITH TIMEZONE, idletime TIMESTAMP WITH TIMEZONE);""")
	print("Table created successfully")
	conn.commit()
	conn.close()

def user_add(username, points=0):
	'''Create a new user by supplying username 1st and then points value'''
	username = validate_username(username) #calls the validate_username email 
	conn = psycopg2.connect("dbname='revlo' user='j'")
	cursor = conn.cursor()
	current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # datetime module works with python database programming out of the box
	cursor.execute("""INSERT INTO players (username, points, lasttransaction) VALUES (%s, %s, %s) RETURNING id;""",(username, points, current_time))
	print("user {0} created".format(username))
	conn.commit()
	conn.close()

def add_points(username, points):
	'''Adds the given amount of points to the supplied user '''
	conn = psycopg2.connect("dbname='revlo' user='j'")
	cursor = conn.cursor()
	cursor.execute("""SELECT points FROM players WHERE username=(%s);""",(username,)) #psycopg2 requires tuples even for single item arguments
	current_points = cursor.fetchone()
	new_points = current_points[0] + points  #psycopg2 returns a tuple
	cursor.execute("""UPDATE players SET points = (%s);""",(new_points,))
	print("Points added to {0}".format(username))
	conn.commit()
	conn.close()

def sub_points(username, points):
	'''Subtracts the given amount of points to the supplied user '''
	conn = psycopg2.connect("dbname='revlo' user='j'")
	cursor = conn.cursor()
	cursor.execute("""SELECT points FROM players WHERE username=(%s);""",(username,)) #psycopg2 requires tuples even for single item arguments
	current_points = cursor.fetchone()
	new_points = current_points[0] - points  #psycopg2 returns a tuple
	if new_points < 0:
		new_points = 0
	cursor.execute("""UPDATE players SET points = (%s);""",(new_points,))
	print("Points subtracted from {0}".format(username))
	conn.commit()
	conn.close()

def gamble(username,points):
	'''Returns True or False for win or lose conditions of the gamble'''
	conn = psycopg2.connect("dbname='revlo' user='j'")
	cursor = conn.cursor()


	if(timer):
	#Checks to see if the transactions are 5 minutes apart
		rand_num = rng()
		if rand_num >= 50:
			add_points(username,points*2)
			cursor.execute("""SELECT points FROM players WHERE username = (%s)""",(username,))
			current_points = cursor.fetchone()[0]
			print("{0} rolled a {1}. {2} won {3} coins and now has {4} coins".format(username, rand_num, username, points*2, current_points) )
		else:
			sub_points(username,points*2)
			cursor.execute("""SELECT points FROM players WHERE username = (%s)""",(username,))
			current_points = cursor.fetchone()[0]
			print("{0} rolled a {1}. {2} lost {3} coins and now has {4} coins".format(username, rand_num, username, points*2, current_points) )
	else:
		print("You can only gamble once every 5 minutes")

	conn.close()

def gamble_notime(username,points):
	'''There is no timer check for this gamble call
	Returns True or False for win or lose conditions of the gamble'''
	conn = psycopg2.connect("dbname='revlo' user='j'")
	cursor = conn.cursor()

	rand_num = rng()
	if rand_num >= 50:
		add_points(username,points*2)
		cursor.execute("""SELECT points FROM players WHERE username = (%s)""",(username,))
		current_points = cursor.fetchone()[0]
		print("{0} rolled a {1}. {2} won {3} coins and now has {4} coins".format(username, rand_num, username, points*2, current_points) )
	else:
		sub_points(username,points*2)
		cursor.execute("""SELECT points FROM players WHERE username = (%s)""",(username,))
		current_points = cursor.fetchone()[0]
		print("{0} rolled a {1}. {2} lost {3} coins and now has {4} coins".format(username, rand_num, username, points*2 ,current_points) )

	conn.close()

def rng():
	'''Random number generator for gamble returns a number between 0-100.
	Returns an int'''
	random_num = random.SystemRandom().randrange(100)
	return(random_num)

def timer(username):
	'''Function that checks current time vs last transaction time to see if they interlap if so return False if not return True'''
	conn = psycopg2.connect("dbname='revlo' user='j'")
	cursor = conn.cursor()
	cursor.execute("""SELECT lasttransaction FROM players WHERE username = (%s);""",(username,))
	last_transac = cursor.fetchone()[0] #fetchone returns a list
	curr_transac = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	if True != year_check(last_transac.split()[0].split("-")[0], curr_transac.split()[0].split("-")[0]):
		#Split the strings and only take the year and compare them
		return True
	else:
		if True != month_check(last_transac.split()[0].split("-")[1], curr_transac.split()[0].split("-")[1]):
			#Split the strings and only take the months and compare them
			return True
		else:
			if True != day_check(last_transac.split()[0].split("-")[2], curr_transac.split()[0].split("-")[2]):
				#Split the strings and only take the days and compare them
				return True
			else:
				if True != hour_check(last_transac.split()[1].split(":")[0], curr_transac.split()[1].split(":")[0]):
					#Split the strings and only take the hours and compare them
					return True
				else:
					if minute_check(last_transac.split()[1].split(":")[1], curr_transac.split()[1].split(":")[1]):
						#Split the strings and only take the minutes and compare them
						return False
					else:
						last_minute = int(last_transac.split()[1].split(":")[1])
						curr_minute = int(curr_transac.split()[1].split(":")[1])
						if last_minute in [55,56,57,58,59]:
							#The five minute difference is different for these
							if last_minute == 55 and (curr_minute >= 1 and curr_minute <=54):
								return True
							elif last_minute == 56 and (curr_minute >= 2 and curr_minute <=55):
								return True
							elif last_minute == 57 and (curr_minute >= 3 and curr_minute <=56):
								return True
							elif last_minute == 58 and (curr_minute >= 4 and curr_minute <=57):
								return True
							elif last_minute == 59 and (curr_minute >= 5 and curr_minute <=58):
								return True
							elif last_minute == 1 and (curr_minute >= 6 and curr_minute <=55):
								return True
							else:
								return False
						else:
							if curr_minute > last_minute:
								if (curr_minute - last_minute) >= 5:
									return True
								else:
									return False
							else:
								if (last_minute - curr_minute) >= 5:
									return True
								else:
									return False

	conn.close()

def year_check(t_year_string, year_string):
	'''Comapare the last transaction year string to the current day string'''
	if t_year_string == year_string:
		return True
	else:
		return False

def month_check(t_month_string, month_string):
	'''Comapare the last transaction month string to the current day string'''
	if t_month_string == month_string:
		return True
	else:
		return False

def day_check(t_day_string, day_string):
	'''Comapare the last transaction day string to the current day string'''
	if t_day_string == day_string:
		return True
	else:
		return False

def hour_check(t_hour_str, hour_str):
	'''Compare the last transaction hour string to the current hour string.
	The hour is in 24 hour format'''
	if t_hour_str == hour_str:
		return True
	else:
		return False

def minute_check(t_minute_str, minute_str):
	'''Compare the lasttransaction minute string to the current minute string'''
	if t_minute_str == minute_str:
		return True

def get_users():
	'''Returns a list of all the users'''
	conn = psycopg2.connect("dbname='revlo' user='j'")
	cursor = conn.cursor()
	cursor.execute("SELECT username FROM players;")
	usernames = cursor.fetchall()
	username_lst = ''
	for names in usernames:
		username_lst += names
	print(username_lst)
	conn.close()

def get_coins(username):
	'''Returns the amount of coins a gien user has.'''
	conn = psycopg2.connect("dbname='revlo' user='j'")
	cursor = conn.cursor()
	cursor.execute("SELECT points FROM players;")
	current_points = cursor.fetchone()
	print(current_points[0])

def delete_user():
	'''Deletes a given user'''

def validate_username(username):
	'''Checks the username supplied for an illegal character. The only character that is not allowed is \ as the one and only character.
	The function returns the username if it is valid. If its not it makes the user supply a new username and returns that.
	So set the username equal to this function call in the function.'''

	if username == "\\":
		print("That username is not valid.")
	while username == "\\":
		username = input("Please specify another username: ")
	print("That username is valid. Thank you")
