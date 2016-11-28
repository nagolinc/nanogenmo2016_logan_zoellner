import numpy as np
import math
from SeededRandom import SeededRandom
import sys
import itertools as it

def hasattrLazy(o,a):
	if isinstance(o,WorldObject):
		return o.__hasattr__(a)

class WorldObject:
	def __init__(self,parent,seed,properties=None,rules=None):
		self.parent=parent
		self.seed=seed
		self._properties=dict(properties) or {}
		self._has={}
		#self._rules={rule.name:rule for rule in (rules or [])}
		self._rules=rules or []		
		self._storedPropertyName=None
		
		
		self.special={"parent":self.parent,"TRUE":True,"FALSE":False,"NONE":None}
		
		if len(self._rules)>0 or self.parent is None:
		
			#and nonsense related to rules
			self._propMap={}
			#for rule in self._getRules().values():
			for rule in self._getRules():
				for propName in rule.outProp:
					self._propMap[propName]=self._propMap.get(propName,[])+[rule]
			#sort _propMap
			for l in self._propMap.values():
				l.sort(key=lambda x:(x.priority,x.name))
		else:
			self._propMap=self.parent._propMap

		
	def _getRules(self):
		if self.parent is None:
			#return dict(self._rules)
			return list(self._rules)
		rules=self.parent._getRules()
		#rules.update(self._rules)
		rules+=self._rules
		return rules
		
		
	def _p(self,propName):
		try:
			return getattr(self,propName)
		except:
			return None
		
	def _rand(self,s=""):
		return SeededRandom(self.seed+s)
		
	def _h(self,propName):
		return self.__hasattr__(propName)
	
	def __hasattr__(self,propName):
	
		#deal with .'s
		if "." in propName:
			propName=propName[:propName.index(".")]
			
		#special properties
		if propName in self.special:
			return True
			
		#numbers
		if propName[0] in "0123456789":
			return True
			
		#check stored values
		if propName in self._has:
			return self._has[propName]
		#check properties
		if propName in self._properties:
			self._has[propName]=True
			return self._has[propName]
		#check rules
		if propName in self._propMap:
			for rule in self._propMap[propName]:
				if rule.canAct(self):
					self._has[propName]=True
					return self._has[propName]
		#check dict
		self._has[propName] = False
		return self._has[propName]
	
	def __getattr__(self,propName):
		
		if "." in propName:
			i=propName.index(".")
			v=self.__getattr__(propName[:i])
			out= getattr(v,propName[i+1:])	
			return out
			
		#special properties
		if propName in self.special:
			return self.special[propName]
			
		#numbers
		if propName[0] in "0123456789":
			return int(propName)
			
	
		if propName in self._properties:
			return self._properties[propName]
		if propName in self._propMap:
			#assert propName not in self.loopCheck
			#self.loopCheck[propName]=True
			for rule in self._propMap[propName]:
				if rule.canAct(self):
					out=rule.act(self)
					self._properties.update(out)
					out= self._properties[propName]
					return out
		#print("error looking for property",propName,"in",self)
		raise AttributeError
	
	def __dir__(self):
		out=super(type(self)).__dir__()
		out+=list(self._properties)
		for propName in self._propMap:
			if hasattrLazy(self,propName):
				out+=[propName]
		return list(set(out))
	
	def __repr__(self):
		p=sorted(list(set(self._properties).union(set([p for p in self._propMap if self._h(p) if p!=p.upper()]))))
		return "WorldObject(%s)"%str(p)
		
		
	def _propertyName(self):
		if self._storedPropertyName:
			return self._storedPropertyName
		if self.parent is None:
			self._storedPropertyName = ""
			return self._storedPropertyName
		
		for k in self.parent._properties:
			if self.parent._properties[k] is self:
				self._storedPropertyName = self.parent._propertyName()+"."+k
				return self._storedPropertyName
		
		print("propertyName",self,self.parent)
		assert False
	

class Rule:
	def __init__(self,name,priority,reqProp,outProp,method=None,conditional=None):
		self.name=name
		self.priority=priority
		self.reqProp=reqProp
		self.outProp=outProp
		self.method=method
		self.conditional=conditional
	def canAct(self,other):
		for propName in self.reqProp:
			if not hasattrLazy(other,propName):
				return False
		if self.conditional is None:
			return True
		return self.conditional(other)
		
		
	def act(self,other):
		if self.method is None:
			return {propName:None for propName in self.outProp}
		return self.method(other)
		
		
		
def outputText(other):
	#list
	if isinstance(other,WorldObject) and other._h("is_list"):
		if other.num==0:
			return "nothing"
		
		if other.num==1:
			return outputText(other._p("item%d"%0))
		s=""
		for i in range(other.num-1):
			s+=outputText(other._p("item%d"%i))+", "
		s+="and "+outputText(other._p("item%d"%(other.num-1) ))
		return s
	#world object
	if isinstance(other,WorldObject) and other._h('description'):		
		out=other.description
		while "[" in out:
			start=out.index("[")
			end=out.index("]")
			propName=out[start+1:end].split(":")[0]
			prop=other._p(propName)
			if prop==None:
				text="NONE"
			else:
				text=outputText(prop)
			out=out[:start]+text+out[end+1:]
		return out
	#default
	return str(other)



		
