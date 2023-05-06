import os
import json
from datetime import datetime
import time
from pandas import DataFrame, concat


class POS:
    def __init__(self):
        self.log_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '../jsons/pos.json'))

        self.init_data()

    def init_data(self):
        with open(self.log_path, 'r') as f:
            data = dict(json.loads(f.read()))
            self.inputs = DataFrame(data['inputs'], columns=[
                                    'date', 'direction', 'amount', 'recordedBy'])
            self.outputs = DataFrame(data['outputs'], columns=[
                                     'date', 'direction', 'amount', 'recordedBy'])

    def write_data(self):
        inputs = []
        outputs = []
        for _, row in self.inputs.iterrows():
            inputs.append(dict(row))

        for _, row in self.outputs.iterrows():
            outputs.append(dict(row))

        with open(self.log_path, 'w') as f:
            json.dump({"inputs": inputs, "outputs": outputs}, f)

    def add_entry(self, mode, direction, amount, recorded_by):
        entry = {
            "date": int(time.time() * 1000),
            "direction": direction,
            "amount": amount,
            "recordedBy": recorded_by
        }

        if mode == 'input':
            self.inputs = concat(
                [self.inputs, DataFrame.from_records([entry])])
        elif mode == 'output':
            self.outputs = concat(
                [self.outputs, DataFrame.from_records([entry])])

        self.write_data()
        self.init_data()

    def search_logs(self, mode=None, date=None, direction=None, amount=None, recorded_by=None):
        df = self.inputs if mode == 'input' else self.outputs
        if date != None:
            if type(date) == int:
                df = df.loc[df['date'] == date]
            elif type(date) == dict:
                df = df.loc[df['date'] >= date['min']]
                df = df.loc[df['date'] <= date['max']]

        if direction != None:
            df = df.loc[df['direction'].str.contains(direction)]

        if amount != None:
            if type(amount) == int:
                df = df.loc[df['amount'] == amount]
            elif type(amount) == dict:
                df = df.loc[df['amount'] >= amount["min"]]
                df = df.loc[df['amount'] <= amount["max"]]

        if recorded_by != None:
            df = df.loc[df['recordedBy'] == recorded_by]

        entries = []
        print(df)
        for _, row in df.iterrows():
            entries.append(dict(row))

        return entries
