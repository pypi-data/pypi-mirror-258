class TuringMachine:
    """
    Class to define a computation Turing Machine
    """

    def __init__(self, states, transition_function):
        self.states = states
        self.transition_function = transition_function
        self.start_state = states.start_state

    def simulator(self, tape):
        """
        Returns a turing machine simulator instance of the current the Turing machine on a given tape.
        """
        return TuringMachineSimulator(self, tape)

    def compute(self, tape):
        simulator = self.simulator(tape)
        while simulator.has_next():
            simulator.next()
        return tape

    def __call__(self, tape):
        return self.compute(tape)


class TuringMachineSimulator:
    """
    Effectively an iterator for a turing machine.
    """

    def __init__(self, turing_machine, tape):
        self.current_state = turing_machine.start_state
        self.transition_function = turing_machine.transition_function
        self.tape = tape

    def has_next(self):
        """
        This method checks if the Turing machine has a next state to move to or not.

        Returns:
            bool: True if the current state of the Turing machine is not a halt state, False otherwise.
        """
        return not self.current_state.is_halt

    def next(self):
        """
        Executes one step of the current machine according according to the current configuration.
        """
        if not self.has_next():
            raise ValueError("No next state")
        self.current_state = self.transition_function.compute_transition(self.current_state, self.tape)

    def configuration(self):
        """
        Returns a string representation of the configuration.
        """
        return self.tape.configuration(self.current_state)

class TransitionFunction:

    def __init__(self, transitions):
        """
        Initializes a Turing machine with the given transitions.

        Parameters:
        transitions (dict): A dictionary that maps TransitionInput to TransitionOutput.
        """
        self.transitions = transitions

    def compute_transition(self, state, tape):
            """
            Computes the transition for the given state and tape.

            Args:
                state (State): The current state of the Turing machine.
                tape (Tape): The tape of the Turing machine.

            Returns:
                State: The next state of the Turing machine.

            Raises:
                ValueError: If the transition function is not defined for the given state and tape character.
            """
            character = tape.read()
            transition_input = TransitionInput(state, character)
            if transition_input not in self.transitions.keys():
                raise ValueError("Transition function not defined for " + transition_input.__str__())
            transition = self.transitions[transition_input]
            transition.write(tape)
            return transition.state

class TransitionFunctionBuilder:

    def __init__(self, states):
        self.transitions = dict()
        self.states = states # set of all states that can be drawn

    def add(self, transition_in, transition_out):
        return self.add(transition_in.state, transition_in.character, transition_out.state, transition_out.character, transition_out.movement)

    def add(self, state_in, character_in, state_out, character_out, movement):
        if not self.states.contains(state_in):
            raise ValueError("Input state must be an existing state in the domain")
        if not self.states.contains(state_out):
            raise ValueError("Output state must be an existing state in the codomain")
        self.transitions[TransitionInput(state_in, character_in)] = TransitionOutput(state_out, character_out, movement)
        return self

    def build(self):
        return TransitionFunction(self.transitions)

class TransitionInput:
    """
    Represents the (state, read character) tuple input to the transition function
    """

    def __init__(self, state, character):
        self.state = state
        self.character = character

    def __hash__(self):
        return self.state.__hash__() + self.character.__hash__()

    def __eq__(self, other):
        return self.state == other.state and self.character == other.character

    def __str__(self):
        return f"({self.state}, {self.character})"

class TransitionOutput:
    """
    Represents (output state, character to write, movement) tuple returned by the transition function.
    """

    def __init__(self, state, character, movement):
        self.state = state
        self.character = character
        self.movement = movement

    def write(self, tape):
        # writes to an input tape
        tape.write(self.character, self.movement)

    def __str__(self):
        return f"({self.state}, {self.character}, {self.movement})"

class State:

    def __init__(self, label, is_start = False, is_halt = False):
        self.label = label
        self.is_start = is_start
        self.is_halt = is_halt

    def __eq__(self, other):
        if other == None:
            return False
        return self.label == other.label

    def __hash__(self):
        return self.label.__hash__()

    def __str__(self):
        return self.label


class StateSet:

    def __init__(self, backing_set, start_state, halt_state):
        self.backing_set = backing_set
        self.start_state = start_state
        self.halt_state = halt_state

    def contains(self, state):
        return state in self.backing_set

