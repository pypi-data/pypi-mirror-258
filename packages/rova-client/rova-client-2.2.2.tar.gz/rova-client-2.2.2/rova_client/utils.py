from datetime import datetime
from datetime import timedelta
from typing import List, Dict

class UniqueIDGenerator:
    def __init__(self):
        self.current = 0
        self.max_val = 2**32 - 1  # Maximum value for 32-bit unsigned integer

    def get_unique_id(self):
        if self.current >= self.max_val:
            raise Exception("Maximum limit of unique IDs reached.")
        self.current += 1
        return self.current

class DateTracker:
    def __init__(self):
        pass
    
    def get_timestamp(self):
        # Get the current date and time
        current_datetime = datetime.now()

        # Extract individual components from the current date and time
        year = current_datetime.year
        month = current_datetime.month
        day = current_datetime.day
        hour = current_datetime.hour
        minute = current_datetime.minute
        second = current_datetime.second

        # Create a new datetime object with the extracted components
        my_date = datetime(year, month, day, hour, minute, second)

        return my_date

class TraceTracker():
    def __init__(self):

        self.last_trace_ids = dict()
        self.trace_to_sessions = dict()
        self.generator = UniqueIDGenerator()
        self.last_event_type = ""

    def set_last_event_type(self, event_type):
      self.last_event_type = event_type

    def get_trace_id(self, user_id, session_id, src):
            
        if((user_id not in self.last_trace_ids) or (session_id not in self.trace_to_sessions.values()) or (self.last_event_type == 'product')):
            
            new_trace_id = self.generator.get_unique_id()
            self.last_trace_ids[user_id] = new_trace_id
            self.trace_to_sessions[new_trace_id] = session_id
            return new_trace_id

        elif(src == "llm" and (session_id in self.trace_to_sessions.values())):
            trace_id = self.last_trace_ids[user_id]
            return trace_id

        else:
            new_trace_id = self.generator.get_unique_id()
            self.last_trace_ids[user_id] = new_trace_id
            self.trace_to_sessions[new_trace_id] = session_id
            return new_trace_id

    
class SessionTracker:
    def __init__(self, timeout):
        self.last_times = dict()
        self.last_session_ids = dict()
        self.timeout = timedelta(seconds=timeout)
        self.generator = UniqueIDGenerator()
    
    def get_session_id(self, user_id, timestamp):
   
        if(user_id not in self.last_times):
            session_id = self.generator.get_unique_id()
            self.last_session_ids[user_id] = session_id
            self.last_times[user_id] = timestamp
            return session_id

        elif(timestamp - self.last_times[user_id] > self.timeout):

            self.last_times[user_id] = timestamp
            session_id = self.generator.get_unique_id()
            self.last_session_ids[user_id] = session_id

            return session_id
        else:
            return self.last_session_ids[user_id]

    
def simplify_dict(d):
    """Simplify the dictionary by merging 'properties' into the parent dictionary."""
    simplified = d.copy()  # Make a shallow copy to avoid modifying the original
    properties = simplified.pop('properties', {})  # Remove 'properties' and save its value
    simplified.update(properties)  # Merge properties into the simplified dict
    return simplified

def reverse_simplify_dict(d):
    """Reverse the simplification, nesting non-event_name keys under 'properties'."""
    # Extract the event_name and remove it from the original dict for a moment
    event_name = d.pop('event_name', None)
    event_type = d.pop('event_type', None)
    # The remaining items in the dictionary are the properties
    properties = d
    # Reconstruct the dictionary with properties nested
    return {'event_name': event_name, 'event_type':event_type, 'properties': properties}

def order_by(data):
    if('timestamp' in data[0]['properties']):
        sorted_data = sorted(data, key=lambda x: x['properties']["timestamp"])
    else:
        sorted_data = data
    return sorted_data
