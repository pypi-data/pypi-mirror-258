class Manager(Employee):
    raiseAmt = 1.10

    def __init__(self, first: str, last: str, salary: int, emps: list = None):
        self.first = first
        self.last = last
        self.salary = salary
        self.email = f'{first.lower()}.{last.lower()}@company.com'
        self.className = self.__class__.__name__
        if emps is None:
            self.emps = []
        else:
            self.emps = emps

    def get_employees(self, rType):
        if rType.lower() == 's':
            employees = ''
            for emp in self.emps:
                employees += f'{emp}\n'
            return employees
        elif rType.lower() == 'l':
            return self.emps
        else:
            return 'Must specify a valid return type for employees (String = S, List = L'

    def add_employee(self, emp):
        if emp not in self.emps:
            self.emps.append(emp.title())

    def remove_employee(self, emp):
        if emp in self.emps:
            self.emps.remove(emp)

    def __repr__(self):
        employees = ''
        for emp in self.emps:
            employees += f'--> {emp}\n'
        return f'Manager\n-------\nName: {self.first} {self.last}\nEmail: {self.email}\nSalary: {self.salary}\n\nEmployees:\n{employees}'
