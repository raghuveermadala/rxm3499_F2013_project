import sys
import simplejson
import pygraphviz as pgv

from_users_arr = []
sub_users_arr = []
dict = {}
															
def getTweets ():
   	      
   outfile = open("edited_dat", "a")
   infile = open("data", "r")			
 #  with open("data") as myfile:
   filedata=open("data")
   G = pgv.AGraph("MERGED.dot")
   while True:
      head=filedata.readline()
      if not head: 
        break 
      tweet = simplejson.loads(head)
      if 'doc' in tweet:
         doc = tweet["doc"]
         from_user=doc["from_user"]
	 from_users_arr.append(from_user)
      for user in from_users_arr:
         if user not in dict:
            dict[user]=0
      

      
      for user in from_users_arr:
         sub_users_arr = G.predecessors(user)
         for user_1 in sub_users_arr:
            if user_1 in dict:
               dict[user_1] += 1
            else:
               dict[user_1] = 1   
      print "The values of the dictionary are : "
      for user in dict:
         String = ""
         string = user," : ", dict[user]
        # print>>outfile, string
         print string
   		 

def main():
	getTweets ()

if __name__ == '__main__':
    main()