def outputText1(other):
	#list
	if isinstance(other,WorldObject) and other._h("is_list"):
		if other.num==1:
			return outputText(other._p("item%d"%0))
		s=""
		for i in range(other.num-1):
			s+=outputText(other._p("item%d"%i))+", "
		s+="and "+outputText(other._p("item%d"%(other.num-1) ))
		return s
	#world object
	if isinstance(other,WorldObject) and other._h('description'):		
		out=other.description
		while "[" in out:
			start=out.index("[")
			end=out.index("]")
			propName=out[start+1:end].split(":")[0]
			prop=other._p(propName)
			if prop==None:
				text="<<NONE>>"
			elif isinstance(prop,WorldObject):
				text=outputText(prop)
				name=prop._propertyName()[1:]
				text="<a href=javascript:void(0) onclick=displayProperty('%s')>%s</a>"%(name,text)
			else:
				text=outputText(prop)
			out=out[:start]+text+out[end+1:]
		return out.replace("\n","<br>\n")
	#default
	return str(other)





def grabProperty(source,toGrab,toPut):
	def grab(other):
		return {toPut:source._p(toGrab)}
	return grab
	
	
def stripLines(s,sep="\n"):
	#strip lines
	s="\n".join([x.strip() for x in s.split("\n") if len(x.strip())>0])
	if sep!="\n":
		s+="\n"
	#split on sep
	return s.split(sep)

def parseForProperties(descriptions):
	properties=[]
	remember={}
	#first collect all of the properties
	t=0
	while "[" in descriptions[t:]:
		start=t+descriptions[t:].index("[")
		stop=t+descriptions[t:].index("]")
		t=stop+1
		aProperty=descriptions[start+1:stop].split(":")
		if "." in aProperty[0]:
			propName=aProperty[0][:aProperty[0].index(".")]
		else:
			propName=aProperty[0]
		if propName not in remember:
			properties+=[aProperty]
		#if aProperty[0] not in remember:
		#	properties+=[aProperty]
		remember[aProperty[0]]=True			
	return properties
	
	
def makeProperty(propName,propType, properties=None, rules=None, seed=None):
	def method(t):
		return {propName:make(propType, properties=properties, rules=rules, seed=seed)(t)}
	return method
	
	
def checkForSeed(seed):
	def check(t):
		return t.parent.seed==seed
	return check


#TODO:FIXME, should be able to assign arbitrary properties and work by
# cloning instead of funky rules!
def makeProperty1(grabbed,propName,propType, properties=None, rules=None, seed=None):
	'''
	other.propName=WorldObject(is_propType)
	 such that other.propName.toPut=other.propName.toGrab for (toPut,toGrab) in grabbed
	This is a useful idiom if (for example) you want a child-object to be the same color as the parent object
	 lion.paw.color=lion.color via method= makeProperty1(['color','color'],'paw','paw')
	and have a Rule("paw",0,['is_lion'],['paw'],method=method)
	'''
	def method(other):
		rules=[Rule("grab_%s"%toPut,-1,[],
			[toPut],method=grabProperty(other,toGrab,toPut),
			conditional=checkForSeed(other.seed) ) 
			for (toPut,toGrab) in grabbed]
		return {propName:make(propType, properties=properties, rules=rules, seed=seed)(other)}
	return method
	
	
def cloneObject(toClone,parent):
	if not isinstance(toClone,WorldObject):
		return toClone
	seed=toClone.seed
	#rules=list(toClone._rules.values())
	rules=list(toClone._rules)
	properties={}
	out=WorldObject(parent,seed,properties,rules)
	for k,v in toClone._properties.items():
		#ignore properties that are ALLCAPS
		if k==k.upper():
			continue	
		if isinstance(v,WorldObject):
			out._properties[k]=cloneObject(v,out)
		elif isinstance(v,SeekParent):
			continue
		else:
			out._properties[k]=v
	return out
	
	
def cloneWithOverrides(grabbed,propName,propType=None,defaultObject=None):
	def gen(t):
		thisObj=defaultObject
		overrides={}
		defaults={}
		if propType is not None:
			thisObj=make(propType,seed=propName)(t)
		for toProp,fromProp in grabbed:
			if toProp=="":
				thisObj=cloneObject(t._p(fromProp),t)
			else:
				if "." in toProp:
					index=toProp.index(".")
					p0,p1=toProp[:index],toProp[index+1:]
					overrides[p0]=overrides.get(p0,[])+[ [p1,"parent."+fromProp] ]
				else:
					defaults[toProp]=cloneObject(t._p(fromProp),t)
		assert thisObj is not None
		if not isinstance(thisObj,WorldObject):
			return thisObj
		for newPropName,value in defaults.items():
			thisObj._properties[newPropName]=value			
		for newPropName,newGrab in overrides.items():
			newDefault=defaults.get(newPropName,thisObj._p(newPropName))
			#print(newPropName,outputText(newDefault))			
			thisObj._properties[newPropName]=cloneWithOverrides(newGrab,thisObj,defaultObject=newDefault)(thisObj)
		return thisObj
	return gen

		
		
