import numpy as np                              # radians-degree conversion, tangent, arrays, linspace
import scipy.interpolate as si                  # create the xy coordinates of the splines
from scipy.interpolate import interp1d          # create a curve based on the xy coordinates of the splines
from scipy.integrate import quad                # integrate splines for disp and awp calculation
from scipy.optimize import least_squares        # solve the equations system
import json, codecs                             # export as json


################################################################################################################
# 1. SAC CURVE
################################################################################################################
def sac_solve(lwl, disp, lcb, alpha_f, alpha_i, b0, bwl, tc, cm):
    alpha_i_sac = np.radians(np.float(alpha_i))       # controls volume distribution inside the ship at the stern
    alpha_f_sac = np.radians(np.float(alpha_f))      # controls volume distribution inside the ship at the bow
    xp0, xp4, yp0, yp4, = 0, lwl, b0, 0
    
    def sac(p):
        xp1_sac, xp2_sac, xp3_sac, yp1_sac, yp2_sac, yp3_sac = p
        points_sac = np.array([[xp0, yp0], [xp1_sac, yp1_sac], [xp2_sac, yp2_sac],
                            [xp3_sac, yp3_sac], [xp4, yp4]])
        x_sac, y_sac = points_sac[:, 0], points_sac[:, 1]
        t_sac = range(len(points_sac))
        ipl_t_sac = np.linspace(0, len(points_sac)-1, 100)
        x_tup_sac, y_tup_sac = si.splrep(t_sac, x_sac, k=4), si.splrep(t_sac, y_sac, k=4)
        x_list_sac = list(x_tup_sac)
        xl_sac = x_sac.tolist()
        x_list_sac[1] = xl_sac+[0, 0, 0, 0]
        y_list_sac = list(y_tup_sac)
        yl_sac = y_sac.tolist()
        y_list_sac[1] = yl_sac+[0, 0, 0, 0]
        x_i_sac, y_i_sac = si.splev(ipl_t_sac, x_list_sac), si.splev(ipl_t_sac, y_list_sac)
        interp_sac = si.interp1d(x_i_sac, y_i_sac, kind='cubic')
        disp_calc = quad(interp_sac, 0, lwl)[0]
        xcenter_sac = 0
        for h in range(0, 99):
            xcenter_sac = xcenter_sac+x_i_sac[h]*y_i_sac[h]*lwl/100
        lcb_calc = xcenter_sac/disp
        maxsac_x, stop = 0, 0
        for i in range(0, len(x_i_sac)-1):
            if (y_i_sac[i+1]) < y_i_sac[i] and stop < 1:
                maxsac_x = x_i_sac[i]
                stop = stop+1
            else:
                i = i+1
        # evaluate the functions
        f1 = max(y_i_sac)-bwl*tc*cm
        f2 = disp_calc-disp
        f3 = lcb-lcb_calc
        f4 = maxsac_x-lwl*0.46
        f5 = yp0+np.tan(alpha_i_sac)*(xp1_sac-xp0)-yp1_sac
        f6 = yp4+np.tan(alpha_f_sac)*(xp4-xp3_sac)-yp3_sac
        return f1, f2, f3, f4, f5, f6


    x0 = np.array([lwl/4, lwl/2, lwl*0.75, 0.2, 1, 0.1])
    bds = ([0, 0, lwl/2, 0, 0, 0], [lwl/2, lwl, lwl, 5, 20, 5])
    res = least_squares(sac, x0, bounds=bds, xtol=0.1)
    xp1, xp2, xp3, yp1, yp2, yp3 = res.x[0], res.x[1], res.x[2], res.x[3], res.x[4], res.x[5]

    # recreate the spline
    points = np.array([[xp0, yp0], [xp1, yp1], [xp2, yp2], [xp3, yp3], [xp4, yp4]])
    x, y = points[:, 0], points[:, 1]
    t = range(len(points))
    ipl_t = np.linspace(0, len(points)-1, 100)
    x_tup, y_tup = si.splrep(t, x, k=4), si.splrep(t, y, k=4)
    x_list = list(x_tup)
    xl = x.tolist()
    x_list[1] = xl+[0, 0, 0, 0]
    y_list = list(y_tup)
    yl = y.tolist()
    y_list[1] = yl+[0, 0, 0, 0]
    x_i, y_i = si.splev(ipl_t, x_list), si.splev(ipl_t, y_list)
    maxsac = max(y_i)

    maxsac_x, stop = 0, 0
    for i in range(0, len(x_i)-1):
        if (y_i[i+1]) < y_i[i] and stop < 1:
            maxsac_x = x_i[i]
            stop = stop+1
        else:
            i = i+1

    # coordinates for sections
    x_sections = np.linspace(0, lwl, 12)       # first and last points are not representative
    interpolation_sac = si.interp1d(x_i, y_i, kind='quadratic')
    sn_sections = interpolation_sac(x_sections)
    sn = max(y_i)
    
    json.dump({'x_sac': x.tolist(), 'y_sac': y.tolist(), 'x_i_sac': x_i.tolist(), 'y_i_sac': y_i.tolist(), 'maxsac': maxsac.tolist(), 'maxsac_x': maxsac_x.tolist(), 'sn_sections': sn_sections.tolist()}, codecs.open('data/sacsolution.json', 'w', encoding='utf-8'), separators=(', ',': '), sort_keys=True)
    
    return x, y, x_i, y_i, maxsac, maxsac_x, sn_sections


