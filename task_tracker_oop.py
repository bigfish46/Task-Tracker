from datetime import datetime, date
import json

class Task:
    default_date_format = "%Y-%m-%d"  # Class variable

    def __init__(self, name, due, done=False):
        self.name = name
        self.due = due if isinstance(due, date) else datetime.strptime(due, self.default_date_format).date()
        self.done = done

    def to_dict(self):
        return {
            "name": self.name,
            "due": self.due.strftime(self.default_date_format),
            "done": self.done
        }

    @classmethod
    def from_dict(cls, data):
        # Class method example:
        # - Receives class as cls
        # - Can access class variables (cls.default_date_format)
        # - Can create new instances of the class (cls())
        return cls(
            name=data["name"],
            due=datetime.strptime(data["due"], cls.default_date_format).date(),
            done=data["done"]
        )

    @classmethod
    def create_today(cls, name):
        # Another class method example:
        # - Creates a task due today
        # - Uses the class to create a new instance
        return cls(name=name, due=date.today())

    @staticmethod
    def is_valid_date_format(date_string):
        # Static method example:
        # - Doesn't receive class or instance
        # - Utility function that doesn't need class state
        # - Could exist outside the class, but logically related
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def calculate_days_between(date1, date2):
        # Another static method example:
        # - Pure utility function
        # - Doesn't need class or instance state
        return (date2 - date1).days

    def __lt__(self, other):
        return self.due < other.due

class TaskManager:
    def __init__(self, filename):
        self.filename = filename
        self.tasks = self.load_tasks()

    def validate_date(self, date_str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return None

    def load_tasks(self):
        try:
            with open(self.filename, "r") as file:
                tasks_data = json.load(file)
                return [Task.from_dict(task_data) for task_data in tasks_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self):
        tasks_to_save = [task.to_dict() for task in self.tasks]
        with open(self.filename, "w") as file:
            json.dump(tasks_to_save, file, indent=2)

    def sort_tasks(self):
        return sorted(self.tasks)

    def show_tasks(self):
        if not self.tasks:
            print("No tasks yet.")
        else:
            print("\nTasks:")
            print("-" * 60)
            sorted_tasks = self.sort_tasks()
            for idx, task in enumerate(sorted_tasks, 1):
                days_left = (task.due - date.today()).days
                status = "Overdue!" if days_left < 0 and not task.done else f"{days_left} days left"
                
                completion_mark = "✓" if task.done else " "
                
                if task.done:
                    status = "Completed"
                    
                print(f"{idx}. [{completion_mark}] {task.name} (Due: {task.due.strftime('%Y-%m-%d')}) - {status}")
            print("-" * 60)

    def add_task(self, name, due):
        task = Task(name, due)
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, idx):
        if 0 <= idx < len(self.tasks):
            removed_task = self.tasks.pop(idx)
            self.save_tasks()
            return removed_task
        return None

    def mark_complete(self, idx):
        if 0 <= idx < len(self.tasks):
            self.tasks[idx].done = True
            self.save_tasks()
            return True
        return False

def main():
    manager = TaskManager("tasks.txt")

    while True:
        print("\n[1] Show tasks\n[2] Add task\n[3] Remove task\n[4] Mark complete\n[5] Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            manager.show_tasks()
        elif choice == "2":
            name = input("Enter task: ")
            due = input("Enter due date (YYYY-MM-DD): ")
            manager.add_task(name, due)
        elif choice == "3":
            manager.show_tasks()
            try:
                idx = int(input("Enter task number to remove: ")) - 1
                removed_task = manager.remove_task(idx)
                if removed_task:
                    print(f"Removed: {removed_task.name}")
                else:
                    print("Invalid number.")
            except ValueError:
                print("Please enter a valid number.")
        elif choice == "4":
            manager.show_tasks()
            try:
                idx = int(input("Enter task number to mark complete: ")) - 1
                if manager.mark_complete(idx):
                    pass
                else:
                    print("Invalid number.")
            except ValueError:
                print("Please enter a valid number.")
        elif choice == "5":
            break

if __name__ == "__main__":
    main() 