class Employee:
    raiseAmt = 1.05

    def __init__(self, first: str, last: str, salary: int):
        self.first = first
        self.last = last
        self.salary = salary
        self.email = f'{first.lower()}.{last.lower()}@company.com'
        self.className = self.__class__.__name__

    def __repr__(self):
        return f'Employee\n--------\nName: {self.first} {self.last}\nEmail: {self.email}\nSalary: {self.salary}'

    def apply_raise(self):
        self.salary = int(self.salary * self.raiseAmt)

    def __int__(self):
        return self.salary

    def worker_type(self):
        return self.className

    def is_workday(self, weekday: int):
        if int(weekday) == weekday:
            if weekday == 6 or weekday == 7:
                return 'It is not a workday'
            else:
                return 'It is a workday'
        else:
            return 'Input a number as weekday. 1 = Monday, 7 = Sunday'