################################################################################################################
# 2. WATERLINE CURVE
################################################################################################################
def wl_solve(lcf, awp, lwl, b0, bwl):
    xp0, yp0, xp1, xp3, yp3 = 0, b0, 0, lwl, 0
    def wl(p):
        yp1_wl, yp2_wl, xp2_wl = p
        # create the spline
        points_wl = np.array([[xp0, yp0], [xp1, yp1_wl], [xp2_wl, yp2_wl], [xp3, yp3]])
        x_wl, y_wl = points_wl[:, 0], points_wl[:, 1]
        t_wl = range(len(points_wl))
        ipl_t_wl = np.linspace(0.0, len(points_wl)-1, 100)
        x_tup_wl, y_tup_wl = si.splrep(t_wl, x_wl, k=3), si.splrep(t_wl, y_wl, k=3)
        x_list_wl = list(x_tup_wl)
        xl_wl = x_wl.tolist()
        x_list_wl[1] = xl_wl+[0, 0, 0, 0]
        y_list_wl = list(y_tup_wl)
        yl_wl = y_wl.tolist()
        y_list_wl[1] = yl_wl+[0, 0, 0, 0]
        x_i_wl, y_i_wl = si.splev(ipl_t_wl, x_list_wl), si.splev(ipl_t_wl, y_list_wl)
        interp_wl = interp1d(x_i_wl, y_i_wl, kind='cubic')
        awp_calc = quad(interp_wl, 0, lwl)[0]
        xcenter_wl = 0
        for j in range(0, 99):
            xcenter_wl = xcenter_wl+x_i_wl[j]*y_i_wl[j]*lwl/100
        lcf_calc = xcenter_wl/(awp*0.5)
        # evaluate the functions
        f1 = awp_calc-awp*0.5
        f2 = lcf_calc-lcf
        f3 = max(y_i_wl)-bwl/2
        return f1, f2, f3

    x0 = np.array([bwl*0.5, bwl*0.5, lwl*0.7])
    bds = ([0, 0, lwl*0.5], [bwl*5, bwl*5, lwl])
    res = least_squares(wl, x0, bounds=bds, xtol=0.1)
    yp1, yp2, xp2 = res.x[0], res.x[1], res.x[2]

    # create the spline
    points = np.array([[xp0, yp0], [xp1, yp1], [xp2, yp2], [xp3, yp3]])
    x, y = points[:, 0], points[:, 1]
    t = range(len(points))
    ipl_t = np.linspace(0.0, len(points)-1, 100)
    x_tup, y_tup = si.splrep(t, x, k=3), si.splrep(t, y, k=3)
    x_list = list(x_tup)
    xl = x.tolist()
    x_list[1] = xl+[0, 0, 0, 0]
    y_list = list(y_tup)
    yl = y.tolist()
    y_list[1] = yl+[0, 0, 0, 0]
    x_i, y_i = si.splev(ipl_t, x_list), si.splev(ipl_t, y_list)

    bwlmax, bwlmax_x, stop = 0, 0, 0
    for i in range(0, len(x_i)-1):
        if (y_i[i+1]) < y_i[i] and stop < 1:
            bwlmax = y_i[i]
            bwlmax_x = x_i[i]
            stop = stop+1
        else:
            i = i+1
    
    # coordinates for sections
    x_sections = np.linspace(0, lwl, 12)       # first and last points are not representative
    interpolation_wl = si.interp1d(x_i, y_i, kind='cubic')
    bn_sections = interpolation_wl(x_sections)*2

    json.dump({'x_wl': x.tolist(), 'y_wl': y.tolist(), 'x_i_wl': x_i.tolist(), 'y_i_wl': y_i.tolist(), 'bwlmax': bwlmax.tolist(), 'bwlmax_x': bwlmax_x.tolist(), 'bn_sections': bn_sections.tolist()}, codecs.open('data/wlsolution.json', 'w', encoding='utf-8'), separators=(', ',': '), sort_keys=True)

    return x, y, x_i, y_i, bwlmax, bwlmax_x, bn_sections

