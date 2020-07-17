from room import Room
from player import Player
from world import World
from util import Stack

import random
from ast import literal_eval

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

traversal_path = []
traversal_graph = {}

visited = set()
stack = Stack()

# Add starting room to stack
stack.push([player.current_room])

while stack.size() > 0:
    cur_path = stack.pop()
    room = cur_path[-1]

    if room not in visited:
        # mark room as visisted
        visited.add(room)

        # populate known rooms into a dictionary
        traversal_graph[room.id] = {"n": "?", "s": "?", "e": "?", "w": "?"}

        # loop through room's exists
        for exit in room.get_exits():
            # check if the current exit has a valid room
            if room.get_room_in_direction(exit) == None:
                traversal_graph[room.id][exit] = None
            else:
                # find the next room
                next_room = room.get_room_in_direction(exit)

                if next_room in visited:
                    continue
                # add this direction to the traversal path
                traversal_path.append(exit)
                # add the next room at current exit to dictionary
                traversal_graph[room.id][exit] = next_room.id
                # copy the current path and add the next room
                copy_path = [*cur_path, next_room]
                stack.push(copy_path)


# # TRAVERSAL TEST
for move in traversal_path:
    player.travel(move)
    visited.add(player.current_room)

if len(visited) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")