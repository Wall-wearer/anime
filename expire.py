import datetime

# used to know when cookie Expiry.
timestamp = 1706412206
expiry_date = datetime.datetime.utcfromtimestamp(timestamp)

print("Expiry Date:", expiry_date)
