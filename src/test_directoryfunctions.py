import os
import shutil
import unittest
from static_site_generator.src.directory_functions import copy_directory_recursive


class TestCopyDirectoryRecursive(unittest.TestCase):
    def setUp(self):
        self.src = "test_src"
        self.dest = "test_dest"
        os.makedirs(self.src, exist_ok=True)
        with open(os.path.join(self.src, "file1.txt"), "w") as f:
            f.write("This is a test file.")
        os.makedirs(os.path.join(self.src, "subdir"), exist_ok=True)
        with open(os.path.join(self.src, "subdir", "file2.txt"), "w") as f:
            f.write("This is another test file.")

    def tearDown(self):
        shutil.rmtree(self.src, ignore_errors=True)
        shutil.rmtree(self.dest, ignore_errors=True)


    def test_copy_directory_recursive(self):
        copy_directory_recursive(self.src, self.dest)

        self.assertTrue(os.path.exists(self.dest))
        self.assertTrue(os.path.isfile(os.path.join(self.dest, "file1.txt")))
        self.assertTrue(os.path.isfile(os.path.join(self.dest, "subdir", "file2.txt")))

if __name__ == "__main__":
    unittest.main()