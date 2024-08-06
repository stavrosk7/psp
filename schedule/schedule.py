from datetime import datetime

# Helper function to parse date strings
def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")

# Function to assign tasks to employees based on the given criteria
def assign_tasks(employees, tasks):
    # Convert tasks to a more manageable format
    task_dict = {task[1]: task for task in tasks}
    
    # Sort tasks by start date to handle predecessors
    tasks_sorted = sorted(tasks, key=lambda x: parse_date(x[3]))
    
    # Initialize assignments and availability
    assignments = {}
    availability = {emp[0]: None for emp in employees}
    
    # Function to check if all predecessor tasks are completed
    def predecessors_completed(task):
        if not task[5]:
            return True
        for pred in task[5].split(', '):
            if pred not in assignments:
                return False
        return True

    total_cost = 0
    project_start_date = None
    project_end_date = None

    # Assign tasks
    for task in tasks_sorted:
        task_id, task_name, task_position, task_start, task_end, task_predecessors = task
        task_start_date = parse_date(task_start)
        task_end_date = parse_date(task_end)
        task_duration = (task_end_date - task_start_date).days + 1

        if project_start_date is None or task_start_date < project_start_date:
            project_start_date = task_start_date
        if project_end_date is None or task_end_date > project_end_date:
            project_end_date = task_end_date
        
        if not predecessors_completed(task):
            continue
        
        # Find the best employee for the task
        best_employee = None
        best_cost = float('inf')
        
        for emp in employees:
            emp_id, emp_name, emp_position, emp_salary = emp
            if emp_position != task_position:
                continue
            if availability[emp_id] and availability[emp_id] > task_start_date:
                continue
            task_cost = task_duration * emp_salary
            if task_cost < best_cost:
                best_employee = emp
                best_cost = task_cost
        
        if best_employee:
            assignments[task_name] = best_employee[1]
            availability[best_employee[0]] = task_end_date
            total_cost += best_cost

    project_duration = (project_end_date - project_start_date).days + 1
    return assignments, project_duration, total_cost



# Perform task assignments
# assignments, project_duration, total_cost = assign_tasks(employees, tasks)
# print(f"Assignments: {assignments}")
# print(f"Project Duration: {project_duration} days")
# print(f"Total Project Cost: ${total_cost:.2f}")