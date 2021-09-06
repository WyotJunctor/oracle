from collections import defaultdict
import random

ENTITY_TEMPLATE_STORE = dict()
TAG_STORE = dict()
ACTION_STORE = dict()


class EntityTemplate:

    NEXT_ENTITY_ID = 0


    def __init__(self, name=None, essential=None, optional=None):
        self.id = self.NEXT_ENTITY_ID
        self.NEXT_ENTITY_ID += 1
        self.name = name if name is not None else f"Entity{self.id}"
        self.essential = essential if essential is not None else set()
        self.optional = optional if optional is not None else set()
        ENTITY_TEMPLATE_STORE[self.name] = self

    ...

    def create(self):
        entity = Entity()
        entity_tags = self.essential.union(
            set([e for e in self.optional if random.choice((True, False))])
        )
        for tag in entity_tags:
            if entity.add_tag(tag) == False:
                return None
        return entity

    ...


...


class Entity:
    def __init__(self):
        self.tags = set()

    def add_tag(self, tag_name, exclude_traits=set()):
        tag = TAG_STORE.get(tag_name)
        if tag is None:
            print("UH OH STINKy:", tag_name)
            raise Exception("ＦＵＵＣＫ")
        for trait in tag.traits:
            if type(trait) in exclude_traits:
                continue
            if trait.init(self) == False:
                return False
        self.tags.add(tag_name)
        return True


class Tag:
    NEXT_TAG_ID = 0

    ...

    def __init__(self, name=None, traits=None):
        self.id = self.NEXT_TAG_ID
        self.NEXT_TAG_ID += 1
        self.name = name if name is not None else f"Tag{self.id}"
        self.traits = traits if traits is not None else set()
        TAG_STORE[self.name] = self

    ...


...


class TagTrait:
    pass


...


class Implies(TagTrait):
    def __init__(self, *args):
        self.implies = args

    ...

    def init(self, entity):
        for tag in self.implies:
            entity.add_tag(tag)

    ...


...


class ImpliesNot(TagTrait):
    def __init__(self, *args):
        self.implies_not = args

    ...

    def init(self, entity):
        for tag in self.implies_not:
            if tag in entity.tags:
                raise Exception("ＦＵＣＫ")

    ...


...


class OneOf(TagTrait):
    def __init__(self, *one_of):
        self.one_of = one_of

    ...

    def init(self, entity):
        entity.add_tag(random.choice(self.one_of), exclude_traits={IsFrom})

    ...


...


class IsFrom(TagTrait):
    def __init__(self, is_from):
        self.is_from = is_from

    ...

    def init(self, entity):
        entity.add_tag(self.is_from, exclude_traits={OneOf})

    ...


...


class Action:
    NEXT_ACTION_ID = 0

    ...

    def __init__(self, name=None):
        self.id = self.NEXT_ACTION_ID
        self.NEXT_ACTION_ID += 1
        self.name = name if name is not None else f"Action{self.id}"
        pass
        ...


...

# ENTITIES

feral_child = EntityTemplate(
    name="Feral Child",
    essential={"Intelligibility"},
    optional={
        "Ferocious",
        "Sacred",
        "Fast",
    },
)

# TAGS

alive = Tag(name="Alive", traits=[ImpliesNot("Object")])

fast = Tag(name="Fast", traits=[Implies("Alive")])

intelligibility = Tag(
    name="Intelligibility",
    traits=[Implies("Alive"), OneOf("Intelligible", "Unintelligible")],
)

intelligible = Tag(name="Intelligible", traits=[IsFrom("Intelligible")])

unintelligible = Tag(name="Unintelligible", traits=[IsFrom("Intelligible")])

dangerous = Tag(
    name="Dangerous",
    traits=[Implies("Alive"), ImpliesNot("Helpless"), OneOf("Ferocious", "Insidious")],
)

ferocious = Tag(name="Ferocious", traits=[Implies("Beseechable"), IsFrom("Dangerous")])
insidious = Tag(name="Insidious", traits=[IsFrom("Dangerous")])
helpless = Tag(name="Helpless", traits=[Implies("Alive")])

sacred = Tag(name="Sacred", traits=[OneOf("Generally", "Apollo")])
generally = Tag(name="Generally", traits=[IsFrom("Sacred")])
apollo = Tag(name="Apollo", traits=[IsFrom("Sacred")])

beseechable = Tag(name="Beseechable", traits=[Implies("Alive")])

feral_child_instance = feral_child.create()

from pprint import pprint

pprint(feral_child_instance.tags)

# construct actions


# initialize entities

# initialize tags

# initialize actions


