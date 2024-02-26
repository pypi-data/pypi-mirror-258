import clickhouse_connect
import uuid
from rova_client.utils import SessionTracker, TraceTracker, DateTracker, simplify_dict, reverse_simplify_dict, order_by
from typing import List, Dict, Any
from itertools import chain
from datetime import datetime


class Rova:

    def __init__(self, auth: str, timeout: int = 1440):
        
        self.accounts = ['buster_dev', 'rova_dev', 'danswer_dev']

        if(not self.check_auth(auth)):
            raise Exception("Invalid key!")
        else:
            self.client = clickhouse_connect.get_client(host='tbbhwu2ql2.us-east-2.aws.clickhouse.cloud', port=8443, username='default', password='V8fBb2R_ZmW4i')
            template = 'USE {}'.format(auth)
            self.client.command(template)
            self.auth = auth
            #print("Key verified! You may begin using the client. ")

        self.product_cols = self.get_cols(auth, 'product')
        self.llm_cols = self.get_cols(auth, 'llm')

        # init clients
        self.session_client = SessionTracker(timeout)
        self.trace_client = TraceTracker()
        self.date_client = DateTracker()
        self.user_id = str(uuid.uuid4()) # not used if user_id is provided
    
    def get_cols(self, auth: str, table: str) -> set[Any]:
        sql = "DESCRIBE TABLE {}.{}".format(auth, table)
        cols = set([name[0] for name in self.client.query(sql).result_rows])
        return cols

    def check_auth(self, auth: str) -> bool:
        return (auth in self.accounts)

    def error_check(self, values: List[List[Any | None]], columns: List[str]) -> int:
        required_keys = {'event_name', 'event_type'}
        if(len(values) <= 0):
            raise ValueError("No data provided!")
        if not required_keys.issubset(columns):
            missing_keys = required_keys - set(columns)
            raise ValueError(f"Missing required data: {missing_keys}")
        return 0
    
    def format_to_rova(self, obj: Dict) -> tuple[Dict, int]:
        args = simplify_dict(obj)
    
        if('timestamp' not in args):
            args['timestamp'] = self.date_client.get_timestamp()
        elif(isinstance(args['timestamp'], str)):
            args['timestamp'] = datetime.strptime(args['timestamp'], "%Y-%m-%d %H:%M:%S")
        if('user_id' not in args or args['user_id'] is None):
            args['user_id'] = self.user_id
        args['session_id'] = self.session_client.get_session_id(args['user_id'], args['timestamp'])
        args['distinct_id'] = uuid.uuid4()
        if(args['event_type']=='llm'):
            args['trace_id'] = self.trace_client.get_trace_id(args['user_id'], args['session_id'], 'llm')
            self.trace_client.set_last_event_type('llm')
            return (args, 1)
        elif(args['event_type']=='product'):   
            self.trace_client.set_last_event_type('product')
            return (args, 0)
        else:
            # should never get here
            return (args, -1)
    
    def capture_handler(self, events_list: List[Dict], flag: int) -> int:

        column_names_set = set(chain.from_iterable(map(dict.keys, events_list)))
        target_set = self.llm_cols if flag else self.product_cols
        column_names = list(filter(target_set.__contains__, column_names_set))

        values_list = list(map(lambda dct: list(map(dct.get, column_names)), events_list))
        error_code = self.error_check(values_list, column_names)

        try:
            if(not flag):
                db = "{}.product".format(self.auth)
                self.client.insert(db, values_list, column_names=column_names)
            else:
                db = "{}.llm".format(self.auth)
                self.client.insert(db, values_list, column_names=column_names)
            return 0
        except Exception as e:
            print(e)
            return -1

    def capture(self, args: List[Dict]) -> int:

        sorted_data = order_by(args)
        data = [self.format_to_rova(obj) for obj in sorted_data]
        prod_events = [item[0] for item in data if item[1] == 0]
        llm_events = [item[0] for item in data if item[1] == 1]
        try:
            if(prod_events):
              self.capture_handler(prod_events, 0)
            if(llm_events):
              self.capture_handler(llm_events, 1)
            return 0
        except Exception as e:
            print(e)
            return -1