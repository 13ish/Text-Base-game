import sys


class TextAdventureGame:
    def __init__(self):
        self.rooms = {
            "camp": {
                "name": "Campfire Clearing",
                "description": (
                    "You stand beside a small campfire, with a well-worn path leading north. "
                    "A torch is propped against a stump."
                ),
                "exits": {"north": "forest"},
                "items": ["torch"],
            },
            "forest": {
                "name": "Moonlit Forest",
                "description": (
                    "Ancient trees loom overhead and the air smells of pine. A narrow trail runs south, "
                    "and an old stone ruin sits to the east."
                ),
                "exits": {"south": "camp", "east": "ruins"},
                "items": ["map"],
            },
            "ruins": {
                "name": "Sunken Ruins",
                "description": (
                    "Broken pillars rise from the earth. A silver key lies in a cracked stone bowl. "
                    "A dark cave yawns to the north."
                ),
                "exits": {"west": "forest", "north": "cavern"},
                "items": ["silver key"],
                "locked_exits": {"north": "silver key"},
            },
            "cavern": {
                "name": "Crystal Cavern",
                "description": (
                    "The cave is lit by a faint blue glow. A brilliant sun crystal rests on a pedestal in the center. "
                    "A stone gate lies to the east."
                ),
                "exits": {"south": "ruins", "east": "gate"},
                "items": ["sun crystal"],
                "locked_exits": {"east": "silver key"},
            },
            "gate": {
                "name": "The Moon Gate",
                "description": (
                    "A massive gate blocks the way out, carved with worn symbols of dawn. "
                    "The final challenge is before you."
                ),
                "exits": {"west": "cavern"},
            },
        }

        self.current_room = "camp"
        self.inventory = []
        self.game_over = False
        self.victory = False
        self.story_flags = {"torch_placed": False}

    def normalize_text(self, text):
        return text.strip().lower()

    def room_items(self, room_name):
        room = self.rooms[room_name]
        return room.get("items", [])

    def show_room(self):
        room = self.rooms[self.current_room]
        print(f"\n=== {room['name']} ===")
        print(room["description"])

        exits = list(room.get("exits", {}).keys())
        if exits:
            print("Exits:", ", ".join(exits))
        else:
            print("Exits: none")

        room_items = self.room_items(self.current_room)
        if room_items:
            print("You can see:", ", ".join(room_items))

    def show_inventory(self):
        if not self.inventory:
            print("Your inventory is empty.")
            return
        print("Inventory:", ", ".join(self.inventory))

    def move(self, direction):
        room = self.rooms[self.current_room]
        exits = room.get("exits", {})

        if direction not in exits:
            print("You cannot go that way.")
            return

        next_room = exits[direction]
        required = room.get("locked_exits", {}).get(direction)
        if required and required not in self.inventory:
            print(f"The path is blocked. You need the {required} to continue.")
            return

        self.current_room = next_room
        print(f"You move {direction}.")
        self.show_room()

        if self.current_room == "gate":
            self.check_gate()

    def take_item(self, item_name):
        room = self.rooms[self.current_room]
        items = room.get("items", [])
        item_name = self.normalize_text(item_name)

        for index, item in enumerate(items):
            if self.normalize_text(item) == item_name:
                del items[index]
                self.inventory.append(item)
                print(f"You pick up the {item}.")
                return

        print(f"You don't see a {item_name} here.")

    def use_item(self, item_name):
        item_name = self.normalize_text(item_name)
        room = self.rooms[self.current_room]

        if self.current_room == "gate":
            if item_name == "silver key":
                if "silver key" in self.inventory:
                    print("You fit the silver key into the gate and hear a metal click.")
                    self.story_flags["gate_unlocked"] = True
                    return
                print("You don't have the silver key.")
                return

            if item_name == "sun crystal":
                if "sun crystal" not in self.inventory:
                    print("You don't have the sun crystal.")
                    return
                if "silver key" not in self.inventory:
                    print("The crystal glows, but the gate remains sealed. You need the silver key.")
                    return
                print("The sun crystal flares to life! The moon gate opens, bathing the world in dawn light.")
                print("You step through and escape the ruins. You win!")
                self.victory = True
                self.game_over = True
                return

        if item_name == "torch":
            if "torch" in self.inventory:
                print("The torch crackles warmly in your hand.")
                return
            print("You don't have a torch to use.")
            return

        if item_name == "map":
            if "map" in self.inventory:
                print("The map shows the route to the ancient gate and the crystal cavern.")
                return
            print("You don't have a map to use.")
            return

        print(f"You cannot use the {item_name} here.")

    def check_gate(self):
        if self.current_room == "gate" and "sun crystal" not in self.inventory:
            print("The gate is sealed tight. You need the sun crystal from the cavern to open it.")

    def help_text(self):
        print("Commands:")
        print("  look / l             - Examine the room")
        print("  inventory / inv      - Check what you have")
        print("  take <item>          - Pick up an item")
        print("  use <item>           - Use or activate an item")
        print("  go <direction>       - Move north, south, east, or west")
        print("  move <direction>     - Alias for go")
        print("  help                 - Show this help")
        print("  quit                 - Exit the game")

    def handle_command(self, command_line):
        command = command_line.strip()
        if not command:
            return

        words = command.split()
        action = words[0].lower()

        if action in {"quit", "exit"}:
            print("You leave the adventure behind.")
            self.game_over = True
            return

        if action in {"help", "?"}:
            self.help_text()
            return

        if action in {"look", "l"}:
            self.show_room()
            return

        if action in {"inventory", "inv"}:
            self.show_inventory()
            return

        if action in {"go", "move"}:
            if len(words) < 2:
                print("Specify a direction, like: go north")
                return
            self.move(words[1].lower())
            return

        if action == "take":
            if len(words) < 2:
                print("What do you want to take?")
                return
            item_name = " ".join(words[1:])
            self.take_item(item_name)
            return

        if action == "use":
            if len(words) < 2:
                print("What do you want to use?")
                return
            item_name = " ".join(words[1:])
            self.use_item(item_name)
            return

        print("I don't understand that command. Try 'help' for the command list.")

    def play(self):
        print("Welcome to Moon Gate.")
        print("A forgotten world waits beneath the stars. Escape the ruins before dawn breaks.")
        print("Type 'help' if you need instructions.")
        self.show_room()

        while not self.game_over:
            try:
                command = input("\nWhat do you do? ")
            except EOFError:
                print("\nThe adventure ends here.")
                break
            self.handle_command(command)
            if self.victory:
                self.game_over = True

        print("\nThanks for playing Moon Gate.")


def main():
    game = TextAdventureGame()
    game.play()


if __name__ == "__main__":
    main()
