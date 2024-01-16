import os


def create_reminder(title, body, list_name):
    script = f'''
        tell application "Reminders"
            set theList to list "{list_name}"
            set newReminder to make new reminder at end of reminders of theList
            set name of newReminder to "{title}"
            set body of newReminder to "{body}"
        end tell
    '''
    os.system(f"osascript -e '{script}'")


title = "Title"
body = "details"
list = "test_list"
create_reminder(title, body, list)
