class Settings:
    """"A class that stores all settings for Alien Invasion"""

    def __init__(self):
        """Initialises games settings"""
        #Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (230,230,230)
        # Determine ship's settings
        self.ship_limit = 3
        # Bullet settings:
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_colour = (60,60,60)
        self.bullets_allowed = 10
        #Alien settings
        self.fleet_drop_speed = 10

        #How quickly the alien point values increase
        self.score_scale = 1.5
    
        #How quickly the game speeds up
        self.speedup_scale = 1.1
        self.speedup_scale_1 = 1.5
        self.speedup_scale_2 = 2.0

        self.initialise_dynamic_settings()

        self.difficulty = "medium"

    def initialise_dynamic_settings(self):
        """Initialise settings that change throughout the game"""
        self.ship_speed = 1.5
        self.alien_speed = 1.0
        self.bullet_speed = 5
        
        #Scoring settings
        self.alien_points = 50

        #fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings and alien point values"""
        if self.difficulty == "easy":
            self.ship_speed *= self.speedup_scale
            self.bullet_speed *= self.speedup_scale
            self.alien_speed *= self.speedup_scale

        if self.difficulty == "medium":
            """Increase speed settings for medium difficulty"""
            self.ship_speed *= self.speedup_scale_1
            self.bullet_speed *= self.speedup_scale_1
            self.alien_speed *= self.speedup_scale_1

        if self.difficulty == "hard":
            """Increase speed settings for hard difficulty"""
            self.ship_speed *= self.speedup_scale_2
            self.bullet_speed *= self.speedup_scale_2
            self.alien_speed *= self.speedup_scale_2
        
        self.alien_points = int(self.alien_points * self.score_scale)
