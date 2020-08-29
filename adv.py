from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

## Understanding Phase:

# To write and algorithm that picks a random unexplored direction from the player's current room, 
# travels and logs that direction, then loops.
# This should cause your player to walk a depth-first traversal. When you reach a dead-end
# (i.e. a room with no unexplored paths), walk back to the nearest room that does contain an unexplored path.

# You can find the path to the shortest unexplored room by using a breadth-first search for a room with a '?' for an
# exit. 


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

## Plan and Execution Phase:

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# Create a function called traverse and pass in player as the argument
def traverse(player):
    # Create an empty set to keep track of the visited rooms
    visited = set() 

    # Create an empty array to store the previouse paths (in case the user needs to go back)
    prev_path = []

    # Through a while loop see the rooms that haven't been traversed
    while len(visited) < len(world.rooms):
        # Grab the current room that the player is in and create a new var
        current_room = player.current_room
        # Grab the exits from the current room exits and create a new var
        current_room_exits = current_room.get_exits()
        # Create a var for the untraveresed directions from the current room
        untraversed = [direction for direction in current_room_exits if current_room.get_room_in_direction(direction) not in visited]

        # Mark the current room as visited
        visited.add(current_room)

        # If there are untraversed rooms, pick a random direction and traverse
        if untraversed:
            direction = untraversed[random.randint(0, len(untraversed)-1)]
            player.travel(direction)
            prev_path.append(direction)
            traversal_path.append(direction)
        # otherwise we are at a dead end, go to the previouse path
        else:
            # Get the last direction that user went in 
            last_direction = prev_path.pop(-1)
            # Reverse the last direction to go back
            reverse_direction = {'s': 'n', 'n': 's', 'w': 'e', 'e': 'w'}
            player.travel(reverse_direction[last_direction])
            traversal_path.append(reverse_direction[last_direction])
    
    # Return the traversal_path array
    return traversal_path

# Set the traversal_path array to the traverse method and pass in the player
traversal_path = traverse(player)





# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
