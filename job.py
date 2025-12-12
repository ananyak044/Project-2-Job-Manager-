#parent class
class Job:

    #constructor
    def __init__(self, name, category, rate, date, hours):
        #check if the value or rate and hours is positive
        if (rate<=0):
            message = "invalid rate" 
            raise ValueError(message)
        elif (hours<=0) or (hours>6):
            message = "invalid hours"
            raise ValueError(message)

        self.name = name
        self.category = category
        self.rate = rate
        self.date = date
        self.hours = hours

        #Method definition
    def get_name(self):
        return self.name

    def get_category(self):
        return self.category

    def get_rate(self):
        return self.rate

    def get_date(self):
        return self.date

    def get_hours(self):
        return self.hours

    #checks if two objects are equal
    def __eq__(self, other):
        if not isinstance(other, Job):
            return False

        if (self.name==other.name) and (self.category==other.category) and (self.rate==other.rate) and (self.date==other.date) and (self.hours==other.hours):
            return True
        else:
            return False

    #returns hash value
    def __hash__(self):
        return hash((self.name, self.category, self.rate, self.date, self.hours))

    #returns the object
    def __str__(self):
        return f'Job("{self.name}", "{self.category}", {self.rate}, "{self.date}", {self.hours})'

    def __repr__(self):
        return f'Job("{self.name}", "{self.category}", {self.rate}, "{self.date}", {self.hours})'
