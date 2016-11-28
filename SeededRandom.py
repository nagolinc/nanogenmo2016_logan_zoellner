import ctypes
import os

#wbd="/home/logan/Documents/SpaghettiSoup/cgi-bin/WorldBuilder"

try:
	wbd=os.environ["OPENSHIFT_REPO_DIR"]+"WorldBuilder/"
except:
	wbd="/home/logan/Documents/openShift/spaghettisoup/WorldBuilder"

_seededRandom=ctypes.CDLL(wbd+'/_seededRandom.so')
_seededRandom.random.restype=ctypes.c_float
_seededRandom.init.restype=ctypes.c_ulonglong

import scipy.stats
import numpy as np
import math

def isPrime(n):
	if n<=1 or n%2==0:
		return False
	for i in range(3,math.ceil(n**0.5)+1,2):
		if n%i==0:
			return False
	return True
	
def invModK(n,k):
	for i in range(k):
		if (n*i)%k==1:
			return i
			
def rotl(n,r,k):
	return (n<<r^(n>>(k-r)))%2**k
	
def nam(n,k):
	log_k=int(math.log(k,2))
	t= n<2**log_k
	return rotl(n,1,log_k)*t+n*(1-t)

def nam_inv(n,k):
	log_k=int(math.log(k,2))
	t=n<2**log_k
	return rotl(n,log_k-1,log_k)*t+n*(1-t)

class SeededRandom:
	'''
	Seeded random function, need to rewrite this in c
	 for speed
	'''
	def __init__(self,seed):
		
		'''
		self.seedIn=seed
		self.a=6364136223846793005
		self.c=1442695040888963
		self.x=0
		self.m=2**64
		for c in seed:
			self.x=(self.x*129+ord(c))%self.m
		#create pointer
		self.ux=ctypes.c_uint64(self.x)
		self.uxp=ctypes.pointer(self.ux)
		'''
		#and same thing using
		xc=_seededRandom.init(ctypes.c_char_p(seed.encode("utf8")),ctypes.c_int(len(seed)) )
		
		self.m=2**64
		self.x=int(xc)
		self.ux=ctypes.c_uint64(self.x)
		self.uxp=ctypes.pointer(self.ux)

		
	
	def clone(self,s=""):
		return SeededRandom(self.seedIn+s)
			
	def step0(self):
		for i in range(self.x%7+1):
			self.x=(self.x*self.a+self.c)%self.m
	
	def step(self):
		_seededRandom.step(self.uxp)
		#self.x=self.ux.value
			
	def random(self):
		self.step()
		return self.ux.value/self.m
	
	def zRandom(self):
		return 1-2*self.random()
	
	def zrandom(self):
		return 1-2*self.random()
	
	def randint(self,v0,v1=None):
		if v1 is None:
			return int(self.random()*v0)
		return v0+int(self.random()*(v1-v0) )
		#self.step()
		#return _seededRandom.randint(self.uxp,ctypes.c_int32(n))
		
	def string(self,k=8):
		abc="abcdefghijklmnopqrstuvwxyz"
		out=""
		for i in range(k):
			out+=abc[self.randint(len(abc))]
		return out
		
	def word(self,syll=3):
		vowels="aeiouy"
		consonants="bcdfghjklmnpqrstvwxz"
		sep="'-"
		s=""
		for i in range(syll):
			s+=consonants[self.randint(len(consonants))]
			s+=vowels[self.randint(len(vowels))]
			if self.random()<0.5:
				s+=vowels[self.randint(len(vowels))]
			if self.random()<0.25:
				s+=sep[self.randint(len(sep))]
		return s[:1].upper()+s[1:]
		
	def seed(self,k=8):
		abc="abcdefghijklmnopqrstuvwxyzABCDEFGJIJKLMNOPQRSTUVWXYZ0123456789"
		out=""
		for i in range(k):
			out+=abc[self.randint(len(abc))]
		return out
		
	def normal(self):
		return scipy.stats.distributions.norm.ppf(self.random())
	
	def scatter(self,n,k):
		'''throw n balls into k buckets'''
		if n<100:
			out=[0]*k
			for i in range(n):
				out[self.randint(k)]+=1
			return out
		mean=n/k
		std=mean**0.5
		d=[int(mean+self.normal()*std) for i in range(k)]
		s=sum(d)
		if s==n:
			out=d
		elif s<n:
			c=self.scatter(n-s,k)
			out=[a+b for a,b in zip(d,c)]
		elif s>n:
			c=self.scatter(s-n,k)
			out=[a-b for a,b in zip(d,c)]
		return out
	
	def weightedRandom(self,l,w):
		s=sum(w)
		if s<=0:
			return l[self.randint(len(l))]
		r=self.random()*s
		t=0
		for x,v in zip(l,w):
			t+=v
			if t>r:
				return v
		assert False
		
	def exponential(self,p):
		t=0
		while self.random()<p:
			t+=1
		return t
		
	def choice(self,l,k=1,returnList=False):
		k=max(1,min(k,len(l)))
		if k==1:
			if returnList:
				return [l[self.randint(len(l))]]
			return l[self.randint(len(l))]
		else:
			indexSet=[]
			while len(indexSet)<k:
				i=self.randint(len(l))
				if i not in indexSet:
					indexSet+=[i]
			return [l[i] for i in indexSet]
			
			
	def randomPrime(self,v0,v1):
		assert v0>=0 and v1-v0>2
		v=0
		while not isPrime(v):
			v=self.randint(v1-v0)+v1
		return v
			
	def getPermutation(self,l,nSteps=5):
		k=np.prod(l)
		logk=int(math.log(k,2))
		add=[ self.randint(k) for i in range(nSteps)]
		mult=[ self.randomPrime(k,k*2) for i in range(nSteps)]
		inv=[invModK(mult[i],k) for i in range(nSteps)]
		exor=[self.randint(2**logk) for i in range(nSteps)]
		
		def wrap(x):
			v=0
			for a,m in zip(x,l):
				v=v*m+a
			return v
			
		def unwrap(v):
			x=[0]*len(l)
			for i,m in enumerate(l[::-1]):
				x[i]=v%m
				v//=m
			return x[::-1]
		
		def fwd(x):
			out=wrap(x)
			for i in range(nSteps):
				out=(out*mult[i]+add[i])%k
				out=(out^exor[i])*(out<2**logk)+out*(out>=2**logk)
				#out=rotl(out,1,logk)
				out=nam(out,k)
			return unwrap(out)
		def bwd(v):
			out =v
			for i in range(nSteps)[::-1]:
				#out=rotl(out,logk-1,logk)
				#out=(((out^exor[i])-add[i])*inv[i])%k
				out=nam_inv(out,k)
				out=(out^exor[i])*(out<2**logk)+out*(out>=2**logk)
				out=((out-add[i])*inv[i])%k
				
			return out
		return fwd,bwd
		
		
		
		
		
		
		

