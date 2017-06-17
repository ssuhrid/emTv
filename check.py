while True:
    # Read states of inputs
    input_state1 = GPIO.input(17)
    input_state2 = GPIO.input(18)
    quite_video = GPIO.input(24)

    # If GPIO(17) is shorted to ground
    if input_state1 != last_state1:
        if (player and not input_state1):
            os.system('killall omxplayer.bin')
            omxc = Popen(['omxplayer', '-b', movie1])
            player = True
        elif not input_state1:
            omxc = Popen(['omxplayer', '-b', movie1])
            player = True

    # If GPIO(18) is shorted to ground
    elif input_state2 != last_state2:
        if (player and not input_state2):
            os.system('killall omxplayer.bin')
            omxc = Popen(['omxplayer', '-b', movie2])
            player = True
        elif not input_state2:
            omxc = Popen(['omxplayer', '-b', movie2])
            player = True

    # If omxplayer is running and GPIO(17) and GPIO(18) are NOT shorted to ground
    elif (player and input_state1 and input_state2):
        os.system('killall omxplayer.bin')
        player = False

    # GPIO(24) to close omxplayer manually - used during debug
    if quit_video == False:
        os.system('killall omxplayer.bin')
        player = False

    # Set last_input states
    last_state1 = input_state1
    last_state2 = input_state2
