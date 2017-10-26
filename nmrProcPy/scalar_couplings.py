'''

This is a module for extracting scalar couplings

'''

import numpy as np
import lmfit

#==================== HNCOCG ===============================================
#==================== HNCOCG ===============================================

def hncocg_eq(j_current, j_others, delay, tc,jcoca,B):
    '''
    the main equation for determining the scalar couplings from the 
    HNCOCG experiment
    
    equation 6

    '''

    #estimate T2C 
    B2 = B**2.
    T2C = np.divide(1., tc*(0.75 + np.divide(B2,150.)))

    #delayDash
    delayDash = delay - np.divide(1,(2*jcoca))

    #since component
    f1 = np.sin(np.pi * j_current * delay)**2.

    #first product 
    f1_product = 1.
    for i in j_others:
        f1_product = f1_product * (np.cos(np.pi * i * delay)**2)
    
    #exponencial 
    indicie = np.divide(-2. * (delay - delayDash ), T2C)
    exp = np.power(np.e, indicie)


    #final product 
    p = j_others
    p.append(j_current)

    f2_product = 1.
    for i in p:
        f2_product = f2_product * ( np.cos(np.pi*i* delayDash)**2. )
    
    #put it all together
    working = f1*f1_product*exp
    final = np.divide(working, f2_product)


    return final

def hncocg_residual(params, icross, iref, delay, tc,jcoca,B):
    '''
    this calculates the residual that is used during the minimsation
    '''

    diffsArray = np.zeros([1,len(icross)])

    count = 0
    for intensity, jc in zip(icross, params):
        intensityRatio = np.divide(intensity, iref)

        other_jc_val = []
        for i in params:
            if i != jc:
                other_jc_val.append(params[i].value)
        

        calc = hncocg_eq(params[jc].value, other_jc_val, delay, tc,jcoca,B)

        diff = intensityRatio - calc
        diffsArray[count] = diff
    
    return diffsArray

def hncocg_intensity2coupling(icross, iref, delay, tc,B,jcoca=54.0):
    '''

    this function calculates the scalar couplings for the 
    hncocg experiment in the bruker library 

    The theory comes from:
    JS Hu + A Bax 1997  JACS 

    Parameters 
    ==========

    icross: float - ref peak intensity
    iref:   list  - list of the cross peak intensity
    delay: float  - delay for the evolution of the j-coupling 
    tc: float     - roational correlation time
    jcoca: float  - CO - Ca jcoupling constant
    B: float      - feild strength in tesla
    
    Returns
    =======
    out : lmfit object - contains the fitted J couplings in the order they appear
                         in the icross

    '''

    #set up the lmfit parameters the values we optimise are the j-couplings 
    params = lmfit.Parameters()
    for indx, entry in enumerate(icross):
        params.add('jc_'+str(indx), value=2.0, min=0., max=5.)

    print params
    out = lmfit.minimize(hncocg_residual, params, args=(icross, iref, delay, tc,jcoca,B))
    