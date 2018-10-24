# Flash Card Maker

Simple, Smart, fast. This tool is designed to build and manage decks of flashcards using the most simplistic method.

To create a deck of flash cards:
	-1) Create a text file
	-2) Type what you want to write on the front side of your first card without hitting <Tab> key or <Enter> key (Instead, you can use a ' -' as a replacement for a line change character by default. The specific keyword can be changed by modifying the config file under kwrd_newline)
	-3) Press the <tab> key. Now you have finished the front side of your card!
	-4) Type what you want to write on the back of the card. Again, you can use '-' to initialize a new line (Tip: to create a bullet, I use ' --'. See some of the test files I have in the WIP folder.)
	-5) Hit <enter>. Now you have finished making your first card!
	-6) Repeat step 2-5 to create more cards

To load a deck:
	-1) Initialize the .exe file (or the .py file if you have python and the neccessary denpendcies) 
	-2) Select deck you have created in the dialog (.txt or .dk file) and click open
	-3) Begin your study session!
	-4) Use 'Next' and 'Prev' button to browse. Use 'Good' button if you feel good about the card and don't want to see it as often, 'Bad' if you feel bad about the card and want to review it in the near feature.
	-5) Shuffle the deck using the shuffle button on the bottom right corner. You can chose shuffle mode in the 'option' menu
	-6) Save your study progress and export the deck by using the 'Save' function under file tab on the top left corner or press Ctrl+S. This will save the deck as a .dk file
	-7) Load a another study session or deck by using the load function under the file tab.

## Features
	-Smart Shuffling. To enable Smart Shuffling, under 'Option' menu, shuffle mode, check 'Allow repeats'. Smart shuffling shuffles the deck based on user accuracy on each card, ajusted by times the card has been studied.


## Dependencies
>PyQt5

