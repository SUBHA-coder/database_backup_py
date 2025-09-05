MongoDB Backup and Restore Utility
A simple yet robust Python command-line utility for managing MongoDB database backups and restoration using the official mongodump and mongorestore tools.

Features
Backup: Easily create a gzipped archive of a MongoDB database. Each backup file is automatically timestamped for easy organization.

Restore: Restore a database from a gzipped archive. The --drop flag is used during restoration to ensure the target database is a clean copy of the backup.

Logging: Provides real-time, timestamped logs for all activities, including success and failure messages.

Simple Interface: Uses Python's argparse module to provide a clear and user-friendly command-line interface.

Prerequisites
To use this script, you must have the following installed:

Python 3.x

MongoDB Database Tools: This package includes the mongodump and mongorestore command-line utilities. These must be installed and accessible from your system's PATH. You can download them from the official MongoDB website.

How to Use
The script uses two main sub-commands: backup and restore.

1. Backup a Database
This command backs up a specified database to a gzipped archive file in the provided output directory. The file name will be automatically generated with a timestamp in the format database_name_YYYYMMDD_HHMMSS.gz.

Syntax:

python your_script_name.py backup --db-name <database_name> [options]

Example:

To back up the database named mydb and save the file to a ./backups directory.

python mongo_utility.py backup --db-name mydb --output-dir ./backups

Arguments:

--db-name (Required): The name of the MongoDB database to back up.

--host (Optional): The database host. Defaults to localhost.

--port (Optional): The database port. Defaults to 27017.

--output-dir (Optional): The directory to store the backup file. Defaults to ./backups.

2. Restore a Database
This command restores a database from a previously created backup file. It will drop all existing collections in the target database before restoring the data.

Syntax:

python your_script_name.py restore --db-name <target_db_name> --backup-file <path_to_backup_file> [options]

Example:

To restore the database named mydb from a specific backup file.

python mongo_utility.py restore --db-name mydb --backup-file ./backups/mydb_20240906_123456.gz

Arguments:

--db-name (Required): The name of the target database where the data will be restored.

--backup-file (Required): The full path to the .gz backup archive file.

--host (Optional): The database host. Defaults to localhost.

--port (Optional): The database port. Defaults to 27017.
