import argparse
import subprocess
import datetime
import os
import shutil

def log_activity(message):
    """Logs a message with a timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def get_backup_path(backup_dir, db_name):
    """Generates a timestamped backup file path."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(backup_dir, f"{db_name}_{timestamp}.gz")

def backup_db(db_name, host, port, output_dir):
    """Backs up a MongoDB database using mongodump."""
    log_activity(f"Starting backup for database '{db_name}'...")
    
    # Create the backup directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    backup_path = get_backup_path(output_dir, db_name)
    
    # Construct the mongodump command
    command = [
        "mongodump",
        f"--host={host}",
        f"--port={port}",
        f"--db={db_name}",
        f"--archive={backup_path}",
        "--gzip"
    ]
    
    try:
        start_time = datetime.datetime.now()
        subprocess.run(command, check=True, capture_output=True, text=True)
        end_time = datetime.datetime.now()
        duration = end_time - start_time
        log_activity(f"Backup completed successfully for '{db_name}'! 🚀")
        log_activity(f"File saved to: {backup_path}")
        log_activity(f"Time taken: {duration}")
    except subprocess.CalledProcessError as e:
        log_activity(f"Error during backup: {e.stderr}")
        log_activity("Backup failed. ❌")
        
def restore_db(db_name, host, port, backup_file):
    """Restores a MongoDB database from a backup file using mongorestore."""
    log_activity(f"Starting restore for database '{db_name}'...")
    
    if not os.path.exists(backup_file):
        log_activity(f"Error: Backup file not found at {backup_file}")
        return

    # Construct the mongorestore command
    command = [
        "mongorestore",
        f"--host={host}",
        f"--port={port}",
        f"--db={db_name}",
        f"--archive={backup_file}",
        "--gzip",
        "--drop"  # Use --drop to overwrite existing database
    ]
    
    try:
        start_time = datetime.datetime.now()
        subprocess.run(command, check=True, capture_output=True, text=True)
        end_time = datetime.datetime.now()
        duration = end_time - start_time
        log_activity(f"Restore completed successfully for '{db_name}'! ✨")
        log_activity(f"Time taken: {duration}")
    except subprocess.CalledProcessError as e:
        log_activity(f"Error during restore: {e.stderr}")
        log_activity("Restore failed. ❌")

def main():
    """Main function to parse command-line arguments and run the utility."""
    parser = argparse.ArgumentParser(description="MongoDB Backup and Restore Utility")
    
    # Top-level commands
    subparsers = parser.add_subparsers(dest='command', required=True, help='Action to perform')
    
    # Backup command
    backup_parser = subparsers.add_parser('backup', help='Backup a MongoDB database')
    backup_parser.add_argument('--db-name', required=True, help='Name of the database to backup')
    backup_parser.add_argument('--host', default='localhost', help='Database host')
    backup_parser.add_argument('--port', type=int, default=27017, help='Database port')
    backup_parser.add_argument('--output-dir', default='./backups', help='Directory to store the backup file')
    
    # Restore command
    restore_parser = subparsers.add_parser('restore', help='Restore a MongoDB database')
    restore_parser.add_argument('--db-name', required=True, help='Name of the target database for restoration')
    restore_parser.add_argument('--host', default='localhost', help='Database host')
    restore_parser.add_argument('--port', type=int, default=27017, help='Database port')
    restore_parser.add_argument('--backup-file', required=True, help='Path to the backup file (.gz archive)')
    
    args = parser.parse_args()
    
    if args.command == 'backup':
        backup_db(args.db_name, args.host, args.port, args.output_dir)
    elif args.command == 'restore':
        restore_db(args.db_name, args.host, args.port, args.backup_file)

if __name__ == "__main__":
    main()