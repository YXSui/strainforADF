import re
import os
import matplotlib.pyplot as plt
import numpy as np
################################################################################
# parameters
v,n,s,e,o,p = [],[],[],[],[],[]
r =  range(-10,11)
r.insert(10,-0.5)
r.insert(12,0.5) 
a = re.compile(r'<.+>\s+<.+>\s+Band\s+gap:\s+(.*)')
b = re.compile(r'<.+>\s+<.+>\s+(.*)\s+E.V')
c = re.compile(r'(.*)\s+A.U.')
d = re.compile(r'<.+>\s+<.+>\s+ENERGY\s+OF\s+FORMATION:\s+(.*)')
fileDir = os.listdir('/public/home/suiyuxuan/strainprl/slabz')

################################################################################
# functions
def str2float1d(k):
    for i in range(len(k)):
        k[i] = float(k[i])
    return k
    
def plotenergy():
    plt.subplot(1,2,1)
    plt.plot(r,ox,linestyle='-',marker='o',color='b')
    plt.ylabel('Energy(eV)')
    plt.xlabel('strain%')
    plt.xlim(-0.11,0.11)
    plt.subplot(1,2,2)
    plt.plot(r,ex,linestyle='-',marker='s',color='r')
    plt.ylabel('Bandgap(eV)')
    plt.xlabel('strain%')
    plt.xlim(-0.11,0.11)
    plt.show()
    
def readfile(filepath):
    with open(filepath,'rb') as f:
        for lines in f.readlines():
            line = lines.strip()
            v.append(line)
        f.close()

################################################################################
if __name__ == '__main__':
    fileDir.sort()
    for i in fileDir:
        if os.path.isdir('/public/home/suiyuxuan/strainprl/slabz/%s'%(i)):
            if os.path.exists('/public/home/suiyuxuan/strainprl/slabz/%s/logfile'%(i)):
                readfile('/public/home/suiyuxuan/strainprl/slabz/%s/logfile'%(i))
            else:
                pass
    for j in range(len(v)): 
        if a.findall(v[j]):
            m = a.findall(v[j])
            n.append(m)
        if d.findall(v[j]):
            m = d.findall(v[j])
            n.append(m)
    for i in range(len(n)):
        s.append(c.match(n[i][0]).group(1))
    str2float1d(s)
    
    for i in range(len(s)):
        if i%2 == 0:
            e.append(s[i])
        else:
            o.append(s[i])   
    
    for i in range(len(r)):
        r[i] = float(r[i])
        r[i] = r[i]/100
    
    e0 = e[0]
    e11 = e[11]
    e22 = e[22]
    e.pop(0)
    e.pop(10)
    e.pop(20)
    ex=e[10:][::-1]+e[:10]        
    ex.insert(0,e11)
    ex.insert(11,e22)
    ex.insert(22,e0)
    o0 = o[0]
    o11 = o[11]
    o22 = o[22]
    o.pop(0)
    o.pop(10)
    o.pop(20)
    ox=o[10:][::-1]+o[:10]
    ox.insert(0,o11)
    ox.insert(11,o22)
    ox.insert(22,o0)
    
    for i in range(len(ox)):
        ox[i] = ox[i]*27.211
        ex[i] = ex[i]*27.211
    
    plotenergy()
    
    t = [r,ex,ox]
    np.savetxt('strain.dat',np.array(t))