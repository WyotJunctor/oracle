from collections import defaultdict
import random
from pprint import pprint

ENTITY_TEMPLATE_STORE = dict()
TAG_STORE = dict()
ACTION_STORE = dict()


def ExStink():
    raise Exception("HOO HOO")


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
        generated_tags = {t for tag in self.essential for t in TAG_STORE[tag].generate(set())}

        for tag in generated_tags:
            if not tag.validate(generated_tags):
                print(f'Also sprach Zarathustra, "{tag}, {generated_tags}"')
                raise Exception("Gott ist tot.")


        optional_sets = [TAG_STORE[opt].generate(generated_tags) for opt in random.sample(
            list(self.optional), random.randint(0, len(self.optional))
        )]
        for tag_set in optional_sets:
            if not all([tag.validate(generated_tags) for tag in tag_set]):
                continue
            else:
                generated_tags.update(tag_set)
        
        entity.tags = generated_tags
        return entity

    ...


...


class Entity:
    def __init__(self):
        self.tags = set()
        self.banned_tags = set()


class Tag:
    NEXT_TAG_ID = 0

    def __init__(self, name=None, traits=None):
        self.id = self.NEXT_TAG_ID
        self.NEXT_TAG_ID += 1
        self.name = name if name is not None else f"Tag{self.id}"
        self.traits = traits if traits is not None else set()
        TAG_STORE[self.name] = self
    
    def generate(self, other_tags):
        if self in other_tags:
            return set()
        return {t for trait in self.traits for t in trait.generate(other_tags)}.union({self})

    def validate(self, other_tags, recip=True):
        if recip is True:
            return all([trait.validate(other_tags) for trait in self.traits]) and all([tag.validate({self}, recip=False) for tag in other_tags])
        else:
            return all([trait.validate(other_tags) for trait in self.traits])

    def __repr__(self):
        return self.name


class TagTrait:
    def __init__(self):
        pass
    
    def generate(self, other_tags):
        return set()

    def validate(self, other_tags):
        return True


class Implies(TagTrait):
    def __init__(self, *target_tags):
        self.target_tags = target_tags

    def generate(self, other_tags):
        return {t for tag in self.target_tags for t in TAG_STORE[tag].generate(other_tags)}


class ImpliesNot(TagTrait):
    def __init__(self, *target_tags):
        self.target_tags = target_tags
    
    def validate(self, other_tags):
        for tag in self.target_tags:
            if TAG_STORE[tag] in other_tags:
                return False
        return True


class IsFrom(TagTrait):
    def __init__(self, target_tag):
        self.target_tag = target_tag

    def generate(self, other_tags):
        if TAG_STORE[self.target_tag] in other_tags:
            return set()
        return {TAG_STORE[self.target_tag]}


class OneOf(TagTrait):
    def __init__(self, *target_tags):
        self.target_tags = target_tags

    def generate(self, other_tags):
        generated_tag = TAG_STORE[random.choice(self.target_tags)]
        if generated_tag in other_tags:
            return set()
        return {generated_tag}


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

# TAGS

alive = Tag(name="Alive", traits=[ImpliesNot("Object")])

object = Tag(name="Object", traits=[ImpliesNot("Alive")])

fast = Tag(name="Fast", traits=[Implies("Alive")])

intelligibility = Tag(
    name="Intelligibility",
    traits=[Implies("Alive"), OneOf("Intelligible", "Unintelligible")],
)

intelligible = Tag(name="Intelligible", traits=[IsFrom("Intelligibility")])

unintelligible = Tag(name="Unintelligible", traits=[IsFrom("Intelligibility")])

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

wise = Tag(name="Wise", traits=[Implies("Intelligibility")])

pprint(TAG_STORE)

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

blind_man = EntityTemplate(
    name="Blind Man",
    essential={"Intelligibility"},
    optional={
        "Sacred",
        "Insidious",
        "Helpless",
        "Wise",
    }
)

#feral_child_instance = feral_child.create()
blind_man_instance = blind_man.create()

pprint(blind_man_instance.tags)
#pprint(feral_child_instance.tags)

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
