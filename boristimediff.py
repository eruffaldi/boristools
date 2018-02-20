import json
import argparse

def findduration(v):
	f0 = v["file"]["1"][0]
	fps=v["media_info"]["fps"][f0]
	duration=v["media_info"]["length"][f0]
	frames = int(duration*fps)
	return duration,fps,frames

def main():

    parser = argparse.ArgumentParser(description='Takes a Boris file, two observations and compares times of Start/Stop events (offset and scaling)')
    parser.add_argument('infile')
    parser.add_argument('--obs1')
    parser.add_argument('--obs2')

    args = parser.parse_args()

    data = json.load(open(args.infile,"rb"))

    print "Looking into",args.obs1,args.obs2
    o1 = data["observations"][args.obs1]
    o2 = data["observations"][args.obs2]

    d1,fps1,f1 = findduration(o1)
    d2,fps2,f2 = findduration(o2)

    st1 = [0,d1]
    st2 = [0,d2]
    for e in o1["events"]:
    	t,s,w = e[0:3]
    	if w == "Start":
    		st1[0] = t
    	elif w == "Stop":
    		st1[1] = t
    for e in o2["events"]:
    	t,s,w = e[0:3]
    	if w == "Start":
    		st2[0] = t
    	elif w == "Stop":
    		st2[1] = t

    print "Info 1: obs,duration,fps,frames(est),interval:",args.obs1,d1,fps1,f1,st1
    print "Info 2: obs,duration,fps,frames(est),interval:",args.obs2,d2,fps2,f2,st2
    print "Offset (2nd wrt 1st) sec",st2[0]-st1[0]
    print "Duration difference (2nd vs 1st) sec (optimal = 0)",(st2[1]-st2[0])-(st1[1]-st1[0])
    print "Duration Ratio (2nd over 1st) sec (optional = 1.0)",(st2[1]-st2[0])/(st1[1]-st1[0])
    print "Duration Ratio (2nd over 1st) frames (optional = 1.0)",(st2[1]-st2[0])*fps2/((st1[1]-st1[0])*fps1)

if __name__ == '__main__':
	main()