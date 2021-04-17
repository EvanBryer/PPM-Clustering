import argparse
parser = argparse.ArgumentParser(description='Perform Sillhouette analysis for k-means clustering.')
req = parser.add_argument_group('Required arguments')
req.add_argument("-p", "--path", help="path to file of new line delimited strings.", required=True)
parser.add_argument("-r", "--radius", help="Radius for PPM clustering. Default is 2.0", type=float, default=2.0)
parser.add_argument("-o", "--out", help="Output file containing clustered data. Default is ./out.txt", default="./out.txt")
req = parser.parse_args()
import ppmd
import io
from datetime import datetime

startTime = datetime.now()

#Select radius for clusters
radius = req.radius
#Path to files
f1 = open(req.path).readlines()
out = open(req.out,"w+")
#PPM compression algorithm
def compress(title):
	byt = str.encode(title)
	with io.BytesIO() as dst:
		with ppmd.Ppmd8Encoder(dst, 7, 16 << 20, 0) as encoder:
		    encoder.encode(byt)
		    encoder.flush()
		dst.seek(0)
		result = dst.getvalue()
	return result

#Find the distance between the two compressed strings
def dist(str1, str2):
	num = len(compress(str1+str2)) + len(compress(str2+str1))
	denom = len(compress(str1+str1)) + len(compress(str2+str2))
	return num/denom

def toFile():
	for i in f1:
		out.write(i)
	print(datetime.now()-startTime)

#Go through all strings to find clusters
val = 0
used = []
for s1 in f1:
	cluster = [s1]
	inds = [val]
	if val in used:
		continue
	for i in range(val+1, len(f1)):
		s2 = f1[i]
		if(abs(len(s1)-len(s2)) < 5):
			d = 10.0 * (dist(s1,s2) - 1.0)
			if d <= radius:
				cluster.append(s2)
				inds.append(f1.index(s2))
				used.append(val)
	print(cluster)
	val = val + 1
	for v in inds:
		used.append(v)
toFile()

