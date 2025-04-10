class LFSR:
    def __init__(self,  register_size, state, taps):
        self.register_size = register_size
        if len(state) != register_size:
            raise ValueError("State length must match register size.")
        self.state = state
        self.taps = taps
        

        # store initial values for reset
        self.initial_register_size = register_size
        self.initial_state = state
        self.initial_taps = taps

    def reset(self):
        self.state = self.initial_state
        self.register_size = self.initial_register_size
        self.taps = self.initial_taps
        print(f'Reset\t: State\t:{self.get_state()}')

    def step(self, step):
        # take last bit of state as output
        output = self.state[-1]
        
        # XOR the first and last bits of the state
        xor = self.state[self.taps[0]] ^ self.state[self.taps[1]]  

        # shift the state to the right and insert the XOR result at the beginning
        self.state = [xor] + self.state[:-1]
        print(f'Step\t: {step+1}\tState\t:{self.get_state()}\tOutput: {output}')
        return output

    def run(self, steps):
        print(f'Step\t: 0\tState\t:{self.get_state()}')
        return [self.step(step) for step in range(steps)]

    def get_register_size(self):
        return self.register_size
    
    def set_register_size(self, new_size):
        if new_size < 2:
            raise ValueError("Register size must be at least 2.")
        self.register_size = new_size
        if len(self.state) > new_size:
            self.state = self.state[:new_size]
        elif len(self.state) < new_size:
            self.state += [0] * (new_size - len(self.state))
    
    def get_taps(self):
        return self.taps
    
    def set_taps(self, new_taps):
        if len(new_taps) != 2:
            raise ValueError("Taps must be a list of two indices.")
        for t in new_taps:
            if t < 0 or t >= self.register_size:
                raise ValueError("Tap index out of bounds.")
        self.taps = new_taps

    def get_state(self):
        return self.state
    
    def set_state(self, new_state):
        if len(new_state) != self.register_size:
            raise ValueError("State length must match register size.")
        self.state = new_state