class StateSetBuilder:

    def __init__(self):
        self.backing_set = set()
        self.start_state = None
        self.halt_state = None
        self.curr_id = 0

    def add(self, state):
        if self.start_state != None and state.is_start:
            raise ValueError("Start state already exists in this state set.")
        elif self.halt_state != None and state.is_halt:
            raise ValueError("Halt state already exists in this state set.")
        else:
            self.curr_id += 1
            self.backing_set.add(state)
            if state.is_start:
                self.start_state = state
            if state.is_halt:
                self.halt_state = state
        return self

    def addAll(self, *states):
        for state in states:
            self.add(state)
        return self

    def build(self):
        if self.start_state == None:
            raise ValueError("No start state defined")
        return StateSet(self.backing_set, self.start_state, self.halt_state)


class Tape:

    def __init__(self, input_string, delimiter = " ", empty_space = "_"):
        # input_string is delimeter-separated string of symbols on the tape
        self.array = input_string.split(delimiter)
        self.empty_space = empty_space
        self.tape_head = 0

    def expand_capacity(self):
        self.array = self.array + [self.empty_space for i in range(len(self.array))]

    def read(self):
        return self.array[self.tape_head]

    def write(self, character, movement):
        if movement not in ["L", "R"]:
            raise ValueError("Movement must be either R or L")
        self.array[self.tape_head] = character
        if movement == "R":
            self.tape_head += 1
        else:
            self.tape_head = max(0, self.tape_head - 1)
        if self.tape_head >= len(self.array):
            self.expand_capacity()

    def configuration(self, state):
        configuration_array = self.array[:self.tape_head] + [state.label] + self.array[self.tape_head:]
        configuration = ""
        for symbol in configuration_array:
            configuration += symbol + " "
        return configuration.strip()

    def __str__(self):
        return " ".join(self.array)

if __name__ == "__main__":

    q_0 = State("q_0", is_start=True)
    q_1 = State("q_1")
    q_2 = State("q_2")
    q_3 = State("q_3")
    q_4 = State("q_4")
    q_5 = State("q_5")
    q_6 = State("q_6")
    q_7 = State("q_7")
    q_h = State("q_h", is_halt=True)

    Q = StateSetBuilder().addAll(
        q_0,
        q_1,
        q_2,
        q_3,
        q_4,
        q_5,
        q_6,
        q_7,
        q_h
    ).build()

    deltaBuilder = TransitionFunctionBuilder(Q)
    deltaBuilder.add(q_0, "a", q_1, "\\dot a", "R")
    deltaBuilder.add(q_1, "a", q_1, "a", "R")
    deltaBuilder.add(q_1, "b", q_1, "b", "R")
    deltaBuilder.add(q_1, "\\#", q_2, "\\#", "R")
    deltaBuilder.add(q_2, "a", q_2, "a", "R")
    deltaBuilder.add(q_2, "b", q_2, "b", "R")
    deltaBuilder.add(q_2, "\\varspace", q_5, "a", "L")
    deltaBuilder.add(q_0, "b", q_3, "\\dot b", "R")
    deltaBuilder.add(q_3, "a", q_3, "a", "R")
    deltaBuilder.add(q_3, "a", q_3, "a", "R")
    deltaBuilder.add(q_3, "\#", q_4, "\#", "R")
    deltaBuilder.add(q_4, "a", q_4, "a", "R")
    deltaBuilder.add(q_4, "b", q_4, "b", "R")
    deltaBuilder.add(q_4, "\\varspace", q_5, "b", "L")
    deltaBuilder.add(q_5, "a", q_5, "a", "L")
    deltaBuilder.add(q_5, "b", q_5, "b", "L")
    deltaBuilder.add(q_5, "\\#", q_6, "\\#", "L")
    deltaBuilder.add(q_6, "a", q_6, "a", "L")
    deltaBuilder.add(q_6, "b", q_6, "b", "L")
    deltaBuilder.add(q_6, "\\dot a", q_0, "\\dot a", "R")
    deltaBuilder.add(q_6, "\\dot b", q_0, "\\dot b", "R")
    deltaBuilder.add(q_0, "\\#", q_7, "\\#", "L")
    deltaBuilder.add(q_7, "\\dot a", q_7, "a", "L")
    deltaBuilder.add(q_7, "\\dot b", q_7, "b", "L")
    deltaBuilder.add(q_7, "a", q_h, "a", "L")
    deltaBuilder.add(q_7, "b", q_h, "b", "L")
    delta = deltaBuilder.build()

    M = TuringMachine(Q, delta)

    tape = Tape("a b a \\#", empty_space="\\varspace")

    simulator = M.simulator(tape)
    while simulator.has_next():
        print(simulator.configuration() + " \\\\")
        simulator.next()

    print(simulator.configuration())

    # print(M(tape))
