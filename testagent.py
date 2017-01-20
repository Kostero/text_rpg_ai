import textplayer.textPlayer as tp
import random

directions = ['east', 'west', 'south', 'north', 'southeast', 'southwest', 'northeast', 'northwest', 'up', 'down']
places = set()

def look():
    return t.execute_command('look')

def get_command():
    return 'go ' + random.choice(directions)

t = tp.TextPlayer('zork1.z5')
start_info = t.run()
print start_info
for i in range(1000):
    command = get_command()
    print command
    command_output = t.execute_command(command)
    print command_output
    places.add(look())
    if t.get_score() is not None:
        (score, possible_score) = t.get_score()
        print("Score:", score, "Possible score:", possible_score)
    else:
        break
t.quit()
for p in places:
    print p
print len(places)