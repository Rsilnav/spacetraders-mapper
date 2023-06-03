import time

from fetch import fetch_systems
from fetch import get_starting_systems
from viewer import view_surrounding

while True:
    success = fetch_systems()
    if success:
        print("AVAILABLE!")
        break
    print("Not yet available")
    time.sleep(10)

for symbol, location in get_starting_systems():
    view_surrounding(symbol, location)