def addDescription(name,reqProps,description,properties="",sep="\n",priority=0,conditional=None,methods=None):

	methods=methods or {}

		
	#parsedProperties=parseForProperties(description)+parseForProperties(properties)
	parsedProperties=parseForProperties(properties+description)
	
	description=stripLines(description,sep)
	
	#properties of form (name:type:childprops)
	reqProp=reqProps.split()
	outProp=["description"]+[x[0] for x in parsedProperties]
	
	
	if len(description)>0 and len(description[0])>0:
				
		addDescription=Rule("add_description_%s"%name,priority,reqProp,["description"],
			method=makeWithRandom({"description":lambda x,r:r.choice(description)}),
			conditional=conditional)
	
		rules=[addDescription]
	else:
		rules=[]
	
	lowPriority=99+priority
	
	#rules from methods
	for propName in methods:
		rules+=[Rule("add_%s_%s"%(name,propName),priority,reqProp,[propName],
			method=lambda t,propName=propName:{propName:methods[propName](t)},
			conditional=conditional)]
			
			
	special={"parent","TRUE","FALSE","NONE"}
	
	for p in parsedProperties:
		if len(p)==0:
			continue
			
		#check for "."s
		if "." in p[0]:
			propName=p[0][:p[0].index(".")]
		else:
			propName=p[0]
		
		if propName in reqProp or propName in methods or propName in special or propName==propName.upper():
			continue
		
		#print("got here",propName)
	
		if len(p)==1:			
			rules+=[Rule("add_%s_%s"%(name,propName),lowPriority,reqProp,[propName],
				makeProperty(propName,propName,seed=propName) ,conditional=conditional)]
		
		elif len(p)==2:
			rules+=[Rule("add_%s_%s"%(name,propName),lowPriority,reqProp,[propName],
				makeProperty(propName,p[1],seed=propName) ,conditional=conditional)]				
		
		elif len(p)==3:
			#properties to clone from parent
			grabbed=[x.split("=") for x in p[2].split(",")]
			
			if len(p[1])==0:
				p[1]=propName
				
			#out[p[0]]=make(p[1],rules=rules,seed=p[0])(other)
			
			#rules+=[Rule("add_%s_%s"%(name,propName),lowPriority,reqProp,[propName],
			#	makeProperty1(grabbed,propName,p[1],seed=propName)  )]
			rules+=[Rule("add_%s_%s"%(name,propName),lowPriority,reqProp,[propName],
				lambda t,grabbed=grabbed,propName=propName,p=p:{propName:cloneWithOverrides(grabbed,propName,p[1])(t)}  
				,conditional=conditional)]
			
			
				
	return rules


		
		



class RealizeTerrain(Rule):
	def __init__(self):
		Rule.__init__(self,"realizeTerrain",0,
			["is_terrain","x","y","z"]
			,["child0","child1","child2","child3"])
		
	def act(self,other):
		seededRandom=SeededRandom(other.seed)
		x=other.x
		y=other.y
		z=other.z
		child0=WorldObject(other,seededRandom.seed(),
			{"is_terrain":True,"x":x*2,"y":y*2,"z":z+1,})
		child1=WorldObject(other,seededRandom.seed(),
			{"is_terrain":True,"x":x*2+1,"y":y*2,"z":z+1})
		child2=WorldObject(other,seededRandom.seed(),
			{"is_terrain":True,"x":x*2,"y":y*2+1,"z":z+1})
		child3=WorldObject(other,seededRandom.seed(),
			{"is_terrain":True,"x":x*2+1,"y":y*2+1,"z":z+1})
		
		return {"child0":child0,"child1":child1,"child2":child2,"child3":child3}

			
class AddTerrain(Rule):
	def __init__(self):
		Rule.__init__(self,"addTerrain",0,["is_world"],["terrain"])
	def act(self,other):
		seededRandom=SeededRandom(other.seed)
		terrain=WorldObject(other,seededRandom.seed(),
			{"is_terrain":True,"x":0,"y":0,"z":0},
			[RealizeTerrain()])
		return {"terrain":terrain}


def whichChild(other):
	dx=other.x-other.parent.x*2
	dy=other.y-other.parent.y*2
	return dx+2*dy



