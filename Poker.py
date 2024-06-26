import random
import itertools

# Define card values and suits using symbols
values = "23456789TJQKA"
suits = ["\u2663", "\u2666", "\u2665", "\u2660"]  # Clubs, Diamonds, Hearts, Spades

# Create a deck of cards
deck = [v + s for v in values for s in suits]

def deal_hand(deck, num_players):
    return [random.sample(deck, 2) for _ in range(num_players)]

def deal_community_cards(deck, num):
    return random.sample(deck, num)

def hand_rank(hand):
    "Return a value indicating the ranking of a hand."
    ranks = "23456789TJQKA"
    if len(hand) != 5:
        return None
    values = sorted([ranks.index(card[0]) for card in hand], reverse=True)
    suits = [card[1] for card in hand]
    
    # Check for straight and flush
    is_flush = len(set(suits)) == 1
    is_straight = values == list(range(values[0], values[0] - 5, -1))
    
    if is_straight and is_flush:
        return (8, values[0])  # Straight flush
    if len(set(values)) == 2:
        return (7, values[1])  # Four of a kind
    if len(set(values)) == 3:
        if values.count(values[0]) == 3 or values.count(values[2]) == 3:
            return (6, values[2])  # Full house
        else:
            return (3, values[1], values)  # Two pair
    if is_flush:
        return (5, values)  # Flush
    if is_straight:
        return (4, values[0])  # Straight
    if len(set(values)) == 4:
        return (2, values[1])  # Three of a kind
    if len(set(values)) == 5:
        if values.count(values[1]) == 2:
            return (1, values[1], values)  # One pair
        else:
            return (0, values)  # High card

def best_hand(hand, community_cards):
    "From the player's hand and the community cards, return the best hand."
    all_cards = hand + community_cards
    all_combinations = itertools.combinations(all_cards, 5)
    return max(all_combinations, key=hand_rank)

class PokerGame:
    def __init__(self, num_players):
        self.num_players = num_players
        self.deck = deck.copy()
        random.shuffle(self.deck)
        self.player_hands = deal_hand(self.deck, self.num_players)
        self.community_cards = []

    def reset(self):
        self.deck = deck.copy()
        random.shuffle(self.deck)
        self.player_hands = deal_hand(self.deck, self.num_players)
        self.community_cards = []
        return self.player_hands

    def deal_flop(self):
        self.community_cards = deal_community_cards(self.deck, 3)
        return self.community_cards

    def deal_turn(self):
        self.community_cards += deal_community_cards(self.deck, 1)
        return self.community_cards

    def deal_river(self):
        self.community_cards += deal_community_cards(self.deck, 1)
        return self.community_cards

    def determine_winner(self):
        best_hands = [best_hand(hand, self.community_cards) for hand in self.player_hands]
        best_ranks = [hand_rank(hand) for hand in best_hands]
        winning_rank = max(best_ranks)
        winners = [i for i, rank in enumerate(best_ranks) if rank == winning_rank]
        return winners, best_hands

# Example usage
num_players = int(input("Enter the number of players: "))
game = PokerGame(num_players)
print("Player Hands:")
for i, hand in enumerate(game.player_hands, 1):
    print(f"Player {i} Hand:", hand)
print("Flop:", game.deal_flop())
print("Turn:", game.deal_turn())
print("River:", game.deal_river())

winners, best_hands = game.determine_winner()
print("Best Hands:")
for i, hand in enumerate(best_hands):
    print(f"Player {i + 1}: {hand}")

print("Winner(s):", ", ".join(f"Player {winner + 1}" for winner in winners))
