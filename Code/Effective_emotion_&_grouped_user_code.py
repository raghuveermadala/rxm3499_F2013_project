import sys
import simplejson
import pygraphviz as pgv
from datetime import datetime
import math

# Declaring required variables
sub_users_arr = []     # Array to store the friends of the user.
dict = {}              # Dictionary to store all the tweets seen by the user.
dict_userTweets = {}   # Dictionary to store the number of tweets made by the user.
user_pos = {}	       # Dictionary to store latitude and longitude values of the users	
user_tweet_loc = {}    # Dictionary to store the effective location of the users on a given day
dict_user_numwords = {} # Dictionary to maintain total numwords related to each user on each day
	    


# calcPosition Method which gives the x and y values of the location from Ref:(0,0)
def calcPosition (lat, lon):
    """
    Calculate position from (0,0) in meters
    """
    nauticalMilePerLat = 60.00721
    nauticalMilePerLongitude = 60.10793
    rad = math.pi / 180.0
    milesPerNauticalMile = 1.15078
    
    y = lat * nauticalMilePerLat
    x = math.cos(lat * rad) * lon * nauticalMilePerLongitude

    return int ((x * milesPerNauticalMile * 1609.344)/50), int ((y  * milesPerNauticalMile * 1609.344)/50)



# getTweets Method															
def getTweets ():
   outfile = open("Effective_emotion_output", "a")
   outfile_2 = open("Grouped_user_output", "a")
   filedata=open("nyc.trim.liwc")
   Graph = pgv.AGraph("MERGED.dot")
   fields = ["Numerals", "swear",   "social",  "family",  "friend",  "humans",  "affect",  "posemo",  "negemo",  "anx",     "anger",   "sad",     "cogmech", "insight", "cause",   "discrep", "tentat",  "certain", "inhib",   "incl",    "excl",    "percept", "see",    "hear",    "feel",    "bio",     "body",    "health",  "sexual",  "ingest",  "relativ", "motion",  "space",   "time",    "work",    "achieve", "leisure", "home",    "money",   "relig",   "death"]
   # reading each line from the file and storing the required fields
   while True:
      head=filedata.readline()
      if not head:
      	break 
      tweet = simplejson.loads(head)
      if 'doc' in tweet:
         doc = tweet["doc"]
         from_user = doc["from_user"]
	 created_at = doc["created_at"]
	 lon = doc["lon"]
	 lat = doc["lat"]   
	 date = datetime.date(datetime.strptime(created_at,"%a, %d %b %Y %H:%M:%S +0000"))


	 # Finding the number of posts the user has posted from a given location pockets in the process of finding effective location
	 x_pos, y_pos = calcPosition (lat, lon)
	 if from_user in user_pos:
		if date in user_pos[from_user]:
		 	if (x_pos, y_pos) in user_pos[from_user][date]:
		 		user_pos[from_user][date][x_pos, y_pos] += 1
		 	else:
				user_pos[from_user][date][x_pos, y_pos] = 1
		else:
			user_pos[from_user][date]={}
			user_tweet_loc[from_user][date] = {}
			user_pos[from_user][date][x_pos, y_pos] = 1		
	
	 else:
		user_pos[from_user] = {}
		#creating a dictionary for later use 
		user_tweet_loc[from_user] = {}
		user_pos[from_user][date] = {}
		user_tweet_loc[from_user][date] = {} 
		user_pos[from_user][date][x_pos, y_pos] = 1

	 # Code for finding effective emotion latent factors 
         # Adding the user values to the dictionary dict_userTweets 
         # which maintains the record of number of tweets made by each user'''
	 if from_user in dict_userTweets.keys():
	    dates = dict_userTweets[from_user]
	    if date in dates:
		dict_user_numwords[from_user][date] += tweet['numwords']
                for field in fields:     
		   dict_userTweets[from_user][date][field] += (float(tweet[field])*float(tweet['numwords']))

		
	    else:
	        dict_userTweets[from_user][date] = {}
		dict_user_numwords[from_user][date] = tweet['numwords']
		for field in fields:
		   dict_userTweets[from_user][date][field] = (float(tweet[field])*float(tweet['numwords']))
                		
	 else: 
	    dict_userTweets[from_user]={}
	    dict_user_numwords[from_user]={}	
	    dict_userTweets[from_user][date] = {}
	    dict_user_numwords[from_user][date] = tweet['numwords']
	    for field in fields:
               dict_userTweets[from_user][date][field] = (float(tweet[field])*float(tweet['numwords']))

   
   
   # Code for dividing each field with the total numwords of the tweets made by the user on a particular day
   for user in dict_userTweets:
	dates = dict_userTweets[user]
	for date in dates:
		for field in fields:
			dict_userTweets[user][date][field] = dict_userTweets[user][date][field]/dict_user_numwords[user][date]



   # Trying to get the location pocket from where the user posted maximum tweets to get the effective location
   for user in user_pos:
	for date in user_pos[user]:
		x_max = 0
		y_max = 0
		count = 0
		for (x_pos, y_pos) in user_pos[user][date]:
			if user_pos[user][date][x_pos, y_pos] > count:
				#x_max = x_pos
				#y_max = y_pos
				user_tweet_loc[user][date] = (x_pos, y_pos)


   ''' You have to divide the tweets sentiment values by total numwords that you are grouped into dict_user_nuwords[][][]
    You are expected to do that while you are writing the data into the file'''




   # Writing the output to the output file (JSON file format)
   for from_user in dict_userTweets.keys():
      dates = dict_userTweets[from_user]
      sub_users_arr = Graph.predecessors(from_user)
      for date in dates:
      	 out_str = ""
         for field in fields:
		if field != 'death':
			out_str = out_str+' '+'"'+field+'"'+': '+'"'+str(dict_userTweets[from_user][date][field])+'", '   
		else:
			out_str = out_str+' '+'"'+field+'"'+': '+'"'+str(dict_userTweets[from_user][date][field])+'"'
	 x,y = user_tweet_loc[from_user][date]
         print>>outfile, '{'+'"from_user": "'+from_user+'", "date": "',date,'", "x_position": "',x,'", "y_position": "',y,'",'+out_str+'}'
	 
	 for user in sub_users_arr:
		#str_in = str(dict_userTweets[from_user][date][field])
		out_str_2 = '{ "user 1": "'+from_user+'", '
		if user in dict_userTweets.keys() and date in dict_userTweets[user].keys():
			out_str_2 = str(out_str_2)+' "user 2": "'+user+'", "date": "'+str(date)+'", '
			for field in fields:
				out_str_2 = str(out_str_2)+' "1.'+field+'"'+': '+'"'+str(dict_userTweets[from_user][date][field])+'", '
				if field != 'death':
					out_str_2 = str(out_str_2)+' "2.'+field+'"'+': '+'"'+str(dict_userTweets[user][date][field])+'", ' 
				else:
					out_str_2 = str(out_str_2)+' "2.'+field+'"'+': '+'"'+str(dict_userTweets[user][date][field])+'"'

	 		print>>outfile_2,out_str_2+'}' 

    
  				
	 
# Call to main function
def main():
	getTweets ()

if __name__ == '__main__':
    main()
