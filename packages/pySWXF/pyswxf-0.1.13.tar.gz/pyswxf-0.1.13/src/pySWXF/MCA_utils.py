import scipy.constants as scc
import numpy as np
from pySWXF.spec_utils import readscan, list_scans, get_mca_data, dtcorrect, merge_duplicates
from matplotlib import pyplot as plt
from lmfit.models import LinearModel, GaussianModel
import xraydb as xdb
from numpy import zeros

def get_mca_data(dir,fname,exposure,quiet=False):
    # exposure is the exposure time of the mca
    # If not quiet, then dtcorrect prints the dead time
    # November CLS DATA
    df = pd.read_csv(dir+fname,sep=' ',header=None)
    xy = df.to_numpy() 
    y= np.array(xy[:,1])
    dsize = 2048
    ndset = int(np.size(y)/(dsize))
    mca = np.reshape(y,(ndset,dsize))
    for i in range(ndset):
        mca[i,:] = dtcorrect(mca[i,:],exposure,quiet)
    return(mca,ndset)

def get_mca_data_DND(specfile,scanno):
    with open(specfile,'r') as fp:
        # read down to start of scan
        start = False
        mca = False
        mca_i = 0
        nmca = 0
        mca_data = []
        M_mca_data = []
        start_chan = 0
        end_chan = 2047
        channels = 2048
        data = []
        for i, line in enumerate(fp):
            if not start and '#S {0:d} '.format(scanno) in line:
                print(f'found scan {scanno:d} at line {i:d}')
                start = True
                title = line
                continue
            if start and '#L' in line:
                cnames = re.split('\s{2,}',line[3:-1]) 
                continue
            if start and '@0' in line:
                mca = True
                nmca = (end_chan-start_chan+1)
                mca_data = np.zeros(nmca)
                mca_i = 0          
            if start and mca:
                line0=line
                if mca_i == 0:
                    ifst = 1
                else:
                    ifst = 1
                if ord(line[-2]) == 92:
                    line = line[:-2]
                tdata = list(map(int,line[ifst:].split())) 
                mca_data[mca_i:min(mca_i+32,nmca)] = tdata
                mca_i += np.size(tdata)
                if mca_i == nmca:
                    M_mca_data.append(mca_data)
                    mca = False
                continue
            if start  and '#S' in line:
                start = False
    return(np.array(M_mca_data))

def dtcorrect(y,exposure,quiet):
    ''' Correct Dead Time for CLS MCA'''
    N = np.sum(y)/exposure
    tau = 4.1e-6
    N0 = fsolve(lambda N0: N - N0*np.exp(-N0*tau),N)[0] 
    if not quiet:
        print('percent dead time: {0:2.0f}'.format((1-N/N0)*100))
    return y*N0/N

def get_mca_data_CLS(dir,fname,scan_nu,quiet=True):
    # exposure is the exposure time of the mca
    # If not quiet, then dtcorrect prints the dead time
    with open(dir+fname,'r') as fd:
        mca_size = 2048
        for line1 in fd:
            if line1.startswith(f"#S {scan_nu:d}"):
                print(f'found scan {scan_nu:d}')
                line2 = fd.readline()
                line3 = fd.readline()
                line4 = fd.readline()
                line5 = fd.readline()
                line6 = fd.readline()
                npt = int(line1.split()[-1])
                mca_size = int(line3.split()[1])
                exposure = float(line4.split()[1])
                pnum = int(line5.split()[1])
                mca = zeros([npt,mca_size])
                Energy = zeros(mca_size)
                for i in range(mca_size):
                    nline = fd.readline()
                    Energy[i] =float(nline.split()[1])
                    mca[0,i] = int(nline.split()[2])
                for j in range(npt-1):
                    for k in range(8):
                        fd.readline()
                    for l in range(mca_size):
                        mca[j+1,l] = int(fd.readline().split()[2])
                break
    for i in range(npt):
                mca[i,:] = dtcorrect(mca[i,:],exposure,quiet)
    return mca,Energy

    def plot_mca_sum(datadir,fname,snum,xmin=1400,xmax=14800,scale='log'):
    mca,Energy = get_mca_data_CLS(datadir,fname,snum,True)
    mca_sum = np.sum(mca,0)
    rr = (Energy>xmin)*(Energy<xmax)
    plt.plot(Energy[rr],mca_sum[rr],'-k')
    plt.xlabel('Energy (keV)')
    plt.ylabel('counts')
    plt.yscale(scale)
    plt.title(f'{fname:s} scan {snum:d}')

def peak_label(Energy,Info,height=.8,linespec='-r'):
    ylim = plt.gca().get_ylim()
    ymul = ylim[1]/ylim[0]
    ymin = np.exp(np.log(ymul)*.2)*ylim[0]
    ymax = np.exp(np.log(ymul)*height)*ylim[0]
    plt.plot([Energy,Energy],[ymin,ymax],linespec)
    plt.text(Energy,ymax,Info)

