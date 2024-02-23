# _Learning about Python Classes_
# Employee System

## Classes:

**Employee**
* Must pass in First Name (str), Last Name (str), Salary (int)
* When printed, outputs all of its information
* When casted into a string, the salary is used
* Has a 'Raise Amount' of 5%
* Can be added to the employee's salary by using the .apply_raise() method
*  * Can be directly modified by assigning an integer value to the class variable
* * Ex: x.raiseAmt = 2  <--Directly modifies the class variable, applying it to all instances

**Manager**
* Must pass in First Name (str), Last Name (str), Salary (int), and the employees under their management (list)
* When printed, outputs all of its information
* When casted into a string, the salary is used
* Has a 'Raise Amount' of 10%
* * Can be added to the employee's salary by using the .apply_raise() method
* Employees under the manager's management can be added
* * Use the .add_employee() method
* Employees under the manager's management can be removed
* * Use the .remove_employee() method
* Check if it is a workday by using the is_workday(int) method
* * Day of the week as an integer must be passed in where 1 = Monday and 7 = Sunday