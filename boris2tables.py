#
#
# per-filename
#
#	key
#	videofile
#	fps
#	length
#	start
#	stop
#	main user
#
# events
#
#	key
#	eventstart
#	eventend
#	name
#	subject
import json
import os
import sys
import csv


def main():
	if len(sys.argv) < 2:
		print "missing file"
		return 
	outpath = "." if len(sys.argv) == 2 else sys.argv[2]
	infile = sys.argv[1]
	indata = json.load(open(infile,"rb"))
	statebehaviors = set([x["code"] for x in indata["behaviors_conf"].values() if x["type"] == "State event"])
	table = []
	events = []
	for k,v in indata["observations"].items():
		print "obs",k
		f0 = v["file"]["1"][0]
		od = dict(key=k,video=os.path.split(f0)[1],fps=v["media_info"]["fps"][f0],duration=v["media_info"]["length"][f0],start=0,stop=-1,subject="")		
		table.append(od)
		for ind in indata["independent_variables"].values():
			#default value
			od["i_" + ind["label"]] = v["independent_variables"].get(ind["label"],ind["default value"])
		# TODO add independent

		laststate = dict()
		for e in v["events"]:
			what = e[2]
			subject = e[1]
			if subject == "":
				subject = od["subject"]
			when = e[0]
			if what in statebehaviors:
				t = (what,subject)
				ed = laststate.get(t)
				if ed is None:
					# keep open
					ed = dict(key=k,event=what,subject=subject,start=when,stop=-1)
					laststate[t] = ed
				else:
					# close and remove
					ed["stop"] = e[0]
					events.append(ed)
					del laststate[t]
			else:
				ed = dict(key=k,event=what,subject=subject,start=when,stop=when)
				events.append(ed)

			if what != "":
				od["subject"] = subject
			if what == "Start":
				od["start"] = e[0]
			elif what == "Stop":
				od["stop"] = e[0]
		for k,v in laststate.items():
			print "issues with left open state",k,v
			events.append(v)

	outevents = os.path.join(outpath,"events.csv")
	outobs = os.path.join(outpath,"observations.csv")
	if len(events) == 0:
		print "no events"
		if os.path.isfile(outevents):
			os.unlink(outevents)
	else:
		writer = csv.DictWriter(open(outevents,"wb"), fieldnames=sorted(events[0].keys()))
		writer.writeheader()
		writer.writerows(events)

	if len(table) == 0:
		print "no observations"
		if os.path.isfile(outobs):
			os.unlink(outobs)
	else:
		writer = csv.DictWriter(open(outobs,"wb"), fieldnames=sorted(table[0].keys()))
		writer.writeheader()
		writer.writerows(table)


if __name__ == '__main__':
	main()