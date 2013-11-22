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
user_tweet_loc = {}

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

    return x * milesPerNauticalMile * 1609.344, y  * milesPerNauticalMile * 1609.344




# getTweets Method															
def getTweets ():
   outfile = open("Output_week12_test_out_1", "a")
   outfile_2 = open("Output_week12_test_out_2", "a")
   filedata=open("nyc.trim.liwc")
   Graph = pgv.AGraph("MERGED.dot")	
   fields = ["Numerals", "swear",   "social",  "family",  "friend",  "humans",  "affect",  "posemo",  "negemo",  "anx",     "anger",   "sad",     "cogmech", "insight", "cause",   "discrep", "tentat",  "certain", "inhib",   "incl",    "excl",    "percept", "see",    "hear",    "feel",    "bio",     "body",    "health",  "sexual",  "ingest",  "relativ", "motion",  "space",   "time",    "work",    "achieve", "leisure", "home",    "money",   "relig",   "death"]
   # reading each line from the file and getting the from user tags
   for x in (0,200000):
      head=[filedata.next() for x in xrange(200000)]	
   
      
      tweet = simplejson.loads(head[x])
      if 'doc' in tweet:
         doc = tweet["doc"]
         from_user = doc["from_user"]
	 created_at = doc["created_at"]
	 lon = doc["lon"]
	 lat = doc["lat"]   
	 date = datetime.date(datetime.strptime(created_at,"%a, %d %b %Y %H:%M:%S +0000"))


	 # Finding the number of posts the used has posted from a given location pockets in the process of finding effective location
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

	
         # Adding the user values to the dictionary dict_userTweets 
         # which maintains the record of number of tweets made by each user'''
	 if from_user in dict_userTweets.keys():
	    user = dict_userTweets[from_user]
	    if date in user:
                for field in fields:     
		   dict_userTweets[from_user][date][field] += (float(tweet[field])*float(tweet['numwords']))

		
	    else:
	        dict_userTweets[from_user][date] = {}
		for field in fields:
		   dict_userTweets[from_user][date][field] = (float(tweet[field])*float(tweet['numwords']))
                		
	 else: 
	    dict_userTweets[from_user]={}
	    dict_userTweets[from_user][date] = {}
	    for field in fields:
               dict_userTweets[from_user][date][field] = (float(tweet[field])*float(tweet['numwords']))



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


   # Writing the output to the output file (JSON file format)
   for from_user in dict_userTweets.keys():
      dates = dict_userTweets[from_user]
      sub_users_arr = Graph.predecessors(from_user)
      for date in dates:
	 id = 1
	 #out_str = "{ "
         #for field in fields:
           #out_str = out_str+' '+'"'+field+'"'+': '+'"'+str(dict_userTweets[from_user][date][field])+'"'+','   
         #print>>outfile, '{'+'"from_user": "'+from_user+'"','"date": "',date,'"', user_tweet_loc[from_user][date], out_str+'}'
	 out_str_2 = '{'
	 for field in fields:
		#str_in = str(dict_userTweets[from_user][date][field])
		out_str_2 = str(out_str_2)+'"1.'+field+'"'+': '+'"'+str(dict_userTweets[from_user][date][field])+'"'+','
		for user in sub_users_arr:
			if user in dict_userTweets.keys() and date in dict_userTweets[user].keys():
				id += 1
				out_str_2 = out_str_2+' '+'"',id,'.'+field+'"'+': '+'"'+str(dict_userTweets[user][date][field])+'"'+','
	 print>>outfile_2,out_str_2 #'{'+'"from_user": "'+from_user+'"','"date": "',date,'"', user_tweet_loc[from_user][date], out_str+'}'

    
  				
	 
# Call to main function
def main():
	getTweets ()

if __name__ == '__main__':
    main()
