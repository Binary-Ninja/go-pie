#!/usr/bin/env python3

import random

TOP = 'top'
BOTTOM = 'bottom'

#go fish actions
DNH='dnh', #does not have
RCV='rcv', #received cards
TAT='tat', #takes a trick
GOF='gof', #went fishing
GFC='gfc', #go fish card, continue turn
RDH='rdh', #ran out of cards, redealt

FRENCH_SUITS = list('cdhs')
STAR_SUITS = list('cdhst')
WHITE_SYMBOL_SUITS = list('♧♢♡♤☆')
BLACK_SYMBOL_SUITS = list('♣♦♥♠★')

FRENCH_RANKS = list('A23456789TJQK')
KNIGHT_RANKS = list('A23456789TJNQK')

LETTER_2_BLACK_SYMBOL = {
'c':'♣',
'd':'♦',
'h':'♥',
's':'♠',
't':'★',
'':'',
}

LETTER_2_WHITE_SYMBOL = {
'c':'♧',
'd':'♢',
'h':'♡',
's':'♤',
't':'☆',
'':'',
}

DEFAULT_SORT_DICT = {
    'ranks':{
        'j':0,
        'A':1,
        '2':2,
        '3':3,
        '4':4,
        '5':5,
        '6':6,
        '7':7,
        '8':8,
        '9':9,
        'T':10,
        'J':11,
        'N':12,
        'Q':13,
        'K':14,
    },
    'suits':{
        '':0,
        'c':1,
        'd':2,
        'h':3,
        's':4,
        't':5,
    },
}

BIGA_SORT_DICT = {
    'ranks':{
        'j':0,
        '2':2,
        '3':3,
        '4':4,
        '5':5,
        '6':6,
        '7':7,
        '8':8,
        '9':9,
        'T':10,
        'J':11,
        'N':12,
        'Q':13,
        'K':14,
        'A':15,
    },
    'suits':{
        '':0,
        'c':1,
        'd':2,
        'h':3,
        's':4,
        't':5,
    },
}

POKER_SORT_DICT = {
    'ranks':{
        'j':0,
        '2':2,
        '3':3,
        '4':4,
        '5':5,
        '6':6,
        '7':7,
        '8':8,
        '9':9,
        'T':10,
        'J':11,
        'N':12,
        'Q':13,
        'K':14,
        'A':15,
    },
}

SUIT_SORT_DICT = {
    'suits':{
        '':0,
        'c':1,
        'd':2,
        'h':3,
        's':4,
        't':5,
    },
}


def new_deck(**kwargs):
    shuffle = kwargs.get('shuffle', False)
    jokers = kwargs.get('jokers', 0)
    ranks = kwargs.get('ranks', FRENCH_RANKS)
    suits = kwargs.get('suits', FRENCH_SUITS)
    deck = Stack()
    for _ in range(jokers):
        deck.add(Card('j', ''), BOTTOM)
    for rank in ranks:
        for suit in suits:
            deck.add(Card(rank,suit), BOTTOM)
    if shuffle:
        deck.shuffle()
    return deck


def check_term(term, ranks=KNIGHT_RANKS, suits=STAR_SUITS):
    return isinstance(term, str) and len(term) == 2 and \
           term[0] in ranks and term[1] in suits


