from room import Room
from player import Player
from world import World
from util import Stack

import random
import collections
from ast import Str, literal_eval

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

opposite_direction = {"n": "s", "s": "n", "e": "w", "w": "e"}
visited = set()

def recursive_traverse():
    moves = []
    for cur_direction in player.current_room.get_exits():
        player.travel(cur_direction)
        if player.current_room in visited:
            player.travel(opposite_direction[cur_direction])
        else:
            visited.add(player.current_room)
            moves.append(cur_direction)
            moves.extend(recursive_traverse())
            player.travel(opposite_direction[cur_direction])
            moves.append(opposite_direction[cur_direction])
    return moves

traversal_path = recursive_traverse()


# # TRAVERSAL TEST
for move in traversal_path:
    player.travel(move)
    visited.add(player.current_room)

if len(visited) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited)} unvisited rooms")


######
# UNCOMMENT TO WALK AROUND
######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")