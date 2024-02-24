import numpy as num
from . import geometry as gx
from scipy.optimize import minimize,fmin_cobyla
from . import find_centroid

class cornerCases(Exception):
    def __init__(self, value):
        self.tag = value
    def __str__(self):
        return repr(self.tag)
        
def Norm(x,y,mode='2D'):
	if mode=='2D':
		return ((x[0]-y[0])**2+(x[1]-y[1])**2)**.5
	elif mode=='3D':
		return ((x[0]-y[0])**2+(x[1]-y[1])**2+(x[2]-y[2])**2)**.5
	elif mode=='Earth1':
		return gx.E.gcd(x[0],x[1],y[0],y[1])
	else:
		raise Unknown(cornerCases)

def sum_error(x,c,r,mode):
	l=len(c)
	e=0
	for i in range(l):
		e=e+(Norm(x,c[i].std(),mode=mode) - r[i])**2
	return e
	
	
		
		
def is_disjoint(cA,fg=0):
	# Currently this function does not support sophisticated checking
	# for  disjoint area
	# on earth surface models
	l=len(cA)
	for i in range(l):
		for j in range(i+1,l):
			if not cA[j].touch(cA[i],fg=fg):
				return True
	return False
	
	
	
def lse(cA,mode='2D',cons=True):
	l=len(cA)
	r=[w.r for w in cA]
	c=[w.c for w in cA]
	S=sum(r)
	W=[(S-w)/((l-1)*S) for w in r]
	p0=gx.point(0,0,0)	#Initialized point
	for i in range(l):
		p0=p0+W[i]*c[i]
	if mode=='2D' or mode=='Earth1':
		x0=num.array([p0.x,p0.y])
	elif mode=='3D':
		x0=num.array([p0.x,p0.y,p0.z])
	else:
		print('Mode unknown...: {}'.format(mode))
		raise Unknown(cornerCases)
	if mode=='Earth1':
		fg1=1
	else:
		fg1=0
	if cons:
		print('GC-LSE geolocating...')
		if not is_disjoint(cA,fg=fg1):
			cL=[]
			for q in range(l):
				def ff(x,q=q):
					return r[q]-Norm(x,c[q].std(),mode=mode)
				cL.append(ff)
			res = fmin_cobyla(sum_error, x0,cL,args=(c,r,mode),consargs=(),rhoend = 1e-5)
			ans=res
		else:
			raise Disjoint(cornerCases)
	else:
		print('LSE Geolocating...')
		res = minimize(sum_error, x0, args=(c,r,mode), method='BFGS')
		ans=res.x
	return gx.point(ans)
	
def CCA(cA,mode='2D',detail=False):
	if mode=='2D':
		from . import shapely_2D
		P=shapely_2D.polygonize([xx.c for xx in cA],[xx.r for xx in cA])
	elif mode=='Earth1':
		from . import shapely_earth1
		P=shapely_earth1.polygonize([xx.c for xx in cA],[xx.r for xx in cA])
	else:
		print("""The combination of centroid method and
		your selected mode does not exist""")
		raise InputError(cornerCases)
	#P=polygonize([xx.c for xx in cA],[xx.r for xx in cA])
	area,n=find_centroid.maxPol(P)
	ans1=area.centroid
	ans=gx.point(ans1.x,ans1.y)
	if detail:
		return (ans,n,P,area)
	else:
		return (ans,n)

	
	
	