class Card:
    def __init__(self, rank_or_value, suit=None):
        if suit is None:
            assert len(rank_or_value) == 2, "object provided must be length 2"
            self.rank = rank_or_value[0]
            self.suit = rank_or_value[1]
        else:
            self.rank = rank_or_value
            self.suit = suit

    def __iter__(self):
        return iter(str(self))

    def __len__(self):
        return 2

    def __getitem__(self, item):
        if item in [0, 'rank']:
            return self.rank
        elif item in [1, 'suit']:
            return self.suit
        else:
            raise KeyError("valid keys for Card: 0, 1, 'ranks', 'suits'")

    def __eq__(self, other, sort_dict=DEFAULT_SORT_DICT):
        return sort_dict['ranks'][self.rank] == sort_dict['ranks'][other[0]] and \
               sort_dict['suits'][self.suit] == sort_dict['suits'][other[1]]
    eq = __eq__

    def __ne__(self, other, sort_dict=DEFAULT_SORT_DICT):
        return not self.eq(other, sort_dict)
    ne = __ne__

    def __gt__(self, other, sort_dict=DEFAULT_SORT_DICT, ranks_first=True):
        if ranks_first:
            if sort_dict['ranks'][self.rank] > sort_dict['ranks'][other[0]]:
                return True
            elif sort_dict['ranks'][self.rank] == sort_dict['ranks'][other[0]]:
                if sort_dict['suits'][self.suit] > sort_dict['suits'][other[1]]:
                    return True
                else:
                    return False
            else:
                return False
        else:
            if sort_dict['suits'][self.suit] > sort_dict['suits'][other[1]]:
                return True
            elif sort_dict['suits'][self.suit] == sort_dict['suits'][other[1]]:
                if sort_dict['ranks'][self.rank] > sort_dict['ranks'][other[0]]:
                    return True
                else:
                    return False
            else:
                return False
    gt = __gt__

    def __lt__(self, other, sort_dict=DEFAULT_SORT_DICT, ranks_first=True):
        if ranks_first:
            if sort_dict['ranks'][self.rank] < sort_dict['ranks'][other[0]]:
                return True
            elif sort_dict['ranks'][self.rank] == sort_dict['ranks'][other[0]]:
                if sort_dict['suits'][self.suit] < sort_dict['suits'][other[1]]:
                    return True
                else:
                    return False
            else:
                return False
        else:
            if sort_dict['suits'][self.suit] < sort_dict['suits'][other[1]]:
                return True
            elif sort_dict['suits'][self.suit] == sort_dict['suits'][other[1]]:
                if sort_dict['ranks'][self.rank] < sort_dict['ranks'][other[0]]:
                    return True
                else:
                    return False
            else:
                return False
    lt = __lt__

    def __ge__(self, other, sort_dict=DEFAULT_SORT_DICT):
        return self.gt(other, sort_dict) or self.eq(other, sort_dict)
    ge = __ge__

    def __le__(self, other, sort_dict=DEFAULT_SORT_DICT):
        return self.lt(other, sort_dict) or self.eq(other, sort_dict)
    le = __le__

    def __str__(self, symbols=None):
        symdict = {
        None:self.suit,
        'black':LETTER_2_BLACK_SYMBOL[self.suit],
        'white':LETTER_2_WHITE_SYMBOL[self.suit],
        }
        suit = symdict.get(symbols, self.suit)
        return self.rank + suit
    str = __str__

    def __repr__(self):
        return "Card({}, {})".format(self.rank, self.suit)


