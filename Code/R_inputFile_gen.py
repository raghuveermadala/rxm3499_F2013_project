import simplejson

fields = ["1.Numerals", "2.Numerals", "1.swear", "2.swear", "1.social", "2.social", "1.family", "2.family", "1.friend", "2.friend", "1.humans", "2.humans", "1.affect", "2.affect", "1.posemo", "2.posemo", "1.negemo", "2.negemo", "1.anx", "2.anx", "1.anger", "2.anger", "1.sad", "2.sad", "1.cogmech", "2.cogmech", "1.insight", "2.insight", "1.cause", "2.cause", "1.discrep", "2.discrep", "1.tentat", "2.tentat", "1.certain", "2.certain", "1.inhib", "2.inhib", "1.incl", "2.incl", "1.excl", "2.excl", "1.percept",  "2.percept", "1.see", "2.see", "1.hear", "2.hear", "1.feel", "2.feel", "1.bio", "2.bio", "1.body", "2.body", "1.health", "2.health", "1.sexual", "2.sexual", "1.ingest", "2.ingest", "1.relativ", "2.relativ", "1.motion", "2.motion", "1.space", "2.space", "1.time", "2.time", "1.work", "2.work", "1.achieve", "2.achieve", "1.leisure", "2.leisure", "1.home", "2.home", "1.money", "2.money", "1.relig", "2.relig", "1.death", "2.death"]

outfile = open("input_fileFor_R", "a")
filedata = open("Grouped_user_output", "r")

out_str = ''
out_str += "user 1, user 2, date,"
for field in fields:
	if field != "2.death":
		out_str += field+','
	else:
		out_str += field
print>> outfile,out_str
out_str = ''
while True:
	head=filedata.readline()
	if not head:
      		break 
      	tweet = simplejson.loads(head)
	out_str += tweet["user 1"]+","+tweet["user 2"]+","+tweet["date"]+","       	
	for field in fields:
		if field != "2.death":
			out_str += tweet[field]+','
		else:
			out_str += tweet[field]
	print>> outfile,out_str
	out_str = ''
