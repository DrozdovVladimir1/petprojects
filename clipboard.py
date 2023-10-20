import sys
import pyperclip
import json
SAVED_DATA = "clipboard.json"
def load_data(filepath):
    try:
        with open(filepath, "r") as f:
            database = json.load(f)
            return database
    except:
        return {}
def save_data(filepath, db):
    with open(filepath, "w") as f:
        json.dump(db, f)



database = load_data(SAVED_DATA)

if len(sys.argv) == 2:
    command =  sys.argv[1]
    if command == 'save':
        key = input('Please enter the key:')
        if key not in database:
            database[key] = pyperclip.paste()
            print('Success.')
        else:
            print(f"Key is already in clipboard. \n {key}->{database[key]}\n Do you want to override it?")
            ans = input("Y/N: ")
            if ans == 'Y' or ans =='YES':
                database[key] = pyperclip.paste()
    elif command == 'load':
        key = input('Please enter the key: ')
        if key not in database:
            print('Key does not exist in clipboard')
        else:
            pyperclip.copy(database[key])
            print(f'Success')
    elif command == 'delete':
        key = input("Please enter the key you want to delete: ")
        if key not in database:
            print('Key does not exist in clipboard')
        else:
            del database[key]
            print("Success")
    elif command == 'all':
        for key in database:
            print(f"{key}->{database[key]}")
    elif command == 'terminate':
        ans = input("Are you sure you want to delete the clipboard? Y/N:")
        if ans == 'Y' or ans.lower()=='YES':
            database = {}
            print('Clipboard deleted successfully.')
else:
    print('Please enter exactly one command')
save_data(SAVED_DATA, database)


#hgjdofgd