#!/usr/bin/python

import os
import xml.etree.ElementTree as ET
import re
import pdb
from experiment import *
import pickle

repairRE = re.compile(r'=([^>\s]+)')

def checkItem(setup, word):
    try:
        if not word.lexsn: #there are elements that are not tagged still
            return False
        else:
            return word.value in setup["words"] or setup["words"] == "*" or not "words" in setup
    except AttributeError:
        return False


def extractData(dirname, setup, outfile):
    datapoints = []
    def replMatch(m):
        return '="%s"' % m.groups()[0]
        
    for fname in os.listdir(dirname):
        fd = open(os.path.join(dirname, fname))
#        parsed = html.fromstring(mytext)
#        for x in parsed.getiterator(): print x.tag, x.attrib, x.text, x.tail

        data = fd.read()
        dataFixed = repairRE.sub(replMatch, data) #put quotes around attributes
        dataFixed = dataFixed.replace('<punc>&</punc>', '<punc>&amp;</punc>')
        dataFixed = dataFixed.replace('""', '"')
        dataFixed = dataFixed.replace('rdf= ', 'rdf="" ')

        try:
            tree = ET.fromstring(dataFixed) #parse into xml
            #now look for all sentences
            #look for <context> <p> <s> treelets"
            for sent in tree.findall('context/p/s'):
                sentNum = sent.attrib['snum']
                words = sent.getchildren()
                tokens = [Token(word.attrib, word.text) for word in words]
                for i in range(len(tokens)):
                    tok = tokens[i]
                    if checkItem(setup, tok):
                        allElse = tokens[0:i]
                        allElse.extend(tokens[i+1:])
                        dp = Datapoint(tok)
                        dp.setContext(allElse)
                        dp.setMetadata(fname, sentNum)
                        datapoints.append(dp)
        except KeyError:
            print fname
            fo = open(fname, "w")
            fo.write(dataFixed)
            fo.close()
            next
        fd.close()
    try:
        fout = open(outfile, "w")
        pickle.dump(datapoints, fout, protocol=2)
        fout.close()
    except:
        print "Error saving"


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Take a directory of semcor files and spit out a pickled representation of each token as its own Datapoint object, with context.')
    parser.add_argument('dirname', metavar='d', type=str, 
                       help='the directory with the files')

    parser.add_argument('experimentfile', metavar='e', type=str, 
                       help='the json specifying the parameters of the experiment')
        
    parser.add_argument('outfile', metavar='o', type=str, 
                       help='the location of the pickled object')
                       
    args = parser.parse_args()

    import json                       
    
    expSetup = json.load(open(args.experimentfile))
    
    extractData(args.dirname, expSetup, args.outfile)
    print args.dirname
    