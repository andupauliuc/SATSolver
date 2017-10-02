class Statistic:
    def __init__(self, seconds, level, variables, used, original, conflicts, learned, limit,
                 agility, MB):
        self.MB = MB
        self.agility = agility
        self.limit = limit
        self.learned = learned
        self.conflicts = conflicts
        self.used = used
        self.original = original
        self.variables = variables
        self.level = level
        self.seconds = seconds

    def __str__(self):
        return "[" + \
               self.seconds + ", " + \
               self.level + ", " + \
               self.variables + ", " + \
               self.used + ", " + \
               self.original + ", " + \
               self.conflicts + ", " + \
               self.learned + ", " + \
               self.limit + ", " + \
               self.agility + ", " + \
               self.MB + ", " + \
               "]"
