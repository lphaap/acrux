from datetime import datetime;
import json

# Log given msg, persist param saves log
def log( msg: str, persistent: bool = False) -> None:
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S");
    try:
        print(timestamp + ": ", msg);
    except:
        print(timestamp + ": Log error");
