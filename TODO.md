- need to make sure coordinates.json line 78, that the section_header has a state called default vs scrolled.


#### Media Gallery
<!-- feed screenshot to calculate how many DATES there are, so it knows if it needs to load more media. can also determine if there even is a NEW picture (LLM compares latest date on screenshot to today's date, to see if we even need to load any media-->


0, 0, View, to VIEW, it's most systematically bullet-proof to click Select All Media and then press: Tab, Enter.


#### Documentation
<!-- let's just go to the Documentation's own section for this... -->
<!-- set a condition where if you're in Documentation View, and you try to leave to do something else, it re-clicks on Provider View first to re-orient. -->

____

<!-- use LLM to program to keep going back until there's a big jump in date discrepancy. start from there. work-up note by note.

1. does it look like it ONLY has text?
    1. click then control (^) + a. did it highlight?
        1. control (^) + c. save. 
        [[
        i need a verification process here to see if it pasted.
        i also need a verification process to make sure the EHR's loaded
        prior to making next moves.
        ]]
    2. if not, run the cliclicktest.py algorithm.
2. if not, take a screenshot, log it, and ignore.
 -->


#### Diagnostics
430, 395, click Diagnostics, click this to enable keyboard navigation
<!-- you need to automatically press TAB 3 + 6 times, to get to cycling through the actual images.

Each time we press tab, grab a screenshot: then ask

prompt idea #1: is there ANY diagnostic sections that actually has an item AKA section has an actual image to view? 

if yes: inner prompt: am I hovering over a section or an item? if hovering over section, is the count 0?
    if yes section, yes zero: press Tab again and repeat prompt.
    if yes section, no zero: press Tab again and press ENTER.
    if no section: press ENTER.

    control (^) + a, control (^) + c, paste to log. wait for refresh to finish (lag), then exit.
     ^^ this causes MAJOR lag.
if no: go to labs.
 -->
30, 115, exit diagnostic report



700, 430, Change Clinical Range, change the date-window of what results are displayed.
<!-- after clicking Chance Clinical Range, you can press `down arrow`, ENTER.

press TAB. then you're ready to type in date: MM/DD/YYYY format.
 -->

#### Microbiology:
<!-- click on an empty space. then do 4 + 8 tabs. then you're ready to start opening. -->

<!-- LLM: screenshot. check if LAST_UPDATED date is already matched to our logs/database.
if NOT matching, that means there's new info.
OPEN!
click the middle! select all! copy! paste to logs! 


ESC to close.
 -->

#### Intake & Output
900, 390, activate Intake & Output, click here to activate keyboard navigation for Intake & Output
<!-- press tab 2 times.
ENTER (refresh).
WAIT 5 seconds. (or until loads)
click activate Intake & Output again.
Tab 5 times.
down arrow (hover total summary, by default is opened). 
ENTER (collapse total summary)
down arrow x3 (go to counts)
ENTER + up arrow (open counts)
ENTER + up arrow (open output)
ENTER + up arrow (open input)
ENTER + up arrow (open total summary)

do the LLM-assisted scroll down until next header algorithm.

 -->
