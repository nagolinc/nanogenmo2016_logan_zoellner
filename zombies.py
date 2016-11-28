rules=['''#DESC

person
  [name]
METHOD
  gender t._rand().choice(["male","female"])
PRIORITY 1


describeMale is_person gender
  [firstName:boyName]
PROP
  [lastName:name]
COND t.gender=="male"
PRIORITY 0


describeFemale is_person gender
  [firstName:girlName] 
PROP  
  [lastName:name]
COND t.gender=="female"
PRIORITY 0


  
boyName
  James
  John
  Robert
  Michael
  William
  David
  Richard
  Charles
  Joseph
  Thomas
  Christopher
  Daniel
  Paul
  Mark
  Donald
  George
  Kenneth
  Steven
  Edward
  Brian
  Ronald
  Anthony
  Kevin
  Jason
  Matthew
  Gary
  Timothy
  Jose
  Larry
  Jeffrey
  Frank
  Scott
  Eric
  Stephen
  Andrew
  Raymond
  Gregory
  Joshua
  Jerry
  Dennis
  Walter
  Patrick
  Peter
  Harold
  Douglas
  Henry
  Carl
  Arthur
  Ryan
  Roger
  Joe
  Juan
  Jack
  Albert
  Jonathan
  Justin
  Terry
  Gerald
  Keith
  Samuel
  Willie
  Ralph
  Lawrence
  Nicholas
  Roy
  Benjamin
  Bruce
  Brandon
  Adam
  Harry
  Fred
  Wayne
  Billy
  Steve
  Louis
  Jeremy
  Aaron
  Randy
  Howard
  Eugene
  Carlos
  Russell
  Bobby
  Victor
  Martin
  Ernest
  Phillip
  Todd
  Jesse
  Craig
  Alan
  Shawn
  Clarence
  Sean
  Philip
  Chris
  Johnny
  Earl
  Jimmy
  Antonio
  Danny
  Bryan
  Tony
  Luis
  Mike
  Stanley
  Leonard
  Nathan
  Dale
  Manuel
  Rodney
  Curtis
  Norman
  Allen

girlName
  Mary
  Patricia
  Linda
  Barbara
  Elizabeth
  Jennifer
  Maria
  Susan
  Margaret
  Dorothy
  Lisa
  Nancy
  Karen
  Betty
  Helen
  Sandra
  Donna
  Carol
  Ruth
  Sharon
  Michelle
  Laura
  Sarah
  Kimberly
  Deborah
  Jessica
  Shirley
  Cynthia
  Angela
  Melissa
  Brenda
  Amy
  Anna
  Rebecca
  Virginia
  Kathleen
  Pamela
  Martha
  Debra
  Amanda
  Stephanie
  Carolyn
  Christine
  Marie
  Janet
  Catherine
  Frances
  Ann
  Joyce
  Diane
  Alice
  Julie
  Heather
  Teresa
  Doris
  Gloria
  Evelyn
  Jean
  Cheryl
  Mildred
  Katherine
  Joan
  Ashley
  Judith
  Rose
  Janice
  Kelly
  Nicole
  Judy
  Christina
  Kathy
  Theresa
  Beverly
  Denise
  Tammy
  Irene
  Jane
  Lori
  Rachel
  Marilyn
  Andrea
  Kathryn
  Louise
  Sara
  Anne
  Jacqueline
  Wanda
  Bonnie
  Julia
  Ruby
  Lois
  Tina
  Phyllis
  Norma
  Paula
  Diana
  Annie
  Lillian
  Emily
  Robin
  Peggy
  Crystal
  Gladys
  Rita
  Dawn
  Connie
  Florence
  Tracy
  Edna
  Tiffany
  Carmen
  Rosa
  Cindy
  Grace
  Wendy
  Victoria
  Edith
  Kim
  Sherry
  Sylvia
  Josephine
  Thelma
  Shannon
  Sheila
  Ethel
  Ellen
  Elaine
  Marjorie
  Carrie
  Charlotte
  Monica
  Esther
  Pauline
  Emma
  Juanita
  Anita
  Rhonda
  Hazel
  Amber
  Eva
  Debbie
  April
  Leslie
  Clara
  Lucille
  Jamie
  Joanne
  Eleanor
  Valerie
  Danielle
  Megan
  Alicia
  Suzanne
  Michele
  Gail
  Bertha
  Darlene
  Veronica
  Jill
  Erin
  Geraldine
  Lauren
  Cathy
  Joann
  Lorraine
  Lynn
  Sally
  Regina
  Erica
  Beatrice
  Dolores
  Bernice
  Audrey
  Yvonne
  Annette
  June
  Samantha
  Marion
  Dana
  Stacy
  Ana
  Renee
  Ida
  Vivian
  Roberta
  Holly
  Brittany
  Melanie
  Loretta
  Yolanda
  Jeanette
  Laurie
  Katie
  Kristen
  Vanessa
  Alma
  Sue
  Elsie
  Beth
  Jeanne
  Vicki
  Carla
  Tara
  Rosemary
  Eileen
  Terri
  Gertrude
  Lucy
  Tonya
  Ella
  Stacey
  Wilma''',
'''#DESC

debug
  <br>!!!---
  debug
  person: [SEEK.person]
  friends: [SEEK.friends]
  party: [SEEK.party]
  obstacles: [SEEK.obstacles]
  ---!!!<br>
MULTI
PROP
  [is_world::=TRUE]

world
PROP
 [debug]

story
	Once upon a time, there was a person named [person].
PROP
  [is_world::=TRUE]

p
 <p>
PROP
  [is_world::=TRUE]
  
location
  mall
  school
  store
  chruch
  theatre
  movies
  band concert
  shop
  
  
enterLocation
  <br>One day [SEEK.person] went to the [location].
PROP
  [is_world::=TRUE]

exitLocation
  [SEEK.person] left the [parent.SEEK.location].<br>
PROP
  [location::=NONE]
  [is_world::=TRUE]
  [party::=LIST]
METHOD
  friends mergeLists("parent.SEEK.friends","parent.SEEK.party")(t)
  
gainFriend
  At the [SEEK.location] [SEEK.person] met [SEEK.person.hisHer] friend [friend:person]. [describePerson::person=friend]
PROP
  [is_world::=TRUE]
  [party::=parent.SEEK.party.GROW,item0=friend]


FOR i=range(5)
  
meetFriend{i}
  At the [SEEK.location] [SEEK.person] met [SEEK.person.hisHer] friend [friend:person]. 
PROP
  [is_world::=TRUE]
  [friend::=parent.SEEK.friends.item{i}]
  [party::=parent.SEEK.party.GROW,item0=friend]
  [friends::=parent.SEEK.friends.REMOVE{i}]
CONDITIONAL t.parent.SEEK.friends.num>{i}

world
PROP
  [meetFriend{i}]
 
END
  
startConversation
  [greeting::person0=person0,person1=person1]
  [greeting1:greeting:person0=person1,person1=person0]
PROP
  [person0::=SEEK.person]
  [person1::=SEEK.party.CHOICE]
  [is_world::=TRUE]

continueConversation
  [questionAndReply::person0=SEEK.person0,person1=SEEK.person1]
  [questionAndReply1:questionAndReply:person0=SEEK.person1,person1=SEEK.person0]
  [statementAndResponse::person0=SEEK.person0,person1=SEEK.person1]
  [statementAndResponse1:statementAndResponse:person0=SEEK.person1,person1=SEEK.person0]
PROP
  [is_world::=TRUE]
  
endConversation
  [goodbye::person0=parent.SEEK.person0,person1=parent.SEEK.person1]
  [goodbye1:goodbye:person0=parent.SEEK.person1,person1=parent.SEEK.person0]
PROP
  [person0::=NONE]
  [person1::=NONE]
  [is_world::=TRUE]

  
passTime
  [SEEK.person] looked around the [SEEK.location].
  [SEEK.person] wondered if any of [SEEK.person.hisHer] friends were here.
  [SEEK.person] stared at [SEEK.person.hisHer] feet in boredom.
  [SEEK.person] glanced down at [SEEK.person.hisHer] watch.
  [SEEK.person] nearly tripped and fell.  [SEEK.person.heShe.ic] looked around, hoping no one had noticed.
PROP
  [is_world::=TRUE]
  
hr
  <hr>
PROP
  [is_world::=TRUE]

chapterTitle
  <h3> Chapter [chapter]: [title] </h3><hr>
PROP
  [is_world::=TRUE]
METHOD
  chapter t.parent.SEEK.chapter+1
 
bookTitle
  <h1> [title], a [genere.CC] [drama.CC]</h1>
PROP
  [is_world::=TRUE]
  
  
world
  This is a story
PROP
  [story]
  [p][hr]
  [chapterTitle][bookTitle]
  [enterLocation][exitLocation]
  [gainFriend]
  [startConversation] [continueConversation] [endConversation]
  [passTime]
PRIORITY 99 

  
init_world is_world
PROP
  [friends::=LIST]
  [party::=LIST]
METHOD
  chapter 0
CONDITIONAL t.parent is None


  ''',
'''#SSM


#[story] = [introduceCharacter::k]

#[story] = [introduceCharacter] [introduceGoal] [obstacleEvent:k-2][completeGoal]

[story] = [bookTitle][chapterTitle][introduction:k/5][chapterTitle][risingAction:k/5][chapterTitle][climax:k/5][chapterTitle][conclusion:k/5][chapterTitle][resolution:k/5]

[introduction] = [introduceCharacter] [introductionEvent:k-1][p]
[introductionEvent::30] = [introductionEvent:k/2][introductionEvent:k/2]

[risingAction] = [introduceConflict] [risingActionEvent:k-1][resolveConflict] [p]

[climax] = [introduceClimax] [climaxEvent:k-1][resolveClimax][p]

[conclusion] = [introduceConclusion] [conclusionEvent:k-1][resolveConclusion][p]


[resolution] = [introduceResolution][resolutionEvent:k-1][p]
[resolutionEvent:30] = [resolutionEvent:k/2] [resolutionEvent:k/2]


''',
'''#DESC

salutation
  hello
  hi
  hey
  howdy
  

greeting
  "[salutation.ic]!" said [person0:person] to [person1:person]<br>
  [person0] waved to [person1]<br>

bye
  Let's talk later
  Got to go
  Well, I'd better be off
  Nice chatting
 
  
goodbye
  "[bye]", said [person0:person] to [person1:person]<br>
  "[bye1:bye]", said [person1]<br>
MULTI
  
  
yes
  yes
  yeah
  I think so
  that's right
  I agree
  couldn't have said it better

no
 no
 nah
 not really
 I don't think so
 that's wrong

maybe
  maybe
  eh, could be
  I don't know

holiday
  Christmas
  Easter
  St Valentines day
  Thanksgiving
  Independence Day
  
question
  Is school going well
  Are you looking forward to [holiday]
  Don't you just love this weather
  Did you hear about the new [genere] [drama], [title]


  
questionAndReply
 "[question]?" asked [person0:person] to [person1:person].<br>
 "[yes.ic]" replied [person1].<br>#
 "[question]?" asked [person0] to [person1].<br>
 "[no.ic]" replied [person1].<br>#
 "[question]?" asked [person0] to [person1].<br>
 "[maybe.ic]" replied [person1].<br>
MULTI


teamNameAdj
  fighting
  mighty
  heroic
  conquering
  awesome
  glorious
  amazing
  everlasting
  proud

statement
  I hope the [teamNameAdj.ic] [animal.plural.CC] win at [sport]
  I hear that [personA:person:gender=MALE] broke up with [personB:person:gender=FEMALE]
  My favorite subject is [subject]
  I love [sport]

response
  That's shocking
  Really? Me too!
  Yeah, everyone know's that

statementAndResponse
  "[statement]" said [person0:person] to [person1].<br>
  "[response]" said [person1].<br>
MULTI

  
  
  
  
  
  
  ''',
'''#DESC

occupation
  web developer
  author
  actor
  puppeteer
  marionetteer
  actuary
  administrative worker
  advertising manager
  aerial rigger
  agricultural adviser
  agricultural machinery mechanic
  agronomist
  air traffic controller
  air traffic safety technician
  aircraft instrument technician
  aircraft mechanic
  airline clerk
  ammunition and explosives operative
  animal technician
  animator
  anthropologist
  applications manager
  apprentice training officer
  archeologist
  architect
  architectural conservation officer
  art critic and historian
  art glazier and window-pane maker
  art metalworker
  art photographer
  art restorer
  articled clerk
  legal assistant
  artificial flower maker
  artistic promotions manager
  assessor
  assistant housekeeper
  assistant printing worker
  astrologer
  astronomer
  athlete
  auctioneer
  audio graphic designer
  auditor
  auto-electrician
  auxiliary shop assistant
  auxiliary worker in geological survey
  auxiliary worker in textile and clothing industry
  auxiliary worker in the timber industry
  auxiliary worker in water management
  auxiliary worker in pharmaceutical and medical production
  baker
  bank clerk
  bank clerk for commercial credit
  banking expert
  barber and hairdresser
  barman
  basket-maker and weaver
  beautician
  beekeeper
  bibliographer
  biochemist
  biologist
  biotechnologist
  biscuit maker
  blacksmith
  blasters foreman
  blast-furnaceman
  blasting works engineer
  boatman
  boiler operator
  boilermaker
  bookbinder
  bookkeeper
  bookmaker
  botanist
  brewer and maltster
  bricklayer
  broadcaster
  brush-maker
  builders labourer
  building and road machinery mechanic
  building electrician
  building fitter
  building inspector
  building machine operator
  building materials production operative
  building tinsmith
  building
  butcher and sausage-maker
  butler
  button maker
  cab
  cabinet maker
  cable car driver
  cable manufacture labourer
  camera mechanic
  camera operator
  canning worker
  capital markets clerk
  captain of an aircraft
  car mechanic
  car service worker
  care assistant
  home care assistant
  home care organiser
  career diplomat
  career guidance counsellor
  caretaker
  carpenter
  cartographer
  cellulose operator
  ceramic model maker
  ceramic painter
  ceramicist
  ceramics
  charter agent
  cheese maker
  chemical industries operative
  chemical industry production manager
  chemical laboratory technician
  chemical plant machine operator in non-ferrous metal production
  chemical plant machine operator
  chemical researcher
  chemical technologist
  chief
  children's nurse
  chimney sweep
  chipboard
  choir master
  choreographer
  circus artiste
  cleaner
  clerk for cash or credit card systems
  cloakroom attendant
  coffee roaster
  coffeehouse keeper
  commentator
  reporter
  journalist
  commercial lawyer
  company lawyer
  composer
  computer engineer
  computer equipment operator
  computer network manager
  computer programmer
  concrete worker
  conductor
  conductor
  confectioner
  conservator
  construction carpenter
  construction
  cook
  corrosion control fitter
  court executive officer
  craft ceramicist
  craft gilder
  craft glass etcher
  craft glassmaker
  craft metal founder and chaser
  craft metalworker and brazier
  craft mosaic maker
  craft plasterer
  craft stonemason
  craft upholsterer
  crane driver
  crate maker
  criminal investigator
  crop treatment operative
  croupier
  customs officer
  cutler
  dairy worker
  dance teacher
  dancer
  data transfer appliance technician
  debt collector
  decorator-paperhanger
  dental surgery assistant
  dental technician
  dentist
  developing and printing technician
  dietician
  digger
  director
  disc jockey
  dish washer
  dispatch clerk
  dispatcher
  diver
  dog trainer
  doorkeeper
  porter
  draughtsperson
  dresser
  driller
  drilling rig operator
  driver of motor vehicles
  driver's mate
  driving instructor
  dust control technician
  ecologist
  economist
  editor
  educational methods specialist
  electrical and power systems design engineer
  electrical equipment design engineer
  electrical equipment inspector
  electrical fitter
  electrician
  electroceramic production operative
  electronic equipment mechanic
  electroplating operator
  employment agent
  enamel worker
  engineering fitter
  engineering maintenance technician
  entertainment officer
  environmental protection inspector
  ergonomist
  ethnographer
  exhibitions production manager
  faith healer
  farm worker
  farmer
  fashion designer
  feed production operator
  film critic
  film designer
  film or videotape editor
  film projectionist
  financial analyst
  financial officer
  fine artist
  fire officer
  fire officer
  fire prevention officer
  fire inspector
  fish farmer
  fish warden
  fisherman
  fitter
  fitter of
  fitter of gas pipelines
  fitter of steel structures
  flight attendant
  flight engineer
  floor fitter
  flower
  shrub or plant grower
  flying instructor
  food industry production manager
  food industry technologist
  foreign exchange clerk
  foreign exchange clerk
  forester
  forester
  forestry machine operator
  forestry worker
  fortune teller
  foster parent
  foundry worker
  fringe
  fruit farmer
  funeral service assistant
  fur coat seamstress
  furnace operator
  furrier
  gardener
  gas industry inspector
  general labourer
  general labourer in petroleum refineries
  geneticist
  geographer
  geological surveying equipment mechanic
  geologist
  geomechanic technician
  geophysicist
  glass decorator
  glass jewellery maker
  glass making machine operator
  glass melter
  glass painter
  glass production worker
  glasscutter
  glassworker
  glazier
  goldsmith
  government licensing officials
  graphic designer
  gravedigger
  guide
  gunsmith
  hand embroiderer
  hand lacemaker
  harbour guard
  hardener
  harpooner
  hatter
  heating and ventilating fitter
  heating engineer
  herbalist
  high-rise work specialist
  historian
  historical monuments administrator
  horse breeder
  host
  hotel porter
  hotel receptionist
  hydrologist
  ice-cream maker
  image consultant
  industrial designer
  information assistant
  information assistant
  inspector of telecommunications equipment
  insulation worker
  insurance clerk
  insurance sales person
  collector
  insurance underwriter
  interior designer interior designer
  interpreter and translator
  investment clerk
  invoice clerk
  jeweller
  jewellery maker
  joiner and cabinetmaker
  judge
  keeper of records
  keeper of service animals
  knitter
  land surveyor
  landscape architect
  laundry worker & dry-cleaner
  laundry worker
  lecturer
  lecturer in vocational courses
  lecturer
  librarian
  lifeguard
  lift attendant
  lift fitter
  lighting technician
  lightning conductor fitter
  lithographer
  livestock farmer
  lottery ticket street vendor
  machine shop worker
  machinery inspector
  maker of non-woven textiles
  make-up artist and wigmaker
  management accountant
  management consultant
  manager
  manager
  marine engineer
  marine hotel manager
  marketing manager
  masseur
  master of ceremonies
  materials handler
  mathematician
  medical laboratory assistant
  mechanic
  mechanic
  mechanical engineering designer
  mechanical engineering production manager
  mechanical engineering technologist
  mechatronic engineer
  metal engraver
  metal grinder
  metal refiner
  metal turner
  metal worker
  metallurgist
  metallurgist of nonferrous metals
  meteorologist
  metrologist
  microbiologist
  midwife
  miller
  milling-machine operator
  mine rescue service mechanic
  mine ventilation technician
  miner
  mining air control technician
  mining electrician
  mining finisher
  mining machine operator
  mining mechanic
  mining rescue worker
  mining
  model
  modeller
  motor vehicle bodybuilder
  mountain guide
  multimedia designer
  multimedia programmer
  municipal police officer
  municipal services worker
  municipal street cleaner
  museum
  music director
  musical instrument mechanic
  musician
  musicologist
  nanny
  naturalist
  newspaper editor
  nuclear power station operator
  nurse
  nursery school teacher
  nutritionist
  office junior
  online customer services operator
  operational analyst
  operations electrician for heavy-current equipment
  operations mechanic
  operative
  operative in chemical and synthetic fibre manufacture
  operator in the tobacco industry
  operator of gas plant equipment
  operator of numerically controlled machine tools
  operator of plastic material processing machines
  optical component maker
  optical instrument mechanic
  ore crusher
  orthopaedic shoemaker
  orthotic
  orthotist
  out-of-school educator
  overhead telecommunications cable fitter
  packer
  paediatrician
  palmists
  paper worker
  paramedic
  patent agent
  paver
  asphalt layer
  pawnbroker
  pedicurist
  manicurist
  personnel officer
  pest control officer
  petroleum and petrochemical process operators
  pharmaceutical industry operative
  pharmaceutical laboratory technician
  pharmacist
  philosopher
  photographer
  photographic reporter
  physicist
  physiotherapist
  piano tuner
  pilot
  pipe fitter
  pizza maker
  plumber
  plywood maker
  police assistant
  police investigator
  police officer
  political scientist
  pollster
  post office counter clerk
  postal service worker
  postal transport worker
  postal worker
  postmaster
  poultry breeder
  poultry butcher
  powder metallurgist
  power engineering specialist
  power station supervisor
  power station
  power system worker
  power truck driver
  prefab construction worker
  press officer
  pricing officer
  priest
  primary school teacher
  printer
  printing machine mechanic
  printing technician
  prison guard
  private detective
  producer
  producer of leather goods
  product designer
  production manager
  production manager in glass and ceramics
  production manager in textile industry
  production manager in wood industry
  production technologist
  professional soldier
  prompter
  property manager
  props master
  psychiatrist
  psychologist
  psychotherapist
  public administration officer
  public notary
  public relations manager
  publican
  publisher
  purchasing officer
  quality control technician
  quality inspector
  radio and tv technician
  radio and tv transmission engineering technician
  radio officer
  radiographer
  rail transport worker
  rail vehicle mechanic
  railway carriage and wagon inspector
  railway electrician
  railway engine mechanic
  railway freight handler
  railway guard
  railway operative
  railway ticket
  railway track construction fitter
  railway yard worker
  real estate agent
  referee
  refrigeration engineer
  refuse collector
  registrar
  removal worker
  reproduction technician
  restorer of applied arts and crafts
  retoucher
  river basin keeper
  road sign assistant
  road transport technician
  rolling-mill operator
  roofer
  room maid
  rope maker
  rotating machine fitter
  rubber operator
  rubber processing machine operator
  safety and communication electrician
  safety engineer
  safety, health and quality inspector
  sales assistant
  sales manager
  sales representative
  scaffolder
  scene painter
  scene-shifter
  script editor
  script writer
  sculptor
  seaman
  secondary school teacher
  secretary
  section supervisor
  security guard
  service mechanic
  sewerage system cleaning operator
  sewing machinist
  shepherd
  goatherd
  shift engineer
  ship fitter
  ship's captain
  ship's officer
  shoemaker
  shop cashier
  shunter
  shunting team manager
  school caretaker
  school inspector
  silkworm breeder
  sericulturist
  singer
  smith
  social worker
  sociologist
  solicitor
  songwriter
  sound effects technician
  sound engineer
  spa resort attendant
  special educational needs teacher
  special effects engineer
  special needs teacher
  specialist in animal husbandry
  spectacle frame maker
  speech therapist
  spinner
  stable hand
  groom
  stage costume maker
  stage designer
  stage manager
  standards engineer
  state attorney
  station manager
  statistician
  stockbroker
  stonemason
  stonecutter
  storekeeper
  stove fitter
  stuntman
  sugar-maker
  surgical toolmaker
  surveyor's assistant
  sweet factory worker
  systems designer
  systems engineer
  tailor
  dressmaker
  tamer
  tanner
  tannery worker
  tax specialist
  tax adviser
  technical editor
  technologist in glass and ceramics
  telecommunications cable fitter
  telecommunications dispatcher
  telecommunications engineer
  telecommunications installation and repair technician
  telecommunications mechanic
  telecommunications technician
  telecommunications worker
  telephone
  teller
  textile printer
  textile refiner
  textile technologist
  textiles dyer
  the doctor
  the hygiene service assistant
  the medical orderly
  the optician
  ticket collector
  tinsmith
  tobacco technologist
  tool setter
  tool-maker
  town planner
  track engineer
  tracklayer
  tractor-driver
  trading standards officer
  traffic police officer
  train dispatcher
  train driver
  trainee
  trainer
  trainman
  tram driver
  transport supervisor
  travel agency clerk
  travel courier
  tunneller
  tutor
  typesetter
  underground mine safety engineer
  upholsterer and decorator
  usher
  valuer
  varnisher
  veterinary surgeon
  veterinary technician
  viniculturist
  wages clerk
  waiter
  wardrobe master
  warehouse clerk
  waste incineration plant worker
  water management controller
  water supply and distribution equipment operator
  water treatment plant operator
  watercourse manager
  watch-maker
  watchman
  weaver
  weaver
  weigher
  weir and dam operator
  welding operator
  well digger
  whaler
  window cleaner
  window-dresser
  winery worker
  wire-drawer
  wood carver
  wood industry technologist
  woodcutting manager
  woodworking operator
  work study engineer
  work study
  work study
  work study
  work study
  worker in electrical engineering production
  worker in gas distribution
  worker in pressing and stamping shops
  worker in recycling services
  worker in shoe production
  worker in the food industry
  worker in the paper industry
  worker in the production of building materials
  worker the in fur processing industry
  worker
  zookeeper

sport
  baseball
  basketball
  football
  soccer
  tennis
  golf
  volleyball
  ultimate frisbee
  debate

animal
  aardvark
  aardwolf
  african buffalo
  african elephant
  african leopard
  albatross
  alligator
  alpaca
  american buffalo 
  american robin
  amphibian   
  anaconda
  angelfish
  anglerfish
  ant
  anteater
  antelope
  antlion
  ape
  aphid
  arabian leopard
  arctic fox
  arctic wolf
  armadillo
  arrow crab
  asp
  ass 
  baboon
  badger
  bald eagle
  bandicoot
  barnacle
  barracuda
  basilisk
  bass
  bat
  beaked whale
  bear   
  beaver
  bedbug
  bee
  beetle
  bird   
  bison
  blackbird
  black panther
  black widow spider
  blue bird
  blue jay
  blue whale
  boa
  boar 
  bobcat
  bobolink
  bonobo
  booby
  box jellyfish
  bovid
  buffalo
  buffalo
  bug
  butterfly
  buzzard
  camel
  canid
  cape buffalo
  capybara
  cardinal
  caribou
  carp
  cat   
  catshark
  caterpillar
  catfish
  cattle   
  centipede
  cephalopod
  chameleon
  cheetah
  chickadee
  chicken   
  chimpanzee
  chinchilla
  chipmunk
  clam
  clownfish
  cobra
  cockroach
  cod
  condor
  constrictor
  coral
  cougar
  cow
  coyote
  crab
  crane
  crane fly
  crawdad
  crayfish
  cricket
  crocodile
  crow
  cuckoo
  cicada
  damselfly
  deer
  dingo
  dinosaur   
  dog   
  dolphin
  donkey   
  dormouse
  dove
  dragonfly
  dragon
  duck   
  dung beetle
  eagle
  earthworm
  earwig
  echidna
  eel
  egret
  elephant
  elephant seal
  elk
  emu
  english pointer
  ermine
  falcon
  ferret
  finch
  firefly
  fish
  flamingo
  flea
  fly
  flyingfish
  fowl
  fox
  frog
  fruit bat
  gamefowl   
  galliform   
  gazelle
  gecko
  gerbil
  giant panda
  giant squid
  gibbon
  gila monster
  giraffe
  goat   
  goldfish
  goose   
  gopher
  gorilla
  grasshopper
  great blue heron
  great white shark
  grizzly bear
  ground shark
  ground sloth
  grouse
  guan   
  guanaco
  guineafowl   
  guinea pig   
  gull
  guppy
  haddock
  halibut
  hammerhead shark
  hamster
  hare
  harrier
  hawk
  hedgehog
  hermit crab
  heron
  herring
  hippopotamus
  hookworm
  hornet
  horse   
  hoverfly
  hummingbird
  humpback whale
  hyena
  iguana
  impala
  irukandji jellyfish
  jackal
  jaguar
  jay
  jellyfish
  junglefowl
  jacana
  kangaroo
  kangaroo mouse
  kangaroo rat
  kingfisher
  kite
  kiwi
  koala
  koi
  komodo dragon
  krill
  ladybug
  lamprey
  landfowl
  land snail
  lark
  leech
  lemming
  lemur
  leopard
  leopon
  limpet
  lion
  lizard
  llama
  lobster
  locust
  loon
  louse
  lungfish
  lynx
  macaw
  mackerel
  magpie
  mammal
  manatee
  mandrill
  manta ray
  marlin
  marmoset
  marmot
  marsupial
  marten
  mastodon
  meadowlark
  meerkat
  mink
  minnow
  mite
  mockingbird
  mole
  mollusk
  mongoose
  monitor lizard
  monkey
  moose
  mosquito
  moth
  mountain goat
  mouse
  mule
  muskox
  narwhal
  newt
  new world quail
  nightingale
  ocelot
  octopus
  old world quail
  opossum
  orangutan
  orca
  ostrich
  otter
  owl
  ox
  panda
  panther
  panthera hybrid
  parakeet
  parrot
  parrotfish
  partridge
  peacock
  peafowl
  pelican
  penguin
  perch
  peregrine falcon
  pheasant
  pig
  pigeon   
  pike
  pilot whale
  pinniped
  piranha
  planarian
  platypus
  polar bear
  pony
  porcupine
  porpoise
  portuguese man o' war
  possum
  prairie dog
  prawn
  praying mantis
  primate
  ptarmigan
  puffin
  puma
  python
  quail
  quelea
  quokka
  rabbit   
  raccoon
  rainbow trout
  rat
  rattlesnake
  raven
  ray 
  ray 
  red panda
  reindeer
  reptile
  rhinoceros
  right whale
  roadrunner
  rodent
  rook
  rooster
  roundworm
  saber-toothed cat
  sailfish
  salamander
  salmon
  sawfish
  scale insect
  scallop
  scorpion
  seahorse
  sea lion
  sea slug
  sea snail
  shark   
  sheep   
  shrew
  shrimp
  silkworm
  silverfish
  skink
  skunk
  sloth
  slug
  smelt
  snail
  snake   
  snipe
  snow leopard
  sockeye salmon
  sole
  sparrow
  sperm whale
  spider
  spider monkey
  spoonbill
  squid
  squirrel
  starfish
  star-nosed mole
  steelhead trout
  stingray
  stoat
  stork
  sturgeon
  sugar glider
  swallow
  swan
  swift
  swordfish
  swordtail
  tahr
  takin
  tapir
  tarantula
  tarsier
  tasmanian devil
  termite
  tern
  thrush
  tick
  tiger
  tiger shark
  tiglon
  toad
  tortoise
  toucan
  trapdoor spider
  tree frog
  trout
  tuna
  turkey   
  turtle
  tyrannosaurus
  urial
  vampire bat
  vampire squid
  vicuna
  viper
  vole
  vulture
  wallaby
  walrus
  wasp
  warbler
  water boa
  water buffalo
  weasel
  whale
  whippet
  whitefish
  whooping crane
  wildcat
  wildebeest
  wildfowl
  wolf
  wolverine
  wombat
  woodpecker
  worm
  wren
  xerinae
  x-ray fish
  yak
  yellow perch
  zebra
  zebra finch

  
insect
  ant
  bee
  wasp
  termite
  spider
  beetle
  centipede
  
  
color
  red
  orange
  yellow
  green
  blue
  indigo
  violet
  purple
  black
  white
  gray
  brown

subject
  math
  social studies
  history
  science
  physics
  chemistry
  science
  Phy-Ed
  computers
  
monster
  zombie
  ghost
  werewolf
  vampire
  killer [animal]
  killer [insect]
  dragon
  monster
  
weapon
  sword
  knife
  ax
  pike
  spear
  lance
  crowbar

actionVerb
  accelerate
  accomplish
  achieve
  acquire
  activate
  adapt
  adjust
  administer
  advise
  allocate
  analyze
  annotate
  anticipate
  apply
  appraise
  arrange
  articulate
  assemble
  assess
  assign
  attaine
  author
  balance
  brief
  budget
  calculate
  catalogue
  categorize
  chair
  change
  channel
  chart
  clarify
  coach
  code
  collaborate
  collect
  communicate
  compare
  compete
  compile
  complete
  compose
  compute
  conceive
  conduct
  confront
  consolidate
  construct
  contact
  continue
  contract
  convene
  coordinate
  correspond
  counsel
  create
  critique
  define
  delegate
  deliver
  demonstrate
  derive
  design
  detect
  determine
  develop
  devise
  diagnose
  direct
  discover
  dispense
  display
  distribute
  draft
  dramatize
  earn
  edit
  educate
  effect
  elicit
  employe
  encourage
  endure
  enlist
  entertain
  establish
  estimate
  evaluate
  examine
  exchange
  execute
  exercise
  exhibit
  expand
  expedite
  experiment
  explain
  explor
  facilitate
  finance
  focus
  forecast
  formulate
  foster
  group
  guide
  identify
  illustrate
  implement
  impose
  improve
  increase
  influence
  inform
  initiate
  inquire
  inspect
  install
  instill
  institute
  instruct
  insure
  interpret
  intervene
  interview
  introduce
  invent
  inventory
  investigate
  judge
  lecture
  listen
  locate
  maintain
  manage
  market
  master
  measure
  mediate
  model
  modify
  mold
  monitor
  motivate
  negotiate
  observe
  obtain
  operate
  organize
  outline
  oversaw
  participate
  perceive
  perform
  persuade
  plan
  predict
  prepare
  prescribe
  present
  preside
  process
  produce
  program
  promote
  protect
  provide
  publicize
  publish
  purchase
  question
  recommend
  record
  recruit
  reduce
  regulate
  reinforce
  render
  repair
  report
  represent
  reproduce
  research
  resolve
  respond
  restore
  retain
  retrieve
  review
  revise
  rewrite
  route
  schedule
  search
  select
  serve
  service
  shape
  share
  simplify
  solicite
  solve
  seek
  specify
  stimulate
  study
  succeed
  suggest
  summarize
  supervise
  support
  survey
  synthesize
  systematize
  target
  taught
  test
  train
  translate
  tutor
  update
  utilize
  verify
  visualize
  write''',
'''#basic rendering rule
renderList=Rule("render",0,["_render_ITEM0"],["render"],lambda t:{"render":collectList("render","render")(t)} )

#SEEK
seekRule=Rule("seek",0,[],["SEEK"],lambda t:{"SEEK":SeekParent(t)})

#name
namePerson=Rule("generateName",0,["is_name"],["description"],
	makeWithRandom({"description":lambda t,r:ic(r.word())}) )


#grammer

male=Rule("maleRule",0,[],["MALE"],lambda t:{"MALE":"male"})
female=Rule("femaleRule",0,[],["FEMALE"],lambda t:{"FEMALE":"female"})

def mkstr(s):
  def gen(t):
    return make(s,{"description":s})(t)
  return gen


def aAn(s):
  print("aAn",s, file=sys.stderr)
  if s[0] in "aeiouyAEIOUY":
    return "an "+s
  return "a "+s

aAnRule=Rule("aAn",0,["description"],["aAn"],lambda t:{"aAn":mkstr(aAn(outputText(t)))(t)})

def heShe(other):
	if other.gender=="female":
		return {"heShe":mkstr("she")(other)}
	elif other.gender=="male":
		return {"heShe":mkstr("he")(other)}
	return {"heShe":mkstr("it")(other)}
	
heShe_rule=Rule("heShe",0,["is_person","gender"],["heShe"],heShe)

def hisHer(other):
	if other.gender=="female":
		return {"hisHer":mkstr("her")(other)}
	elif other.gender=="male":
		return {"hisHer":mkstr("his")(other)}
	return {"hisHer":mkstr("its")(other)}
	
hisHer_rule=Rule("hisHer",0,["is_person","gender"],["hisHer"],hisHer)


def himHer(other):
	if other.gender=="female":
		return {"himHer":"her"}
	elif other.gender=="male":
		return {"himHer":"him"}
	return {"himHer":"it"}
	
himHer_rule=Rule("himHer",0,["is_person","gender"],["himHer"],himHer)


pluralExceptions={"mouse":"mice",
  "goose":"geese",
  "fish":"fish",
  "squid":"squid",
  "deer":"deer",
  }

def pluralRule(s):
  for k,v in pluralExceptions.items():
    if len(s)>=len(k) and s[-len(k):]==k:
      return s[:-len(k)]+v
  if len(s)>=1 and s[-1:] in "xsz":
    return s+"es"
  if len(s)>2 and s[-2:] in ["ch","sh"]:
    return s+"es"
  return s+"s"



plural=Rule("plural",0,["description"],["plural"],lambda t:{"plural":mkstr(pluralRule(outputText(t)))(t)})	


def ic(s):
  return s[:1].upper()+s[1:]


icRule=Rule("ic",0,["description"],["ic"],lambda t:{"ic":mkstr(ic(outputText(t)))(t)})	

commonWords=["the","is","am","to","for","a","an","by"]

def cc(s):
  	return " ".join([ss if ss in commonWords else ss[0].upper()+ss[1:] for ss in s.split(" ")])
  
ccRule=Rule("cc",0,["description"],["CC"],lambda t:{"CC":mkstr(cc(outputText(t)))(t)})


#verbs
special_ed={"write":"wrote","seek":"sought"}


def ed(s):
  for k,v in special_ed.items():
    if len(s)>=len(k) and s[-len(k):]==k:
      return s[:-len(k)]+v
  if s[-1]=="y" and s[-2] not in "aeiouy":
    return s[:-1]+"ied"
  elif s[-1]=="e":
    return s+"d"
  else:
    return s+"ed"   

def ing(s):
  if s[-1]=="e":
    return s[:-1]+"ing"
  else:
    return s+"ing"


edRule=Rule("ED",0,["description"],["ED"],lambda t:{"ED":mkstr(ed(outputText(t)))(t)})
ingRule=Rule("ING",0,["description"],["ING"],lambda t:{"ING":mkstr(ing(outputText(t)))(t)})

    
    


#some stuff for lists
addList=Rule("add_list",0,[],["LIST"],lambda t:{"LIST":make("list",{"num":0})(t)})


def growList(l):
  num=l.num
  properties={"num":num+1}
  for i in range(num):
    properties["item%d"%(i+1)]=l._p("item%d"%i)
    properties["item0"]=None
  return make("list",properties)(l)

growList_rule=Rule("list_grow",0,["is_list","num"],["GROW"],lambda t: {"GROW":growList(t)})


removeRules=[Rule("REMOVE%d"%i,0,["is_list","num"],["REMOVE%d"%i], lambda t,i=i:{"REMOVE%d"%i:removeElementFromList(t,i)(t)}, lambda t,i=i:t.num>i) for i in range(99)]


choiceRule=Rule("list_choice",0,["is_list","num"],["CHOICE"],lambda t:{"CHOICE":t._p("item%d"%t.parent._rand().randint(t.num))} )

def describeList(l):
    if l.nObjects==0:
      return "nothing"
    s=""
    for i in range(l.nObjects):
      s+="[item%d]"%i
      if i<nObjects-2:
        s+=", "
      if i==nObjects-2:
        s+=" and "
    return s

describeList_rule=Rule("list_describe",0,["is_list","nObjects"],["description"],lambda t:{"description":describeList(t)})

someRules=[renderList,seekRule,aAnRule,
           male,female,
           heShe_rule,hisHer_rule,himHer_rule,
           edRule,ingRule,
           plural,namePerson,icRule,ccRule,
          addList,growList_rule,choiceRule]+removeRules

#pointless comment




''',
'''#DESC

hungrily
  hungrily
  greedily
  viciously
  drooling
  wide-eyed
  with a toothy grin

jumped
  jumped
  leaped
  charged
  bowled
  rushed
  darted
  charged
  galavanted


  
fightAction
  The [monster] stared at [person] [hungrily].
  The [monster] suddenly [jumped] at [person].
  [person] lashed at the [monster] with [person.hisHer] [person.weapon].
  [person] narrowly dodged as the [monster] [jumped] forward.
  The [monster] [jumped] backwards as [person] lashed out at it with [person.hisHer] [person.weapon]



  
  

''',
'''#DESC

horde
  horde
  group
  pack
  bunch
  
hordeAppears
  <br>Suddenly a horde of zombies appeared
PROP
  [is_world::=TRUE]

  
finally
  finally
  at last
  
  
hordeEnds
  [finally.ic] [SEEK.person] and [SEEK.person.hisHer] friends escaped the zombie horde.
  [finally.ic] the last zombie was killed and the [horde] of zombies was gone.
PROP
  [is_world::=TRUE]
  
zombieFiller
  <br>"Brains!" moaned one of the zombies.<br>
  The zombies milled around aimlessly.
  The zombies stared into the distance with their blank eyes.
PROP
  [is_world::=TRUE]

suddenly
  suddenly
  without warning
  all of the sudden
  unexpectedly
  
zombieAttacksProtagonist
  [suddenly.ic] one of the zombies broke away from the pack and attacked [person0::=SEEK.person].
PROP
  [is_world::=TRUE]

zombieAttacksFriend
  [suddenly.ic] one of the zombies broke away from the pack and attacked [person0::=SEEK.party.CHOICE].
PROP
  [is_world::=TRUE]

  
#people have weapons now
addWeaponToPerson is_person
PROP
  [weapon::=fist]
  [fist]
PRIORITY 99


weapon
  knife
  ax
  crowbar
  metal bar
  baseball bat
  chainsaw

findWeapon
  Looking around for something to fight with, [person] happened to notice a nearby [weapon] and picked it up.
PROP
  [weapon]
  [person::=parent.SEEK.person,weapon=weapon]
  [is_world::=TRUE]
  
FOR whichFriend=range(3)

findWeapon_friend{whichFriend}
  Looking around for something to fight with, [SEEK.party.item{whichFriend}] happened to notice a nearby [weapon] and picked it up.
PROP
  [weapon]
  [party::=parent.SEEK.party,item{whichFriend}.weapon=weapon]
  [is_world::=TRUE]

world
PROP
  [findWeapon_friend{whichFriend}]
  
END


fist
  fist

stabbed
  stabbed
  poked
  thrust
  jabbed

lunged
  lunged
  jumped
  leaped
  rushed
  sprinted
  
zombieAttackContinues
  The zombie [lunged] at [person0].
  [person0] [stabbed] at the zombie with [person0.hisHer] [person0.weapon].
PROP
  [person0::=parent.SEEK.person0]
  [is_world::=TRUE]

obstacle
  trash can
  chair
  table
  potted plant
  
  
zombieAttackEnds
  [finally.ic] [SEEK.person0] decapitated the zombie.
  [finally.ic] [SEEK.person0] hid behind [obstacle.aAn] and the zombie wandered away.
PROP
  [is_world::=TRUE]
  
exhortation
  Good job
  Keep trying
  You can do it
  Atta boy
  Awesome
  Wow
  
  
shoutOfEncouragement
  <br>"[exhortation]!" shouted [SEEK.person] to [SEEK.friends.CHOICE].<br>
  <br>"[exhortation]!" shouted [SEEK.friends.CHOICE] to [SEEK.person].<br>
PROP
  [is_world::=TRUE]
  
zombieWorldEvents is_world
PROP
  [hordeAppears] [hordeEnds]
  [shoutOfEncouragement]
  [zombieAttacksProtagonist] [zombieAttacksFriend] [zombieAttackContinues] [zombieAttackEnds]
  [zombieFiller][findWeapon]

  

  
  
''',
'''#DESC

introduceCharacter
	Once upon a time, there was a person named [person].
PROP
  [is_world::=TRUE]
METHOD
  storyLevel 0
  
introductionEvent
	[filler]
PROP
  [is_world::=TRUE]
  
  
fillerEvent
  [filler]
PROP
  [is_world::=TRUE]

  
learnMoreAbout
  learn more about the [target]
METHOD
  obstacleType "learn"
  
introduceConflict
  [SEEK.person] stumbled upon a couple of scientists experimenting with [zombieOrigin.aAn].
PROP
  [is_world::=TRUE]
  [goal:learnMoreAbout:target=zombieOrigin]
  [obstacles::=parent.SEEK.obstacles.GROW,item0=goal]
METHOD
  storyLevel 1


resolveConflict
  [SEEK.person] had learned all that [SEEK.person.heShe] needed to know, the [SEEK.zombieOrigin] was creating zombies!
PROP
  [is_world::=TRUE]
  [obstacles::=parent.SEEK.obstacles.REMOVE0]
  
  
  
risingActionEvent
	[filler]
PROP
  [is_world::=TRUE]

  
  
zombies
  zombies
  
escapeFromZombies
  escape from the [target:zombies]
METHOD
  obstacleType "escape"
  
  
introduceClimax
  Suddenly, it seemed like there were zombies everywhere!
PROP
  [is_world::=TRUE]
  [escapeFromZombies]
  [obstacles::=parent.SEEK.obstacles.GROW,item0=escapeFromZombies]
METHOD
  storyLevel 2
  
resolveClimax
  <br>"This is foolish," said [SEEK.person].  "We can't keep running from the zombies, we have go go after the source, the [SEEK.zombieOrigin]!"<br>
PROP
  [is_world::=TRUE]
  [obstacles::=parent.SEEK.obstacles.REMOVE0]
  
climaxEvent
	[filler]
PROP
  [is_world::=TRUE]

destroyZombieOrigin
  destroy the [target::=SEEK.zombieOrigin]
METHOD
  obstacleType "destroy"

introduceConclusion
  If only we could get rid of the [SEEK.zombieOrigin], we could defeat the zombies, thought [SEEK.person].
PROP
  [is_world::=TRUE]
  [destroyZombieOrigin]
  [obstacles::=parent.SEEK.obstacles.GROW,item0=destroyZombieOrigin]
METHOD
 storyLevel 3  

  
resolveConclusion
  At last, [SEEK.person] was able to destory the [SEEK.zombieOrigin].
PROP
  [is_world::=TRUE]
  [obstacles::=parent.SEEK.obstacles.REMOVE0]

conclusionEvent
	[filler]
PROP
  [is_world::=TRUE]
  
  
introduceResolution
  I'm so glad we were able to destory the [SEEK.zombieOrigin] and save the world, thought [SEEK.person]
PROP
  [is_world::=TRUE]
METHOD
 storyLevel 4  

resolutionEvent
	[filler]
PROP
  [is_world::=TRUE]
  
  
  
world
PROP
  [introduceCharacter][introductionEvent]
  [introduceConflict][risingActionEvent][resolveConflict]
  [introduceClimax][climaxEvent][resolveClimax]
  [introduceConclusion][conclusionEvent][resolveConclusion]
  [introduceResolution][resolutionEvent]
  [fillerEvent]
''',
'''#DESC

zombieOrigin
  radioactive spider
  vaccine for stupidity
  time travel device
  cure for cancer
  super solider enhancement
  

  ''',
'''#SSM

[introductionEvent:5] = [enterLocation] [locationEvent:k-2] [exitLocation]
[risingActionEvent:5] = [obstacleEvent:k]
[climaxEvent:5] = [obstacleEvent:k]
[conclusionEvent:5] = [obstacleEvent:k]
[resolutionEvent:12:30] = [enterLocation] [locationEvent:k-2] [exitLocation]

[introductionEvent::12] = [fillerEvent::k]
[risingActionEvent::12] = [fillerEvent::k]
[climaxEvent::12] = [fillerEvent::k]
[conclusionEvent::12] = [fillerEvent::k]
[resolutionEvent::12] = [fillerEvent::k]


#random things that happen in a location
[locationEvent:10] = [locationEvent:k/2] [locationEvent:k-k/2]
[locationEvent] =   [gainFriend] [locationEvent:k-1] IF t.SEEK.party.num<3 and t.SEEK.friends.num+t.SEEK.party.num<5

[locationEvent] = [fillerEvent] [locationEvent:k-1]

FOR i=range(5)
[locationEvent] =  [meetFriend{i}] [locationEvent:k-1] IF t.SEEK.party.num<3 and t.SEEK.friends.num>{i}
END

[locationEvent:3:10] = [p][startConversation] [continueConversationState::k-2] [endConversation][p] IF t.SEEK.party.num>0
[locationEvent:1:1] = [passTime]

#fighting a zombie horde
[locationEvent:10:100] = [p] [hordeAppears] [zombieEvent:k-2] [hordeEnds] [p] IF t.SEEK.storyLevel in [2,3]

[zombieEvent:10] = [zombieEvent:k/2] [zombieEvent:k-k/2]
[zombieEvent:1:1] = [shoutOfEncouragement] IF t.SEEK.friends.num > 0
[zombieEvent:3:10] = [zombieAttacksProtagonist] [zombieAttackContinues::k-2] [zombieAttackEnds]
[zombieEvent:3:10] = [zombieAttacksFriend]  [zombieAttackContinues::k-2] [zombieAttackEnds] IF t.SEEK.party.num>0
[zombieEvent] = [zombieFiller] [zombieEvent:k-1]
[zombieEvent] = [findWeapon] [zombieEvent:k-1] IF t.SEEK.person.weapon.description=="fist"

FOR whichFriend=range(3)
[zombieEvent] = [findWeapon_friend{whichFriend}] [zombieEvent:k-1] IF t.SEEK.party.num>{whichFriend} and t.SEEK.party.item{whichFriend}.weapon.description=="fist"
END




''',
'''#DESC

phone
  the phone
  facetime
  snapchat
  twitter

recreationalActivity
  play videogames
  watch tv
  take a nap
  read a book about [animal.plural]
  feed my pet [animal]
  practice [sport]
  check facebook
  talk to [person] on [phone]

filler
  [SEEK.person] thought about [SEEK.person.hisHer] favorite animal, [animal.plural].
  [SEEK.person] tried to remember whether [SEEK.person.heShe] had any [subject] homework.
  <br>"I wonder what would happen if you crossed [animal1.aAn:animal] with [animal2.aAn:animal]," thought [SEEK.person] to [SEEK.person.himHer]self.<br>
  [SEEK.person] ran [SEEK.person.hisHer] hands through [SEEK.person.hisHer] hair.
  <br>"I can't wait to go home and [recreationalActivity]," thought [SEEK.person].<br>
  
''',
'''#DESC


continueConversation_introduction
  "I wonder what it would be like if there were a zombie apocalypse," said [SEEK.person0].
  "Stop worrying about things that will never happen and work on your [subject] homework," scolded [SEEK.person1].
MULTI
PROP
  [is_world::=TRUE]

continueConversation_risingAction
  "I saw some scientists experimenting with [SEEK.zombieOrigin]," said [SEEK.person0].  "I'm worried they might accidentally create a zombie."
  "You're just imagining things because you love zombies so much," said [SEEK.person1].
MULTI
PROP
  [is_world::=TRUE]
  

continueConversation_climax
  "There are zombies everywhere!" said [SEEK.person0].  "I'm so glad I've been training for this my whole life."
  "Stop rubbing it in," said [SEEK.person1].  "Some of us are actually unhappy about the apocalypse."
MULTI
PROP
  [is_world::=TRUE]
  
continueConversation_conclusion
  "Once we destory the [SEEK.zombieOrigin], this will all be over," said [SEEK.person0].
  "Great, then I can go back to my [subject] homework," said [SEEK.person1]
MULTI
PROP
  [is_world::=TRUE]
 
continueConversation_resolution
  "I'm so glad the zombies are finally gone," said [SEEK.person0].
  "Really? You seemed to enjoy fighting them," smirked [SEEK.person1].
MULTI
PROP
  [is_world::=TRUE]
  
world
PROP
  [continueConversation_introduction]
  [continueConversation_risingAction]
  [continueConversation_climax]
  [continueConversation_conclusion]
  [continueConversation_resolution]
''',
'''#SSM

[continueConversationState:1:1] = [continueConversation]
[continueConversationState:1:1] = [complementPerson]

[continueConversationState:1:1] = [continueConversation_introduction] IF t.SEEK.storyLevel==0 and t._rand().random()<0.1
[continueConversationState:1:1] = [continueConversation_risingAction] IF t.SEEK.storyLevel==1 and t._rand().random()<0.1
[continueConversationState:1:1] = [continueConversation_climax] IF t.SEEK.storyLevel==2 and t._rand().random()<0.1
[continueConversationState:1:1] = [continueConversation_conclusion] IF t.SEEK.storyLevel==3 and t._rand().random()<0.1
[continueConversationState:1:1] = [continueConversation_resolution] IF t.SEEK.storyLevel==4 and t._rand().random()<0.1




''',
'''#DESC

height
  average
  tall
  short
  medium
  tiny
  dwarfish
  gigantic

person
PROP
  [height]
  [hairColor:color]
  [eyeColor:color]
  [favoriteColor:color]
  [topColor:color]
  [bottomColor:color]
  

describePerson
  [person] was of [person.height] height with [person.hairColor] hair.
  [person]'s favorite color was [person.favoriteColor]
  [person] was wearing [person.top.aAn] and [person.bottom.aAn].
  

universalTopType
  jacket
  shirt
  sweater
  hoodie
  jersey
  
girlsTopType
  blouse
  tank top
  [universalTopType]

boysTopType
  [universalTopType]
  
universalBottomType
  pair of pants
  pair of shorts
  
girlsBottomType
  [universalBottomType]
  skirt
  pair of leggings
  
boysBottomType
  [universalBottomType]
  kilt
  
boysBottom
  [color] [boysBottomType]
  [color] [universalBottomType]

  
girlsBottom
  [color] [girlsBottomType]
  [color] [universalBottomType]

boysTop
  [color] [boysTopType]
  [color] [universalTopType]
  
girlsTop
  [color] [girlsTopType]
  [color] [universalTopType]
  
  
person
PROP
  [top:girlsTop]
  [bottom:girlsBottom]
CONDITIONAL t.gender=="female"


person
PROP
  [top:boysTop]
  [bottom:boysBottom]
CONDITIONAL t.gender=="male"

thanks
  thanks
  thank you
  aww, that's sweet
  that's so nice of you
  I really appreciate that
  
  
admire
  love
  like
  really appreciate
  admire
  am jealous of
  

complement
  I [admire] your [person.hairColor] hair
  I [admire] your [person.eyeColor] eyes
  I [admire] your [person.topColor] [person.top]
  I [admire] your [person.bottomColor] [person.bottom]
  I think it's cool that your favorite color is [person.favoriteColor]
  
complementPerson
  "[complement::person=SEEK.person1]," said [SEEK.person0].
  "[thanks]," said [SEEK.person1].
  #
  "[complement::person=SEEK.person0]," said [SEEK.person1].
  "[thanks]," said [SEEK.person0].
MULTI
PROP
  [is_world::=TRUE]

  
world
PROP
  [complementPerson]


''',
'''#DESC

goal
  save the world
  bake a pie
  travel to mars
METHOD
  obstacleType "misc"

introduceGoal
  "My goal is to [goal]," thought [SEEK.person] to [SEEK.person.himHer]self.
PROP
  [is_world::=TRUE]
  [obstacles::=parent.SEEK.obstacles.GROW,item0=goal]

  
completeGoal
  At last [SEEK.person] was able to [parent.SEEK.obstacles.item0]
PROP
  [is_world::=TRUE]
  [obstacles::=parent.SEEK.obstacles.REMOVE0]
  

obstacle_buy
  buy [target.aAn:animal]
PROP
  [goal]
  [person]
  [introduction:intro_buy:target=target,goal=goal,person=person]
  [resolution:resolve_buy:target=target,goal=goal,person=person]
METHOD
  obstacleType "buy"
  
#Types I'm considering are "find","earn","befriend"
#currently have "learn" "buy" "destory" "escape"

intro_buy
  <br>"Before I can [goal]," I need to buy [target.aAn] said [person].<br>

resolve_buy
  <br>At last [person] was able to buy [target.aAn]
  "Now that I have this [target], I'll be able to [goal]," said [person].<br>
MULTI

  
  
storyObstacle
  [obstacle::=obstacles.CHOICE]
PROP
  [goal]
  [person]
  [_obstacles_ITEM0:obstacle_buy:goal=goal,person=person]
METHOD
  obstacles collectList("obstacles")(t)
 

gainObstacleEvent
  [storyObstacle.obstacle.introduction]
PROP
  [obstacle::=storyObstacle.obstacle]
  [storyObstacle::goal=parent.SEEK.obstacles.item0,person=SEEK.person]
  [is_world::=TRUE]
  [obstacles::=parent.SEEK.obstacles.GROW,item0=obstacle]

resolveObstacleEvent
  [parent.SEEK.obstacles.item0.resolution]
PROP
  [is_world::=TRUE]
  [obstacles::=parent.SEEK.obstacles.REMOVE0]
  
  
obstacleFillerEvent
  [filler]
PROP
  [is_world::=TRUE]
 

resolveGoalFiller
  [filler]
PROP
  [is_world::=TRUE]


shyly
  shyly
  awkwardly
  sheepishly
  bashfully
  
continueConversation_obstacle
  "So, what have you been up to recently?" asked [SEEK.person1]
  "I'm trying to [SEEK.obstacles.CHOICE]," answered [SEEK.person0].
  #
  "Rumor has it that you're planning to [SEEK.obstacles.CHOICE]," said [SEEK.person1].
  "[yes]," said [SEEK.person0] [shyly]
MULTI
PROP
  [is_world::=TRUE]

  
continueConversation_obstacle2
  "Why are you trying to [SEEK.obstacles.item0]?" asked [SEEK.person1]
  "If I can [SEEK.obstacles.item0], it will help me [SEEK.obstacles.item1]" answered [SEEK.person0].
  #
  "Rumor has it that you're planning to [SEEK.obstacles.item0]," said [SEEK.person1].
  "[yes]," said [SEEK.person0] [shyly].  "It's to help me [SEEK.obstacles.item1]."
MULTI
PROP
  [is_world::=TRUE]  
  
  
  
  
world
PROP
  [introduceGoal][completeGoal]
  [gainObstacleEvent]
  [obstacleFillerEvent][resolveGoalFiller]
  [resolveObstacleEvent]
  [continueConversation_obstacle][continueConversation_obstacle2]

world_init is_world
PROP
  [obstacles::=LIST]
CONDITIONAL t.parent is None



  
  


  

  ''',
'''#SSM


[obstacleEvent:5:500] = [gainObstacleEvent] [obstacleFillerEvent:k/3][obstacleEvent:k/3][resolveObstacleEvent][resolveGoalFiller:k/3] IF t.SEEK.obstacles.num<3
[obstacleEvent:1:5] = [obstacleFillerEvent::k]
[obstacleEvent:3] = [enterLocation] [locationEvent:k-2] [exitLocation] IF t.SEEK.obstacles.num>=3
[obstacleEvent:200] = [obstacleEvent:k/2] [obstacleEvent:k/2]

[obstacleFillerEvent:100] = [obstacleFillerEvent:k//2] [obstacleFillerEvent:k//2]
[obstacleFillerEvent:3:100] = [enterLocation] [locationEvent:k-2] [exitLocation]
[obstacleFillerEvent::3] = [obstacleFillerEvent::k]

[resolveGoalFiller:100]=[resolveGoalFiller][resolveGoalFiller]
[resolveGoalFiller:3:100] = [enterLocation] [locationEvent:k-2] [exitLocation]
[resolveGoalFiller::3] = [resolveGoalFiller::k]

[continueConversationState:1:1] = [continueConversation_obstacle] IF t.SEEK.obstacles.num>0 and t._rand("obstacle").random()<1.0
[continueConversationState:1:1] = [continueConversation_obstacle2] IF t.SEEK.obstacles.num>1 and t._rand("obstacle2").random()<1.0


#location event for each of the obstacle types


[locationEvent] = [obstacleFiller_buy][locationEvent:k-1] IF t.SEEK.obstacles.num>0 and t.SEEK.obstacles.item0.obstacleType=="buy"
[locationEvent] = [obstacleFiller_learn][locationEvent:k-1] IF t.SEEK.obstacles.num>0 and t.SEEK.obstacles.item0.obstacleType=="learn"
[locationEvent] = [obstacleFiller_escape][locationEvent:k-1] IF t.SEEK.obstacles.num>0 and t.SEEK.obstacles.item0.obstacleType=="escape"
[locationEvent] = [obstacleFiller_destory][locationEvent:k-1] IF t.SEEK.obstacles.num>0 and t.SEEK.obstacles.item0.obstacleType=="destroy"

''',
'''#DESC

genere
  sci-fi
  fantasy
  western
  steampunk
  romance
  musical
  time travel
  
drama
  drama
  play
  book
  novel
  movie
  TV series


theNoun
  the [animal]
  the [insect]
  the [monster]
  the [weapon]
  the color [color]
  the [occupation]
  the [sport] player
  [boyName]
  [girlName]
  
noun
  [animal]
  [insect]
  [monster]
  [weapon]
  [color]
  [occupation]
  [sport] player

wwo
  with
  without
  
perks
  perks
  price
  cost
  benefits
  
zen
  zen
  art
  history
  science
  
title
  What [theNoun.CC] [actionVerb.ED.CC]
  What [actionVerb.ED.CC] [theNoun.CC]?
  [theNoun.CC.ic] and [theNoun2.CC:theNoun]
  The [color.CC] [noun.CC]
  Why [theNoun.CC] [actionVerb.ED.CC] [theNoun2.CC]
  Why [noun.aAn.CC]'s Favorite Color is [color.CC]
  How I [actionVerb.ED.CC] [theNoun.CC]
  [theNoun.CC.ic] [wwo] [noun.aAn.CC]
  [theNoun.CC.ic] [wwo] [noun.plural.CC]
  How [theNoun.CC] got [actionVerb.ED.CC]
  The [perks.CC] of Being [noun.aAn.CC]
  When I [actionVerb.ED.CC] [theNoun.CC]
  Who [actionVerb.ED.CC] [theNoun.CC]?
  [actionVerb.ING.CC] [theNoun.CC]
  The [zen.CC] of [theNoun.CC]
  
  
  
  ''',
'''#DESC
#Types I'm considering are "find","earn","befriend"
#currently have "learn" "buy" "destory" "escape"

obstacleFiller_buy
  [SEEK.person] looked around, trying to pick out the best [SEEK.obstacles.item0.target] to buy.
PROP
  [is_world::=TRUE]

obstacleFiller_destroy
  [SEEK.person] attacked the [SEEK.obstacles.item0.target] with [SEEK.person.hisHer] [SEEK.person.weapon].
PROP
  [is_world::=TRUE]

  
obstacleFiller_learn
  [SEEK.person] examined the [SEEK.obstacles.item0.target] carefully, trying to learn as much about it as possible.
PROP
  [is_world::=TRUE]
  
obstacleFiller_escape
  [SEEK.person] ran as fast as possible, trying to escape from the [SEEK.obstacles.item0.target].
PROP
  [is_world::=TRUE]

world
PROP  
  [obstacleFiller_buy]
  [obstacleFiller_learn]
  [obstacleFiller_destroy]
  [obstacleFiller_escape]
  
''']
