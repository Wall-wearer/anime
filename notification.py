import os


def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))


title = "This is a title"
body = "This is the body"
notify(title, body)