class ContinuousField(Rule):
	def __init__(self,fieldName,seedName,z0=0,z1=0,power=2,heightFunction=None):
		self.fieldName=fieldName
		self.z0=z0
		self.z1=z1
		self.power=power
		self.heightFunction=heightFunction
		self.seedName=seedName
		Rule.__init__(self,"add_field_%s"%self.fieldName,0,["is_terrain","x","y","z"],
			["_v%d_field_%s"%(i,self.fieldName) for i in range(4)]+[self.fieldName])
	
	def falloff(self,z):
		if z<self.z0:
			return 0
		if z<=self.z1:
			return 1
		return 1/self.power**(z-self.z0)
		
	def computeHeight(self,hp,x,y,z,terrainSeed):
		if self.heightFunction is not None:
			h= self.heightFunction(hp,x,y,z)
			if h is not None:
				return h
		fo=self.falloff(z)
		return hp+SeededRandom("terrain_%s_%d_%d_%d"%(terrainSeed,x,y,z)).zRandom()*fo
	
	def act(self,other):
		'''
		0-1
		|x|
		2-3
		'''
		x=other.x
		y=other.y
		z=other.z		
		f=["_v%d_field_%s"%(i,self.fieldName) for i in range(4)]		
		if other.parent is not None and hasattrLazy(other.parent,"is_terrain"):
			w=whichChild(other)
			hp0=other.parent._p(f[0])
			hp1=other.parent._p(f[1])
			hp2=other.parent._p(f[2])
			hp3=other.parent._p(f[3])
			hp01=(hp0+hp1)/2
			hp02=(hp0+hp2)/2
			hp13=(hp1+hp3)/2
			hp23=(hp2+hp3)/2
			hx=(hp0+hp1+hp2+hp3)/4
			if w==0:
				h=[hp0,hp01,hp02,hx]
			elif w==1:
				h=[hp01,hp1,hx,hp13]
			elif w==2:
				h=[hp02,hx,hp2,hp23]
			elif w==3:
				h=[hx,hp13,hp23,hp3]
		else:
			h=[0,0,0,0]
		fo=self.falloff(z)
		#h[0]+=SeededRandom("terrain_%s_%d_%d_%d"%(self.terrainSeed,x,y,z)).zRandom()*fo
		#h[1]+=SeededRandom("terrain_%s_%d_%d_%d"%(self.terrainSeed,x+1,y,z)).zRandom()*fo
		#h[2]+=SeededRandom("terrain_%s_%d_%d_%d"%(self.terrainSeed,x,y+1,z)).zRandom()*fo
		#h[3]+=SeededRandom("terrain_%s_%d_%d_%d"%(self.terrainSeed,x+1,y+1,z)).zRandom()*fo
		#get terrain seed
		terrainSeed=searchParents(other,self.seedName)._p(self.seedName)		
		#adjust heights
		h[0]=self.computeHeight(h[0],x,  y,  z, terrainSeed)
		h[1]=self.computeHeight(h[1],x+1,y,  z, terrainSeed)
		h[2]=self.computeHeight(h[2],x  ,y+1,z, terrainSeed)
		h[3]=self.computeHeight(h[3],x+1,y+1,z, terrainSeed)
		
		out= {f[i]:h[i] for i in range(4)}
		out[self.fieldName]=np.mean(h)
		return out
		


def getPatch(terrain,x,y,z):
	if x<0 or x>=1 or y<0 or y>=1:
		return None

	while z>0:
		v0=int(x*2)
		v1=int(y*2)
		v=v0+v1*2
		terrain=terrain._p("child%d"%v)
		x=(x*2)%1
		y=(y*2)%1
		z=z-1
	return terrain

def getField(terrain,fieldName,k):
	arr=[[getPatch(terrain,x,y,k)._p(fieldName) for y in np.linspace(0,1,2**k,endpoint=False)] for x in np.linspace(0,1,2**k,endpoint=False) ]
	return np.array(arr)
	
def getMap(terrain,k):
	h=getField(terrain,"terrainHeight",k)
	return h*(h>0)


def getObjects0(terrain,k,objectType):
	arr=[getPatch(terrain,x,y,k) for y in np.linspace(0,1,2**k,endpoint=False) for x in np.linspace(0,1,2**k,endpoint=False)]
	arr=[t for t in arr if hasattrLazy(t,"has_%s"%objectType) and t._p("has_%s"%objectType)>0]
	return arr

def getObjects1(terrain,k,objectType):
	has="has_%s"%objectType
	out=[terrain]
	for i in range(k):
		out=[t._p("child%d"%i) for t in out for i in range(4) if hasattrLazy(t._p("child%d"%i),has) and t._p("child%d"%i)._p(has)>0 ]
	return out
	
def getObjects(terrain,k,propName):
	arr=[getPatch(terrain,x,y,k) for y in np.linspace(0,1,2**k,endpoint=False) for x in np.linspace(0,1,2**k,endpoint=False)]
	arr=[t for t in arr if t._h(propName)]
	return arr

class AddObjects(Rule):
	def __init__(self,objectType,numObject,reqProp,conditional):
		self.objectType=objectType
		self.numObject=numObject
		self.conditional=conditional
		Rule.__init__(self,"add_%s"%self.objectType,1,reqProp,["has_%s"%self.objectType])
	
	def canAct(self,other):
		if not Rule.canAct(self,other):
			return False
		return self.conditional(other)
	def act(self,other):
		return {"has_%s"%self.objectType:self.numObject}

