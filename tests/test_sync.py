import unittest
import os
import shutil
from sync import copy_source_to_replica, check_replica, log

class TestFolderSync(unittest.TestCase):
    def setUp(self):
        # Create temporary directories for testing
        self.source_folder = 'test_source'
        self.replica_folder = 'test_replica'
        os.makedirs(self.source_folder, exist_ok=True)
        os.makedirs(self.replica_folder, exist_ok=True)

    def tearDown(self):
        # Clean up temporary directories after testing
        shutil.rmtree(self.source_folder)
        shutil.rmtree(self.replica_folder)

    def test_copy_source_to_replica(self):
        # Test copying files from source to replica folder
        # Create a test file in the source folder
        test_file_path = os.path.join(self.source_folder, 'test.txt')
        with open(test_file_path, 'w') as f:
            f.write('Test content')
        # Call the function to be tested
        copy_source_to_replica(self.source_folder, self.replica_folder, 'test_log.txt')
        # Check if the file is copied to the replica folder
        replica_test_file_path = os.path.join(self.replica_folder, 'test.txt')
        self.assertTrue(os.path.exists(replica_test_file_path))

    def test_check_replica(self):
        # Test checking for mismatched files in replica folder
        # Create a test file in the replica folder
        test_file_path = os.path.join(self.replica_folder, 'test.txt')
        with open(test_file_path, 'w') as f:
            f.write('Test content')
        # Call the function to be tested
        check_replica(self.source_folder, self.replica_folder, 'test_log.txt')
        # Check if the file is deleted from the replica folder
        self.assertFalse(os.path.exists(test_file_path))

    def test_log(self):
        # Test logging function
        # Call the logging function
        log_message = 'Test log message'
        log_file_path = 'test_log.txt'
        log(log_message, log_file_path)
        # Check if the log file exists and contains the log message
        self.assertTrue(os.path.exists(log_file_path))
        with open(log_file_path, 'r') as f:
            content = f.read()
        self.assertIn(log_message, content)

if __name__ == '__main__':
    unittest.main()