class Stack:
    def __init__(self, cards=[]):
        self.cards = [Card(thing) for thing in cards]
        self.sort_dict = None

    def __str__(self, symbols=None):
        list = [card.str(symbols) for card in self.cards]
        return "{}".format(list)
    str = __str__

    def __repr__(self):
        return "Stack({})".format(str(self))

    def list(self):
        return self.cards

    def tuple(self):
        return tuple(self.cards)

    def __set__(self):
        return set(self.cards)

    def __iter__(self):
        return iter(self.cards)

    def __getitem__(self, item):
        return self.cards[item]

    def __len__(self):
        return len(self.cards)

    def __eq__(self, other):
        return self.cards == other.cards

    def __ne__(self, other):
        return not self == other

    @property
    def size(self):
        return len(self.cards)

    def shuffle(self, times=1):
        for _ in range(times):
            random.shuffle(self.cards)

    def compare_stacks(self, other, to_sort=True):
        x = self.copy()
        y = other.copy()
        if to_sort:
            x.sort()
            y.sort()
        return x == y

    def add(self, card, end=TOP):
        card = Card(card)
        if end is TOP:
            self.cards.insert(0, card)
        elif end is BOTTOM:
            self.cards.append(card)
        else:
            raise ValueError("end is not 'TOP' or 'BOTTOM'")

    def add_list(self, cards, end=TOP):
        cards = list(cards)
        if end is TOP:
            self.cards = cards + self.cards
        elif end is BOTTOM:
            self.cards = self.cards + cards
        else:
            raise ValueError("end is not 'TOP' or 'BOTTOM'")

    def deal(self, num=1, end=TOP):
        stack = []
        if end is TOP:
            x = 0
        elif end is BOTTOM:
            x = -1
        else:
            raise ValueError("end is not 'TOP' or 'BOTTOM'")
        for i in range(num):
            try:
                stack.append(self.cards[x])
                del self.cards[x]
            except IndexError:
                return Stack(stack)
        return Stack(stack)

    def empty(self, return_cards=False):
        if return_cards:
            x = self.cards
        else:
            x = None
        self.cards = []
        return x

    def is_empty(self):
        return True if self.cards == [] else False

    def find(self, term, limit=0):
        return_list = []
        for card in self.cards:
            if term in card or str(term) == card:
                return_list.append(self.cards.index(card))
                if (not (limit <= 0)) and len(return_list) == limit:
                    return return_list
        return return_list

    def find_list(self, terms, limit=0):
        return_list =[]
        for term in terms:
            return_list.append(self.find(term, limit))
        return return_list

    def get(self, term, limit=0):
        return_list = []
        for card in self.cards:
            if term in card or str(term) == card:
                return_list.append(card)
                if (not (limit <= 0)) and len(return_list) == limit:
                    return return_list
        return return_list

    def get_list(self, terms, limit=0):
        return_list =[]
        for term in terms:
            return_list += self.get(term, limit)
        return return_list

    def insert(self, card, index=-1):
        self.cards.insert(index, card)

    def insert_list(self, cards, index=-1):
        self.cards.insert(index, cards)

    def remove(self, term):
        for card in self.cards[:]:
            if term in card or term == card:
                self.cards.remove(card)

    def remove_list(self, terms):
        card_list = self.get_list(terms)
        for card in card_list:
            self.cards.remove(card)

    def random_card(self, remove=False, num=1):
        card = random.sample(self.cards, num)[0]
        if remove:
            del self.cards[self.cards.index(card)]
        return card

    def reverse(self):
        self.cards = self.cards[::-1]

    def set_cards(self, cards):
        self.cards = list(cards)

    def split(self, index=None):
        if index is None:
            index = len(self.cards) // 2
        return Stack(self.cards[:index]), Stack(self.cards[index:])

    def copy(self):
        return Stack(self.cards)

    def max(self, num=1, sort_dict=DEFAULT_SORT_DICT, ranks_first=True):
        temp = self.copy()
        temp.sort(sort_dict, ranks_first, True)
        return_list = []
        for i in range(num):
            return_list.append(temp.cards[i])
        return return_list

    def min(self, num=1, sort_dict=DEFAULT_SORT_DICT, ranks_first=True):
        temp = self.copy()
        temp.sort(sort_dict, ranks_first, False)
        return_list = []
        for i in range(num):
            return_list.append(temp.cards[i])
        return return_list

    def sort(self, sort_dict=DEFAULT_SORT_DICT, ranks_first=True, reverse=False):
        if sort_dict != self.sort_dict:
            self.sort_dict = sort_dict
        if 'suits' in self.sort_dict and 'ranks' in self.sort_dict:
            if ranks_first:
                ranks_dict = {}
                for card in self.cards:
                    if card.rank in ranks_dict:
                        ranks_dict[card.rank].append(card)
                    else:
                        ranks_dict[card.rank] = [card]
                for rank in ranks_dict:
                    ranks_dict[rank].sort(key=self._sort_key_func_card_suit, reverse=reverse)
                ranks_list = list(ranks_dict)
                ranks_list.sort(key=self._sort_key_func_rank, reverse=reverse)
                self.cards = []
                for rank in ranks_list:
                    for card in ranks_dict[rank]:
                        self.cards.append(card)
            else:
                suits_dict = {}
                for card in self.cards:
                    if card.suit in suits_dict:
                        suits_dict[card.suit].append(card)
                    else:
                        suits_dict[card.suit] = [card]
                for suit in suits_dict:
                    suits_dict[suit].sort(key=self._sort_key_func_card_rank, reverse=reverse)
                suits_list = list(suits_dict)
                suits_list.sort(key=self._sort_key_func_suit, reverse=reverse)
                self.cards = []
                for suit in suits_list:
                    for card in suits_dict[suit]:
                        self.cards.append(card)
        elif 'ranks' in self.sort_dict:
            self.cards.sort(key=self._sort_key_func_card_rank, reverse=reverse)
        elif 'suits' in self.sort_dict:
            self.cards.sort(key=self._sort_key_func_card_suit, reverse=reverse)
        else:
            raise KeyError("'suits' or 'ranks' not found in sorting dictionary")

    def is_sorted(self, sort_dict=DEFAULT_SORT_DICT, ranks_first=True):
        other = self.copy()
        other.sort(sort_dict, ranks_first)
        return self == other

    def _sort_key_func_rank(self, rank):
        return self.sort_dict['ranks'][rank]

    def _sort_key_func_suit(self, suit):
        return self.sort_dict['suits'][suit]

    def _sort_key_func_card_rank(self, card):
        return self.sort_dict['ranks'][card.rank]

    def _sort_key_func_card_suit(self, card):
        return self.sort_dict['suits'][card.suit]