class Scatter(Rule):
	def __init__(self,objectType,reqProp,conditional):
		self.objectType=objectType
		self.conditional=conditional
		Rule.__init__(self,"scatter_%s"%self.objectType,1,reqProp,["has_%s"%self.objectType])


	def canAct(self,other):
		
		if not Rule.canAct(self,other):
			return False
		
		if other.parent is None or not hasattrLazy(other.parent,"has_%s"%self.objectType):
			return False
		
		if other.parent._p("has_%s"%self.objectType)<=0:
			return False
		
		return self.conditional(other)
		
	
	def act(self,other):
		has="has_%s"%self.objectType
		seededRandom=SeededRandom("scatter_%s_%s"%(self.objectType,other.parent.seed))
		children=[i for i in range(4) if hasattrLazy(other.parent._p("child%d"%i),"has_%s"%self.objectType) ]
		w=whichChild(other)
		if w not in children:
			return {has:0}
		v=other.parent._p("has_%s"%self.objectType)
		scatter=seededRandom.scatter(v,len(children))
		thisV=scatter[children.index(w)]
		return {has:thisV}

def checkHeight(h0,h1,fieldName,z):
	def check(other):
		if other.z>z:
			return False
		v=[other._p("_v%d_field_%s"%(i,fieldName)) for i in range(4)]
		mx=np.max(v)
		mn=np.min(v)
		return not (mx<h0 or mn>h1)
	return check
	
	
def checkField(v0,v1,fieldName):
	def check(other):
		v=[other._p("_v%d_field_%s"%(i,fieldName)) for i in range(4)]
		mx=np.max(v)
		mn=np.min(v)
		return not (mx<v0 or mn>v1)
	return check
	
def coinFlip(seed,p):
	def check(other):
		seededRandom=SeededRandom("%s_%s"%(other.seed,seed))
		return seededRandom.random()<p
	return check
	
def And(*args):
	def check(other):
		for f in args:
			if not f(other):
				return False
		return True
	return check


def dJoin(*dicts):
	out={}
	for d in dicts:
		out.update(d)
	return out

	
def make(objectType,properties=None,rules=None,seed=None):
	seed=seed or objectType
	rules=rules or []
	properties=properties or {}
	def gen(other):
		seededRandom=SeededRandom("%s_%s"%(other.seed,seed) )
		return WorldObject(other,seededRandom.seed(),dJoin({"is_%s"%objectType:True},properties),rules)
	return gen
	
def makeWithRandom(properties):
	def gen(other):
		outProp={}
		keys=sorted(list(properties.keys()))
		for k in keys:
			v=properties[k]
			random=SeededRandom("%s_%s"%(other.seed,k))
			outProp[k]=v(other,random)
		return outProp
	return gen
	
def sample(terrain,z,seed,weight=None):
	seededRandom=SeededRandom(seed)
	for i in range(z):
		if weight is not None:
			w=[weight(terrain._p("child%d"%i)) for i in range(4)]
		else:
			w=[0]*4
		i= seededRandom.weightedRandom(range(4),w)
		terrain=terrain._p("child%d"%i)
	return terrain

		
addCities=AddObjects("city",20,["is_terrain","z"],lambda x:x.z==0)
scatterCities=Scatter("city",["is_terrain","z","terrainHeight"],checkField(0,2,"terrainHeight") )
	
#why didn't we run into these problems at work?
# we did, just didn't notice it yet

#would I rather do a long-tailed distribution for cities like I did before?

		
def searchParents(other,propName):
	while other is not None:
		if other._h(propName):
			return other
		other=other.parent
	return None
	
def searchParentsAll(other,propName):
	out=[]
	while other is not None:
		if other._h(propName):
			out+=[other]
		other=other.parent
	return out
	
	
def addPropertiesWithRandom(seed,propGens,reqProp):
	outProp=list(propGens.keys())
	def gen(other):
		random=SeededRandom("%s_%s"%(other.seed,seed))
		#I need to sort the order of the keys!
		keys=sorted(list(propGens.keys()))
		out= {k:propGens[k](other,random) for k in keys}
		return out
	return Rule("add_properties_%s"%seed,0,reqProp,outProp,gen)


		
def dist(obj0,obj1,dx=0,dy=0):
	x1=obj1.x*2**(obj0.z-obj1.z)
	y1=obj1.y*2**(obj0.z-obj1.z)
	return ((obj0.x+dx-x1)**2+(obj0.y+dx-y1)**2)**0.5


def chooseType(seed,labels,weights,reqProp):
	c=np.concatenate([[0],np.cumsum(weights)])/np.sum(weights)
	
	def checkV(v0,v1):
		def check(t):
			r=SeededRandom("%s_%s"%(t.seed,seed)).random()
			return v0<r and r<v1
		return check
	
	def addLabel(l):
		def method(t):
			return {l:True}
		return method
	
	return [Rule("add_label_%s_%s"%(seed,l),0,
		reqProp,[l],addLabel(l),
		checkV(c[i],c[i+1]) ) for i,l in enumerate(labels) ]


#maybe update getattr so it handles obj.prop1.prop2 constructs?

def listObject(parent,seed,l):
	SeededRandom(parent.seed+seed).seed()
	properties={"is_list":True,"num":len(l)}
	#properties.update({"item%d"%i:l[i] for i in range(len(l))})
	out=WorldObject(parent,seed,properties)
	for i,item in enumerate(l):
		out._properties["item%d"%i]=cloneObject(item,out)
	return out
	


def ic(s):
	return s[:1].upper()+s[1:]


def Not(conditional):
	def check(t):
		return not conditional(t)
	return check


