from Basis import Basis, flavour_matrix
import math, re
from math import sqrt
from itertools import combinations_with_replacement as comb
from itertools import product
from __init__ import PID
########################################################################
# Higgs basis class
class HiggsBasis(Basis):
    # Kinetic terms
    KIN_ind =['dM']
    HBKIN = KIN_ind
    
    # Z Vertex Corrections
    dGLze = flavour_matrix('dGLze', kind='hermitian', domain='complex')
    dGRze = flavour_matrix('dGRze', kind='hermitian', domain='complex')
    dGLzv = flavour_matrix('dGLzv', kind='hermitian', domain='complex')
    dGLzu = flavour_matrix('dGLzu', kind='hermitian', domain='complex')
    dGRzu = flavour_matrix('dGRzu', kind='hermitian', domain='complex')
    dGLzd = flavour_matrix('dGLzd', kind='hermitian', domain='complex')
    dGRzd = flavour_matrix('dGRzd', kind='hermitian', domain='complex')

    # W Vertex Corrections
    dGLwl = flavour_matrix('dGLwl', kind='hermitian', domain='complex')
    dGLwq = flavour_matrix('dGLwq', kind='hermitian', domain='complex')
    dGRwq = flavour_matrix('dGRwq', kind='general'  , domain='complex')

    VERTEX_ind = dGLze + dGRze+ dGLzu+ dGRzu+ dGLzd+ dGRzd + dGLwl + dGRwq
    VERTEX_dep = dGLzv + dGLwq
    HBVERTEX = VERTEX_ind + VERTEX_dep
    
    # Single Higgs couplings to gauge bosons
    HVV_ind = ['dCz','Cgg','Czz','Caa','Cza','Czbx',
                       'CTgg','CTzz','CTaa','CTza']
    HVV_dep = ['dCw','Cww','CTww','Cwbx','Cabx']
    HBHVV = HVV_ind + HVV_dep
    
    # Single Higgs couplings to fermions
    dYu = flavour_matrix('dYu', kind='general', domain='real')
    dYd = flavour_matrix('dYd', kind='general', domain='real')
    dYe = flavour_matrix('dYe', kind='general', domain='real')
    Su  = flavour_matrix('Su', kind='general', domain='real')
    Sd  = flavour_matrix('Sd', kind='general', domain='real')
    Se  = flavour_matrix('Se', kind='general', domain='real')
    
    HFF_ind = dYu + dYd + dYe + Su + Sd + Se
    HBHFF = HFF_ind
    
    # Higgs contact interactions HVff
    CLze = flavour_matrix('CLze', kind='hermitian', domain='complex')
    CRze = flavour_matrix('CRze', kind='hermitian', domain='complex')
    CLzv = flavour_matrix('CLzv', kind='hermitian', domain='complex')
    CLzu = flavour_matrix('CLzu', kind='hermitian', domain='complex')
    CRzu = flavour_matrix('CRzu', kind='hermitian', domain='complex')
    CLzd = flavour_matrix('CLzd', kind='hermitian', domain='complex')
    CRzd = flavour_matrix('CRzd', kind='hermitian', domain='complex')
    CLwl = flavour_matrix('CLwl', kind='hermitian', domain='complex')
    CLwq = flavour_matrix('CLwq', kind='hermitian', domain='complex')
    CRwq = flavour_matrix('CRwq', kind='general'  , domain='complex')
    
    HVFF_dep = (CLze + CRze + CLzv + CLzu + CRzu 
              + CLzd + CRzd + CLwl + CLwq + CRwq)
    HBHVFF = HVFF_dep
    
    # Triple and quartic gauge couplings [Sec. 3.7]
    
    V3_ind = [ 'Lz','C3G','LTz','CT3G' ]
    V3_dep = [ 'dG1z','dKa','dKz','La','KTa','KTz','LTa' ]
    HBV3 = V3_ind + V3_dep
    
    V4_dep = ['dGw4','dGw2z2','dGw2za']
    HBV4 = V4_dep
    
    D2V4_dep = ['Ldw4', 'Ldzdw_zw', 'Ldzdw_aw', 
                'Ldadw_aw', 'Ldadw_zw', 'Ldg_g3',
                'LTdw4', 'LTdzdw_zw', 'LTdzdw_aw',
                'LTdadw_aw', 'LTdadw_zw', 'LTdg_g3']
    HBD2V4 = D2V4_dep
    
    # Couplings of two Higgs bosons [Sec. 3.8]
    H3_ind = ['dL3']
    HBH3 = H3_ind
    
    HHVV_dep = ['Cgg2','CTgg2']
    HBHHVV = HHVV_dep
    
    Y2u = flavour_matrix('Y2u', kind='symmetric', domain='complex')
    Y2d = flavour_matrix('Y2d', kind='symmetric', domain='complex')
    Y2e = flavour_matrix('Y2e', kind='symmetric', domain='complex')
    HHFF_dep = Y2u + Y2d + Y2e
    HBHHFF = HHFF_dep
    
    # 4-fermion operators
    fourfermi_ind = ['cll1122','cpuu3333'] # needed for SILH <-> Warsaw
    fourfermi_dep = ['cll1221'] # affects Gf input
    HB4F = fourfermi_ind + fourfermi_dep
    
    # Full set of independent and dependent coefficients
    independent = (KIN_ind + VERTEX_ind  + HVV_ind + HFF_ind + V3_ind
                  + H3_ind + fourfermi_ind )
                
    dependent   = (VERTEX_dep  + HVV_dep + HVFF_dep + V3_dep + V4_dep
                   + D2V4_dep + HHVV_dep + HHFF_dep + fourfermi_dep )
    # Required inputs/masses             
    required_masses = {1, 2, 3, 4, 5, 6, 11, 12, 13, 14, 15, 16}
    required_inputs = {1, 2, 3, 4} # aEWM1, Gf, aS, MZ
    
    blocks = {'HBKIN':HBKIN,'HBVERTEX':HBVERTEX, 'HBHVV':HBHVV, 'HBHFF':HBHFF,
              'HBHVFF':HBHVFF, 'HBV3':HBV3, 'HBV4':HBV4,'HBD2V4':HBD2V4,
              'HBH3':HBH3, 'HBHHVV':HBHHVV, 'HBHHFF':HBHHFF, 'HB4F':HB4F}
    
    translate_to={'mass'}
    
    def calculate_inputs(self): # calculate a few required EW params from aEWM1, Gf, MZ
        ee2 = 4.*math.pi/self.inputs['aEWM1'] # EM coupling squared
        gs2 = 4.*math.pi*self.inputs['aS'] # strong coupling squared
        Gf, MZ = self.inputs['Gf'], self.inputs['MZ']
        s2w = (1.- sqrt(1. - ee2/(sqrt(2.)*Gf*MZ**2)))/2. # sin^2(theta_W)
        c2w = (1.-s2w)
        gw2 = ee2/s2w # SU(2) coupling squared
        gp2 = gw2*s2w/c2w # Hypercharge coupling squared
        vev =  2.*MZ*sqrt(c2w/gw2)
        return s2w, c2w, ee2, gw2, gp2, MZ, vev, gs2

    def calculate_dependent(self):
        s2w, c2w, ee2, gw2, gp2, MZ, vev, gs2 = self.calculate_inputs() 
        A = self
        MW = MZ*sqrt(c2w)
        # Higgs and EW gauge bosons [Sec 3.4] [eqn (3.11)]
        A['dCw']  = A['dCz']  + A['dM']*4. 
        A['Cww']  = A['Czz']  + A['Cza']*2.*s2w  + A['Caa'] *s2w**2
        A['CTww'] = A['CTzz'] + A['CTza']*2.*s2w + A['CTaa']*s2w**2 
        A['Cwbx'] = (A['Czbx']*gw2 + A['Czz']*gp2 - A['Caa']*ee2*s2w 
                    - A['Cza']*(gw2-gp2)*s2w )/(gw2-gp2)
        A['Cabx'] = (A['Czbx']*2.*gw2 + A['Czz']*(gw2+gp2) 
                    - A['Caa']*ee2 - A['Cza']*(gw2-gp2))/(gw2-gp2)
        
        # Gauge-current and Higgs-gauge-current contact interactions [Sec 3.6]
        for i,j in comb((1,2,3),2):# dependent dgV coeffs [eqn (3.5)]
            indx = '{}{}'.format(i,j)
            if i==j:
                A['dGLzv'+indx] = A['dGLze'+indx] + A['dGLwl'+indx] 
                A['dGLwq'+indx] = A['dGLzu'+indx] - A['dGLzd'+indx]
            else:
                for part in ('_Re', '_Im'):
                    tail = indx + part
                    A['dGLzv'+tail] = A['dGLze'+tail] + A['dGLwl'+tail] 
                    A['dGLwq'+tail] = A['dGLzu'+tail] - A['dGLzd'+tail]
     
        # list of all z/w vertex corrections
        for dG in self.HBVERTEX: # 4-point coeffs [eqn (3.18)]
            cvff = dG.replace('dG','C')
            A[cvff] = A[dG]
                
        # Triple gauge couplings [Sec 3.7] [eqn (3.21)] 
        A['dG1z'] = (A['Caa']*ee2*gp2 + A['Cza']*(gw2-gp2)*gp2 
                    - A['Czz']*(gw2+gp2)*gp2 - A['Czbx']*(gw2+gp2)*gw2 
                    )/2./(gw2-gp2)
        A['dKa'] = - (A['Caa']*ee2  + A['Cza']*(gw2-gp2) 
                    - A['Czz']*(gw2+gp2) )*gw2/2./(gw2+gp2)
        A['KTa'] = - ( A['CTaa']*ee2 + A['CTza']*(gw2-gp2) 
                    - A['CTzz']*(gw2+gp2))*gw2/2./(gw2+gp2)
        A['dKz'] = A['dG1z'] - gp2/gw2*A['dKa']
        A['KTz'] = - A['KTa']*gp2/gw2
        A['La'] = A['Lz']
        A['LTa'] = A['LTz']
        
        # Quartic gauge couplings [Sec 3.7] [eqn (3.23)] 
        A['dGw4'] = 2.*c2w*A['dG1z']
        A['dGw2z2'] = 2.*A['dG1z']
        A['dGw2za'] = A['dG1z']
        # two derivative quartic gauge couplings [Sec 3.7] [eqn (3.24)] 
        A['Ldw4'] = -gw2/2./MW**2*A['Lz']
        A['LTdw4'] = -gw2/2./MW**2*A['LTz']
        A['Ldzdw_zw'] = -gw2*c2w/MW**2*A['Lz']
        A['LTdzdw_zw'] = -gw2*c2w/MW**2*A['LTz']
        A['Ldzdw_aw'] = -ee2/MW**2*A['Lz']
        A['LTdzdw_aw'] = -ee2/MW**2*A['LTz']
        A['Ldadw_aw'] = -sqrt(ee2*gw2*c2w)/MW**2*A['Lz']
        A['LTdadw_aw'] = -sqrt(ee2*gw2*c2w)/MW**2*A['LTz']
        A['Ldadw_zw'] = -sqrt(ee2*gw2*c2w)/MW**2*A['Lz']
        A['LTdadw_zw'] = -sqrt(ee2*gw2*c2w)/MW**2*A['LTz']
        A['Ldg_g3'] = 3.*sqrt(gs2)**3/vev**2*A['C3G']
        A['LTdg_g3'] = 3.*sqrt(gs2)**3/vev**2*A['CT3G']
        
        # Couplings of two Higgs bosons [Sec 3.8] [eqn (3.27)]
        def delta(i,j):
            return 1. if i==j else 0.
        A['Cgg2'], A['CTgg2'] = A['Cgg'], A['CTgg']
        for i,j in comb((1,2,3),2):
            for f in ('u','d','e'):
                name = '{}{}{}'.format(f,i,j)
                Yij   = A['dY' + name]
                sinij = A['S' + name] 
                cosij = sqrt(1. - sinij**2)
                A['Y2{}_Re'.format(name)] = (3.*Yij*cosij 
                                               - A['dCz']*delta(i,j))
                A['Y2{}_Im'.format(name)] = 3.*Yij*sinij
        # 4-fermion operators [Sec. 3.9]
        # [eqn (3.32)]
        A['cll1221'] = 2.*(A['dGLwl11'] + A['dGLwl22'] - 2.*A['dM']) 
        
        self.mass[24] = MW + A['dM']
        
        
    def calculate_dependent_old(self):
        p = self.par_dict
        s2w, c2w, ee2, gw2, gp2, MZ, vev, gs2= self.calculate_inputs() 
        MW = MZ*sqrt(c2w)
        # Higgs and EW gauge bosons [Sec 3.4] [eqn (3.11)]
        p['dCw']  = p['dCz']  + p['dM']*4. 
        p['Cww']  = p['Czz']  + p['Cza']*2.*s2w  + p['Caa'] *s2w**2
        p['CTww'] = p['CTzz'] + p['CTza']*2.*s2w + p['CTaa']*s2w**2 
        p['Cwbx'] = (p['Czbx']*gw2 + p['Czz']*gp2 - p['Caa']*ee2*s2w 
                    - p['Cza']*(gw2-gp2)*s2w )/(gw2-gp2)
        p['Cabx'] = (p['Czbx']*2.*gw2 + p['Czz']*(gw2+gp2) 
                    - p['Caa']*ee2 - p['Cza']*(gw2-gp2))/(gw2-gp2)
        
        # Gauge-current and Higgs-gauge-current contact interactions [Sec 3.6]
        for i,j in comb((1,2,3),2):# dependent dgV coeffs [eqn (3.5)]
            ind = '{}{}'.format(i,j)
            if i==j:
                p['dGLzv'+ind] = p['dGLze'+ind] + p['dGLwl'+ind] 
                p['dGLwq'+ind] = p['dGLzu'+ind] - p['dGLzd'+ind]
            else:
                for part in ('_Re', '_Im'):
                    tail = ind + part
                    p['dGLzv'+tail] = p['dGLze'+tail] + p['dGLwl'+tail] 
                    p['dGLwq'+tail] = p['dGLzu'+tail] - p['dGLzd'+tail]
     
        # list of all z/w vertex corrections
        for dG in self.HBVERTEX: # 4-point coeffs [eqn (3.18)]
            cvff = dG.replace('dG','C')
            p[cvff] = p[dG]
                
        # Triple gauge couplings [Sec 3.7] [eqn (3.21)] 
        p['dG1z'] = (p['Caa']*ee2*gp2 + p['Cza']*(gw2-gp2)*gp2 
                    - p['Czz']*(gw2+gp2)*gp2 - p['Czbx']*(gw2+gp2)*gw2 
                    )/2./(gw2-gp2)
        p['dKa'] = - (p['Caa']*ee2  + p['Cza']*(gw2-gp2) 
                    - p['Czz']*(gw2+gp2) )*gw2/2./(gw2+gp2)
        p['KTa'] = - ( p['CTaa']*ee2 + p['CTza']*(gw2-gp2) 
                    - p['CTzz']*(gw2+gp2))*gw2/2./(gw2+gp2)
        p['dKz'] = p['dG1z'] - gp2/gw2*p['dKa']
        p['KTz'] = - p['KTa']*gp2/gw2
        p['La'] = p['Lz']
        p['LTa'] = p['LTz']
        
        # Quartic gauge couplings [Sec 3.7] [eqn (3.23)] 
        p['dGw4'] = 2.*c2w*p['dG1z']
        p['dGw2z2'] = 2.*p['dG1z']
        p['dGw2za'] = p['dG1z']
        
        # two derivative quartic gauge couplings [Sec 3.7] [eqn (3.24)] 
        p['Ldw4'] = -gw2/2./MW**2*p['Lz']
        p['LTdw4'] = -gw2/2./MW**2*p['LTz']
        p['Ldzdw_zw'] = -gw2*c2w/MW**2*p['Lz']
        p['LTdzdw_zw'] = -gw2*c2w/MW**2*p['LTz']
        p['Ldzdw_aw'] = -ee2/MW**2*p['Lz']
        p['LTdzdw_aw'] = -ee2/MW**2*p['LTz']
        p['Ldadw_aw'] = -sqrt(ee2*gw2*c2w)/MW**2*p['Lz']
        p['LTdadw_aw'] = -sqrt(ee2*gw2*c2w)/MW**2*p['LTz']
        p['Ldadw_zw'] = -sqrt(ee2*gw2*c2w)/MW**2*p['Lz']
        p['LTdadw_zw'] = -sqrt(ee2*gw2*c2w)/MW**2*p['LTz']
        p['Ldg_g3'] = 3.*sqrt(gs2)**3/vev**2*p['C3G']
        p['LTdg_g3'] = 3.*sqrt(gs2)**3/vev**2*p['CT3G']
        
        # Couplings of two Higgs bosons [Sec 3.8] [eqn (3.27)]
        def delta(i,j):
            return 1. if i==j else 0.
        p['Cgg2'], p['CTgg2'] = p['Cgg'], p['CTgg']
        for i,j in comb((1,2,3),2):
            for f in ('u','d','e'):
                name = '{}{}{}'.format(f,i,j)
                Yij   = p['dY' + name]
                sinij = p['S' + name] 
                cosij = sqrt(1. - sinij**2)
                p['Y2{}_Re'.format(name)] = (3.*Yij*cosij - p['dCz']*delta(i,j))
                p['Y2{}_Im'.format(name)] = 3.*Yij*sinij
        # 4-fermion operators [Sec. 3.9]
        # [eqn (3.32)]
        p['cll1221'] = 2.*(p['dGLwl11'] + p['dGLwl22'] - 2.*p['dM']) 
            
########################################################################
