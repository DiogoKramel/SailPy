# http://www.shiplab.hials.org/app/shipmotion/
import numpy as np
import json, codecs

def motion(criticaldamping, heading, delta, vboatmed, position, waveamplitude):
    dimensions_obj = codecs.open('output/dimensions.json', 'r', encoding='utf-8').read()
    dimensions = json.loads(dimensions_obj)
    cb = np.float(dimensions["cb"])
    draft = np.float(dimensions["tc"])
    bwl = np.float(dimensions["bwl"])
    lwl = np.float(dimensions["lwl"])
    cwp = np.float(dimensions["cwp"])
    gm = np.float(dimensions["gmt"])
    
    #cwp = 0.715
    #gm = 4.2
    #lwl = 96
    #cb = 0.53
    #bwl = 14
    #draft = 2.5
    #criticaldamping = 0.2       # empirical damping ratio (porcentagem/100)
    #delta = 0.6         # prismatic length ratio
    #heading = 90        # wave incident angle in degrees
    #vboatmed = 10      # output from vpp in knots
    #position = 0       # relative position to CG in %
    #waveamplitude = 1
    criticaldamping = np.float(criticaldamping)/100
    delta = np.float(delta)/100
    heading = np.float(heading)
    vboatmed = np.float(vboatmed) 
    position = np.float(position)
    waveamplitude = np.float(waveamplitude)
    
    betha = np.radians(heading)
    wavefrequency = np.zeros(1000)
    waveperiod = np.zeros(1000)
    verticalmovement = np.zeros(1000)
    verticalacceleration = np.zeros(1000)
    pitchmovement = np.zeros(1000)
    heavemovement = np.zeros(1000)
    bendingmoment = np.zeros(1000)
    rollmovement = np.zeros(1000)

    g = 9.81;            
    breadth = bwl*cb
    speed = vboatmed*0.5144444
    fn = speed/(g*lwl)**0.5
    position = lwl*position/200

    for i in range (0, 1000):
        wavefrequency[i] = 0.05+1.95*i/1000
        wavenumber = wavefrequency[i]**2/g
        effwavenumber = np.absolute(wavenumber*np.cos(betha))
        smithfactor = np.exp(-wavenumber*draft)
        alpha = 1-fn*(wavenumber*lwl)**0.5*np.cos(betha)
        sectionalhydrodamping = 2*np.sin(0.5*wavenumber*breadth*alpha**2)*np.exp(-wavenumber*draft*alpha**2)
        a = (1-wavenumber*draft)**2
        b = (sectionalhydrodamping**2/(wavenumber*breadth*alpha**3))**2
        f = (a+b)**0.5
        F = smithfactor*f*(2/(effwavenumber*lwl))*np.sin(effwavenumber*lwl/2)
        G = smithfactor*f*(24/((effwavenumber*lwl)**2*lwl))*(np.sin(effwavenumber*lwl/2)-(effwavenumber*lwl/2)*np.cos(effwavenumber*lwl/2))
        eta = 1/((1-2*wavenumber*draft*alpha**2)**2+(sectionalhydrodamping**2/(wavenumber*breadth*alpha**2))**2)**0.5
        FRFheave=waveamplitude*eta*F
        FRFpitch=waveamplitude*eta*G

        verticalmovement[i] = (FRFheave**2+FRFpitch**2*position**2)**0.5
        verticalacceleration[i] = alpha**2*wavenumber*g*verticalmovement[i]
        pitchmovement[i] = (FRFpitch**2*position**2)**0.5
        heavemovement[i] = np.absolute(FRFheave)
                
        # bending moment responses
        phi = 2.5*(1-cb)
        fcb = (1-phi)**2+0.6*alpha*(2-phi) 
        fv = 1+3*fn**2   
        bendingmoment[i] = waveamplitude*(smithfactor*((1-wavenumber*draft)/(lwl*effwavenumber)**2)*(1-np.cos(effwavenumber*lwl/2)-(effwavenumber*lwl/4)*np.sin(effwavenumber*lwl/2))*fv*fcb*(np.absolute(np.cos(betha)))**(1/3))*1025*g*bwl*lwl**2/200000
        # tem um problem em algum lugar porque eu nao devia ter dividido tudo por 20000

    ####### ROLL
    rollhydrodamping = 1;
    excitationfrequency=10000000;
    B0 = bwl

    tn = 0.85*bwl*10/gm**0.5/10               # estimated tn value 
    restoringmomentcoeff = g*1025*cb*lwl*bwl*draft*gm

    for i in range (0, 1000):
        wavefrequency[i] = 0.05+1.95*i/1000
        waveperiod[i] = 2*np.pi/wavefrequency[i]
        wavenumber = wavefrequency[i]**2/g
        alpha = 1-fn*(wavenumber*lwl)**0.5*np.cos(betha)
        encounterfreq = wavefrequency[i]*alpha
        effwavenumber = np.absolute(wavenumber*np.cos(betha))

        breadthratio = (cwp-delta)/(1-delta)
        B1 = breadthratio*B0
        A0 = cb*B0*draft*(delta*breadthratio*(1-delta))
        A1 = breadthratio*A0

        # sectional damping coefficient
        breadthdraftratio = B0/draft
        if breadthdraftratio>3:
            a0 = 0.256*breadthdraftratio-0.286
            b0 = -0.11*breadthdraftratio-2.55
            d0 = 0.033*breadthdraftratio-1.419
            a1 = 0.256*breadthdraftratio-0.286
            b1 = -0.11*breadthdraftratio-2.55
            d1 = 0.033*breadthdraftratio-1.419
        else:
            a0 = -3.94*breadthdraftratio-13.69
            b0 = -2.12*breadthdraftratio-1.89
            d0 = 1.16*breadthdraftratio-7.97
            a1 = -3.94*breadthdraftratio+13.69
            b1 = -2.12*breadthdraftratio-1.89
            d1 = 1.16*breadthdraftratio-7.97
        
        b44_0 = 1025*A0*B0**2*a0*np.exp(b0*encounterfreq**(-1.3))*encounterfreq**d0/(B0/(2*g))**0.5
        b44_1 = 1025*A1*B1**2*a1*np.exp(b1*encounterfreq**(-1.3))*encounterfreq**d1/(B1/(2*g))**0.5
        
        # total damping
        dampingratio = (b44_1/b44_0)**0.5
        b44 = lwl*b44_0*(delta+b44_1*(1-delta)/b44_0)
        add_damping = restoringmomentcoeff*tn/np.pi
        rollhydrodamping = b44+add_damping*criticaldamping

        # excitation frequency
        if heading == 90 or heading == 270:
            excitationfrequency = (1025*g**2*b44_0/encounterfreq)**0.5*(delta*dampingratio*(1-delta))*lwl
        else:
            A = np.absolute(np.sin(betha))*(1025*g**2/encounterfreq)**0.5*b44_0**0.5*2/effwavenumber
            B = (np.sin(0.5*delta*lwl*effwavenumber))**2
            C = (dampingratio*np.sin(0.5*(1-delta)*lwl*effwavenumber))**2
            D = 2*dampingratio*np.sin(0.5*delta*lwl*effwavenumber)*np.sin(0.5*(1-delta)*lwl*effwavenumber)*np.cos(0.5*lwl*effwavenumber)
            excitationfrequency = A*(B+C+D)**0.5

        A = (-(encounterfreq*tn/(2*np.pi))**2+1)**2
        B = restoringmomentcoeff**2
        C = (encounterfreq*rollhydrodamping)**2

        rollmovement[i] = waveamplitude*excitationfrequency/(A*B+C)**0.5

    return wavefrequency, verticalacceleration, heavemovement, pitchmovement, rollmovement, bendingmoment, waveperiod
