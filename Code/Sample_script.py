import sys
import simplejson
import pygraphviz as pgv


# Declaring required variables
sub_users_arr = []     # Array to store the friends of the user.
dict = {}              # Dictionary to store all the tweets seen by the user.
dict_userTweets = {}   # Dictionary to store the number of tweets made by the user. 


# getTweets Method															
def getTweets ():
   outfile = open("Output_dat", "a")
   filedata=open("data")
   G = pgv.AGraph("MERGED.dot")

   # reading each line from the file and getting the from user tags
   while True:
      head=filedata.readline()
      if not head: 
        break 
      tweet = simplejson.loads(head)
      if 'doc' in tweet:
         doc = tweet["doc"]
         from_user=doc["from_user"]
	 
         # Adding the user values to the dictionary dict_userTweets 
         # which maintains the record of number of tweets made by each user'''
	 if from_user in dict_userTweets:
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
      
   		 
# Call to main function
def main():
	getTweets ()

if __name__ == '__main__':
    main()
