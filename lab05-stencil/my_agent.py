# from my_rl_lemonade_agent import rl_agent_submission 
import argparse
import random
import numpy as np
# from my_lemonade_agent import nrl_agent_submission 
from agt_server.agents.base_agents.lemonade_agent import LemonadeAgent
from agt_server.local_games.lemonade_arena import LemonadeArena
from agt_server.agents.test_agents.lemonade.stick_agent.my_agent import StickAgent
from agt_server.agents.test_agents.lemonade.always_stay.my_agent import ReserveAgent
from agt_server.agents.test_agents.lemonade.decrement_agent.my_agent import DecrementAgent
from agt_server.agents.test_agents.lemonade.increment_agent.my_agent import IncrementAgent

# NOTE: The README will contain helpful methods for implementing your agent, please take a look at it!
class MyAgent(LemonadeAgent):
    def setup(self):
        self.name = "JBot"
        self.num_actions = 12                     
        self.num_states = 12 * 12 * 12             
        self.q_table = np.full((self.num_states, self.num_actions), 8.0) 
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.5                
        self.last_state = 0
        self.last_action = None
        # pass
    
    def determine_state(self):
        my_hist = self.get_action_history()
        opp1_hist = self.get_opp1_action_history()
        opp2_hist = self.get_opp2_action_history()

        if not my_hist:
            return 0

        my_last = my_hist[-1]
        opp1_last = opp1_hist[-1] if opp1_hist else random.randint(0, 11)
        opp2_last = opp2_hist[-1] if opp2_hist else random.randint(0, 11)

        rel1 = (opp1_last - my_last) % 12
        rel2 = (opp2_last - my_last) % 12
        return rel1 * 12 + rel2
    
    def get_action(self):
        state = self.determine_state()
        self.last_state = state
        if random.random() < self.epsilon:
            action = random.randint(0, self.num_actions - 1)
        else:
            action = int(np.argmax(self.q_table[state]))

        self.last_action = action
        return action
        # raise NotImplementedError

    def update(self):
        if self.last_action is None:
            return

        reward_hist = self.get_util_history()
        if not reward_hist:
            return
        reward = reward_hist[-1]

        next_state = self.determine_state()
        old_value = self.q_table[self.last_state, self.last_action]
        next_max = np.max(self.q_table[next_state])

        new_value = (1 - self.learning_rate) * old_value + \
                    self.learning_rate * (reward + self.discount_factor * next_max)
        self.q_table[self.last_state, self.last_action] = new_value
        # pass
    

# # TODO: Give your agent a NAME 
# name = ??? # TODO: PLEASE NAME ME D:
# # NOTE: If you want to submit MyAgent please set agent_submission = MyAgent(name)

################### SUBMISSION #####################
# TODO: Set to your RL Agent by default, change it to whatever you want as long as its a agent that inherits LemonadeAgent
# agent_submission = rl_agent_submission
agent_submission = MyAgent("JBot")
################### SUBMISSION #####################

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='My Agent')
    parser.add_argument('--join_server', action='store_true',
                        help='Connects the agent to the server')
    parser.add_argument('--ip', type=str, default='127.0.0.1',
                        help='IP address (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8080,
                        help='Port number (default: 8080)')
    
    args = parser.parse_args()

    if args.join_server:
        agent_submission.connect(ip=args.ip, port=args.port)
    else:
        arena = LemonadeArena(
        num_rounds=1000,
        timeout=10,
        players=[
            agent_submission,
            StickAgent("Bug1"),
            ReserveAgent("Bug2"),
            DecrementAgent("Bug3"),
            IncrementAgent("Bug4")
        ])
        
        # NOTE: FEEL FREE TO EDIT THE AGENTS HERE TO TEST AGAINST A DIFFERENT DISTRIBUTION OF AGENTS. A COUPLE OF EXAMPLE AGENTS
        #       TO TEST AGAINST ARE IMPORTED FOR YOU. 
        arena.run()
        
    
