# This document is complete.
This document officially has ALL the coordinates of button clicks that is required for
do-ro.

# Keeping a log of coordinates here, manually doing the screenshot method


x, y, name, description(optional)


# Home
360, 130, Patient List, see various Patient Lists

## Patient Lists
220, 280, Pink A, see my team's patient list. requires you to be in Patient Lists

### Specific Patient List
640, 340, Length Of Stay, sort toggle for Length Of Stay. requires you to be in a specific patient list.
900, 340, Discharged, sort toggle for Discharged boolean. requires you to be in a specific patient list.

200, 358, Patient 1, double click to see patient 1. needs vision language model assistance.
200, 376, Patient 2
200, 394, Patient 3
200, 411, Patient 4
200, 429, Patient 5
200, 447, Patient 6
200, 465, Patient 7
200, 483, Patient 8
200, 501, Patient 9
200, 519, Patient 10
200, 537, Patient 11
200, 555, Patient 12
200, 574, Patient 13
200, 592, Patient 14
200, 610, Patient 15
200, 627, Patient 16
200, 645, Patient 17
200, 663, Patient 18
200, 681, Patient 19
200, 698, Patient 20

#### Specific Patient
250, 350, Demographics
400, 350, Inpatient/Manage
550, 350, Inpatient Quick Orders

<!-- Check for warning column with LLM. note and log the warning, and delete it.-->

<!-- NOTE!! Even if you 'delete' it AKA 'Hide SmartZone',
the UI looks different vs. patients without any warnings. 

the UI that's aligned to the RIGHT seems to have a 44 pixel shift. make note.
-->

![Hidden SmartZone](/media/Hidden%20SmartZone.png)
![No SmartZone](/media/No%20SmartZone.png)



1550, 270, screenshot left-upper corner
1799, 1149, screenshot right-lower corner
1575, 290, delete warning, seems to be called internally as 'Hide SmartZone'



