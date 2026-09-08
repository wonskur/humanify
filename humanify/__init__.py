class Human:
    def __init__(self, name, gender, race, birth_date):
        self.__name = name
        self.__gender = gender
        self.__race = race
        self.__birth_date = birth_date
        self.__position = [0, 0, 0]
        self.__is_alive = True
        self.__death_reason = None
        self.__health = 100
        self.__energy = 100
        self.__hunger = 0
        self.__thirst = 0
        self.__breath_state = "idle"
        self.__oxygen_level = 98
        self.__age = 0
        self.__time_alive = 0
    
    def live(self, seconds):
        if not self.__is_alive:
            return
        
        self.__time_alive += seconds
        self.__update_vitals(seconds)
        self.__check_death()
    
    def inhale(self):
        if not self.__is_alive:
            return f"{self.__name} is dead, reason: {self.__death_reason}"
        
        if self.__breath_state == "hold":
            self.__breath_state = "inhale"
            self.__oxygen_level = min(100, self.__oxygen_level + 2)
        elif self.__breath_state != "inhale":
            self.__breath_state = "inhale"
            self.__oxygen_level = min(100, self.__oxygen_level + 1)
    
    def exhale(self):
        if not self.__is_alive:
            return f"{self.__name} is dead, reason: {self.__death_reason}"
        
        if self.__breath_state == "hold":
            self.__breath_state = "exhale"
            self.__oxygen_level = max(0, self.__oxygen_level - 1)
        elif self.__breath_state != "exhale":
            self.__breath_state = "exhale"
            self.__oxygen_level = max(0, self.__oxygen_level - 2)
    
    def hold_breath(self, seconds):
        if not self.__is_alive:
            return f"{self.__name} is dead, reason: {self.__death_reason}"
        
        self.__breath_state = "hold"
        for _ in range(seconds):
            self.__oxygen_level = max(0, self.__oxygen_level - 3)
            if self.__oxygen_level <= 0:
                self.die("suffocation")
                break
    
    def move_forward(self, steps):
        if not self.__is_alive:
            return
        if self.__energy < steps * 2:
            return "Too tired to move"
        
        self.__position[0] += steps
        self.__energy = max(0, self.__energy - steps * 2)
    
    def move_backward(self, steps):
        if not self.__is_alive:
            return
        if self.__energy < steps * 2:
            return "Too tired to move"
        
        self.__position[0] -= steps
        self.__energy = max(0, self.__energy - steps * 2)
    
    def eat(self, amount):
        if not self.__is_alive:
            return
        
        self.__hunger = max(0, self.__hunger - amount)
        self.__energy = min(100, self.__energy + amount // 2)
    
    def run(self, steps):
        if not self.__is_alive:
            return
        if self.__energy < steps * 4:
            return "Too tired to run"
    
        self.__position[0] += steps * 2
        self.__energy = max(0, self.__energy - steps * 4)
        self.__thirst = min(100, self.__thirst + steps * 0.1)
    
    def drink(self, amount):
        if not self.__is_alive:
            return
        self.__thirst = max(0, self.__thirst - amount)
        if self.__thirst == 0 and amount > 20:
            self.__health = max(0, self.__health - (amount - 20) * 0.1)
    
    def sleep(self, hours):
        if not self.__is_alive:
            return
        
        energy_restore = hours * 10
        self.__energy = min(100, self.__energy + energy_restore)
    
    def take_damage(self, amount):
        if not self.__is_alive:
            return
        
        self.__health = max(0, self.__health - amount)
        if self.__health <= 0:
            self.die("health dropped to zero")
    
    def heal(self, amount):
        if not self.__is_alive:
            return
        
        self.__health = min(100, self.__health + amount)
    
    def die(self, reason):
        if self.__is_alive:
            self.__is_alive = False
            self.__death_reason = reason
    
    def is_alive(self):
        return self.__is_alive
    
    def get_health(self):
        return self.__health
    
    def get_energy(self):
        return self.__energy
    
    def get_position(self):
        return self.__position.copy()
    
    def get_oxygen(self):
        return self.__oxygen_level
    
    def get_status(self):
        if not self.__is_alive:
            return f"{self.__name} is dead, reason: {self.__death_reason}"
        
        return {
            "name": self.__name,
            "health": self.__health,
            "energy": self.__energy,
            "hunger": self.__hunger,
            "thirst": self.__thirst,
            "oxygen": self.__oxygen_level,
            "position": self.__position.copy(),
            "breath_state": self.__breath_state
        }
    
    def get_age(self):
        return self.__age
    
    def __update_vitals(self, seconds):
        self.__hunger = min(100, self.__hunger + seconds * 0.01)
        self.__thirst = min(100, self.__thirst + seconds * 0.015)
        self.__energy = max(0, self.__energy - seconds * 0.005)
        if self.__hunger > 80:
            self.__health = max(0, self.__health - seconds * 0.01)
        if self.__thirst > 80:
            self.__health = max(0, self.__health - seconds * 0.02)
        if self.__breath_state != "hold":
            if self.__oxygen_level < 95:
                self.__oxygen_level = min(100, self.__oxygen_level + 0.5)
            elif self.__oxygen_level > 98:
                self.__oxygen_level = max(0, self.__oxygen_level - 0.3)
    
    def __check_death(self):
        if self.__health <= 0:
            self.die("health reached zero")
        elif self.__oxygen_level <= 0:
            self.die("oxygen deprivation")
        elif self.__hunger >= 100:
            self.die("starvation")
        elif self.__thirst >= 100:
            self.die("dehydration")