"""

Actions expect tags or tag patterns

need to be able to find entity templates by their attributes
need to be able to enforce constraints in the create method

action -> compatible(Unintelligible, ^Intelligible) entity.create(constraints)
            feral child (Intelligibility)


action -> entity
action -> entity -> complication -> solution(action -> entity)


Kill -> Go To
    (Big, Dangerous, Creature) -> generates a big dangerous creature entity
    ()

Kill -> Gryphon -> 

complications consider the tags of the involved entity and the action (and the action's implied hierarchy)

Go To
Creature
Hidden
    -> go ask a (wise) entity
    -> search a (dark) location
    -> find some (magical, object) entity

does solution just consider the complication
does each complication know which solutions it can generate
does the validation of the solution involve just the complication, or does it also consider the entity/action



Complications-
(Need to reach but) Lost -> Alive|Object
    Gather Information, Explore
(Need to reach but) Hidden -> Object|Location
    Gather Information, Explore
(Need to reach but) Guarded -> *
    Circumvent, Defeat
(Need to reach but) Imprisoned -> Alive, ^Location
    Rescue, Visit
(Need to deal but) Obstinate* -> Intelligibility
    Overcome, Trick, Exchange 
(Need to reach but) Trapped -> Location
(Need to reach but) Stuck -> Alive, ^Location
(Need to deal but) Hostile -> Alive
(Need to harm but) Invincible -> Alive
    Vincibilify, 
(Need to deal but) Mute -> Intelligible
(Need to deal but) Transfigured -> Alive|Object, ^Location
(Need to harm but) Mighty -> Alive
(Need to deal/harm but) Wily -> Alive, Intelligibility
(Need to use but) Destroyed -> Object
(Need to deal/reach/harm but) Dead -> Alive, ^Location
(Need to \do\ but) Impossible* -> Impossible
(Need to deal but) Grudge -> Alive, Intelligibility
(Need to harm but) Friend -> Alive, Intelligibility
(Need to deal/harm but) Man-Eating -> Alive, Dangerous
(Need to reach but) Obstructed -> Location
(Need to harm but) Sacred -> *



End Goals-
Tame
Catch
Kill
Sacrifice
Marry
Acquire
Destroy
Expel
Drink
Find
Eat
Raze
Persuade
Desecrate
Dedicate

Mid Goal-
Rescue
Evade
Explore
Circumvent
Consult

Actions-
Challenge
Fight
Drink
Eat

Goal: Sacrifice at Altar
Complication: No one can find it
Solutions: Gather Information, Explore
    Gather Information: Consult Wise, Consult Intelligible
    Complication (Consult Wise): Hostile, Lost, Wants Something, Cursed
    Solutions (Hostile): Defeat, Persuade, Threaten, Beseech
    Complication (Defeat): Strong, Invincible, Wily, Magical, Divine
    Solutions (Invincible): Magic, Gather Information

    Complication (Consult Intelligible): Hostile, Lost, Wants Something, Cursed
    Explore: 


Alive -> ^Object
Destructibility {
    Destructible
    Indestructible
}
Object -> ^Alive, Destructibility
Container -> Object
Location
Intelligibility -> Alive {
    Intelligible
    Unintelligible
}
Wise -> Intelligibility
Weapon -> Object
Armor -> Object
Valuable
Dangerous -> Alive, ^Helpless {
    Ferocious -> Beseechable
    Insidious
}
Helpless -> Alive
Fast -> Alive
Sacred {
    Generally
    Apollo
}
Magical
Disguise For {
    Divine
    Regal
    Magical
}
Hiding Place -> Location
Dark -> Location
Approachability  {
    Spooky
    Imposing
    Pleasant
    Pathetic 
}
Beseechable -> Alive


Feral Child
    {
        Essential: Intelligibility
        Optional:
            Ferocious
            Sacred
            Fast
    } 

Abandoned Babe
    {
        Essential: Alive
        Optional:
            Sacred
            Helpless
    } 

Altar
    {
        Essential: Object, Sacred
        Optional:
    }

Amphora
    {
        Essential: Container
        Optional:
            Valuable
    } 

Basilisk
    {
        Essential: Creature, Ferocious
        Optional:
            Fast
    } 

Bear
    {
        Essential: Creature
        Optional:
            Disguise For
            Ferocious
            Fast
            Sacred
    } 

Blind Man
    {
        Essential: Intelligibility
        Optional:
            Sacred
            Insidious
            Helpless
            Wise
    } 

Boar
    {
        Essential: Creature, Ferocious, Fast
        Optional:
            Disguise For
            Sacred
    } 

Bow
    {
        Essential: Weapon
        Optional:
            Magical, Indestructible
            Sacred, Valuable
            Valuable
    } 

Breastplate
    {
        Essential: Armor
        Optional:
            Sacred, Valuable
            Valuable
            Magical, Indestructible
    } 

Bull
    {
        Essential: Creature, Ferocious, Fast, Valuable
        Optional:
            Disguise For
            Sacred
    } 

Cauldron
    {
        Essential: Container
        Optional:
            Valuable
    } 

Cave
    {
        Essential: Location
        Optional:
            Dark
            Spooky
            Hiding Place
            Sacred

    } 

Chasm
    {
        Essential: Location
        Optional:
            Dark
            Spooky
            Hiding Place
    }

Field of Flowers
    {
        Essential: Location
        Optional:
            Hiding Place
            Sacred

    } 

Gorge
    {
        Essential: Location
        Optional:
            Dark
            Hiding Place
            Spooky
    } 

Mountain
    {
        Essential: Location
        Optional:
            Sacred
    } 

Palace
    {
        Essential: Location
        Optional:
            Sacred
    } 

River
    {
        Essential: Location
        Optional:
            Sacred
            Alive
            Dangerous
            Beseechable
            Wise
    } 

Ruins
    {
        Essential: Location
        Optional:
            Sacred
            Hiding Place
    } 

Town
    {
        Essential: Location
        Optional:
            Sacred
            Hiding Place
    } 

Temple
    {
        Essential: Location, Sacred
        Optional:
            Hiding Place
    } 

Hole
    {
        Essential: Hiding Place, Dark
        Optional:
            Spooky
    }
"""
