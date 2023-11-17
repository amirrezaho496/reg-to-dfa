import tree.syntax_tree as stree

# TODO: get aphabet dict and followpos dict then caculate Dtran


class DTranItem:
    def __init__(self, id: int) -> None:
        self.id = id
        self.state = set()
        self.destination: dict[str, set] = {}
        self.checked: bool = False
        self.is_final: bool = False
        pass

    def set_destination(self, letter: str, destination: set):
        self.destination[letter] = destination
        pass


class DTran:
    def __init__(self, fp_table: dict[int, set] = {}, alpha_dict: dict[int, str] = {}) -> None:
        self.table: list[DTranItem] = []
        self.followpos_table: dict[int, set] = fp_table
        self.alphabet_dict: dict[int, str] = alpha_dict
        pass

    def add_state(self, state: DTranItem):
        self.table.append(state)
        pass

    def get_item_by_state(self, state: set) -> DTranItem:
        for item in self.table:
            if item.state == state:
                return item
        return None
    
    def get_keys_by_letter(self, letter : str):
        keys = set([key for key, value in self.alphabet_dict.items() if value == letter])
        return keys
    
    def get_all_uniq_letters(self):
        return set(self.alphabet_dict.values())
    
    def are_all_states_checked(self):
        for item in self.table:
            if not item.checked:
                return False
        return True
        
        
    def add_destination(self, state: set, letter: str, destination: set):
        item = self.get_item_by_state(state)
        if item is not None:
            item.set_destination(letter, destination)
        pass
    
    def create_d_tran(self, start_state: set):
        self.table.clear()
        id = 1
        first = DTranItem(id)
        first.state = start_state
        self.add_state(first)
        
        all_letters = self.get_all_uniq_letters()
        
        while not self.are_all_states_checked():
            for item in self.table:
                if not item.checked:
                    for letter in all_letters:
                        keys = self.get_keys_by_letter(letter)
                        destination = set()
                        for key in keys:
                            if key in item.state:
                                destination = destination.union(self.followpos_table[key])
                        if destination:
                            existing_item = self.get_item_by_state(destination)
                            if existing_item is None:
                                id += 1
                                new_item = DTranItem(id)
                                new_item.state = destination
                                self.add_state(new_item)
                            item.set_destination(letter, destination)
                    item.checked = True

        self.detect_final_states()
        pass
    
    def detect_final_states(self):
        final_keys = self.get_keys_by_letter(stree.SHARP)
        for item in self.table:
            if any(key in item.state for key in final_keys):
                item.is_final = True
                
    def get_final_states_ids(self):
        return [item.id for item in self.table if item.is_final]

    def print_d_tran(self):
        print(f"{'State ID':<10} {'State':<20} {'Is final':<10} {'Destinations':<20}")
        for item in self.table:
            destinations = ', '.join([f"{letter} --> {str(destination):<20}" for letter, destination in item.destination.items()])
            print(f"{item.id:<10} {str(item.state):<20} {str(item.is_final):<10} {destinations:<20}")

    def print_d_tran_table(self):
        print(f"{'State ID':<10} {'State':<20} {'Is final':<10}")
        for item in self.table:
            print(f"{item.id:<10} {str(item.state):<20} {str(item.is_final):<10}")
            print(f"{'Letter':<10} {'Destination':<20}")
            for letter, destination in item.destination.items():
                print(f"{letter:<10} {str(destination):<20}")
            print("\n")
            
    def convert_dtran_to_dict(dtran):
        dfa = {}
        for item in dtran.table:
            state_transitions = {}
            for letter, destination in item.destination.items():
                # Assuming each state has only one destination for each letter
                destination_item = dtran.get_item_by_state(destination)
                if destination_item is not None:
                    state_transitions[letter] = destination_item.id
            dfa[item.id] = state_transitions
        return dfa

