import sys,os,subprocess,json,argparse

def main():
	duration = 0

    parser = argparse.ArgumentParser(description='Build BORIS from data')
    parser.add_argument('--template',help="template BORIS file to load")
    parser.add_argument('--videopath',help="path with mp4 to scan")
    parser.add_argument('--output',help="output JSON BORIS")
    parser.add_argument('--removeobs',help="remove observations from template",action="store_true")

    args = parser.parse_args()

	d = args.videopath

	if args.template is not None:
		j = json.load(open(args.template,"rb"))
		jos = j["observations"]
		if args.removeobs:
			jos.clear()
	else:
		j = {}
		j["independent_variables"] = {}
		jos = {}
		j["observations"] = jos
		j["subjects_conf"] = {}
		j["project_name"] = "Vigilante"
		j["behavioral_categories"] = []
		j["project_description"] = ""
		j["coding_map"] = {}
		j["project_format_version"] = "1.6"
		j["time_format"] = "hh:mm:ss"
		j["project_date"] = "2017-04-28T23:25:55"
		j["behaviors_conf"] = {}		

	for x in os.listdir(d):
		if x.endswith(".mp4"):
			fp = os.path.join(d,x)
			jfp = fp + ".json"
			if not os.path.isfile(jfp):
				os.system("ffprobe -v quiet -print_format json -show_format -show_streams \"%s\" > \"%s\"" % (fp,jfp))
			if os.path.isfile(jfp):
				q = json.load(open(jfp,"rb"))
				if  "streams" in q:
					du = float(q["streams"][0]["duration"])
					fa,fb = [float(ff) for ff in q["streams"][0]["avg_frame_rate"].split("/")]
					fps = fa/fb
					duration += du
					name = x.split("_")[0]
					jo = {}
					jos[name] = jo
					jo["time offset"] = 0.0
					jo["independent_variables"] = {}
					jo["visualize_spectrogram"] = False
					jo["time offset second player"] = 0
					jo["file"] = {}
					jo["date"] = "2017-04-28T23:31:17"
					jo["events"] = []
					jo["media_info"] = dict(fps={},hasVideo={},length={},hasAudio={})
					jo["media_info"]["fps"][fp] = fps
					jo["media_info"]["hasVideo"][fp] = True
					jo["media_info"]["length"][fp] = du
					jo["media_info"]["hasAudio"][fp] = False
					jo["file"]["1"] = [fp]
					jo["file"]["2"] = []
					jo["description"] = x
					jo["type"] = "MEDIA"
					jo["close_behaviors_between_videos"] = False
				else:
					print "issue with json of",fp
			else:	
				print "cannot scan",fp	
	json.dump(j,open(args.output,"wb"),sort_keys=True,indent=4, separators=(',', ': '))


if __name__ == '__main__':
	main()

