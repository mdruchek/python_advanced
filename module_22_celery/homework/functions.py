import csv
import os
from typing import List, Dict
from zipfile import ZipFile


def get_emails_from_csv(mailing_list_file) -> List:
    mailing_emails = []
    if os.path.isfile(mailing_list_file):
        with open(mailing_list_file, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                mailing_emails.append(row['email'])
    return mailing_emails


def adding_data_to_csv(mailing_list_file, user_data: Dict[str, str]):
    mailing_list_file_exists: bool = False
    if os.path.isfile(mailing_list_file):
        mailing_list_file_exists = True

    with open(mailing_list_file, 'a', newline='') as csvfile:
        fieldnames = ['username', 'email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not mailing_list_file_exists:
            writer.writeheader()
        writer.writerow({'username': user_data.get('username'), 'email': user_data.get('email')})
    return True


def deleting_data_from_csv(mailing_list_file, email: str):
    mailings_data = []
    email_exists_in_mailing_list = False
    if os.path.isfile(mailing_list_file):
        with open(mailing_list_file, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if email == row['email']:
                    email_exists_in_mailing_list = True

                else:
                    mailings_data.append(row)

        with open(mailing_list_file, 'w', newline='') as csvfile:
            fieldnames = ['username', 'email']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for user_data in mailings_data:
                writer.writerow({'username': user_data.get('username'), 'email': user_data.get('email')})
        if email_exists_in_mailing_list:
            return True
        return False


def archiving_files(files: List, task_id: str):
    arch_name = f'{task_id}.zip'
    with ZipFile(file=arch_name, mode='w') as arch:
        for file in files:
            arch.write(file)
            os.remove(file)
    return arch_name
