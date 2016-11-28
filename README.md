##############
#
# © 2016 Logan Zoellner
# All Rights Reserved
#
###########


We can generate a story using 2 basic elements:
1) A world
and
2) A story generator


A "world" stores a persistent state
containing information about
characters, setting, plot devices
and other information necessary
for the generation.
The "world" has a tree-structure where
different branches in the tree
represent different possible paths
the story can take.  For example,
the root node 

"Once upon a time there was a boy named Jack."

might have 2 nodes

"Jack went up a hill."

and

"Jack met a girl named Jill."

With one of these representing an action, and another
introducing another character.
Traveling down the "Jack went up a hill."
node will lead to another world object
in which the "location" attribute is now

"up a hill"

whereas traveling down the "Jack met a girl named Jill."
node will result in a world object with "Jill" added
to a list of Jack's friends.
In this way, each branch represents a different parallel
world that the story can pass through.
A story can be built up by passing through branches of the
new "child" world.
For instance, we could first travel down the "Jack went up a hill branch."
and then the "Jack met a girl named Jill." branch, resulting
in the story
"Once upon a time there was a boy named Jack.  Jack went up a hill.  Jack met a girl named jill"
After traveling down these branches, the new world state will have
both the "up a hill" location attribute and the "Jill" friend attribute.

In addition to the "world", there is also a storytelling object,
which is responsible for choosing the "path" through the 
world-tree that the story takes.
For instance, we may have a storyteller with the following instructions
[story]=[introduce Jack] [Jack meets Jill] [Jack goes up a Hill] [Jack goes down a hill]
This isn't very helpful, because it means we have to specify every part of
our story, but we can use repetition and combination to create
more complicated stories.  For example, we can define a new combination
[hill Adventure]=[Jack went up a hill] [Jack went down a hill]
and have our story be:

[story]=[introduce Jack] [Jack meets Jill] {[hill Adventure] x 100}

Our story will now be:

There once was a boy named Jack

Jack met a girl named Jill.

Jack went up a hill.

Jack went down a hill.

Jack went up a hill.

Jack went down a hill.

... (100 times)

Jack went up a hill.

Jack went down a hill.


This still isn't very interesting until we start adding
variation.
Suppose our world object had a child node:
"Jack saw a [random animal]",
where "[random Animal]" was replaced with an animal from a list of animal names.
We can now change our hill Adventure to

[hill Adventure]=[Jack went up a hill] [Jack sees animal] [Jack went down a hill]

And our story will look more like:

Jack went up a hill.

Jack went down a hill.

Jack saw a cat.

Jack went up a hill.

Jack saw a dog.

Jack went down a hill.

... (100 times)

Jack went up a hill.

Jack saw a pig.

Jack went down a hill.


This still sounds very simple and formulaic, but
the possibilities with persistent states
and random generation are actually endless. 
This is even more true, because we can make our
"storyteller" choose between different choices,
and even decide what to do conditionally depending
on the state of the world.
For example, if Jack sees a bear, he may run way
but if he sees a dog, he may pet it.


In the example code, both the world and the storyteller
are implemented in python, but with a custom "language"
that makes it easier to craft stories.
The language consists of rules that tell us either

1) How to generate new states for the world object

or

2) What states the story object has

The "world" consists of rules for generating "objects" 
which have attributes, and 
the child-worlds are themselves simply attributes.
The world itself is simply the top-level object
and its child-worlds (which the story may visit)
are attributes of this world

An example of how to use this language for the story
we just described can be found in jackAndJill.py


A much more complicated set of rules can be found
in zombies.py .
I don't think this is readable at 50,000 words yet
(maybe 5000 is the max?), but individual chunks
of it seem okay at least.

  








   

























