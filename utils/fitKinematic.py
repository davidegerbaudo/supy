import math, __init__ as utils,ROOT as r
try:
    import scipy.optimize as opt
except: pass
try:
    import numpy as np
except:
    pass

widthTop = 13.1/2
###########################
class leastsqLeptonicTop(object) :
    '''Fit jet, lepton, and missing energy to the hypothesis t-->blv.'''

    def __init__(self, b, bResolution, mu, nuXY, nuErr, 
                 massT = 172.0, widthT = widthTop, massW = 80.4, zPlus = True ) :

        for key,val in zip(['',                     'XY',   'Z',   'E',      'T2',    'T',   'Phi'],
                           [mu,np.array([mu.x(),mu.y()]),mu.z(),mu.e(),mu.Perp2(),mu.Pt(),mu.Phi()]) : setattr(self,"mu"+key,val)

        for key,val in zip(['massW2','massT','invT','bound','sign','rawB','nuXY','fitNu'],
                           [massW**2,massT,1./widthT,False,[-1,1][zPlus],b,nuXY,utils.LorentzV()]) : setattr(self,key,val)

        self.bXY = np.array([b.x(),b.y()])

        eig,self.Rinv = np.linalg.eig(nuErr)
        self.R = self.Rinv.transpose()
        self.inv = 1./np.append([bResolution],np.sqrt(np.maximum(1,eig)))

        self.setFittedNu(nuXY)
        _,self.rawW,self.rawT = np.cumsum([mu,self.fitNu,self.rawB])
        
        self.residualsBSLT = self.fit()
        self.chi2 = self.residualsBSLT.dot(self.residualsBSLT)
        _,self.fitW,self.fitT = np.cumsum([mu,self.fitNu,self.fitB])
        
    def setFittedNu(self,nuXY) :
        P = self.massW2 + 2* nuXY.dot(self.muXY)
        self.discriminant = 1 - 4 * self.muT2 * nuXY.dot(nuXY) / P**2
        nuZ = 0.5 * P / self.muT2 * (self.muZ + self.sign*self.muE*math.sqrt(max(0,self.discriminant)))
        self.fitNu.SetPxPyPzE(nuXY[0],nuXY[1],nuZ,0)
        self.fitNu.SetM(0)

    def setBoundaryFittedNu(self,phi) :
        nuT = 0.5 * self.massW2 / (self.muT * (1 - math.cos(self.muPhi-phi)))
        self.setFittedNu( nuT * np.array([math.cos(phi), math.sin(phi)]) )
        
    def fit(self) :
        def lepResiduals(d) : # deltaB, dS, dL
            self.fitB = self.rawB * (1+d[0])
            self.setFittedNu(self.nuXY - d[0]*self.bXY + self.Rinv.dot(d[1:]))
            return np.append( self.inv * d,
                              self.invT * (self.massT - (self.mu + self.fitNu + self.fitB ).M()) )
        
        def lepBoundResiduals(x) : # deltaB, phi
            self.fitB = self.rawB * (1+x[0])
            self.setBoundaryFittedNu(x[1])
            nuXY = [self.fitNu.x(),self.fitNu.y()]
            dS,dL = self.R.dot(nuXY - self.nuXY + x[0]*self.bXY)
            return np.append( self.inv * [x[0],dS,dL],
                              self.invT * (self.massT - (self.mu + self.fitNu + self.fitB).M()) )

        deltas,_ = opt.leastsq(lepResiduals, 3*[0], epsfcn=0.01, ftol=1e-3)
        if 0 <= self.discriminant : return lepResiduals(deltas)
        self.bound = True
        best,_ = opt.leastsq(lepBoundResiduals, [0, math.atan2(self.nuXY[1],self.nuXY[0])], epsfcn=0.01, ftol=1e-3)
        return lepBoundResiduals(best)
        
###########################
class leastsqHadronicTop(object) :
    '''Fit three jets to the hypothesis t-->bqq.

    Index 2 is the b-jet.
    Resolutions are expected in units of sigma(pT)/pT.'''

    def __init__(self, jetP4s, jetResolutions, massT = 172.0, widthT = widthTop, massW = 80.4, widthW = 2.085/2 ) :
        for key,val in zip(['massT','massW','invT','invW'],
                           [massT,massW,1./widthT,1./widthW]) : setattr(self,key,val)
        
        self.rawJ = jetP4s;
        self.invJ = 1./np.array(jetResolutions)
        self.fit()
        _,self.fitW,self.fitT = np.cumsum(self.fitJ)
        _,self.rawW,self.rawT = np.cumsum(self.rawJ)

    def fit(self) :
        def hadResiduals(d) :
            _,W,T = np.cumsum(self.rawJ * (1+d))
            return np.append((d*self.invJ), [ (self.massW-W.M())*self.invW,
                                              (self.massT-T.M())*self.invT])

        self.deltaJ,_ = opt.leastsq(hadResiduals,3*[0],epsfcn=0.01, ftol=1e-3)
        self.fitJ = self.rawJ * (1+self.deltaJ)
        self.residualsPQBWT = hadResiduals(self.deltaJ)
        self.chi2 = self.residualsPQBWT.dot(self.residualsPQBWT)
