import unittest
import os
import json
from datetime import datetime, date
from task_tracker_oop import Task, TaskManager

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_tasks.json"
        self.manager = TaskManager(self.test_file)

        # Clear existing test tasks
        self.manager.tasks = []
        self.manager.save_tasks()

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_task(self):
        task = Task("Test Task", "2025-05-20")
        self.manager.tasks.append(task)
        self.manager.save_tasks()

        self.manager.tasks = []  # clear to test loading
        self.manager.tasks = self.manager.load_tasks()
        self.assertEqual(len(self.manager.tasks), 1)
        self.assertEqual(self.manager.tasks[0].name, "Test Task")
        self.assertEqual(self.manager.tasks[0].due, date(2025, 5, 20))

    def test_mark_complete(self):
        task = Task("Incomplete Task", "2025-05-20", False)
        self.manager.tasks.append(task)
        self.manager.mark_complete(0)  # Using the manager's method instead of direct modification

        self.manager.tasks = self.manager.load_tasks()
        self.assertTrue(self.manager.tasks[0].done)

    def test_remove_task(self):
        task1 = Task("Task 1", "2025-05-20")
        task2 = Task("Task 2", "2025-05-21")
        self.manager.tasks = [task1, task2]
        self.manager.save_tasks()

        removed_task = self.manager.remove_task(0)  # Using the manager's method
        self.manager.tasks = self.manager.load_tasks()

        self.assertEqual(len(self.manager.tasks), 1)
        self.assertEqual(self.manager.tasks[0].name, "Task 2")
        self.assertEqual(removed_task.name, "Task 1")

    def test_serialization_to_dict(self):
        task = Task("Serialize Test", "2025-05-22", True)
        task_dict = task.to_dict()
        expected = {"name": "Serialize Test", "due": "2025-05-22", "done": True}
        self.assertEqual(task_dict, expected)

    def test_from_dict(self):
        data = {"name": "Deserialize Test", "due": "2025-05-23", "done": False}
        task = Task.from_dict(data)
        self.assertEqual(task.name, "Deserialize Test")
        self.assertEqual(task.due, date(2025, 5, 23))  # Compare with date object
        self.assertFalse(task.done)

    def test_sort_tasks(self):
        # Test that tasks are properly sorted by due date
        task1 = Task("Later Task", "2025-05-20")
        task2 = Task("Earlier Task", "2025-05-19")
        self.manager.tasks = [task1, task2]
        
        sorted_tasks = self.manager.sort_tasks()
        self.assertEqual(sorted_tasks[0].name, "Earlier Task")
        self.assertEqual(sorted_tasks[1].name, "Later Task")

    def test_invalid_date_format(self):
        # Test the static method for date validation
        self.assertTrue(Task.is_valid_date_format("2025-05-20"))
        self.assertFalse(Task.is_valid_date_format("05-20-2025"))
        self.assertFalse(Task.is_valid_date_format("invalid"))

if __name__ == "__main__":
    unittest.main() 