################################################################################################################
# 3. KEEL CURVE
################################################################################################################
def keel_solve(lwl, tc):
    xp0, yp0, xp3, yp3, xp2 = 0, 0, lwl, 0, 0.85*lwl
    def keel(p):
        xp1_keel, yp1_keel = p
        # create the spline
        points_keel = np.array([[xp0, yp0], [xp1_keel, yp1_keel], [xp2, yp1_keel], [xp3, yp3]])
        x_keel, y_keel = points_keel[:, 0], points_keel[:, 1]
        t_keel = range(len(points_keel))
        ipl_t_keel = np.linspace(0, len(points_keel)-1, 100)
        x_tup_keel, y_tup_keel = si.splrep(t_keel, x_keel, k=3), si.splrep(t_keel, y_keel, k=3)
        x_list_keel = list(x_tup_keel)
        xl_keel = x_keel.tolist()
        x_list_keel[1] = xl_keel+[0, 0, 0, 0]
        y_list_keel = list(y_tup_keel)
        yl_keel = y_keel.tolist()
        y_list_keel[1] = yl_keel+[0, 0, 0, 0]
        x_i_keel, y_i_keel = si.splev(ipl_t_keel, x_list_keel), si.splev(ipl_t_keel, y_list_keel)
        # evaluate the function
        f1 = tc-max(-y_i_keel)
        f2 = (xp1_keel*0.8+xp2)-lwl
        return f1, f2

    x0 = np.array([lwl*0.2, -tc])
    bds = ([0, -3*tc], [lwl/2, 0])
    res = least_squares(keel, x0, bounds=bds, xtol=0.1)
    xp1, yp1 = res.x[0], res.x[1]
    yp2 = yp1

    # create the spline
    points = np.array([[xp0, yp0], [xp1, yp1], [xp2, yp2], [xp3, yp3]])
    x, y = points[:, 0], points[:, 1]
    t = range(len(points))
    ipl_t = np.linspace(0, len(points)-1, 100)
    x_tup, y_tup = si.splrep(t, x, k=3), si.splrep(t, y, k=3)
    x_list = list(x_tup)
    xl = x.tolist()
    x_list[1] = xl+[0, 0, 0, 0]
    y_list = list(y_tup)
    yl = y.tolist()
    y_list[1] = yl+[0, 0, 0, 0]
    x_i, y_i = si.splev(ipl_t, x_list), si.splev(ipl_t, y_list)

    # coordinates of the maximul draft
    stop, tnx = 0, 0
    for i in range(0, len(x_i)-1):
        if (y_i[i+1]) > y_i[i] and stop < 1:
            tnx = x_i[i]
            stop = stop+1
        else:
            i = i+1
    
    # coordinates for sections
    x_sections = np.linspace(0, lwl, 12)       # first and last points are not representative
    interpolation_keel = si.interp1d(x_i, y_i, kind='cubic')
    tn_sections = -interpolation_keel(x_sections)
    tn_sections[0] = 0
    tn_sections[len(tn_sections)-1] = 0

    json.dump({'x_keel': x.tolist(), 'y_keel': y.tolist(), 'x_i_keel': x_i.tolist(), 'y_i_keel': y_i.tolist(), 'tnx': tnx.tolist(), 'tn_sections': tn_sections.tolist()}, codecs.open('data/keelsolution.json', 'w', encoding='utf-8'), separators=(', ',': '), sort_keys=True)

    return x, y, x_i, y_i, tnx, tn_sections


################################################################################################################
# 4. SECTIONS
################################################################################################################
# create the coordinates for the sections in x, y and z axis
def section_solve(tn_sections, bn_sections, sn_sections, lwl, beta_n):
    x_sections = np.linspace(0, lwl, 12)
    pcon_yaxis = 10
    kn = np.tan(np.radians(beta_n))
    qn_sections, pn_sections = np.zeros(pcon_yaxis+1), np.zeros(pcon_yaxis+1)
    section_x_sections, section_y_sections, section_z_sections = [], [], []
    for n in range(1, pcon_yaxis+1):
        qn_sections[n] = (tn_sections[n]-kn*bn_sections[n]/2)*(bn_sections[n]/2)*(tn_sections[n]*bn_sections[n]/2-sn_sections[n]/2-kn/2*(bn_sections[n]/2)**2)**(-1)-1
        pn_sections[n] = (tn_sections[n]-kn*bn_sections[n]/2)/(bn_sections[n]/2)**qn_sections[n]
        section_x_sections.append([x_sections[n]] * 10)
        section_y_sections.append(np.linspace(0, bn_sections[n]/2, 25))
        if qn_sections[n]<0:      # INVESTIGAR POR QUE O QN[10] DÁ NEGATIVO?
            qn_sections[n]=qn_sections[n-1]
        section_z_sections.append((kn*section_y_sections[n-1]+pn_sections[n]*section_y_sections[n-1]**qn_sections[n])-tn_sections[n])
    return section_x_sections, section_y_sections, section_z_sections