class GoFishGame:
    def __init__(self, ranks=FRENCH_RANKS, suits=FRENCH_SUITS):
        self.deck = new_deck(ranks=ranks, suits=suits, shuffle=True)
        self.ranks = ranks
        self.suits = suits
        self.players = []
        self.hand_size = 6 if len(self.players) < 5 else 5
        self.quit = False

    def prepare(self):
        assert len(self.players) in (3,4,5,6), "go fish supports 3-6 players"
        random.shuffle(self.players) #first player chosen at random
        if self.verbose:
            print('='*80)
            print("Player order:")
            for player in self.players:
                print("{}. {}".format(self.players.index(player)+1, player))
        for player in self.players:
            player.hand = self.deck.deal(self.hand_size)
        for player in self.players:
            player.prepare()
        self.continue_prompt()

    def run(self, verbose=True, symbols=None):
        self.verbose = verbose
        self.symbols = symbols
        self.prepare()
        while not self.quit:
            for player in self.players:
                if self.quit:
                    break
                if self.verbose:
                    print('='*80)
                    print("{}'s turn:".format(player.name))
                    print("Number of cards: {}".format(player.num_cards))
                    print("Tricks: {}".format(player.tricks))
                    print("Points: {}".format(player.points))
                    self.continue_prompt()
                while not self.quit:
                    if self.verbose:
                        print('='*80)
                    player.hand.sort()
                    if not player.hand.is_empty():
                        askee, rank = player.ask()
                    else:
                        if self.deck.is_empty():
                            if self.verbose:
                                print("{} has no cards and the deck is empty!".format(player))
                            break
                        else:
                            self.check_for_empty(askee)
                            askee, rank = player.ask()
                    cards = askee.hand.get(rank)
                    if self.verbose:
                        print("{} asked {} for a {}!".format(player, askee, rank))
                    if cards == []:
                        self.update_players(DNH, player, askee, rank)
                        if self.verbose:
                            print("{} said to go fish!".format(askee))
                        if self.deck.is_empty():
                            if self.verbose:
                                print("The deck is empty!")
                                self.continue_prompt()
                            break
                        else:
                            card = self.deck.deal()[0]
                            player.hand.add(card)
                            if rank == card.rank:
                                self.update_players(GFC, player, rank)
                                if self.verbose:
                                    print("{} went fishing and drew a {}!".format(player, rank))
                                self.check_for_tricks(player)
                            else:
                                self.update_players(GOF, player)
                                if self.verbose:
                                    print("{} went fishing!".format(player))
                                self.check_for_tricks(player)
                                if self.verbose:
                                    self.continue_prompt()
                                break
                    else:
                        self.update_players(RCV, player, askee, rank, len(cards))
                        askee.hand.remove_list([str(card) for card in cards])
                        player.hand.add_list(cards)
                        if self.verbose:
                            print("{} gave {} {}(s) to {}!".format(askee, len(cards), rank, player))
                        self.check_for_tricks(player)
                        self.check_for_empty(askee)
                        self.check_for_empty(player)
                    if self.verbose:
                        self.continue_prompt()
        print("Game exited.")

    def add_player(self, player, name, *args, **kwargs):
        self.players.append(player(name, self, *args, **kwargs))

    def check_for_empty(self, player):
        if player.hand.is_empty() and not self.quit:
            player.hand = self.deck.deal(self.hand_size)
            self.update_players(RDH, player)
            if self.verbose:
                print("{} ran out of cards!".format(player))
                print("{} was redealt {} cards!".format(player, len(player.hand)))
            self.check_for_tricks(player)

    def check_for_tricks(self, player):
        tricks = {}
        for card in player.hand:
            if card.rank in tricks:
                tricks[card.rank] += 1
            else:
                tricks[card.rank] = 1
        for rank in tricks:
            if tricks[rank] == len(self.suits):
                player.tricks.append(rank)
                player.hand.remove_list([rank])
                if self.verbose:
                    print("{} takes a trick of {}s!".format(player, rank))
                self.update_players(TAT, player, rank)
        self.check_for_win()

    def check_for_win(self):
        tricks_list = []
        for player in self.players:
            tricks_list += player.tricks
        if len(tricks_list) == len(self.ranks):
            self.quit = True
            if self.verbose:
                print('='*80)
                print("The game is over!")
                self.players.sort(key=self._sort_key_func_player_tricks, reverse=True)
                for player in self.players:
                    print("{}. {}, with {} point(s)".format(self.players.index(player)+1, player, player.points))
            return

    def _sort_key_func_player_tricks(self, player):
        return player.points

    def continue_prompt(self):
        r = input("Press [Enter] to continue (or type 'q' to quit): ")
        if r.lower() in ('q', 'quit'):
            r = input("Are you sure you want to quit? (y/n): ")
            if r.lower() in ('y', 'yes'):
                self.quit = True

    def update_players(self, action, *args):
        for player in self.players:
            player.update(action, *args)


