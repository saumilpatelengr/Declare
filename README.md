# 🎮 Declare



## 📝 Description
Declare is a fast-paced card game designed for 2 players, utilizing a standard 52-card deck. Using strategy, probability, and deception, the goal of the game is to have your opponent have the highest amount of points before you receive more than or equal to 100 points.



## 🎥 Gameplay Demo
![Gameplay](/assets/images/demo/demo.gif)



## 🕹️ Gameplay Overview
### Goal of the Game
The goal of the game is to have the opponent have the highest amount of points before you receive 
more than or equal to 100 points. To achieve this, you have to have the least number of points in your 
hand when a player declares each round. If you receive more than or equal to 100 points across any 
number of rounds, the game is over and the opponent’s total score will be your score for that game. 
A game is played until you receive more than or equal to 100 points.

### Contents and Setup
The game is played with a standard deck of 52 cards. Points are scored by the rank associated with a 
card. Cards with rank 2-10 have points equal to their rank. Face cards (J, Q, K) are all equal to 10 
points. Aces are equal to 1 point. The game starts with each player being dealt 5 cards from the deck. 
The rest of the deck is then placed face down between the players.

### How to Play
To complete a turn, you must either click the DECLARE button to end the round or by dropping cards 
from your hand. You should click the DECLARE button when you think you have the least number of 
points in your hand compared to your opponent. You must drop a single card or multiple cards of the 
same rank on each of your turns (unless you declare). To select the card(s) you want to drop, you can 
simply click on them and they will start to hover. After selecting what cards you want to drop, you 
must either click on the deck to draw a card or the discard pile to pickup the top card. All dropped 
cards will be put into the discard pile face up.

### Scoring
When a player declares, the value of all of their cards are added up to get their total. Totals are then 
compared between players. If the declaring player has the lowest total, they receive 0 points and 
the opposing player receives their total as points. However, if the opposing player has a lower total 
compared to the declaring player, then the declaring player’s attempt is broken. The opposing player 
receives -10 points and the declaring player receives the total points of both players.



## 🎛️ Controls
This game is played entirely with the mouse.

* **Left Click (Buttons with Words)** - Navigate different screens and gameplay; have words to show what each button does (Ex: 'MENU' button takes you back to the main menu)

* **Left Click (Back Arrow Button)** - Returns you back to the previous screen

* **Left Click (Sound/Music Buttons)** - Allow the user to mute or unmute sound/music in the game

* **Left Click (Deck)** - Allows the player to draw a card from the deck

* **Left Click (Player Hand)** - Allows the player to select cards they want to drop on their turn

* **Left Click (Discard Pile)** - Allows the player to pickup the top card of the discard pile

* **Hovering with Mouse** - Enlarges cards in the player's hand



## ✨ Features
* Mouse controls
* Enemy AI
* Score tracking
* High score system
* Card hover effects
* Clickable UI buttons
* Background music and sound effects
* Multi screen user interface
* Persistent save system for high scores and settings
* Pixel art graphics
* Responsive and smooth gameplay
* Scales to different screen sizes



## 🚀 Running from Source / Download
This repository is provided for portfolio purposes only. See the LICENSE file for details. To play the game, please download or purchase the official release using the link below.

Download the latest version here:

Coming Soon!



## 📂 Project Structure
```
├── assets              #Game resources
│   ├── audio           #Contains audio files (.mp3)
│   ├── fonts           #Contains font files
│   ├── images          #Contains image files (.png) for cards and UI
│   └── pixil           #Contains .pixil files used to create .png assets
└── src                 #Main game source code
```



## ⚙️ Game Mechanics
* Cards are represented as Card objects and managed in Python lists as a deck, a discard pile, and hands of cards
* The game runs in a turn-based loop where the user can select cards to drop, draw a card from the deck, pick up a card from the discard pile, or declare their hand through the UI
* The AI opponent makes decisions based on how many points it has in its hand, the top card of the discard pile, and which combination of cards yields the highest total value when dropped
* Each round is represented as a Game object and when a new round starts, a new Game object is created
* After someone declares, points are determined by comparing total hand values and seeing if someone broke an attempt or not
* The game's state is continuously updated through a central game loop handling input, logic, and rendering



## 🛠️ Technologies Used
Python 3.14.2

Pygame (Game Framework; licensed under LGPL 2.1)

Built-in Python libraries:
* os
* sys
* random
* json
* collections.Counter



## 🤝 Contributing
This is a personal portfolio project maintained solely by the author. I am not accepting external contributions, pull requests, or issues.



## 🙏 Credits
* Card Graphics - drawsgood - [8Bit Deck Card Assets](https://drawsgood.itch.io/8bit-deck-card-assets)

* Button Sound Effect - DRAGON-STUDIO - [Button Press](https://pixabay.com/sound-effects/film-special-effects-button-press-386165/)

* Card Sound Effect - OxidVideos - [Taking playing card](https://pixabay.com/sound-effects/film-special-effects-taking-playing-card-522520/)

* Background Music - Fresh_Morning - [India fantasia](https://pixabay.com/music/modern-jazz-india-fantasia-169996/)

* Pixel Font - Rosetta Type Foundry - Designed by David Březina - [Handjet](https://fonts.google.com/specimen/Handjet)



## 👨‍💻 Author

**Saumil Patel**

Solo developer and maintainer of this project.



## 📜 License
© 2026 Saumil Patel. All rights reserved.
This repository is provided for portfolio purposes only. See the LICENSE file for details.
