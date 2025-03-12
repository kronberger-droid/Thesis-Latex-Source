#Author: Karlo Jurina
#Literature: "John D. Anderson: Modern Compressible Flow With Historical Perspective"

import math
import numpy as np
import matplotlib.pyplot as plt
import sys

plotting = True

#Inputs
#=========================#
M_e = 2                         #design exit Mach number
n = 30                            #number of characteristics
D_t = 40e-6                         #throat diameter  
#=========================#  
  
gamma = 1.41     

k1 = 1+((gamma-1)/2*M_e**2)
k2 = (gamma+1)/(2*(gamma-1))
r = D_t/2
nu_e = math.sqrt((gamma+1)/(gamma-1))*math.atan(math.sqrt((gamma-1) \
        /(gamma+1)*(M_e**2-1)))-math.atan(math.sqrt(M_e**2-1))
nu_ed = nu_e*180/math.pi
thetaMax = nu_e/2
theta_start = np.linspace(0.001,thetaMax,n)
thetaD = theta_start*180/np.pi
Aratio = 1/M_e*(2*k1/(gamma+1))**k2     #ratio between Outlet and Critical Section
D_e = Aratio*D_t
N = int(n*(n+3)/2)

nui = np.zeros((n,n))
thetai = np.zeros((n,n))
C_Ii = np.zeros((n,n))
C_IIi = np.zeros((n,n))

nub = np.zeros((1,n))
thetab = np.zeros((1,n))
C_Ib = np.zeros((1,n))
C_IIb = np.zeros((1,n))
               
thetai[:,0] = theta_start
nui[:,0] = thetai[:,0]
C_Ii[:,0] = 2*nui[:,0]
C_IIi[:,0] = nui[:,0]-thetai[:,0]

for i in range(n-1):
    for j in range(n-1-i):
        if j == 0:
          thetai[j,i+1] = 0
          nui[j,i+1] = C_Ii[j+1,i]
          C_Ii[j,i+1] = nui[j,i+1]+thetai[j,i+1]
          C_IIi[j,i+1] = nui[j,i+1]-thetai[j,i+1]
        else:
          nui[j,i+1] = 1/2*(C_Ii[j+1,i]+C_IIi[j-1,i+1])  
          thetai[j,i+1] = 1/2*(C_Ii[j+1,i]-C_IIi[j-1,i+1]) 
          C_Ii[j,i+1] = nui[j,i+1]+thetai[j,i+1]
          C_IIi[j,i+1] = nui[j,i+1]-thetai[j,i+1]  
            
for i in range(n):
    thetab[0,i] = thetai[n-1-i,i]
    C_IIb[0,i] = C_IIi[n-1-i,i]
    nub[0,i] = thetab[0,i]+C_IIb[0,i]
    C_Ib[0,i] = thetab[0,i]+nui[0,i]
    
z1 = np.zeros((1,n))
nu= np.vstack((nui,z1))
theta= np.vstack((thetai,z1))
C_I= np.vstack((C_Ii,z1))
C_II= np.vstack((C_IIi,z1))

z2 = np.zeros((n+1,1))
nu= np.hstack((nu,z2))
theta= np.hstack((theta,z2))
C_I= np.hstack((C_I,z2))
C_II= np.hstack((C_II,z2))

for i in range(n):
    nu[n-i,i] = nub[0,i]
    theta[n-i,i] = thetab[0,i] 
    C_I[n-i,i] = C_Ib[0,i] 
    C_II[n-i,i] = C_IIb[0,i]
thetad = theta*180/math.pi

M = np.zeros((n+1,n+1))
mi = np.zeros((n+1,n+1))
theta_p_mi = np.zeros((n+1,n+1))
theta_m_mi = np.zeros((n+1,n+1))
fun = np.zeros((n+1,n+1))
fun1 = np.zeros((n+1,n+1))
fun2 = np.zeros((n+1,n+1))
dfun_dM = np.zeros((n+1,n+1))

for i in range(n+1):
    for j in range(n+1):
        if (j>n-i):
            continue
        elif (i == n):
            continue
        M_0 = 1.05
        gamma1 = (gamma+1)/(gamma-1)
        dM = 0.01
        fun[j,i] = (math.sqrt(gamma1)*math.atan(math.sqrt(gamma1**(-1)*\
                      (M_0**2-1)))-math.atan(math.sqrt(M_0**2-1)))\
                       -nu[j,i]
        
        while (abs(fun[j,i]) > 1e-5):
            M1 = M_0+dM
            M2 = M_0-dM
            fun1[j,i] = (math.sqrt(gamma1)*math.atan(math.sqrt(gamma1**(-1)*\
                      (M1**2-1)))-math.atan(math.sqrt(M1**2-1)))\
                       -nu[j,i]
            fun2[j,i] = (math.sqrt(gamma1)*math.atan(math.sqrt(gamma1**(-1)*\
                      (M2**2-1)))-math.atan(math.sqrt(M2**2-1)))\
                       -nu[j,i]       
            dfun_dM[j,i] = (fun1[j,i]-fun2[j,i])/(2*dM)
            fun[j,i] = (math.sqrt(gamma1)*math.atan(math.sqrt(gamma1**(-1)*\
                      (M_0**2-1)))-math.atan(math.sqrt(M_0**2-1)))\
                       -nu[j,i]
            M[j,i] = M_0-(fun[j,i]/dfun_dM[j,i])
            M_0 = M[j,i]
            mi[j,i] = math.asin(1/M[j,i])
            theta_p_mi[j,i] = theta[j,i]+mi[j,i]
            theta_m_mi[j,i] = theta[j,i]-mi[j,i]
