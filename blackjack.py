import random

class Dealer:
  def __init__(self):
    self.deck = [
      '♥A', '♥2', '♥3', '♥4', '♥5', '♥6', '♥7', '♥8', '♥9', '♥10', '♥J', '♥Q', '♥K',
      '♦A', '♦2', '♦3', '♦4', '♦5', '♦6', '♦7', '♦8', '♦9', '♦10', '♦J', '♦Q', '♦K',
      '♣A', '♣2', '♣3', '♣4', '♣5', '♣6', '♣7', '♣8', '♣9', '♣10', '♣J', '♣Q', '♣K',
      '♠A', '♠2', '♠3', '♠4', '♠5', '♠6', '♠7', '♠8', '♠9', '♠10', '♠J', '♠Q', '♠K'
    ]
    self.players = []
    self.shuffle_deck = []

  def shuffle(self):
    self.novy_deck()
    while len(self.shuffle_deck)!= 52:
        delka = len(self.deck)
        x = random.randint(0,delka-1)
        self.shuffle_deck.append(self.deck.pop(x))
    self.deck = self.shuffle_deck
    self.shuffle_deck=[]
    return self.deck

  def novy_deck(self):
    self.deck = [
      '♥A', '♥2', '♥3', '♥4', '♥5', '♥6', '♥7', '♥8', '♥9', '♥10', '♥J', '♥Q', '♥K',
      '♦A', '♦2', '♦3', '♦4', '♦5', '♦6', '♦7', '♦8', '♦9', '♦10', '♦J', '♦Q', '♦K',
      '♣A', '♣2', '♣3', '♣4', '♣5', '♣6', '♣7', '♣8', '♣9', '♣10', '♣J', '♣Q', '♣K',
      '♠A', '♠2', '♠3', '♠4', '♠5', '♠6', '♠7', '♠8', '♠9', '♠10', '♠J', '♠Q', '♠K'
    ]


  def deal(self, n):
    ruka = []
    x = 0
    for i in range(n):
        if len(self.deck)==0:
            self.shuffle()
        if len(self.deck)!=0:
            ruka.append(self.deck.pop(0))
            x+=1
            if x == n:
                break
    return ruka

  def addPlayer(self, player):
    self.players.append(player)

  def startRound(self):
    self.shuffle()
    for player in self.players:
        player.hand=[]
        player.human = True
    offermore = True
    print()
    print('-------Rozdávám-------')
    for player in self.players:
        player.acceptCard(self.deal(2))

    while offermore == True:
        offermore = False
        for player in self.players:
          player.temporaryCards()    
          if player.strategy != "Dealer":
            if player.getHandValue() < 21:
              if player.needsCard():
                player.acceptCard(self.deal(1))
                offermore = True
        print('-------Rozdávám-------')     

    print("---Konec kola---Dealer hraje---")    
    offermore = True                
    while offermore == True:
        offermore = False
        for player in self.players:
          if player.strategy == "Dealer":
            player.finalDealer()   
            if player.getHandValue() < 21:
              if player.needsCard():
                player.acceptCard(self.deal(1))
                offermore = True
    print('--- Kolo skončilo ---')
    self.announceWinner()

  def announceWinner(self):
    results = []
    for player in self.players:
      points = player.getHandValue()
      if points > 21:
        points = 0
      results.append({'name':player.strategy, 'points': points, 'jmeno':player.name})
    self.bubbleSort(results)
    veta = 'vyhrál'
    for i in range(0, len(results)):

        if results[i]['name'] != 'Dealer' and results[i]['points'] != 0:
            print(results[i]['jmeno'], veta , 'se ziskem', results[i]['points'], 'bodů')
            if veta == 'vyhrál':
                self.vitezstvi(results[i]['name'], i)

        elif results[i]['name'] != 'Dealer' and results[i]['points'] == 0:
            print(results[i]['jmeno'], 'prohrává se ziskem', results[i]['points'], 'bodů')

        elif results[i]['name'] == 'Dealer' and results[i]['points'] != 0:
            print('Dealer získal' ,results[i]['points'], 'bodů')
            if veta == 'vyhrál' and i < 2:
                self.vitezstvi(results[i]['name'], i)
            veta = 'prohrává'

        elif results[i]['name'] == 'Dealer' and results[i]['points'] == 0:
            print('Dealer získal' ,results[i]['points'], 'bodů')
            veta = 'prohrává'

    print('-----------------')
    self.vyhlasitviteze()


