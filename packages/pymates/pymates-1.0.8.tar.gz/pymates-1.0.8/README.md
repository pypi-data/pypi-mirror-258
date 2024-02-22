# Matt's Automatic Tracking Encounter Software

Videos:

<https://youtu.be/IkLZOhnaS2c>

<https://youtu.be/GtdwyRFSZAA>

Simple encounter tracker I slapped together in 3 days.
Entirely programmed for android phones on an android phone.

No I'm not joking.
![programming](https://i.imgur.com/BLCC92W.png)


## Important:
The reason this needs root is because like all the other encounter trackers it works by taking captures of the screen. This is not usually possible on android because to capture the screen you must use the screenshot API which will only show content the app that requested the screenshot has rendered which is useless for this.

I solved this issue by using a command that's tucked away in the binaries of android "screencap" this returns an unadulterated screenshot but is only accessible via root.

The nature of this is somewhat of a security concern but these captures are immediately deleted after scanning for Pokémon.

These captures never leave your device but as a precaution I still wouldn't leave it capturing if anything other than pokemmo is on screen.

You can toggle capture by pressing enter with no command typed in.

### I am not liable nor responsible if you brick your phone trying to root it! If you don't understand phone rooting then it's probably not a great idea to root your phone just for this. There are pros and cons to rooted android.

## Requirements:


| rooted phone                                                     |
| ---------------------------------------------------------------- |
| termux float - <https://github.com/termux/termux-float/releases> |
| termux - <https://github.com/termux/termux-app/releases>         |
| tsu - (in termux: pkg install tsu)                               |
| python (in termux: pkg install python)                           |
| tesseract (in termux: pkg install tesseract)                     |
| pytesseract (in termux: pip install pytesseract)                 |
| opencv2 (in termux: pkg install opencv-python)                   |


don't get your hopes up too high. this is janky and sometimes doesnt work. if you have an issue please leave a report on the github issues page
<https://github.com/Th3M4ttman/MATES/issues>

## Installation:

### Automatic
in termux enter:

pip install pymates

### Manual
download the latest release from the releases section and run:

pip install /whereever/you/put/the/wheel/mates.whl

### Additional
if you want to run mates without having to type sudo every time add this to the end of your bashrc located in  /data/data/com.termux/files/usr/etc/bash.bashrc

alias mates="sudo mates"

and if you wanna make it even easier to launch:

alias m=mates


## Usage:

To run the software run "sudo mates" in termux float or "mates" if you added the alias

![interface](https://i.imgur.com/d97zLJc.jpeg)


| Number | Component                    |
| ------ | ---------------------------- |
| 1      | Capture indicator            |
| 2      | Shiny bonus chance           |
| 3      | Donator/Charm/Link indicator |
| 4      | Combat indicator             |
| 5      | Reported Pokémon indicator   |
| 6      | Singles tracking indicator   |
| 7      | Command input/output         |


press enter to toggle capture on and off

Or type in commands


| Command                | Use                                            | Notes                                                                                      |
| ---------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Reset (Pokémon)        | Resets encounters for selected Pokémon.        | If given no Pokémon resets all                                                             |
| add (number) (Pokémon) | Adds number \* Pokémon encounters              | You can also use "+"                                                                       |
| sub (number) (Pokémon) | Subtracts number \* Pokémon encounters         | You can also use "-"                                                                       |
| track (Pokémon)        | Sets the Pokémon as a tracked pokemon          | If given no Pokémon it tracks all Pokémon with registered encounters. You can also use "t" |
| untrack (Pokémon)      | Sets the Pokémon as an untracked pokemon       | If given no Pokémon it untracks all. You can also use "u"                                  |
| total                  | Toggles the visibility of the total encounters |                                                                                            |
| charm                  | Toggles shiny charm                            |                                                                                            |
| donator                | Toggles donator                                |                                                                                            |
| link                   | Toggles shiny charm link                       |                                                                                            |
| singles                | Toggles single tracking                        |                                                                                            |
