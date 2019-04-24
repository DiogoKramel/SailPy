import numpy as np
from scipy import interpolate, optimize
import csv
import json, codecs

def vpp_solve(sailset, lwl, loa, bwl, tc, disp, lcb, lcf, cb, cm, cp, cwp, awp, alcb, am, boa, scb, kb, kg, itwp, GMtrans, bmt, fb, lr, xcea, mcrew, P, E, I, J, BAD, SL, LPG, spanR, tipcR, rootcR, tiptcksR, roottcksR, sweepRdeg, spanK, tipcK, rootcK, tiptcksK, roottcksK, sweepKdeg, marcaK, marcaR, EHM, EMDC, hsr, savefile):
    parameters=[]
    code=[]
    for index, line in enumerate(open('assets/data/dimensions.txt')):
        if index<=4:        #pular primeiras 5 linhas
            continue
        else:
            line=line.strip()
            code.append(line.split()[0])
            parameters.append(line.split()[1])
    count=0
    for name in code:
        globals()[name] =float(parameters[int(count)])  #assign parameters valeus to their names
        count+=1

    ### 2 COEFICIENTES AUXILIARES ###
    vector_delf=np.zeros(9)     #delft series
    AA=[['FroudeNo' 'a0' 'a1' 'a2' 'a3' 'a4' 'a5' 'a6' 'a7' 'a8'], [0.10, -0.0014, 0.0403, 0.047, -0.0227, -0.0119, 0.0061, -0.0086, -0.0307, -0.0553], [0.15, 0.0004, -0.1808, 0.1793, -0.0004, 0.0097, 0.0118, -0.0055, 0.1721, -0.1728], [0.20, 0.0014, -0.1071, 0.0637, 0.009, 0.0153, 0.0011, 0.0012,0.1021, -0.0648], [0.25, 0.0027, 0.0463, -0.1263, 0.015, 0.0274, -0.0299, 0.011, -0.0595, 0.122], [0.30, 0.0056, -0.8005, 0.4891, 0.0269, 0.0519, -0.0313, 0.0292, 0.7314, -0.3619], [0.35, 0.0032, -0.1011, -0.0813, -0.0382, 0.032, -0.1481, 0.0837, 0.0233, 0.1587], [0.40, -0.0064, 2.3095, -1.5152, 0.0751, -0.0858, -0.5349, 0.1715, -2.455, 1.1865], [0.45, -0.0171, 3.4017, -1.9862, 0.3242, -0.145, -0.8043, 0.2952, -3.5284, 1.3575], [0.50, -0.0201, 7.1576, -6.3304, 0.5829, 0.163, -0.3966, 0.5023, -7.1579, 5.2534], [0.55, 0.0495, 1.5618, -6.0661, 0.8641, 1.1702, 1.761, 0.9176, -2.1191, 5.4281], [0.60, 0.0808, -5.3233, -1.1513, 0.9663, 1.6084, 2.7459, 0.8491, 4.7129, 1.1089]]

    vector_incli=np.zeros(6)    #delta hull - inclinacao do casco
    BB=[['FroudeNo' 'u0' 'u1' 'u2' 'u3' 'u4' 'u5'], [0.25, -0.0268, -0.0014, -0.0057, 0.0016, -0.007, -0.0017], [0.30, 0.6628, -0.0632, -0.0699, 0.0069, 0.0459, -0.0004], [0.35, 1.6433, -0.2144, -0.164, 0.0199, -0.054, -0.0268], [0.40,-0.8659, -0.0354, 0.2226, 0.0188, -0.58, -0.1133], [0.45, -3.2715, 0.1372, 0.5547, 0.0268, -1.0064, 0.2026], [0.50, -0.1976, -0.148, -0.6593, 0.1862, -0.7489, -0.1648], [0.55, 1.5873, -0.3749, -0.7105, 0.2146, -0.4818, -0.1174]]

    vector_inclivisc=np.zeros(4)    #delta hull viscous
    CC=[['phi' 's0' 's1' 's2' 's3'], [5, -4.112, 0.054, -0.027, 6.329], [10, -4.522, -0.132, -0.077, 8.738], [15, -3.291, -0.389, -0.118, 8.949], [20, 1.85, -1.2, -0.109, 5.364], [25, 6.51, -2.305, -0.066, 3.443], [30, 12.334, -3.911, 0.024, 1.767], [35, 14.648, -5.182, 0.102, 3.497]] 

    vector_keel=np.zeros(4)         # keel
    DD=[['FroudeNo' 'A0' 'A1' 'A2' 'A3'], [0.2, -0.00104, 0.00172, 0.00117, -0.00008], [0.25, -0.0055, 0.00597, 0.0039, -0.00009], [0.3, -0.0111, 0.01421, 0.00069, 0.00021], [0.35, -0.00713, 0.02632, -0.00232, 0.00039], [0.4, -0.03581, 0.08649, 0.00999, 0.00017], [0.45, -0.0047, 0.11592, -0.00064, 0.00035], [0.5, 0.00553, 0.07371, 0.05991, -0.00114], [0.55, 0.04822, 0.0066, 0.07048, -0.00035], [0.6, 0.01021, 0.14173, 0.06409, -0.00192]]

    ### 1.5 Converting radians parameters to degree and mass to volume and declaring empty array
    pi=np.pi
    sweepR=np.radians(sweepRdeg)              #rudders sweep angle
    sweepK=np.radians(sweepKdeg)              #keels sweep angle

    ### 1.6 Configuracao dos ventos de incidencia
    if marcaS==1 or marcaS==4:                #S=1 main and genoa S=4 main S=2 main and spin S=3 main, genoa and spin
        betatwdeg=np.arange(30,181,5)         #true wind angle from 30 to 180 degrees
        initialguess=np.array([np.radians(5),4,np.radians(15),np.radians(-4)])
    if marcaS==2 or marcaS==3:                #in case there is a spinnaker
        betatwdeg=np.arange(120,181,5)
        initialguess=np.array([np.radians(0),3.7,np.radians(20),np.radians(-10)])
    betatw=np.radians(betatwdeg)
    veltw=np.arange(3.08667,11.31779,1.02889)                   #true wind speed evaluated from 5 to 20 m/s
    len_betatw=np.size(betatw)
    len_veltw=np.size(veltw)
    vboatfinal,betatwfinal=np.zeros((len_veltw,len_betatw)),np.zeros((len_veltw,len_betatw))

    ### 2. VPP E OTIMIZACAO
    def vpp_solve2(solution):
        leeway=solution[0]     #declarar as quatro variaveis que resolvem o problema
        vboat= solution[1]
        heel= solution[2]
        deltaR=solution[3]
        
        vboat=abs(vboat)
        leeway=abs(leeway)
        alfaK=np.arcsin(np.sin(leeway)*np.cos(heel))
        
        Fn=(vboat)/(grav*lwl)**0.5                 #Froud number
        dimcan=divcan*rho                          #mass displacement
        tcks=(tiptcksR+roottcksR)/2
        tcksK=(tiptcksK+roottcksK)/2

        ### 2.1 Wind info and aerodynamic data ###
        #apparent wind
        velaw=(vboat**2+veltw[t]**2-2*vboat*veltw[t]*np.cos(pi-leeway-betatw[u]))**0.5
        betaaw=np.arctan2((veltw[t]*np.sin(betatw[u])-vboat*np.sin(leeway)),(veltw[t]*np.cos(betatw[u])+vboat*np.cos(leeway)))
        
        #heel e leeway com sinais opostos
        if leeway>0 and heel>0:
            heel=-heel
        if leeway<0 and heel<0:
            heel=-heel

        ### 2.2 Resistance ###
        ### 2.2.1 Viscous forces
        ### 2.2.1.1 Keel
        cmK=(rootcK+tipcK)/2
        ReK= ((vboat)*cmK)/ni
        CfK=(0.075/((np.log(ReK)/np.log(10))-2)**2)-(1800/ReK)
        SK=cmK*spanK            #SK: lateral surface of the keel = cordamedia*span
        SwK=2*SK                #SwK: wetted surface of the keel
        if marcaK==1:
            kK=2*(tcksK)+60*(tcksK)**4                  #NACA 4 dig  
        else:
            kK=1.2*(tcksK)+70*(tcksK)**4                #NACA 6 dig 
        RvK=0.5*rho*vboat**2*CfK*(1+kK)*SwK
        ### 2.2.1.2 Rudder 
        cmR=(rootcR+tipcR)/2
        ReR=((vboat)*cmR)/ni
        CfR=(0.075/((np.log(ReR)/np.log(10))-2)**2)-(1800/ReR)
        SR=cmR*spanR
        SwR=2*SR
        if marcaR==1:
            kR=2*(tcks)+60*(tcks)**4                      #NACA 4 dig  
        else:
            kR=1.2*(tcks)+70*(tcks)**4                   #NACA 6 dig 
        RvR=0.5*rho*vboat**2*CfR*(1+kR)*SwR
        ### 2.2.1.3 Bulb
        if lbK>0:
            ReB=((vboat)*lbK)/ni
            CfB=(0.075/((np.log(ReB)/np.log(10))-2)**2)-(1800/ReB)
            RvB=0.5*rho*vboat**2*CfB*SbK
        else:
            RvB=0
        ### 2.2.1.4 Canoe Body
        scb=(1.97+0.171*(bwl/tcan))*((0.65/cm)**(1/3))*(divcan*lwl)**0.5
        Recb=(0.7*lwl*(vboat))/ni
        kcb=0.09
        Cfcb=(0.075/((np.log(Recb)/np.log(10))-2)**2)-(1800/Recb)
        Rvcb=0.5*rho*vboat**2*Cfcb*(1+kcb)*scb

        ### 2.2.2 Forcas de sustentacao tridimensionais
        ### 2.2.2.1 Keel 
        AReK=2*spanK**2/SK
        dcl=2*pi*AReK/(2+np.cos(sweepK)*(AReK**2/(np.cos(sweepK))**4+4)**0.5)
        CtipK=1
        Lcb_fact=1
        LK=0.5*rho*(vboat**2)*CtipK*dcl*alfaK*Lcb_fact*SK

        ### 2.2.2.2 Leme (inclui efeitos de superficie livre e interacao com casco e quilha)
        deltaR0=0
        alfaR0=np.arcsin(-np.cos(heel)*np.sin(deltaR0)+np.sin(leeway)*np.cos(deltaR0)*np.cos(heel))
        angle=-np.cos(heel)*np.sin(deltaR)+np.sin(leeway)*np.cos(deltaR)*np.cos(heel)
        if angle < 0.9 and angle > -0.9: 
            alfaR = np.arcsin(angle)
        else:
            alfaR = 0

        # reducao do angulo de ataque no leme devido ao downwash da quilha (ref. Oossanen 4.3.10)
        alfaIk=1.5*((lr/(3*cmK))**0.25)*LK/(0.5*rho*(vboat**2)*SK)/(pi*AReK)
        alfaR0=alfaR0-alfaIk
        alfaR=alfaR-alfaIk

        # calculo do efeito de superficie livre sobre a ARe (ref. Oossanen 4.3.6)
        fsr=1-hsr/(cmR/4)
        FnR=vboat/(grav*cmR)**0.5

        if fsr>0:
            if FnR<=0.5:
                FAReR=2
            elif FnR>0.5 and FnR<0.6413:
                FAReR=4.246*FnR-0.1230
            else:
                FAReR =1+0.422/(FnR)**3
            AReR=fsr*FAReR*(spanR**2/SR)
        else:
            AReR=2*(spanR**2/SR)

        # reducao da velocidade do leme na esteira do veleiro (ref. Oossanen 4.3.10)
        w=0.10+4.5*(tcan/(hsr+spanR))*cb*cp*bwl/(lwl*cwp*(7-6*cb/cwp)*(2.8-1.8*cp))
        CtipR=1-0.135/AReR**(2/3)
        dclR=2*pi*AReR/(2+np.cos(sweepR)*(AReR**2/(np.cos(sweepR))**4+4)**0.5)
        LR0=0.5*rho*(((1-w)*vboat)**2)*CtipR*dclR*alfaR0*SR
        LR=0.5*rho*(((1-w)*vboat)**2)*CtipR*dclR*alfaR*SR

        ### forcas de Sustentacao no plano Horizontal 
        if lbK>0 and AbK>0: 
            Sfbulb=0.5*rho*(vboat**2)*(0.5*pi*lbK**2+1.8*AbK*abs(alfaK))*alfaK
        else:
            Sfbulb=0
        Sfcb=0.5*rho*(vboat**2)*(0.5*pi*tcan**2+1.8*alcb*abs(alfaK))*alfaK

        ### 2.2.3  Resistencia Induzida
        ### 2.2.3.1 Keel
        TR=tipcK/rootcK
        sig=(0.012-0.057*TR+0.095*TR**2-0.04*TR**3)*AReK
        Ri_K=((LK**2)*(1+sig))/(0.5*rho*(vboat**2)*SK*pi*AReK) 

        ### 2.2.3.2 Hull
        AReCb=2*tcan/(0.75*lwl)
        Ri_Cb=(Sfcb/np.cos(heel))**2/(0.5*rho*vboat**2*alcb*pi*AReCb)

        ### 2.2.3.3 Rudder
        TRr=tipcR/rootcR
        sigR=(0.012-0.057*TRr+0.095*TRr**2-0.04*TRr**3)*AReR
        Ri_R=((LR**2)*(1+sigR))/(0.5*rho*(vboat**2)*SR*pi*AReR)

        Ri=Ri_R+Ri_Cb+Ri_K

        ### 2.2.4 Resistencia Residual
        ### 2.2.4.1 Procura e interpola os coeficientes de Delft
        if Fn>0.6:
            Fn1=0.6
        if Fn<0.1:
            Fn1=0.1
        else:
            Fn1=Fn
            
        for k in range (1,10,1):
            if float(AA[k][0])<=Fn1 and Fn1<=float(AA[k+1][0]):
                XX=[float(AA[k][0]),float(AA[k+1][0])]
                for j in range (1,10,1):
                    YY=[float(AA[k][j]),float(AA[k+1][j])]
                    vector_delf[j-1]=interpolate.interp1d(XX,YY)(Fn1)

        if marcaawp==1:             #estimativa de Gerritsma
            awp=(1.313*cp+0.0371*(lwl/(divcan)**(1/3))-0.0857*cp*(lwl/(divcan)**(1/3)))*lwl*bwl
        LCBfpp=(lwl/2)-lcb          #entrada LCB e contada pela secao central, preciso da contada a partir da secao frontal
        LCFfpp=(lwl/2)-lcf           #idem LCB

        if Fn1<0.1:
            Rr=0
        else:
            Rr=divcan*rho*grav*(vector_delf[0]+(vector_delf[1]*LCBfpp/lwl+vector_delf[2]*cp+vector_delf[3]*divcan**(2/3)/awp+vector_delf[4]*bwl/lwl)*divcan**(1/3)/lwl+(vector_delf[5]*divcan**(2/3)/scb+vector_delf[6]*LCBfpp/LCFfpp+vector_delf[7]*(LCBfpp/lwl)**2+vector_delf[8]*cp**2)*divcan**(1/3)/lwl)

        ### 2.2.4.2 Procura e interpola os coeficientes de Inclinacao
        if Fn>0.55:
            Fn2=0.55
        if Fn<0.25:
            Fn2=0.25
        else:
            Fn2=Fn

        for k in range (1,7,1):
            if float(BB[k][0])<=Fn2 and Fn2<=float(BB[k+1][0]):
                SS=[float(BB[k][0]),float(BB[k+1][0])]
                for j in range(1,7,1):
                    TT=[float(BB[k][j]),float(BB[k+1][j])]
                    vector_incli[j-1]=interpolate.interp1d(SS,TT)(Fn2)

        vector_incli[:] = [x / 1000 for x in vector_incli]

        ### 2.2.4.3 Procura e interpola os coeficientes viscosos de inclinacao
        if (abs(heel))>0.35:
            heel2=0.35
        else:
            heel2=abs(heel)
        heel2=np.degrees(heel2)

        for k in range (1,7,1):
            if float(CC[k][0])<=heel2 and heel2<=float(CC[k+1][0]):
                UU=[float(CC[k][0]),float(CC[k+1][0])]
                for j in range (1,5,1):
                    VV=[float(CC[k][j]),float(CC[k+1][j])]
                    vector_inclivisc[j-1]=interpolate.interp1d(UU,VV)(heel2)

        ### 2.2.4.4 Procura e interpola os coeficientes de Delft Para a Quilha
        if Fn>0.6:
            Fn3=0.6
        if Fn<0.2:
            Fn3=0.2
        else:
            Fn3=Fn
            
        for k in range (1,9,1):
            if float(DD[k][0])<=Fn3 and Fn3<=float(DD[k+1][0]):
                ZZ=[float(DD[k][0]),float(DD[k+1][0])]
                for j in range (1,5,1):
                    WW=[float(DD[k][j]),float(DD[k+1][j])]
                    vector_keel[j-1]=interpolate.interp1d(ZZ,WW)(Fn3)

        # estimativas de Zcbk e Disp_k, caso nao fornecidos
        zcbK=spanK*(2*tipcK+rootcK)/(3*(tipcK+rootcK))
        dispK=0.6*spanK*tcksK*cmK**2

        # resistencia residual da quilha
        if Fn3<0.2:
            Rrk=0
        else:
            Rrk=dispK*rho*grav*(vector_keel[0]+vector_keel[1]*((tcan+spanK)/bwl)+vector_keel[2]*((tcan+zcbK)**3/dispK)+vector_keel[3]*(divcan/dispK))

        ### 2.2.4.5 Acrescimo da Resistencia residual devido a inclinacao
        if Fn2<0.25:
            Rincli20=0
        else:
            Rincli20=divcan*rho*grav*(vector_incli[0]+vector_incli[1]*lwl/bwl+vector_incli[2]*bwl/tcan+vector_incli[3]*(bwl/tcan)**2+vector_incli[4]*lcb+vector_incli[5]*lcb**2)
        Rincli=Rincli20*6*abs(heel)**1.7

        ### 2.2.4.6 Acrescimo da Resistencia residual da quilha devido a inclinacao
        CH=-3.5837*(tcan/(tcan+spanK))-0.0518*(bwl/tcan)+0.5958*(tcan/(tcan+spanK))*(bwl/tcan)+0.2055*(lwl/divcan**(1/3))
        Rinclik=dispK*rho*grav*CH*Fn**2*abs(heel)

        ### 2.2.4.7 Acrescimo da resistencia viscosa devido a inclinacao - inclinacoes menores
        #do que 5 grau sao aproximadas pela situacao sem inclinacao - inclinacoes
        #maiores do que 35 graus sao aproximadas por uma inclinacao de 35 graus
        if abs(heel)<np.radians(5):
            Scbincl=scb
        else:
            Scbincl=scb*(1+1/100*(vector_inclivisc[0]+vector_inclivisc[1]*bwl/tcan+vector_inclivisc[2]*(bwl/tcan)**2+vector_inclivisc[3]*cm))
        Rvcb=0.5*rho*vboat**2*Cfcb*(1+kcb)*Scbincl
        Rv=Rvcb+RvR+RvK+RvB

        ### 2.2.4.8 Decomposicao das forcas [i j k] 
        # matriz de mudanca de base da quilha Lb0=Mb0_bteta*Lbteta
        a=np.matrix([[1, 2], [3, 4]])
        Mb0_bteta=np.matrix([[1,0,0],[0,np.cos(heel),-np.sin(heel)],[0,np.sin(heel),np.cos(heel)]])
        Lk_bteta=np.array([LK*np.sin(alfaK),-LK*np.cos(alfaK),0])[np.newaxis]
        Lk_bteta=Lk_bteta.T
        # lift na quilha
        Lk_b0=Mb0_bteta*Lk_bteta
        #vLK=[abs(LK*np.sin(leeway)*np.cos(heel))-abs(LK*np.cos(heel)*np.cos(leeway))*np.sign(leeway),abs(LK*np.sin(heel))]

        # matriz de mudanca de base do leme Mbteta_bdelta 
        Mbteta_bdelta =np.matrix([[np.cos(deltaR),-np.sin(deltaR),0],[np.sin(deltaR),np.cos(deltaR),0],[0,0,1]])
        Lr_bdelta=np.array([LR*np.sin(alfaR),-LR*np.cos(alfaR),0])[np.newaxis, :]
        Lr_bdelta=Lr_bdelta.T
        # lift no leme 
        Lr_b0=Mb0_bteta*Mbteta_bdelta*Lr_bdelta

        # parcela delta=0
        Lr0_bteta=np.array([LR0*np.sin(alfaR0),-LR0*np.cos(alfaR0),0])[np.newaxis]
        Lr0_bteta=Lr0_bteta.T
        Lr0_b0=Mb0_bteta*Lr0_bteta
        # forca lateral do bulbo
        vSfbulb=[0,-abs(Sfbulb*np.cos(leeway))*np.sign(leeway),0]
        # casco 
        vSfcb=[0,-abs(Sfcb*np.cos(leeway))*np.sign(leeway),0]

        ### 2.2.4.9 Somatorio das resistencias
        Rt=abs(Rv)+abs(Ri_K)+abs(Ri_Cb)+abs(Ri_R)+abs(Rr)+abs(Rincli)+abs(Rrk)+abs(Rinclik)
        #vRt=Rt*[-1 0 0]
        Rtx=Rt

        ### 2.2.4.10 Momento de Munk do casco
        M_munk=-divcan*rho*0.9*leeway*vboat**2

        ### 2.3 Momento Hidrostatico e estimativa para GZ valida somente para angulos menores que 30 graus
        ### 2.3.1 Estabilidade residual e efeito de superficie
        D2=-0.0406+0.0109*(bwl/tcan)-0.00105*(bwl/tcan)**2   #Fator de reducao da estabilidade em funcao de Fn
        #D3=0.0636-0.0196*(bwl/tcan)       #Fator de correcao para a CEE (considerar zero se passar a CEE correta)
        D3=0                                                                          #Esta usando a CEE correta
        if (-0.5236)<heel and heel<0.5236:
            MN=(D2*heel*Fn+np.sign(heel)*D3*heel**2)*lwl
        else:
            MN=(D2*heel*Fn+np.sign(heel)*D3*heel**2)*lwl
        if marcacoef==1:
            hg=abs(np.degrees(heel))
            GZ=np.sign(np.sin(heel))*(coef0+coef1*hg+coef2*hg**2+coef3*hg**3+coef4*hg**4+coef5*hg**5+coef6*hg**6)+MN
        else:
            GZ=GMtrans*np.sin(heel)-np.sign(heel)*abs(MN)              #Aproximacao da CEE 
        Mrhull=GZ*(divcan*rho)*grav

        ### 2.3.2 Variacao da posicao da trip bcrew - max para bwt=30 e no centro para bwt>=120
        if np.degrees(betatw[u])<30:
            bcrew=poscrew*(0.475*boa-0.305)
        elif np.degrees(betatw[u])>=30 and np.degrees(betatw[u])<=120:
            bcrew = poscrew*(0.475*boa-0.305)*np.cos(np.radians((np.degrees(betatw[u])-30)))
        else:
            bcrew=0
        Mr=Mrhull+np.sign(Mrhull)*abs(mcrew*grav*bcrew*np.cos(heel))

        ### 2.3.3 Posicao vertical do centro de esforco hidrodinamico em relacao a linha dagua
        CEh=0.45*(spanK+tcan)

        ### 2.4 Modelagem Aerodinamica
        ### 2.4.1 Area
        if leeway>0 and betaaw<0:
            betaaw=-betaaw
        if leeway<0 and betaaw>0:
            betaaw=-betaaw

        if marcaS==1:       #main and genoa
            #Mestra
            Am=P*E/2
            CEm=(0.39*P)+BAD
            #Genoa
            Aj=0.5*LPG*(I**2+J**2)**0.5
            CEj=0.39*I
            #Mizzen
            Amz=0.5*Pmz*Emz
            CEmz=0.39*Pmz+BADmz
            #Foretriangle
            Af=0.5*I*J
            #Area Nominal
            An=Af+Am+Amz
            #Centro de esforco em relacao ao deck
            CEaup=(CEm*Am+CEj*Aj+CEmz*Amz)/An
        if marcaS==2:       #main and spinnaker
            #Mestra
            Am=P*E/2
            CEm=(0.39*P)+BAD
            #Genoa
            Aj=0.5*LPG*(I**2+J**2)**0.5
            CEj=0.39*I
            #Spinnaker
            As=1.15*SLp*J
            CEs=0.59*I
            #Mizzen
            Amz=0.5*Pmz*Emz
            CEmz=0.39*Pmz+BADmz
            #Foretriangle
            Af=0.5*I*J
            #Area Nominal
            An=Af+Am+Amz
            #Centro de esforco em relacao ao deck
            CEadw=(CEm*Am+CEs*As+CEmz*Amz)/An
        if marcaS==3:       #both combinations
            #Mestra
            Am=P*E/2
            CEm=(0.39*P)+BAD
            #Genoa
            Aj=0
            CEj=0
            #Spinnaker
            As=1.15*SLp*J
            CEs=0.59*I
            #Mizzen
            Amz=0.5*Pmz*Emz
            CEmz=0.39*Pmz+BADmz
            #Foretriangle
            Af=0
            #Area Nominal
            An=Af+Am+Amz
            #Centro de esforco em relacao ao deck
            CEaup=(CEm*Am+CEj*Aj+CEmz*Amz)/An
            CEaup=CEaup
        if marcaS==4:       #only main
            #Mestra
            Am=P*E/2
            CEm=(0.39*P)+BAD
            #Genoa
            Aj=0
            CEj=0
            #Spinnaker
            As=1.15*SLp*J
            CEs=0.59*I
            #Mizzen
            Amz=0.5*Pmz*Emz
            CEmz=0.39*Pmz+BADmz
            #Foretriangle
            Af=0
            #Area Nominal
            An=Af+Am+Amz
            #Centro de esforco em relacao ao deck
            CEaup=(CEm*Am+CEj*Aj+CEmz*Amz)/An
            CEaup=CEaup

        ### 2.4.2 Coeficientes de Lift e Drag de cada vela - procura e interpola os coeficientes
        ### 2.4.2.1 Spinnaker
        # coeficients of cls (y) and cds (z) for several betaaw (x)
        x=[0.48844444, 0.72, 0.8, 1.05, 1.31, 1.74, 2.27, 2.62, 3.14]
        y=[0.0, 1.31, 1.56, 1.71, 1.69, 1.4, 0.83, 0.5, 0.0]
        z=[0.1, 0.15, 0.2, 0.4, 0.7, 1.0, 1.1, 1.1, 1.1]
        Cls=np.interp(betaaw,x,y)
        Cds=np.interp(betaaw,x,z)

        ### 2.4.2.2 Jib-genoa
        # coeficients of clj (y) and cdj (z) for several betaaw (x)
        x=[0.12211111, 0.26166667, 0.34888889, 0.471, 0.87222222, 1.04666667, 1.74444444, 2.61666667, 3.14]
        y=[0.0, 1.0, 1.375, 1.45, 1.43, 1.25, 0.4, 0.0, -0.1] 
        z=[0.05, 0.023, 0.031, 0.037, 0.25, 0.35, 0.73, 0.95, 0.9]
        Clj=np.interp(betaaw,x,y)
        Cdj=np.interp(betaaw,x,z)

        ### 2.4.2.3 Main
        # coeficients of clm (y) and cdm (z) for several betaaw (x)
        x=[0.0, 0.12211111, 0.157, 0.20933333, 1.04666667, 1.57, 2.09333333, 2.61666667, 3.14] 
        y=[0.0, 1.0, 1.22, 1.35, 1.25, 0.96, 0.58, 0.25, -0.1] 
        z=[0.05, 0.03, 0.027, 0.027, 0.114, 0.306, 0.671, 1.11, 1.2]
        Clm=np.interp(betaaw,x,y)
        Cdm=np.interp(betaaw,x,z)
        
        ### 2.4.2.4 Main Full
        # coeficients of clm (y) and cdm (z) for several betaaw (x)
        x=[0.0, 0.12211111, 0.157, 0.20933333, 1.04666667, 1.57, 2.09333333, 2.61666667, 3.14]
        y=[0, 1.15, 1.4,1.55, 1.44, 0.96, 0.58, 0.25, -0.1]
        z=[0.027, 0.027, 0.027, 0.027, 0.103, 0.275, 0.671, 1.11, 1.2]
        Clmf=np.interp(betaaw,x,y)
        Cdmf=np.interp(betaaw,x,z)

        ### 2.4.2.5 Coeficiente de Lift
        if marcaS==1 or marcaS==4:
            if tala==0:
                Clup=(Clm*Am+Clj*Aj)/An
            else:
                Clup=(Clmf*Am+Clj*Aj)/An
        if marcaS==2:
            if tala==0:
                Cldw=(Clm*Am*Cls*As)/An
            else:
                Cldw=(Clmf*Am*Cls*As)/An

        ### 2.4.2.6 Drag parasita
        if marcaS==1 or marcaS==4:
            if tala==0:
                Cdp=(Cdm*Am+Cdj*Aj)/An
            else:
                Cdp=(Cdmf*Am+Cdj*Aj)/An
        if marcaS==2:
            if tala==0:
                Cdp=(Cdm*Am+Cds*As)/An
            else:
                Cdp=(Cdmf*Am+Cds*As)/An

        if (betatw[u])<(pi/3):
            AR=((1.1*(EHM+fb))**2)/An
        else:
            AR=((1.1*EHM)**2)/An

        Cd0=1.13*((boa*fb)+(EHM*EMDC))/An         #Drag do mastro e casco
        if marcaS==1 or marcaS==4:
            Cdl=(0.005+1/(pi*AR))*Clup**2            #Drag induzido
            Cdup=Cdp+Cdl+Cd0                         #Coeficiente de Drag
        if marcaS==2:
            Cdl=(0.005+1/(pi*AR))*Cldw**2            #Drag induzido
            Cddw=Cdp+Cdl+Cd0                         #Coeficiente de Drag

        ### 2.6.2.5 Forcas de sustentacao
        #alfa_aero=np.arcsin(np.cos(heel)*np.sin(betaaw))
        alfa_aero=betaaw
        #Lift na base bteta inclinada 
        #Lift e Drag contravento
        if marcaS==1 or marcaS==4:
            LSup=0.5*rhoair*(velaw*np.cos(heel))**2*Clup*An*np.sign(alfa_aero)
            DSup=0.5*rhoair*(velaw*np.cos(heel))**2*Cdup*An
            CEa=CEaup
            LS=LSup
            DS=DSup
        if marcaS==2:
            LSdw=0.5*rhoair*(velaw*np.cos(heel))**2*Cldw*An*np.sign(alfa_aero)
            DSdw=0.5*rhoair*(velaw*np.cos(heel))**2*Cddw*An
            CEa=CEadw                             
            LS=LSdw
            DS=DSdw

        LS_Bteta=np.array([LS*np.sin(alfa_aero),LS*np.cos(alfa_aero),0])[np.newaxis,:]
        LS_Bteta=LS_Bteta.T
        DS_Bteta=np.array([-DS*np.cos(alfa_aero),DS*np.sin(alfa_aero),0])[np.newaxis,:]
        DS_Bteta=DS_Bteta.T
        LS_B0=Mb0_bteta*LS_Bteta
        LSx=LS*np.cos(heel)*np.sin(betaaw)
        D_S=Mb0_bteta*DS_Bteta
        
        ZCEa=CEa+fb
        F=[(LS_B0[0]+D_S[0])+Lk_b0[0]+Lr_b0[0]-Rt,(LS_B0[1]+D_S[1])+Lk_b0[1]+Lr_b0[1]+vSfcb[1],(LS_B0[1]+D_S[1])*(CEa+fb)+(-CEh)*(Lk_b0[1]+Lr_b0[1]+vSfcb[1])+Mr,(LS_B0[0]+D_S[0])*ZCEa*np.sin(heel)+(LS_B0[1]+D_S[1])*xcea-(Lr_b0[1]-Lr0_b0[1])*lr+M_munk]
        Fx=F[0] #avanco
        Fy=F[1] #deriva
        Mx=F[2] #banda
        Mz=F[3] #trim

        ### estimativa do momento e angulo de pitch
        #Mpitch=(LS_B0[0]+D_S[0])*(CEa+fb+CEh)
        #pitch=np.degrees(np.arcsin(Mpitch/(divcan*rho*grav*GMlong)))
        #vmg=-vboat*np.cos(abs(leeway)+abs(betatw[u]))

        return np.array([np.float(Fx),np.float(Fy),np.float(Mx),np.float(Mz)])
            
    for t in range (0,len_veltw,1):    #para otimizacao, o for t e identado juntamente com bwl 
        for u in range (0,len_betatw,1):
            sol = optimize.root(vpp_solve2, initialguess) # solve for Powell hybrid method (hybr) ou Levenber-Marquart (lb)
            vboatfinal[t,u] = sol.x[1]
            betatwfinal[t,u]=betatw[u]
            betatwfinaldeg=np.degrees(betatwfinal)
            #print(vboatfinal)
            print(sol)
    
    #print(vboatfinal)
   
    return vboatmed, vboatmed