def K_label(elem,height=.8):
    lines = xdb.xray_lines(elem,'K')
    lines = ['Ka1','Kb1']
    nlab = 0
    for line in lines:
        try:
            lE = xdb.xray_lines(elem,'K')[line][0]
            N2 = xdb.xray_lines(elem,'K')[line][1]
            if nlab == 0:
                peak_label(lE,elem,linespec='-r',height=height)
                nlab += 1
            else:
                peak_label(lE,'',linespec='--r',height=.6)
        except:
            continue

def L_label(elem,height=.8):
    edges = ['L1','L2','L3']
    for edge in edges:
        N1 = xdb.xray_edge(elem,edge)[1]
        N1 *= xdb.xray_edge(elem,edge)[2]-1
        lines = xdb.xray_lines('Au',edge)
        for line in lines:
            try:
                lE = xdb.xray_lines(elem,edge)[line][0]
                N2 = xdb.xray_lines(elem,edge)[line][1]
                if N2*N1 > .02:
                    peak_label(lE,elem,linespec='-y')
            except:
                continue
def get_br_amps(Energy,mcas,rr):
    DeltaE = (Energy[-1]-Energy[0])/2048
    dms = np.shape(mcas)
    y = np.zeros(dms[0])
    dy = np.zeros(dms[0])
    par = Br_peak_mod.make_params()
    par['A_Au'].value=1e5
    par['A_Br'].value=1e5
    par['sig'].value=111
    par['sig'].vary = 0
    par['intercept'].value=0
    par['slope'].value=0
    result = Br_peak_mod.fit(np.sum(mcas,0)[rr],x=Energy[rr],params=par)
    #nresult.plot_fit()
    par = result.params;
    par['A_Au'].value /= dms[0]
    par['A_Br'].value /= dms[0]
    for i,mca in enumerate(mcas):
        result = Br_peak_mod.fit(mca[rr],x=Energy[rr],params=par)
        y[i] = result.params['A_Br'].value/DeltaE
        dy[i] = result.params['A_Br'].stderr/DeltaE
    return y, dy

def plot_br_fluor(datadir,fspec,scans):
    if np.size(scans) == 1:
        scans =[scans]
    fvort =fspec+"_Vortex.mca"
    data,scan_info  = readscan(datadir+fspec,scans[0])
    mu = data['MU'].to_numpy()
    for i, snum in enumerate(scans):
        if i==0:
            mcas,Energy = get_mca_data_CLS(datadir,fvort,snum,True)
        else:
            tmcas,Energy = get_mca_data_CLS(datadir,fvort,snum,True)
            mcas += tmcas
    rr = (Energy>11000)*(Energy<12500)
    y,dy = get_br_amps(Energy,mcas,rr)
    plt.errorbar(mu,y,dy,fmt='ks')
    plt.xlabel('mu (deg)')
    plt.ylabel('Br fluorescence (fit) ')
    scanlist = ''
    for snum in scans:
        scanlist += f'{snum:d} '
    plt.title(f'{fspec:s} scans {scanlist:s}')
    
def get_edge_absorb(element,edge):
    Ee = xdb.xray_edge(element, edge, energy_only=True)
    delE = 50
    xlow = xdb.incoherent_cross_section_elam(element, Ee-delE)
    xhigh = xdb.incoherent_cross_section_elam(element, Ee+delE)
    del_x = xhigh-xlow 
    return del_x

def Au_L_peak(A,sig0,energy):
    E0 = 14500
    element = 'Au'
    edges = ['L1','L2','L3']
    y = energy*0
    norm = 0
    for edge in edges:
        # First get edge amplitude
        lines = xdb.xray_lines(element,edge)
        N1 = get_edge_absorb(element,edge)
        for line in lines:
                lE = xdb.xray_lines(element,edge)[line][0]
                N2 = xdb.xray_lines(element,edge)[line][1]
                N3 = xdb.fluor_yield(element, edge, line, E0)[0]
                sig = sig0*energy/Br_ka 
                arg = (energy-lE)**2/2/sig**2
                amp = 1/np.sqrt(2*np.pi*sig**2)
                y += N1*N2*N3*amp*np.exp(-arg)
                norm += N1*N2*N3
    y /= norm
    y *= A
    return y
def Br_K_peak(A,sig,energy):
    Br_ka = xdb.xray_lines('Br','K')['Ka1'][0]
    arg = (energy-Br_ka)**2/2/sig**2
    amp = A/np.sqrt(2*np.pi*sig**2)
    y = amp*np.exp(-arg)
    return y

def Br_peak_sim(x,A_Br,A_Au,sig):
     y = Br_K_peak(A_Br,sig,x)
     y += Au_L_peak(A_Au,sig,x)
     return y

Br_background = LinearModel()
Br_peak_mod = Model(Br_peak_sim)+Br_background