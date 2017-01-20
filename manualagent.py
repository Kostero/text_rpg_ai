import textplayer.textPlayer as tp

def get_command():
    print '\n>>',
    return raw_input()

t = tp.TextPlayer('zork1.z5')
start_info = t.run()
print start_info
while True:
    command = get_command()
    command_output = t.execute_command(command)
    print command_output
    if t.get_score() is not None:
        (score, possible_score) = t.get_score()
        print("Score:", score, "Possible score:", possible_score)
    else:
        break
t.quit()