###########################
class leastsqHadronicTop2(object) :
    '''Fit three jets to the hypothesis t-->bqq.

    Index 2 is the b-jet.
    Resolutions are expected in units of sigma(pT)/pT.'''

    def __init__(self, jetP4s, jetResolutions, massT = 172.0, massW = 80.4) :
        self.Wm2,self.Tm2 = massW**2,massT**2
        self.rawJ = jetP4s;
        self.invJ = 1./np.array(jetResolutions)
        self.fit()
        _,self.fitW,self.fitT = np.cumsum(self.fitJ)
        _,self.rawW,self.rawT = np.cumsum(self.rawJ)

    @staticmethod
    def deltas(P, givenQ, motherMass2) :
        p_m2 = P.M2()
        dot = P.E() * givenQ.E() - P.P() * givenQ.P() * r.Math.VectorUtil.CosTheta(P,givenQ) # PtEtaPhiM coordinate LVs fail to implement ::Dot()
        dmass = motherMass2 - givenQ.M2()
        if not p_m2 : return  (0.5 * dmass / dot - 1,)
        disc = math.sqrt(dot**2 - p_m2*(2*dot + p_m2 - dmass))
        return  ((-dot+disc)/p_m2,
                 (-dot-disc)/p_m2)

    def fit(self) :
        def hadResiduals(d0) :
            j0 = self.rawJ[0]*(1+d0[0])
            self.deltaJ,residuals = min( [ (deltaJ, deltaJ*self.invJ)
                                           for deltaJ in [ np.array([d0[0],d1,d2])
                                                           for d1 in self.deltas( self.rawJ[1], j0                      , self.Wm2)
                                                           for d2 in self.deltas( self.rawJ[2], j0 + self.rawJ[1]*(1+d1), self.Tm2)
                                                           if d1>-1 and d2>-1] ],
                                         key = lambda x: x[1].dot(x[1]))
            return residuals

        opt.leastsq(hadResiduals,[0],epsfcn=0.01, ftol=1e-3)
        self.residualsPQB = hadResiduals(self.deltaJ)
        self.chi2 = self.residualsPQB.dot(self.residualsPQB)
        self.fitJ = self.rawJ * (1+self.deltaJ)
###########################


class leastsqLeptonicTop2(object) :
    '''Fit jet, lepton, and missing energy to the hypothesis t-->blv.'''

    def __init__(self, b, bResolution, mu, nuXY, nuErr, 
                 massT = 172.0, massW = 80.4) :

        c = r.Math.VectorUtil.CosTheta(mu,b)
        s = math.sqrt(1-c*c)

        Wm2 = massW**2
        mu_p = mu.P()
        b_p = b.P()
        b_e = b.E()
        b_m2 = b.M2()
        #b_e2 = b_m2 + b_p**2
        #b_e = math.sqrt(b_e2)
        Q = 0.5 * (massT**2 - Wm2 - b_m2)

        #A_munu = np.array([[  0, 0,               x0],
        #                   [  0, 1,                0],
        #                   [ x0, 0, Wm2 - x0**2]])
        #R = np.array([[c, -s, 0],
        #              [s,  c, 0],
        #              [0,  0, 1]])
        #A_b = R.dot(np.array([[  b_m2/b_e2, 0,          -Q*b_p/b_e2],
        #                      [          0, 1,                    0],
        #                      [-Q*b_p/b_e2, 0, Wm2 - Q**2/b_e2]])).dot(R.transpose())

        x0 = -Wm2 / (2*mu_p)
        #y0 = -( x0*c + Q/b_p ) / s
        #self.x0, self.y0 = x0, y0
        #self.A_munu, self.A_b = A_munu, A_b
        #self.evals,v = np.linalg.eig( np.linalg.inv(A_munu).dot(A_b) )
        #self.valid = any(e.imag for e in self.evals)

        denom = b_e - c*b_p
        y1 = - s*x0*b_p / denom
        x1 = (x0*b_e + Q) / denom - y1**2/x0
        #print "( %.1f, %.1f )"%( x1, y1 )
        #if not self.valid : return
        Z2 = x0**2 - Wm2 - 2*x0*x1 - y1**2
        if Z2 < 0 : return
        Z = math.sqrt( Z2 )

        #coords = [np.array([ x1 - (y1/x0)*(Z), y1+Z, 1]).transpose(),
        #          np.array([ x1 + (y1/x0)*(Z), y1-Z, 1]).transpose()]
        #
        #for coord in coords :
        #    print "( %.1f, %.1f )"%tuple(coord[:2]),
        #    print coord.transpose().dot(A_munu).dot(coord),
        #    print coord.transpose().dot(A_b).dot(coord)

        def R(axis, angle) :
            '''axis 0,1,2 correspond to x,y,z; angle in radians'''
            c,s = math.cos(angle),math.sin(angle)
            R = c * np.eye(3)
            for i in [-1,0,1] : R[ (axis-i)%3, (axis+i)%3 ] = i*s + (1 - i*i)
            return R

        b_theta = b.theta()

        R_z = R(2, -mu.phi() )
        R_y = R(1,  0.5*math.pi - mu.theta() )
        sinB__ = R_y[2,0] * math.cos(b_theta) * math.cos(b.phi() - mu.phi())  + R_y[0,0] * math.sin(b_theta)
        cosB__ = math.sqrt(1-sinB__**2)
        R_x = np.array([[1,      0,       0],
                        [0, sinB__, -cosB__],
                        [0, cosB__,  sinB__]])

        R_T = np.dot( R_z.transpose(), np.dot( R_y.transpose(), R_x.transpose() ) )


        def nu(t) :
            c = math.cos(t)
            return R_T.dot( np.array([ x1 - mu_p - Z*c*y1/x0,
                                       y1 + Z*c,
                                       Z * math.sin(t) ]).transpose())

        fitNu = utils.LorentzV()
        for i in range (1000) :
            x,y,z = nu(i*math.pi*2/1000)
            fitNu.SetPxPyPzE(x,y,z,0); fitNu.SetM(0)
            _,W,T = np.cumsum([fitNu,mu,b])
            print (6*"%.2f\t")%(x,y,z,fitNu.M(),W.M(), T.M())
