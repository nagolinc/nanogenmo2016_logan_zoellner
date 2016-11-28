rules=['''#DESC

world
  The world
PROP
  [intro]
  [meetJill]
  [upHill]
  [downHill]
  [seeAnimal]

intro
  There once was a boy named Jack.<br>
PROP
  [is_world::=TRUE]
  
meetJill
  Jack met a girl named Jill.<br>
PROP
  [is_world::=TRUE]
  
upHill
  Jack went up a hill.<br>
PROP
  [is_world::=TRUE]
  
downHill
  Jack went down the hill.<br>
PROP
  [is_world::=TRUE]
  
seeAnimal
  Jack saw an [animal].<br>
PROP
  [is_world::=TRUE]
  
animal
  dog
  cat
  bear
  pig
  lion
  

''',
'''#SSM

[story]=[intro][meetJill][hillEvent::k]
[hillEvent:1]=[upHill][seeAnimal][downHill]


''']





