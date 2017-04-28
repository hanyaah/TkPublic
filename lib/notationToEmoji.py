from lib.moveConversionDict import *

#======================================================================
#=============BEGIN Replacing Move Notation with INTERMEDIATES ========
#======================================================================

def moveReplace(userInput_Move):
    process_Move = userInput_Move

    #first replace those that can't possibly be a subset of other notation sets, like the multiaxis series.
    #Step 1: Replace the QuadButton Presses
    process_Move = process_Move.replace('1+2+3+4',quadButton['1+2+3+4'])

    #Step 2: Replace the TriButton Presses
    for tri in triButton:
        process_Move = process_Move.replace(tri, triButton[tri])

        #Step 3: Replace the DuoButton Presses
    for duo in duoButton:
        process_Move = process_Move.replace(duo, duoButton[duo])

        #Step 4: Replace SoloButton Presses
    for solo in soloButton:
        process_Move = process_Move.replace(solo, soloButton[solo]) 

    output_Move = process_Move
    outputString = 'Initial Attack Buttons Replaced: ' + output_Move

    #Step 5: Replace Axis Buttons
    for axis in multiAxis:
        process_Move = process_Move.replace(axis, multiAxis[axis])

    for axis in diagAxis:
        process_Move = process_Move.replace(axis,diagAxis[axis])

    for axis in straightAxis:
        process_Move = process_Move.replace(axis,straightAxis[axis])

    process_Move = process_Move.replace('n', nullAxis['n'])

    outputString = 'Initial Axis Buttons Replaced: ' + output_Move

    #Replace the intermediates with the final 
    output_Move = moveReplaceFinal(process_Move)
    

    return output_Move

#=====================================================================
#=============END Replacing Move Notation with INTERMEDIATES==========
#=====================================================================

#==================================================================================
#=============BEGIN Replacing INTERMEDIATES with Icons (FINAL Conversion)==========
#==================================================================================

def moveReplaceFinal(intermediate_Move):
    process_Move = intermediate_Move

    #first replace those that can't possibly be a subset of other notation sets, like the multiaxis series.
    #Step 1: Replace the QuadButton Presses
    process_Move = process_Move.replace('1+2+3+4',quadButton['1+2+3+4'])

    #Step 2: Replace the TriButton Presses
    for tri in triButton:
        process_Move = process_Move.replace(tri, triButton[tri])

        #Step 3: Replace the DuoButton Presses
    for duo in duoButtonFinal:
        process_Move = process_Move.replace(duo, duoButtonFinal[duo])

        #Step 4: Replace SoloButton Presses
    for solo in soloButtonFinal:
        process_Move = process_Move.replace(solo, soloButtonFinal[solo])    

    output_Move = process_Move
    outputString = 'Intermediate Attack Buttons Replaced: ' + output_Move

    #Step 2: Replace Axis Buttons
    for axis in multiAxisFinal:
        process_Move = process_Move.replace(axis, multiAxisFinal[axis])

    for axis in diagAxisFinal:
        process_Move = process_Move.replace(axis,diagAxisFinal[axis])

    for axis in straightAxisFinal:
        process_Move = process_Move.replace(axis,straightAxisFinal[axis])

    process_Move = process_Move.replace('NEWT', nullAxisFinal['NEWT'])

    output_Move = process_Move
    outputString = 'Intermediate Axis Buttons Replaced: ' + output_Move

    return output_Move

#==================================================================================
#=============END Replacing INTERMEDIATES with Icons (FINAL Conversion)============
#==================================================================================

#Function below is called by Main Script
def icon_move_processor(char_move_notation):
    stanceHolder = '' #initialize stanceHolder

    for fStance in stance:
      #temporarily remove recognized stances to prevent moveReplace from overwriting them
      if fStance in char_move_notation:
          char_move_notation = char_move_notation.replace(fStance, "")
          stanceHolder = fStance

    processed_icon_move = moveReplace(char_move_notation.lower())

    #Add stances back to string
    processed_icon_move = stanceHolder + processed_icon_move

    return(processed_icon_move)