def patchInPatch(a,b):
	x0=b.x*2**(a.z-b.z)
	x1=x0+2**(a.z-b.z)
	y0=b.y*2**(a.z-b.z)
	y1=y0+2**(a.z-b.z)
	return x0<=a.x and a.x<=x1 and y0<=a.y and a.y<=y1
	
	
def patchInSquare(a,b):
	x0=(b.x-b.radius)*2**(a.z-b.z)
	x1=x0+2*b.radius*2**(a.z-b.z)
	y0=(b.y-b.radius)*2**(a.z-b.z)
	y1=y0+2*b.radius*2**(a.z-b.z)
	return x0<=a.x and a.x<=x1 and y0<=a.y and a.y<=y1
	
def d2(x0,y0,x1,y1):
	return ((x0-x1)**2+(y0-y1)**2)**0.5
	
def patchIntCircle(a,b):
	x2=b.x*2**(a.z-b.z)
	y2=b.y*2**(a.z-b.z)
	r2=b.radius*2**(a.z-b.z)
	x=np.clip(x2,a.x,a.x+1)
	y=np.clip(y2,a.y,a.y+1)
	d=d2(x,y,x2,y2)
	return d<r2
	
def patchInCircle(a,b):
	x2=b.x*2**(a.z-b.z)
	y2=b.y*2**(a.z-b.z)
	r2=b.radius*2**(a.z-b.z)
	return d2(a.x,a.y,x2,y2)<r2 and d2(a.x+1,a.y+1,x2,y2)<r2 and d2(a.x+1,a.y,x2,y2)<r2 and d2(a.x,a.y+1,x2,y2)<r2

	
def patchInObject_circle(objectName):
	def check(t):
		p=searchParentsAll(t,objectName)
		for t2 in p:
			if patchInCircle(t,t2._p(objectName)):
				return True
		return False
	return check

def placeNonintersectingObjects(objectName,reqProp,z0,z1,inside=None,method=None,conditional=None):
	
	#inside(a,b) should tell us if a is inside b
	if inside is None:
		inside=patchInPatch
	
	def insideAnother(t):
		parents=searchParentsAll(t.parent,objectName)
		for p in parents:
			if inside(t,p._p(objectName)):
				return True
		return False
		
	if method is None:
		method=lambda t:{objectName:make(objectName)}
	
	if conditional is None:
		conditional=lambda t:True
	
	placeObject=Rule("place_%s"%objectName,0,reqProp,[objectName],
		method=method,
		conditional=And(lambda t:t.z in range(z0,z1),conditional,Not(insideAnother))
		#conditional=conditional
	)
	return placeObject
		


def sampleInArea(seed,obj0,z,conditional,maxK=100):
	#find terrain
	terrain=searchParents(obj0,"is_terrain")
	if terrain is None:
		return None
	#convert object coordinates to terrain coordinates
	x=obj0.x*2**(terrain.z-obj0.z)-terrain.x
	y=obj0.y*2**(terrain.z-obj0.z)-terrain.y
	radius=obj0.radius*2**(terrain.z-obj0.z)
	
	stepSize=2**(z-obj0.z)
	n=int(radius/stepSize+1)
	
	#and search
	r=SeededRandom(seed)
	for i in range(maxK):
		dx=x+r.zrandom()*radius
		dy=y+r.zrandom()*radius
		patch=getPatch(terrain,dx,dy,z-terrain.z)
		if conditional(patch):
			return patch


def permuteInArea(seed,obj0,obj1,conditional,maxK=10):
	terrain=searchParents(obj0,"is_terrain")
	if terrain is None:
		return None
	#coords for obj1
	x1=obj1.x*2**(terrain.z-obj1.z)-terrain.x
	y1=obj1.y*2**(terrain.z-obj1.z)-terrain.y
	i0,j0=int(x1*2**(obj1.z-terrain.z)),int(y1*2**(obj1.z-terrain.z))
	stepSize=2**(obj0.z-obj1.z)
	z=obj0.z
	#convert object coordinates to terrain coordinates
	x=obj0.x*2**(terrain.z-obj0.z)-terrain.x
	y=obj0.y*2**(terrain.z-obj0.z)-terrain.y
	radius=obj0.radius*2**(terrain.z-obj0.z)

	
	#we are going to search for patches of the
	# form x+stepSize*i,y+stepSize*j for i in range(r/stepSize+1) for j in range(r/stepSize+1)
	n=int(radius/stepSize+1)
	r=SeededRandom("%s_%s"%(obj0.seed,seed))
	for k in range(maxK):
		fwd,bwd=r.getPermutation([n,n])
		i,j=fwd([i0,j0])
		dx,dy=x+i*stepSize,y+j*stepSize
		patch=getPatch(terrain,dx,dy,obj1.z-terrain.z)
		if conditional(patch):
			return patch







def collectList(propName,outProp=None):
	if outProp is None:
		outProp=propName
	def gen(t):
		items=[]
		#for propName1 in t._propMap:
		#	if propName1.startswith("_"+propName+"_ITEM"):
		for itemNum in range(99):
			propName1="_"+propName+"_ITEM%d"%itemNum
			if propName1 in t._propMap:
				for rule in t._propMap[propName1]:
					if rule.canAct(t):
						out=rule.act(t)
						items+=[out[propName1]]
			else:
				break
		properties={"item%d"%i:items[i] for i in range(len(items))}
		properties["num"]=len(items)
		properties["is_list"]=True
		return WorldObject(t,t.seed+"_"+outProp,properties)
	return gen

