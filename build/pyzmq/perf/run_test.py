import re,time
import sys
from subprocess import Popen,PIPE

from local_lat import main as local_lat
from local_thr import main as local_thr
from remote_lat import main as remote_lat
from remote_thr import main as remote_thr

def run_thr(args):
    local = Popen('python local_thr.py'.split()+args,stdout=PIPE,stdin=PIPE)
    remote = Popen('python remote_thr.py'.split()+args,stdout=PIPE,stdin=PIPE)
    remote.wait()
    local.wait()
    out,_ = local.communicate()
    lines = out.splitlines()
    result = lines[-1]
    throughput = re.findall(r'[0-9\.]+',result)[0]
    return float(throughput)
    
def run_lat(args):
    local = Popen('python local_lat.py'.split()+args,stdout=PIPE,stdin=PIPE)
    remote = Popen('python remote_lat.py'.split()+args,stdout=PIPE,stdin=PIPE)
    line = ''
    while 'latency' not in line:
        line = remote.stdout.readline()
    if 'latency' in line:
        latency = re.findall(r'[0-9\.]+',line)[0]
    remote.wait()
    local.wait()
    return float(latency)

def multi_lat(args, n=3):
    lats = [ run_lat(args) for i in xrange(3) ]
    avg = sum(lats) / len(lats)
    return avg,min(lats),max(lats)

def multi_thr(args, n=3):
    thrs = [ run_thr(args) for i in xrange(3) ]
    avg = sum(thrs) / len(thrs)
    return avg,min(thrs),max(thrs)

def generate_vs_msg_size(nmsgs, msg_sizes=[2**p for p in range(6,21)], samples=5):
    print nmsgs
    x = msg_sizes
    thr = []
    lat = []
    for msg_size in msg_sizes:
        args = ('tcp://127.0.0.1:12345 %i %i'%(msg_size, nmsgs)).split()
        thr.append(multi_thr(args,samples))
        print 'thr: %i %s'%(msg_size, thr[-1])
        lat.append(multi_lat(args,samples))
        print 'lat: %i %s'%(msg_size, lat[-1])
    return x,thr,lat

def generate_vs_nmsgs(msg_size, nmsgs_s=[2**p for p in range(4,14)], samples=5):
    print msg_size
    x = nmsgs_s
    thr = []
    lat = []
    for nmsgs in nmsgs_s:
        args = ('tcp://127.0.0.1:12345 %i %i'%(msg_size, nmsgs)).split()
        thr.append(multi_thr(args,samples))
        print 'thr: %i %s'%(nmsgs, thr[-1])
        lat.append(multi_lat(args,samples))
        print 'lat: %i %s'%(nmsgs, lat[-1])
    return x,thr,lat
    
    
def do_plot(x,thr,lat, ref=1024, vs='nmsgs'):
    import pylab
    pylab.figure()
    if vs == 'msg_size':
        title = "%i msgs"%ref
        xlabel = "msg size (B)"
    else:
        title = "msg size = %i B"%ref
        xlabel = "nmsgs"
    pylab.grid(True, which='major')
    # pylab.grid(True, which='minor')
    pylab.title(title)
    pylab.xlabel(xlabel)
    t_a,t_min,t_max = zip(*thr)
    pylab.loglog(x,t_a,'b',label='throughput')
    pylab.loglog(x,t_min,'b:')
    pylab.loglog(x,t_max,'b:')
    pylab.ylabel("Mb/s")
    pylab.legend(loc='upper left')
    ax2 = pylab.twinx()
    l_a,l_min,l_max = zip(*lat)
    pylab.loglog(x,l_a,'g',label='latency')
    pylab.loglog(x,l_min,'g:')
    pylab.loglog(x,l_max,'g:')
    pylab.ylabel("msec")
    pylab.legend(loc='upper right')
    
