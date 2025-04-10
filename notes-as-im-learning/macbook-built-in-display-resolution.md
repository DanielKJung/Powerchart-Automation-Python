Screen Width: 4104
Screen Height: 1296

# output screen dimensions
osascript -e 'tell application "Finder"
    set _bounds to bounds of window of desktop
end tell

set screenWidth to item 3 of _bounds
set screenHeight to item 4 of _bounds

log "Screen Width: " & screenWidth
log "Screen Height: " & screenHeight'


# resizing command with built-in finder screen size variable
tell application "Citrix Viewer"
   activate
   delay 0.5
   
   -- Use Finder to get screen dimensions
   tell application "Finder"
       set _bounds to bounds of window of desktop
   end tell
   
   -- Calculate width and height
   set screenWidth to item 3 of _bounds
   set screenHeight to item 4 of _bounds
   
   -- Set window position and size
   tell application "System Events"
       tell process "Citrix Viewer"
           set frontmost to true
           if exists window 1 then
               -- First set to a small size to force reset
               set size of window 1 to {800, 600}
               delay 0.2
               set size of window 1 to {800, 600}
               delay 0.2
               
               -- Position at top-left (with slight adjustment for menu bar)
               set position of window 1 to {0, 25}
               -- Set size to full width and height minus menu bar
               set size of window 1 to {screenWidth, screenHeight - 25}
           end if
       end tell
   end tell
end 

# resizing command with hard-coded resolution for maximum consistency/reliability
osascript -e 'tell application "Citrix Viewer"
   activate
   delay 0.5
   
   -- Set width and height
   set screenWidth to 1800
   set screenHeight to 1169
   
   -- Set window position and size
   tell application "System Events"
       tell process "Citrix Viewer"
           set frontmost to true
           if exists window 1 then
               -- First set to a small size to force reset
               set size of window 1 to {800, 600}
               delay 0.2
               set size of window 1 to {800, 600}
               delay 0.2
               
               -- Position at top-left (with slight adjustment for menu bar)
               set position of window 1 to {0, 40}
               -- Set size to full width and height minus menu bar
               set size of window 1 to {screenWidth, screenHeight-60}
           end if
       end tell
   end tell
end tell
'