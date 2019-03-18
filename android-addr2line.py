#!/usr/bin/python
import sys, getopt, os, re, subprocess
    
def main(argv):
    dump_file = ''
    sym_file = ''
    try:
        opts, args = getopt.getopt(argv,"hs:d:",["sym=","dump="])
    except getopt.GetoptError:
        print 'android_addr2line.py --sym <sym file> --dump <dump file>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'android_addr2line.py --sym <sym file> --dump <dump file>'
            sys.exit()
        elif opt in ("-s", "--sym"):
            sym_file = arg
        elif opt in ("-d", "--dump"):
            dump_file = arg

    print "###start with### dumpfile: "+dump_file + "### symfile: " + sym_file

    dump_f = open(dump_file, 'r')

    for line in dump_f.readlines():
        address = get_address(line)
        if address is not None:
            source = get_source_line(address,sym_file)
	    x = line.split('(')
            print x[0] + str(source)
        else:
            print line

def get_address(line):
    search = re.search('#[0-9]{2} +pc +([0-9A-Fa-f]{8}) +/data', line)
    if search is None:
        return None
    else:
        return search.groups(1)[0]

#should export the path of arm-linux-androideabi-addr2line from ndk
def get_source_line(address, symfile):
    output = subprocess.check_output(['arm-linux-androideabi-addr2line', '-C', '-f', '-e', symfile, address]).split('\n')
    return (output[0], output[1])


if __name__ == '__main__':
    main(sys.argv[1:])
