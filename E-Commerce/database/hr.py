import os
import secrets
from json import dumps, dump, loads


class HR:
    def __init__(self):
        self.agents_path= os.path.abspath(os.path.join(os.path.dirname(__file__), '../jsons/agents.json'))
        self.all_agents= []
        self.init_data()

    def init_data(self):
        self.all_agents= []
        with open(self.agents_path, 'r') as f:
            data= dict(loads(f.read()))

            for value in data.values():
                self.all_agents.append(value)

    def write_data(self):
        data= {agent['id']: agent for agent in self.all_agents}
        with open(self.agents_path, 'w') as f:
            dump(data, f)

    def update_agent(self, payload):
        try:
            for agent in self.all_agents:
                if agent['id'] == payload['id']:
                    del payload['id']
                    for key in payload.keys():
                        agent[key]= payload[key]
                    
                    self.write_data()
                    return True
            return False
        except Exception as e:
            print(e)
            return False

    def create_agent(self, payload):
        try:
            payload['id']= str(secrets.token_hex(12))
            self.all_agents.append(payload)

            self.write_data()
            return True
        except Exception as e:
            print(e)
            return False

    def get_agent_by_id(self, agent_id):
        try:
            for agent in self.all_agents:
                if agent['id'] == agent_id:
                    return agent
            
            return False
        except Exception as e:
            print(e)
            return None
        
    def delete_agent(self, agent_id):
        try:
            for agent in self.all_agents:
                if agent['id'] == agent_id:
                    del self.all_agents[self.all_agents.index(agent)]

            self.write_data()
            return True

        except Exception as e:
            print(e)
            return False

    def kpi(self, mode, agent_id, amount):
        try:
            for agent in self.all_agents:
                if agent['id'] == agent_id:
                    if mode == 'decipline':
                        agent['deciplines'].append(amount)
                    elif mode == 'bonus':
                        agent['bonuses'].append(amount)

                self.write_data()
            return True
        except Exception as e:
            print(e)
            return False
            