def makeList(propName,num):
	def gen(t):
		properties={"is_list":True,"num":num}
		seed=t.seed+"_LIST_"+propName
		obj=WorldObject(t,seed,properties=properties)
		for i in range(num):
			obj._properties["item%d"%i]=make(propName,seed=seed+"_item%d"%i)(obj)
		return obj
	return gen
			


def removeElementFromList(listObject,whichElement):
	def gen(t):
		n=listObject.num-1
		properties={"is_list":True,"num":n}
		obj=WorldObject(t,listObject.seed,properties=properties)
		#copy elements except i
		for i in range(whichElement):
			obj._properties["item%d"%i]=listObject._p("item%d"%i)
		for i in range(whichElement,n):
			obj._properties["item%d"%i]=listObject._p("item%d"%(i+1) )
		return obj		
	return gen
	

#def mergeLists(list0,list1):
def mergeLists(propName0,propName1):
	def gen(t):
		list0=t._p(propName0)
		list1=t._p(propName1)
		print(t.seed,propName0,propName1,[list0,list1])
		seed=list0.seed+"_"+list1.seed
		n=list0.num+list1.num
		properties={"is_list":True,"num":n}
		obj=WorldObject(t,seed,properties=properties)
		#copy elements except i
		for i in range(list0.num):
			obj._properties["item%d"%i]=list0._p("item%d"%i)
		for i in range(list1.num):
			obj._properties["item%d"%(list0.num+i)]=list1._p("item%d"%i )
		print(obj)
		return obj		
	return gen


class SeekParent:
	def __init__(self,obj):
		self.obj=obj
		
		
	def _p(self,propName):
		try:
			return getattr(self,propName)
		except:
			return None
		
		
	def __getattr__(self,propName):
		#deal with "."
		if "." in propName:
			index=propName.index(".")
			obj1=self._p(propName[:index])
			if obj1 is not None:
				return obj1._p(propName[index+1:])
			else:
				return None
		#search parents
		p=searchParents(self.obj,propName)
		if p is None:
			return None
		return p._p(propName)


#helper function to render nodeGraphs


def nodeGraphRenderer(propName,method,depth=0):

	rule=Rule("render_%s"%propName,0,["is_terrain",propName],["_render_ITEM0"],
		lambda t:{"_render_ITEM0":make("render",{"x":t._p(propName).x-t._p(propName).radius,"y":t._p(propName).y-t._p(propName).radius,"z":t._p(propName).z,
		                                  "radius":t._p(propName).radius*2,
		                                  "nodeGraph":method(t),
		                                  "type":"nodeGraph",
		                                  "depth":depth,
		                                  "txt":outputText1(t._p(propName))})(t)}                
		)
	return rule



def patchRenderer(name,reqProp,method,depth=-1):
	renderPatch=Rule(name,0,["is_terrain"]+reqProp,["_render_ITEM0"],
	lambda t:{"_render_ITEM0":make("render",{"x":t.x,"y":t.y,"z":t.z,
		"radius":1,
		"color":method(t),
		"type":"patch",
		"depth":depth,
		"txt":""})(t)}
	)
	return renderPatch




def desc(name,description,properties="",sep="\n",priority=0,conditional=None,methods=None,reqProps=None):
	if reqProps is None:
		reqProps="is_"+name
	return addDescription(name,reqProps,description,properties,sep,priority,conditional,methods)




#######
#
# Story state machine
#
######


def parseForProperties1(descriptions):
	properties=[]
	#first collect all of the properties
	t=0
	while "[" in descriptions[t:]:
		start=t+descriptions[t:].index("[")
		stop=t+descriptions[t:].index("]")
		t=stop+1
		aProperty=descriptions[start+1:stop].split(":")
		properties+=[aProperty]
	return properties


#going to try out the storygen stuff here
def getList(l,*defaults):
	return [l[i] if len(l)>i and l[i] else defaults[i] for i in range(len(defaults))]
	