# dealer vyhrává pouze pokud víc hráčů prohrálo než vyhrálo

  def vitezstvi(self, name, i):
    for player in self.players:
        if name == player.strategy:
            player.points += 1

  def vyhlasitviteze(self):
    for player in self.players:
        print(player.name , "vyhrál" , player.points ,"krát.")
    print ('------GRATULUJEME------')
    print()


  def bubbleSort(self, res):
    count = len(res)
    for j in range(count - 1, 0, -1):
        swaps = False
        for i in range(j):
            if res[i]['points'] < res[i + 1]['points']:
                res[i], res[i + 1] = res[i + 1], res[i]
                swaps = True
        if not swaps:
            break

class Player:
  def __init__(self, name, strategy, points):
    self.name = name
    self.strategy = strategy
    self.points = points
    self.hand = []
    self.human = True

  def getHandValue(self):
    suma = 0
    for karta in self.hand:
        if karta[1] in ['K','Q','J']:
            suma+=10
        elif karta[1] in ['A']:
          pass   
        else:
            suma+=int(karta[1:])
    for karta in self.hand:
      if karta[1] in ['A']:
            if (suma + 11) < 22:
                suma+=11
            else:
                suma+=1        
    return suma

  def getDealerValue(self):
      suma = 0
      for karta in self.hand:
          if karta[1] in ['A']:
              if (suma + 11) < 22:
                  suma+=11
              else:
                  suma+=1
          elif karta[1] in ['K','Q','J']:
              suma+=10
          else:
              suma+=int(karta[1:])
          break    
      return suma

  def acceptCard(self, cards):
    self.hand.extend(cards)
#    if self.strategy == "Dealer":
#       print (self.dealerCards() + 'v hodnotě ' + str(self.getDealerValue()))
#    else:    
#        print(self.listCards() + 'v hodnotě ' + str(self.getHandValue()))


  def needsCard(self):
        stav = True

        if self.strategy == 'Simon':
            if self.getHandValue() <= 0:
                stav = True
            else:
                stav = False
        elif self.strategy == 'Cautious':
            if self.getHandValue() <= 15:
                stav = True
            else:
                stav = False

        elif self.strategy == 'Bold':
            if self.getHandValue() <= 19:
                stav = True
            else:
                stav = False


        elif self.strategy == 'Dealer':
            if self.getHandValue() < 17:
                stav = True
            else:
                stav = False

        elif self.strategy == 'Human':
            if self.human == True:
                more = input(self.listCards() + 'v hodnotě ' + str(self.getHandValue())  + ', chce další(A/N)?:')
                if more == 'A' or more == 'a':
                    stav = True
                else:
                    stav = False
                    self.human = False
            else:
                stav = False
                self.human = False

        return stav

  def temporaryCards(self):
      if self.strategy == "Dealer":
        print (self.dealerCards() + 'v hodnotě ' + str(self.getDealerValue()))
      else:    
        print(self.listCards() + 'v hodnotě ' + str(self.getHandValue()))
        
  def finalDealer(self):
      print(self.listCards() + 'v hodnotě ' + str(self.getHandValue()))

  def listCards(self):
    hlaska = self.name + ' má nyní karty: '
    for card in self.hand:
        hlaska += card + ' '
    return hlaska

  def dealerCards(self):
    hlaska = self.name + ' má nyní karty: '
    for card in self.hand:
        hlaska += card + ' XX '
        break
    return hlaska


newDealer = Dealer()
player1 = Player('Dealer','Dealer', 0)
player2 = Player('Hráč 1', 'Simon' , 0)
player3 = Player('Hráč 2', 'Cautious', 0)
player4 = Player('Hráč 3','Bold', 0)

newDealer.addPlayer(player1)
newDealer.addPlayer(player2)
newDealer.addPlayer(player3)
newDealer.addPlayer(player4)

for i in range (0,5):
    newDealer.startRound()
