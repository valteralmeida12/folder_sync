import argparse
import os
import shutil
import time

# Global variables to store deleted and created items
deleted_items = set()
created_items = set()

# Copy content from the source to the replica floder
def copy_source_to_replica(source_folder, replica_folder, log_file):
    # Check if replica folder exists or not
    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)

    # Copy all the directories from the source folder to the replica folder
    for root, dirs, files in os.walk(source_folder):
        for directory in dirs:
            # Source directory path
            source_directory_path = os.path.join(root, directory)
            # replica directory path
            replica_directory_path = os.path.join(replica_folder, os.path.relpath(source_directory_path, source_folder)) 
            
            try:
                # Create any none existing directories in the replica folder
                if not os.path.exists(replica_directory_path):
                    os.makedirs(replica_directory_path)
                    # Create timestamp
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

                    # Format log messages
                    log_create_message = f"{timestamp} - Created directory {source_directory_path}"
                    log_copy_message = f"{timestamp} - Copied {source_directory_path} to {replica_directory_path}"

                    # Logging
                    log(log_create_message, log_file)
                    log(log_copy_message, log_file)

                    # Add directory to created items
                    created_items.add(replica_directory_path)

            except PermissionError as e:
                    print(f"PermissionError: {e}")

        for file in files:
            # File in root directory
            source_file_path = os.path.join(root, file)
            # replica file in replica directory
            replica_file_path = os.path.join(replica_folder, os.path.relpath(source_file_path, source_folder))
            
            try:
                # Check if source files doesn't exist or if it has been modified
                if not os.path.exists(replica_file_path) or os.path.getmtime(source_file_path) > os.path.getmtime(replica_file_path):
                    shutil.copy2(source_file_path,replica_file_path)
                    # Create timestamp
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Format log message
                    log_create_message = f"{timestamp} - Created {source_file_path}"
                    log_copy_message = f"{timestamp} - Copied {source_file_path} to {replica_file_path}"

                    # Logging
                    log(log_create_message, log_file)
                    log(log_copy_message, log_file)
                    
                    # Add file to created items
                    created_items.add(replica_file_path)

            except (PermissionError, FileNotFoundError) as e:
                print(f"PermissionError or FileNotFoundError: {e}")


# Clear any mismatched content form the replica folder
def check_replica(source_folder, replica_folder, log_file):
    # Check if replica folder exists or not
    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)
    
    # Iterate over the directories in the replica folder
    for root, dirs, files in os.walk(replica_folder):
        for file in files:
            # replica file path
            replica_file_path = os.path.join(root, file)
            # Source file path
            source_file_path = os.path.join(source_folder, os.path.relpath(replica_file_path, replica_folder))
            
            try:
                # Log if any file from the source directory was deleted
                if not os.path.exists(source_file_path) and replica_file_path not in deleted_items:
                    # Remove file from replica folder
                    os.remove(replica_file_path)

                    # Create timestamp
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

                    # Format log message
                    log_message = f"{timestamp} - {source_file_path} file deleted!"
                    log(log_message, log_file)

                    # Add file to deleted items
                    deleted_items.add(replica_file_path)

            except (PermissionError, FileNotFoundError) as e:
                    print(f"PermissionError or FileNotFoundError: {e}")

        for directory in dirs:
            # replica directory path
            replica_directory_path = os.path.join(root, directory)
            # Source directory path
            source_directory_path = os.path.join(source_folder, os.path.relpath(replica_directory_path, replica_folder))
            
            try:
                # Log if any directory from the source directory was deleted
                if not os.path.exists(source_directory_path) and replica_directory_path not in deleted_items:
                    # Remove directory recursively
                    shutil.rmtree(replica_directory_path)

                    # Create timestamp
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

                    # Format log message
                    log_message = f"{timestamp} - {source_directory_path} directory was deleted!"
                    log(log_message, log_file)

                    # Add directory to deleted items
                    deleted_items.add(replica_directory_path)

            except PermissionError as e:
                print(f"PermissionError: {e}")
        
        # Cross-reference deleted and created items to remove re-created items from deleted items
        for item in created_items:
            if item in deleted_items:
                # Remove item from deleted items
                deleted_items.remove(item)

        # Clear the created items set
        created_items.clear()


# Logger    
def log(message, log_file):
    try:
        with open(log_file, 'a') as f:
            f.write(f"{message}\n")
    except (PermissionError, FileNotFoundError) as e:
        print(f"Error occurred while writing to log file: {e}")


def main():
    parser = argparse.ArgumentParser(description='Sync two folders periodically')
    parser.add_argument('source_folder', type=str, help='Path to the source folder')
    parser.add_argument('replica_folder', type=str, help='Path to the replica folder')
    parser.add_argument('log_file', type=str, help='Path to the log file')
    parser.add_argument('interval', type=int, help='Time interval for sync (in seconds)')
    args = parser.parse_args()

    while True:
        copy_source_to_replica(args.source_folder, args.replica_folder, args.log_file)
        check_replica(args.source_folder, args.replica_folder, args.log_file)
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
