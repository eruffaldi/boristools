import sys,os,json,argparse,csv


def main():
    duration = 0

    parser = argparse.ArgumentParser(description='Build BORIS from data')
    parser.add_argument('--input',help="input BORIS file to load",required=True)
    parser.add_argument('--observation',help="which observation to modify if need to be forced")
    parser.add_argument('--csvinput',help="which csv import (e.g. format of boris2table): event,key,start,stop,subject",required=True)
    parser.add_argument('--output',help="output JSON BORIS",required=True)
    parser.add_argument('--removeevents',help="remove observations from template",action="store_true")

    args = parser.parse_args()

    print "loading boris",args.input
    j = json.load(open(args.input,"rb"))
    print "loading csv",args.csvinput
    p = csv.DictReader(open(args.csvinput,"rb"))
    alld = [d for d in p]
    print "processing"

    focuskey = args.observation

    # build list of relevant observation keys
    if focuskey is None:    
        allkeys = set([d["key"] for d in alld])
    else:
        allkeys = set([focuskey])

    if args.removeevents:
        print "removing existing events"
        for k in allkeys:
            j["observations"][k]["events"] = []

    # for all events as dictionary
    print "generating"
    for d in alld:
        key = focuskey if focuskey is not None else d["key"]
        event = d["event"]
        start = d["start"]
        stop = d["stop"]
        subject = d["subject"]

        # output event: time subject event ignore ignore
        e = [start,subject,event,"",""]
        j["observations"][key]["events"].append(e)
        if stop != start:
            # we put out of order, then we'll reorder by time
            e = [stop,subject,event,"",""]
            j["observations"][key]["events"].append(e)

    # reorder all the events by start
    print "reordering"
    for k in allkeys:
        j["observations"][key]["events"].sort(key = lambda x: x[0])


    print "emitting"
    json.dump(j,open(args.output,"wb"),sort_keys=True,indent=4, separators=(',', ': '))


if __name__ == '__main__':
    main()