class StoryStateMachine:
	'''
	This allows you to write stories as a combination of substories
	for example:
	
	 [I_go_to_the_mall] = [I_get_in_my_car] [I_drive_to_the_mall] [I_buy_some_stuff] [I_drive_back_home]
	
	There is also control over the "size" of a story, and a parameter to easily repeat an element
	
	 [story:minSize:maxSize]= [part0:k/2] [part1:k/2]
	
	Note the special "k" syntax, which will evaluate whatever size is given for story
	Finally, you can combine multiple rules and one will be chosen randomly
	
	 [story]=[introduceHero][randomEvent][conclusion]
	 [randomEvent]=[bossFight]
	 [randomEvent]=[daringRomance]	 
	
	
	'''
	def __init__(self, description):
		#format is [state:minElts:maxElts] = [state0:numElements:numRepeats][state1:numElements:numRepeats]...
		self.states={}
		
		self.parseLines(description)
		
		
	def parseLines(self,description):
		lines=stripLines(description)
		i=0
		while i<len(lines):
			line=lines[i]	
			#deal with FOR
			if line.startswith("FOR"):
				index = line.index(" ")
				pairs=[ x.split("=") for x in line[index+1:].split(" ") if len(x)]
				names=[x[0] for x in pairs]
				ranges=[eval(x[1]) for x in pairs]
				for j in range(i+1,len(lines)):
					if lines[j].startswith("END"):
						break
				newStr="\n".join(lines[i+1:j])
				for ii in it.product(*ranges):
					self.parseLines(newStr.format(**dict(zip(names,ii))))
				i=j
			#comments
			elif line.startswith("#"):
				pass
			#default (new state)	
			else:			
				#deal with conditionals
				if " IF " in line:
					index=line.index(" IF ")
					conditional = eval("lambda t:"+line[index+4:])
					line=line[:index]
				else:
					conditional=lambda t:True
				#grab properties
				p=parseForProperties1(line)
				if len(p)>=2:
					#handle property 0
					p0=getList(p[0],"state0","2","999999")
					#handle other properties
					thisStates=[ getList(l,"state0","1","1")  for l in p[1:] ]
					#update states
					self.states[ p0[0] ]=self.states.get(p0[0],[])+ [ [int(p0[1]),int(p0[2]),thisStates,conditional] ]
			#and iterate
			i+=1
	
	def act(self,world,entryState,entrySize=1,entryRepeat=1,seed=""):
		output=[""]
		random=SeededRandom(seed)
	
		stack=[ [ [entryState,entrySize,entryRepeat] ] ]
		currentState=world
		
		while len(stack):
			#print(stack)
			state,size,repeat=stack[-1][0]
			try:
				possibleStates=[ z for x,y,z,c in self.states.get(state,[]) if x<=size and y>=size and c(currentState) ]
			except:
				output+=[str([state,size,currentState])]
				break
			newStates=None
			if len(possibleStates)>0:
				chosenState=random.choice(possibleStates)
				newStates=[ [x,int( eval("lambda k:"+y)(size) ), int( eval("lambda k:"+z)(size) ) ] for x,y,z in chosenState ]
			
			elif currentState._h(state) and size==1:
				currentState=currentState._p(state)
				txt=outputText(currentState)
				if txt!=output[-1]:
					output+=[txt]
			
			else:
				print("Error processing story state:",state,size,file=sys.stderr)
				output+=["{ERROR %s %d}"%(state,size)]
			
			#and step
			if repeat>1:
				stack[-1][0][2]=repeat-1
			else:
				stack[-1]=stack[-1][1:]
			if len(stack[-1])==0:
				stack=stack[:-1]
			
			#and add new state
			if newStates:
				stack+=[ newStates ]
			
			
		return " ".join(output)


def parseDescription(txt):

	someRules=[]

	name=None
	reqProp=None
	description=""
	properties=""
	mode="DONE"
	sep="\n"
	priority=0
	conditional=None
	methods={}
	
	
	lines=txt.split("\n")
	i=0
	while i<len(lines):
		line=lines[i]
		if line=="" or len(line.strip())==0:
			#generate description
			if name is not None:
				someRules+=desc(name, description, properties, sep, priority,reqProps=reqProp,conditional=conditional,methods=methods)
				name=None
				reqProp=None
				description=""
				properties=""
				mode="DONE"
				sep="\n"
				priority=0
				conditional=None
				methods={}
		#comment
		elif line.startswith("#"):
			pass
		#for
		elif line.startswith("FOR"):
			index = line.index(" ")
			pairs=[ x.split("=") for x in line[index+1:].split(" ") if len(x)]
			names=[x[0] for x in pairs]
			ranges=[eval(x[1]) for x in pairs]
			for j in range(i+1,len(lines)):
				if lines[j].startswith("END"):
					break
			newStr="\n".join(lines[i+1:j])
			for ii in it.product(*ranges):
				someRules+=parseDescription(newStr.format(**dict(zip(names,ii))))
			i=j
			
		elif line[0] in " \t":
			if mode=="description":
				description+=line+"\n"
			elif mode=="properties":
				properties+=line+"\n"
			elif mode=="method":
				line=line.strip()
				index=line.index(" ")
				propName=line[:index]
				method=eval("lambda t:"+line[index+1:])
				methods[propName]=method
		elif line.startswith("PROP"):
			mode="properties"
		elif line.startswith("METHOD"):
			mode="method"
		elif line.startswith("COND"):
			index=line.index(" ")
			conditional=eval("lambda t:"+line[index+1:])
		elif line.startswith("MULTI"):
			sep="#"
		elif line.startswith("PRIORITY"):
			priority=int(line.split()[1])
		else:
			if " " in line:
				index=line.index(" ")
				name=line[:index]
				reqProp=line[index+1:]
			else:
				name=line
			mode="description"
		i+=1
	
	#generate description
	if name is not None:
		someRules+=desc(name, description, properties, sep, priority,reqProps=reqProp,conditional=conditional,methods=methods)
	
	return someRules
	
	
	
		



