##### Inpatient/Manage
(I'm going to translate Inpatient/Manage to one hash-tag to allow more sub-sectioning.)

# Inpatient/Manage
<!-- 
x1 = 370
x2 = 1774

y1 = 370
y2 = 1149 -->
370, 370, screenshot left-upper corner
1774, 1149, screenshot right-lower corner

1783, 380, scroll up
1783, 1130, scroll down, press 17 times to load a new 'page' while maintaining slight context.


## Inpatient/Manage LLM Logic
- click the section heading.
- if you can't see the header of the next predicted section, it means there's more content/information
    - scroll down 17 times (enough to maintain sliver of context while loading new 'page')
    - re-assess if you can see the header of the next predicted section [while loop-type vibes]. continue until you can.

## Section Headers 
### Default (completely scrolled-up)
355, 410, Section List Scroll Up, press 6 times to return to default (completely scrolled-up)
355, 1130, Section List Scroll Down, press 6 times to view the others.

300, 420, Hospital Course
300, 465, Action & Situational Awareness
300, 490, Reminders
300, 515, Problem List
300, 540, Histories
300, 565, Implant History
300, 590, Allergies
300, 615, Immunizations
300, 640, Lines/Tubes/Drains
300, 665, Risk Indicators
300, 690, Media Gallery
300, 715, Documentation
300, 740, Diagnostics
300, 765, Labs
300, 790, Microbiology
300, 815, Pathology
300, 840, Intake and Output
300, 865, Vital Signs
300, 890, Medications
300, 915, Patient Timeline Medications
300, 955, Quality Measures
300, 980, Order Profile
300, 1015, Subjective/History of Present Illness (HPI)
300, 1050, Review of Systems (ROS)
300, 1075, Objective/Physical Exam
300, 1100, Assessment and Plan

#### History
440, 440, Problems
520, 440, Procedure
600, 440, Family
680, 440, Social

#### Media Gallery
<!-- feed screenshot to calculate how many DATES there are, so it knows if it needs to load more media. can also determine if there even is a NEW picture (LLM compares latest date on screenshot to today's date, to see if we even need to load any media-->
370, 370, screenshot left-upper corner
559, 1149, screenshot right-lower corner


560, 495, Select All Media
450, 490, all media from latest date
450, 520, all media from 2nd to latest date
450, 550, 3rd
450, 580, 4th
450, 610, 5th

0, 0, View, to VIEW, it's most systematically bullet-proof to click Select All Media and then press: Tab, Enter.

##### Media Viewer
400, 420, previous image
435, 420, next image

<!-- these coordinates are warning-proof. -->
240, 360, screenshot left-upper corner, screen-grab entire media viewer for comfort
1704, 1149, screenshot right-lower corner, screen-grab entire media viewer for comfort

<!-- these coordinates are warning-proof. -->
258, 585, screenshot right-lower corner, screen-grab media only for vLM
1690, 1127, screenshot right-lower corner, screen-grab media only for vLM

#### Documentation
<!-- let's just go to the Documentation's own section for this... -->
<!-- set a condition where if you're in Documentation View, and you try to leave to do something else, it re-clicks on Provider View first to re-orient. -->

100, 505, Documentation, go to a dedicated Documentation View.

<!-- these coordinates are warning-proof. -->
1600, 380, previous note, towards more recent notes
1700, 380, next note, towards older notes

<!-- these coordinates are warning-proof. -->
250, 1120, previous page, towards more recent pages.
350, 1120, next page, towards older pages.

400, 450, note 1, 1st note of the page
400, 486, note 2, 2nd note of the page
400, 522, note 3, 3rd note of the page
400, 558, note 4, 4th note of the page
400, 594, note 5, 5th note of the page
400, 630, note 6, 6th note of the page
400, 666, note 7, 7th note of the page
400, 702, note 8, 8th note of the page
400, 738, note 9, 9th note of the page
400, 774, note 10, 10th note of the page
400, 810, note 11, 11th note of the page
400, 846, note 12, 12th note of the page
400, 882, note 13, 13th note of the page
400, 918, note 14, 14th note of the page
400, 954, note 15, 15th note of the page
400, 990, note 16, 16th note of the page
400, 1026, note 17, 17th note of the page
400, 1062, note 18, 18th note of the page

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

#### Labs
100, 380, Results Review, go to a dedicated Results Review View (includes vitals, labs, and radiology/diagnostics)

500, 350, All Radiology, see all Radiology/Diagnostics results in Results Review view.
400, 350, All Laboratory, see all Lab results in Results Review view.
350, 350, Vitals, see all Vitals results in Results Review view.

700, 430, Change Clinical Range, change the date-window of what results are displayed.
<!-- after clicking Chance Clinical Range, you can press `down arrow`, ENTER.

press TAB. then you're ready to type in date: MM/DD/YYYY format.
 -->
500, 470, Copy All Laboratory Table
500, 470, Copy All Vitals Table

#### Microbiology:
<!-- click on an empty space. then do 4 + 8 tabs. then you're ready to start opening. -->

<!-- LLM: screenshot. check if LAST_UPDATED date is already matched to our logs/database.
if NOT matching, that means there's new info.
OPEN!
click the middle! select all! copy! paste to logs! 


ESC to close.
 -->
900, 390, activate Microbiology, click here to activate keyboard navigation for microbiology
900, 600, copy microbiology results


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

#### Patient Timeline Medications

<!-- if WARNING, subtract 44 from 1726 to get 1682, as the X-coordinate. -->
1726, 901, scroll down, press 9 times to load a new page (with sliver of context)
1726, 515, scroll up

380, 460, screenshot left-upper corner
1740, 915, screenshot right-lower corner



### 6-scroll clicks down
300, 880, Health Maintenance
300, 905, Visits List
300, 930, External Referrals
300, 960, New Order Entry
300, 980, Transfusion, patient blood bank details and transfusion history
300, 1005, Asthma Action Plan

#### click these to WRITE notes
300, 1070, Inpatient Progress Note
300, 1100, Admission H&P
300, 1125, Select Other Note

