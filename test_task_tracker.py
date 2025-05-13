import unittest
import os
from datetime import date
from task_tracker import load_tasks, save_tasks

class TestTaskTracker(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_tasks.txt"
        self.sample_tasks = [
            {
                "description": "Task 1",
                "due_date": date(2024, 12, 31),
                "completed": False
            },
            {
                "description": "Task 2",
                "due_date": date(2024, 12, 31),
                "completed": True
            }
        ]

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_and_load_tasks(self):
        save_tasks(self.test_file, self.sample_tasks)
        loaded = load_tasks(self.test_file)
        self.assertEqual(len(loaded), len(self.sample_tasks))
        for saved, loaded_task in zip(self.sample_tasks, loaded):
            self.assertEqual(saved["description"], loaded_task["description"])
            self.assertEqual(saved["due_date"], loaded_task["due_date"])
            self.assertEqual(saved["completed"], loaded_task["completed"])

    def test_load_tasks_file_not_found(self):
        # Make sure the file doesn't exist
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        loaded = load_tasks(self.test_file)
        self.assertEqual(loaded, [])

if __name__ == "__main__":
    unittest.main() 