class GoFishPlayer:
    def __init__(self, name, game):
        self.name = name
        self.game = game
        self.hand = Stack()
        self.tricks = []

    def __str__(self):
        return self.name

    @property
    def points(self):
        return len(self.tricks)

    @property
    def num_cards(self):
        return len(self.hand)

    def prepare(self):
        pass

    def update(self, action, *args):
        pass

    def ask(self):
        raise Exception("'ask' method should be overwritten in child class")


class GoFishHuman(GoFishPlayer):
    def ask(self):
        print("Your cards: ", self.hand.str(self.game.symbols))
        askee = self.ask_for_askee()
        rank = self.ask_for_rank()
        return askee, rank

    def ask_for_askee(self):
        player_list = self.game.players[:]
        player_list.remove(self)
        str_list = [str(player) for player in player_list]
        while True:
            askee = input("Who do you want to ask? {}: ".format(str_list))
            if askee in str_list:
                askee = player_list[str_list.index(askee)]
                return askee
            else:
                print("That is not a player in the game.")

    def ask_for_rank(self):
        ranks_list = [card.rank for card in self.hand]
        while True:
            rank = input("What rank do you want to ask for? ")
            if rank in ranks_list:
                return rank
            else:
                print("That is not a rank in your hand.")


class GoFishAIPerfectMemory(GoFishPlayer):
    def __init__(self, name, game, memory_percent=1):
        GoFishPlayer.__init__(self, name, game)
        self.memory_percent = memory_percent
        self.memory = {}
        self.update_dict = {
        DNH:self.update_DNH,
        RCV:self.update_RCV,
        TAT:self.update_TAT,
        GOF:self.update_GOF,
        GFC:self.update_GFC,
        RDH:self.update_RDH,
        }

    def prepare(self):
        for player in self.game.players:
            self.memory[player] = {
            'has':{},
            'dnh':[],
            }

    def update(self, action, *args):
        self.update_dict[action](*args)

    def update_DNH(self, player, askee, rank):
        if not rank in self.memory[player]['has']:
            self.memory[player]['has'][rank] = 1
        self.memory[askee]['dnh'].append(rank)

    def update_RCV(self, player, askee, rank, num):
        if rank in self.memory[player]['has']:
            self.memory[player]['has'][rank] += num
        else:
            self.memory[player]['has'][rank] = num + 1
        if rank in self.memory[askee]['has']:
            del self.memory[askee]['has'][rank]
        self.memory[askee]['dnh'].append(rank)

    def update_TAT(self, player, rank):
        if rank in self.memory[player]['has']:
            del self.memory[player]['has'][rank]

    def update_GOF(self, player):
        self.memory[player]['dnh'] = []

    def update_GFC(self, player, rank):
        self.memory[player]['has'][rank] += 1

    def update_RDH(self, player):
        self.memory[player]['has'] = {}
        self.memory[player]['dnh'] = []

    def ask(self):
        player_list = [player for player in self.memory]
        card_list = [card for card in self.hand]
        for player in player_list:
            if player == self:
                continue
            for card in card_list:
                if card.rank in self.memory[player]['has']:
                    return player, card.rank
        random.shuffle(player_list)
        random.shuffle(card_list)
        for player in player_list:
            if player == self:
                continue
            for card in card_list:
                if not card.rank in self.memory[player]['dnh']:
                    return player, card.rank


class GoFishAIRandom(GoFishPlayer):
    def ask(self):
        player_list = self.game.players[:]
        player_list.remove(self)
        askee = random.choice(player_list)
        ranks_list = [card.rank for card in self.hand]
        rank = random.choice(ranks_list)
        return askee, rank


def main():
    g = GoFishGame(ranks=FRENCH_RANKS, suits=FRENCH_SUITS)
    g.add_player(GoFishAIRandom, input("Name AI 1: "))
    g.add_player(GoFishAIPerfectMemory, input("Name AI 2: "))
    g.add_player(GoFishHuman, input("Name player 1: "))
    g.add_player(GoFishHuman, input("Name player 2: "))
    g.run(symbols='black')


if __name__ == '__main__':
    main()
