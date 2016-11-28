import sys
from worldBuilder3 import *
import pdfkit


def createWorldFromRules(rules,seed="SEED"):
	'''
	rules should be a list of strings each of 
	 which when exec'd assings a list of Rule objects
	 to the variable someRules
	E.g. 
	someRules=[Rule("rule",0,[],[])]
	'''

	generatedRules=[]
	
	validRules=[]
	
	ssmDescription=""
	
	
	#accumulate rules
	for rule in rules:
		#parse descriptions
		if rule.startswith("#SSM"):
			ssmDescription+=rule
			try:
				ssm=StoryStateMachine(rule)
				ns=sum([len(x) for x in ssm.states.values()])
				validRules+=[(ns,True)]
			except:
				validRules+=[(0,False)]
		#story rule
		elif rule.startswith("#DESC"):
			someRules=parseDescription(rule)
			generatedRules+=someRules
			validRules+=[(len(someRules),True)]			
		#python rule
		else:
			try:
			#if True:
				#sr={"someRules":[],"someMetaRules":[]}
				#exec(rule,globals(),sr)
				#someRules=sr["someRules"]
				#someMetaRules=sr["someMetaRules"]
				global someRules
				global someMetaRules
				someRules=[]
				someMetaRules=[]
				#print(rule, file=sys.stderr)
				exec(rule,globals(),globals())
				assert np.alltrue([isinstance(r,Rule) for r in someRules])
				assert np.alltrue([isinstance(r,MetaRule) for r in someMetaRules])
				generatedRules+=someRules
				validRules+=[(len(someRules),True)]	
			except:
				print("\n\n\nWARNING: trouble evaluating rule:\n\n\n",rule, file=sys.stderr)
				validRules+=[(0,False)]
				continue
			
			
	#print("INFO: got %d => %d rules"%(len(rules),len(generatedRules)), file=sys.stderr)
	#print([[x.name,x.reqProp,x.outProp] for x in generatedRules], file=sys.stderr)
	
	
	#create world
	w=WorldObject(None,seed,{"is_world":True},rules=generatedRules)
	
	w.storyStateMachine=StoryStateMachine(ssmDescription)	
	
	return w,validRules
	
	
if __name__=='__main__':

	if len(sys.argv)==1 or sys.argv[1]=="zombie":
		from zombies import rules
		name="output"	
	elif len(sys.argv)>1 and sys.argv[1]=="Jack":
		from jackAndJill import rules
		name="jack"
		
	if len(sys.argv)>2:
		size=int(sys.argv[2])
	else:
		size=6000

	if len(sys.argv)>3:
		name=sys.argv[3]
		
	if len(sys.argv)>4:
		seed=sys.argv[4]
	else:
		seed="SEED"
	
	
	w,v=createWorldFromRules(rules,seed=seed)
	s=w.storyStateMachine.act(w,"story",size,seed=seed)
	f=open(name+".html",'w')
	f.write(s)
	f.close()
	pdfkit.from_file(name+".html",name+".pdf")





	
