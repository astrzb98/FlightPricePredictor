

class Flights:
    def __init__(self, fly_from, fly_to, date_from, date_to):
        self.fly_from = fly_from
        self.fly_to = fly_to
        self.date_from = date_from
        self.date_to = date_to

    def get_fly_from(self):
        return self.fly_from

    def get_fly_to(self):
        return self.fly_to

    def get_date_from(self):
        return self.date_from

    def get_date_to(self):
        return self.date_to

    def set_fly_from(self, fly_from):
        self.fly_from = fly_from

    def set_fly_to(self, fly_to):
        self.fly_to = fly_to

    def set_date_from(self, date_from):
        self.date_from = date_from

    def set_date_to(self, date_to):
        self.date_to = date_to