theta_p_mid = theta_p_mi*180/math.pi
theta_m_mid = theta_m_mi*180/math.pi
mid = mi*180/math.pi     

xp = np.zeros((n+1,n+1))
yp = np.zeros((n+1,n+1))
m_I = np.zeros((n+1,n+1))
m_II = np.zeros((n+1,n+1))

for i in range(n+1):
    for j in range(n+1):
        if (j>n-i):
            continue
        elif (i == n):
            continue  
        elif (i == 0 and j<n):
            m_I[j,i] = math.tan(theta_m_mi[j,i])
        elif (i == 0 and j == n):
            m_I[j,i] = math.tan(theta[j,i])
        elif (j == n-i and i>0):
            m_I[j,i] = math.tan(1/2*(theta[j,i]\
                                          +theta[j+1,i-1]))
        else:
            m_I[j,i] = math.tan(1/2*(theta_m_mi[j,i]\
                                          +theta_m_mi[j+1,i-1]))
                
for i in range(n+1):
    for j in range(n+1):
        if (j>n-i):
            continue
        elif (i == n):
            continue  
        if (j == 0):
            m_II[j,i] = math.tan(theta_p_mi[j,i])
        else:
            m_II[j,i] = math.tan(1/2*(theta_p_mi[j,i]\
                                           +theta_p_mi[j-1,i]))
                
for i in range(n+1):
    for j in range(n+1):
        x0 = 0
        y0 = r
        if (j>n-i):
            continue
        elif (i == n):
            continue 
        if (j == 0 and i == 0):
            xp[j,i] = x0-y0/m_I[j,i]
            yp[j,i] = 0
        elif (j > 0 and i == 0):
            xp[j,i] = (y0-yp[j-1,i]+m_II[j,i]*xp[j-1,i]\
                            -m_I[j,i]*x0)/(m_II[j,i]-m_I[j,i])
            yp[j,i] = y0+m_I[j,i]*(xp[j,i]-x0)
        elif (j == 0 and i>0):
            yp[j,i] = 0
            xp[j,i] = (yp[j+1,i-1]-((-1)*yp[j+1,i-1])\
                            +((-1)*m_I[j,i])*xp[j+1,i-1]\
                            -m_I[j,i]*xp[j+1,i-1])/((-1)\
                            *m_I[j,i]-m_I[j,i])
        elif(j>0 and i >0):
            xp[j,i] = (yp[j+1,i-1]-yp[j-1,i]+m_II[j,i]*xp[j-1,i]\
                            -m_I[j,i]*xp[j+1,i-1])/(m_II[j,i]-m_I[j,i])
            yp[j,i] = yp[j+1,i-1]+m_I[j,i]*(xp[j,i]-xp[j+1,i-1])
            
Aratio1 = yp[1,n-1]/y0             #calculated ratio between outlet and critical section

#contour points
xWallPoints = np.zeros(n+1)
yWallPoints = np.zeros(n+1)

xWallPoints[0] = x0;
yWallPoints[0] = y0;
for i in range(n):
    xWallPoints[i+1] = xp[n-i,i]      
    yWallPoints[i+1] = yp[n-i,i]
    
    
    

if(plotting == True):        
    plt.figure()
    plt.grid(True)
    plt.plot([x0,xp[n,0]],[y0,yp[n,0]],'-bo')
    plt.plot([xp[1,0],xp[0,1]],[yp[1,0],yp[0,1]],'--bo')
    for i in range(n+1):
        if (i<n):
            plt.plot([x0,xp[i,0]],[y0,yp[i,0]],'--bo')
        for j in range(n+1):
            if (j>n-i):
                continue
            elif (i == n):
                continue
            elif (j<n-i):
                plt.plot([xp[j,i],xp[j+1,i]],[yp[j,i],yp[j+1,i]],'--bo')
            elif (j == n-i and i<n-1):
                plt.plot([xp[j,i],xp[j-1,i+1]],[yp[j,i],yp[j-1,i+1]],'-bo')
    for i in range(n+1):
        for j in range(i):
            if (i>1 and i<n):
                plt.plot([xp[i-j,j],xp[i-1-j,j+1]],\
                         [yp[i-j,j],yp[i-1-j,j+1]],'--bo')
                                                     
    ypf = -1*yp
    y0f = -1*y0
    plt.plot([x0,xp[n,0]],[y0f,ypf[n,0]],'-bo')
    plt.plot([xp[1,0],xp[0,1]],[ypf[1,0],ypf[0,1]],'--bo')
    for i in range(n+1):
        if (i<n):
            plt.plot([x0,xp[i,0]],[y0f,ypf[i,0]],'--bo')
        for j in range(n+1):
            if (j>n-i):
                continue
            elif (i == n):
                continue
            elif (j<n-i):
                plt.plot([xp[j,i],xp[j+1,i]],[ypf[j,i],ypf[j+1,i]],'--bo')
            elif (j == n-i and i<n-1):
                plt.plot([xp[j,i],xp[j-1,i+1]],[ypf[j,i],ypf[j-1,i+1]],'-bo')
    for i in range(n+1):
        for j in range(i):
            if (i>1 and i<n):
                plt.plot([xp[i-j,j],xp[i-1-j,j+1]],\
                         [ypf[i-j,j],ypf[i-1-j,j+1]],'--bo')


    plt.show()

#Mach number on centerline
# =============================================================================
#         Mc = np.zeros((n,1))
#         xc = np.zeros((n,1))
#         for i in range(n):
#             Mc[i] = M[0,i]
#             xc[i] = xp[0,i]
#         Mc = np.append(Mc,M[1,n-1])
#         xc = np.append(xc,xp[1,n-1])
#         
#         plt.figure()
#         plt.grid(True)
#         plt.plot(xc,Mc)
# =============================================================================
