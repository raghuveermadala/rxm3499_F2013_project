import sys
import simplejson
import pygraphviz as pgv
from datetime import datetime


# Declaring required variables
sub_users_arr = []     # Array to store the friends of the user.
dict = {}              # Dictionary to store all the tweets seen by the user.
dict_userTweets = {}   # Dictionary to store the number of tweets made by the user.



# getTweets Method															
def getTweets ():
   outfile = open("Output_dat", "a")
   filedata=open("nyc.trim.liwc")
#   G = pgv.AGraph("MERGED.dot")
   fields = ["Numerals", "swear",   "social",  "family",  "friend",  "humans",  "affect",  "posemo",  "negemo",  "anx",     "anger",   "sad",     "cogmech", "insight", "cause",   "discrep", "tentat",  "certain", "inhib",   "incl",    "excl",    "percept", "see",    "hear",    "feel",    "bio",     "body",    "health",  "sexual",  "ingest",  "relativ", "motion",  "space",   "time",    "work",    "achieve", "leisure", "home",    "money",   "relig",   "death"]
   # reading each line from the file and getting the from user tags
   while True:
      head=filedata.readline()
      if not head: 
        break 
      tweet = simplejson.loads(head)
      if 'doc' in tweet:
         doc = tweet["doc"]
         from_user = doc["from_user"]
	 created_at = doc["created_at"]   
	 date = datetime.date(datetime.strptime(created_at,"%a, %d %b %Y %H:%M:%S +0000"))
	
         # Adding the user values to the dictionary dict_userTweets 
         # which maintains the record of number of tweets made by each user'''
	 if from_user in dict_userTweets.keys():
	    #print date
	    #print "dates in the user are : ", dict_userTweets[from_user].items(), "\n"
	    #print "Values in the user are : ", dict_userTweets[from_user][date].values(), "\n","\n"
	    #date_1 = dict_userTweets[from_user]
	    #for date_2 in date_1:
	    #   print date_1
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
   
   for from_user in dict_userTweets.keys():
      dates = dict_userTweets[from_user]
      for date in dates:
	 out_str = "{ "
         for field in fields:
           out_str = out_str+' '+'"'+field+'"'+': '+'"'+str(dict_userTweets[from_user][date][field])+'"'+','   
         print>>outfile, '{'+from_user, date, out_str+'}'   
                




'''
           dict_userTweets[from_user] += 1
         else:
	    dict_userTweets[from_user] = 1    

   # For each user in dict_userTweets retrieving all his friends and adding 
   # the number of tweets made by him as their "tweets seen" value    
   for user in dict_userTweets:
      sub_users_arr = G.predecessors(user)
      for user_1 in sub_users_arr:
         if user_1 in dict:
            dict[user_1] += dict_userTweets[user]
         else:
            dict[user_1] = dict_userTweets[user]   
  
   # Printing all the values of the dictionary in to a text file 
   print>>outfile, "\nTHE TOTAL NUMBER OF TWEETS SEEN BY EACH USER ARE AS FOLLOWS :"
   for user in dict:
      String = ""
      string = user," : ", dict[user]
      print>>outfile, string
'''      
   		 
# Call to main function
def main():
	getTweets ()

if __name__ == '__main__':
    main()
