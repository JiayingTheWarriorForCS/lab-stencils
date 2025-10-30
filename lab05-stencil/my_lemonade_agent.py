from agt_server.agents.base_agents.lemonade_agent import LemonadeAgent
from agt_server.local_games.lemonade_arena import LemonadeArena
from agt_server.agents.test_agents.lemonade.stick_agent.my_agent import StickAgent
from agt_server.agents.test_agents.lemonade.always_stay.my_agent import ReserveAgent
from agt_server.agents.test_agents.lemonade.decrement_agent.my_agent import DecrementAgent
from agt_server.agents.test_agents.lemonade.increment_agent.my_agent import IncrementAgent
import random


class MyNRLAgent(LemonadeAgent):
    def setup(self):
        pass

    def get_action(self):
        # raise NotImplementedError
        opp1_hist = self.get_opp1_action_history()
        opp2_hist = self.get_opp2_action_history()

        if not opp1_hist or not opp2_hist:
            return random.randint(0, 11)
        opp1 = opp1_hist[-1]
        opp2 = opp2_hist[-1]
        avg = ((opp1 + opp2) // 2) % 12
        best = (avg + 6) % 12 
        return best

    def update(self):
        pass
    

# TODO: Give your agent a NAME 
name = "JLBot" # TODO: PLEASE NAME ME D:


################### SUBMISSION #####################
nrl_agent_submission = MyNRLAgent(name)
####################################################


if __name__ == "__main__":
    arena = LemonadeArena(
        num_rounds=1000,
        timeout=10,
        players=[
            nrl_agent_submission,
            StickAgent("Bug1"),
            StickAgent("Bug2"),
            StickAgent("Bug3"),
            StickAgent("Bug4")
        ]
    )
    ## NOTE: FEEL FREE TO EDIT THE AGENTS HERE TO TEST AGAINST A DIFFERENT DISTRIBUTION OF AGENTS. A COUPLE OF EXAMPLE AGENTS
    #       TO TEST AGAINST ARE IMPORTED FOR YOU. 
    arena.run()
    