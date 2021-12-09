from random import shuffle

# List of symbols used in the game Dobble (Spot It! in the US)
symbols = ["Anchor", "Apple", "Bomb", "Cactus", "Candle", "Carrot",
           "Cheese", "Chess knight", "Clock", "Clown", "Diasy flower", "Dinosaur",
           "Dolphin", "Dragon", "Exclamation mark", "Eye", "Fire", "Four leaf clover",
           "Ghost", "Green splats", "Hammer", "Heart", "Ice cube", "Igloo", "Key",
           "Ladybird", "Light bulb", "Lightning bolt", "Lock", "Maple leaf", "Milk bottle",
           "Moon", "No Entry sign", "Orange scarecrow man", "Pencil", "Purple bird",
           "Purple cat", "Purple dobble sign", "Question Mark", "Red lips", "Scissors",
           "Skull and crossbones", "Snowflake", "Snowman", "Spider", "Spider’s web",
           "Sun", "Sunglasses", "Target", "Taxi", "Tortoise", "Treble clef", "Tree",
           "Water drop", "Dog", "Yin and Yang", "Zebra"]

# The number of symbols on a card has to be a prime number + 1
numberOfSymbolsOnCard = 8  # (7 + 1)
shuffleSymbolsOnCard = False

cards = []

# Work out the prime number
n = numberOfSymbolsOnCard - 1

# Total number of cards that can be generated following the Dobble rules
numberOfCards = n ** 2 + n + 1  # e.g. 7^2 + 7 + 1 = 57


def create_cards(shuffle_cards=True):
    # Add first set of n+1 cards (e.g. 8 cards)
    for i in range(n + 1):
        # Add new card with first symbol
        cards.append([1])
        # Add n+1 symbols on the card (e.g. 8 symbols)
        for j in range(n):
            cards[i].append((j + 1) + (i * n) + 1)

    # Add n sets of n cards
    for i in range(n):
        for j in range(n):
            # Append a new card with 1 symbol
            cards.append([i + 2])
            # Add n symbols on the card (e.g. 7 symbols)
            for k in range(0, n):
                val = (n + 1 + n * k + (i * k + j) % n) + 1
                cards[len(cards) - 1].append(val)

    # Shuffle symbols on each card
    if shuffle_cards:
        for card in cards:
            shuffle(card)
        shuffle(cards)
    return cards


# Output all cards
def print_cards(cards):
    i = 0
    for card in cards:
        i += 1
        line = str(i) + " - ["
        for number in card:
            line = line + symbols[number - 1] + ", "
        line = line[:-2] + "]"
        print(line)


def image_lookup():
    return {
             0: 'resized/white.png',
             1: 'resized/ap.png',#'resized/anchor.png',
             2: 'resized/apple.png',
             3: 'resized/birdie.png',
             4: 'resized/bolt.png',
             5: 'resized/bomb.png',
             6: 'resized/bottle.png',
             7: 'resized/cactus.png',
             8: 'resized/candle.png',
             9: 'resized/car.png',
             10: 'resized/carrot.png',
             11: 'resized/cheese.png',
             12: 'resized/chess_knight.png',
             13: 'resized/clock.png',
             14: 'resized/clover.png',
             15: 'resized/clown.png',
             16: 'resized/daisy.png',
             17: 'resized/dinosaur.png',
             18: 'resized/dobble.png',
             19: 'resized/dog.png',
             20: 'resized/dolphin.png',
             21: 'resized/dragon.png',
             22: 'resized/exclamation_mark.png',
             23: 'resized/eye.png',
             24: 'resized/fire.png',
             25: 'resized/ghost.png',
             26: 'resized/glasses.png',
             27: 'resized/hammer.png',
             28: 'resized/heart.png',
             29: 'resized/icecube.png',
             30: 'resized/igloo.png',
             31: 'resized/key.png',
             32: 'resized/kitty.png',
             33: 'resized/ladybug.png',
             34: 'resized/lightbulb.png',
             35: 'resized/lips.png',
             36: 'resized/man.png',
             37: 'resized/maple_leaf.png',
             38: 'resized/moon.png',
             39: 'resized/net.png',
             40: 'resized/no_entry.png',
             41: 'resized/padlock.png',
             42: 'resized/pencil.png',
             43: 'resized/question_mark.png',
             44: 'resized/scissors.png',
             45: 'resized/skull.png',
             46: 'resized/snowflake.png',
             47: 'resized/snowman.png',
             48: 'resized/spider.png',
             49: 'resized/spots.png',
             50: 'resized/sun.png',
             51: 'resized/target.png',
             52: 'resized/treble_clef.png',
             53: 'resized/tree.png',
             54: 'resized/turtle.png',
             55: 'resized/waterdrop.png',
             56: 'resized/yin_yang.png',
             57: 'resized/zebra.png'
        }