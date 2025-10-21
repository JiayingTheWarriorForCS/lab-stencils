import pickle
import os
from agt_server.agents.base_agents.sa_agent import SimultaneousAuctionAgent
from agt_server.agents.test_agents.sa.truth_bidder.my_agent import TruthfulAgent
from localbid import local_bid

class SCPPAgent(SimultaneousAuctionAgent):
    def setup(self):
        # NOTE: Many internal methods (e.g. self.get_valuations) aren't available during setup.
        # So we delay any setup that requires those until get_action() is called.
        
        self.mode = 'TRAIN'
        self.simulation_count = 0
        self.NUM_SIMULATIONS_PER_ITERATION = 100
        self.ALPHA = 0.1
        self.num_iterations_localbid = 100
        self.price_file = f"learned_price_{self.name}.pkl"

        self.valuation_function = None
        self.learned_prices = None  # point estimate
        self.curr_prices = []     

    def load_prices(self):
        """
        Load the learned price from disk, if it exists.
        """
        if os.path.exists(self.price_file):
            with open(self.price_file, "rb") as f:
                self.learned_prices = pickle.load(f)
        else:
            self.initialize_prices()

    def save_prices(self):
        """
        Save the learned distribution to disk.
        """
        with open(self.price_file, "wb") as f:
            pickle.dump(self.learned_prices, f)

    def initialize_prices(self):
        """
        Initialize prices to zero for all goods.
        You can modify this to use a different initialization strategy.
        """
        self.learned_prices = {g: 0.0 for g in self.goods}

    def get_action(self):
        """
        Compute and return a bid vector by running the LocalBid routine with marginal values.
        In RUN mode, load the price from disk.
        In TRAIN mode, initialize a new price if needed.
        """
        self.valuation_function = self.calculate_valuation
        self.load_prices()
        return self.get_bids()
    
    def get_bids(self):
        bids = local_bid(
            self.goods, 
            self.valuation_function, 
            self.learned_prices
        )
        return bids

    def update(self):
        price_history = self.get_price_history()
        if not price_history:
            return
        
        observed_prices = price_history[-1]
        if not observed_prices:
            return

        # TODO: insert observed prices into self.curr_prices
        # TODO: update simulation_count
        self.curr_prices.append(observed_prices)
        self.simulation_count += 1

        if self.simulation_count % self.NUM_SIMULATIONS_PER_ITERATION == 0:
            # TODO: Find point estimate (mean) from recent observations
            price_total = {g: 0.0 for g in self.goods}
            for price in self.curr_prices:
                for good in self.goods:
                    price_total[good] += price[good]
            
            p_mean = {g: price_total[g] / len(self.curr_prices) for g in self.goods}
            p_old = self.learned_prices
            new_prices = {g: (1 - self.ALPHA) * p_old[g] + self.ALPHA * p_mean[g] for g in self.goods}
            self.learned_prices = new_prices
            self.curr_prices = []

            # TODO: Find new price. Use exponential smoothing update pt = (1 − α) pt−1 + αp_mean
           
            # TODO: Convergence check
            # TODO: Update learned_prices. Reset the current prices list. 

            if self.mode == "TRAIN":
                # TODO: Save the updated prices to disk
                self.save_prices()
                # pass

################### SUBMISSION #####################
agent_submission = SCPPAgent("SCPP Agent")
####################################################

if __name__ == "__main__":
    import argparse
    import time
    from agt_server.local_games.sa_arena import SAArena

    parser = argparse.ArgumentParser(description='SCPP Agent')
    parser.add_argument('--join_server', action='store_true',
                        help='Connects the agent to the server')
    parser.add_argument('--ip', type=str, default='127.0.0.1',
                        help='IP address (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8080,
                        help='Port number (default: 8080)')
    parser.add_argument('--mode', type=str, default='TRAIN',
                        help='Mode: TRAIN or RUN (default: TRAIN)')

    args = parser.parse_args()
    agent_submission.mode = args.mode
    print(agent_submission.mode)

    if args.join_server:
        agent_submission.connect(ip=args.ip, port=args.port)
    elif args.mode == "TRAIN":
        arena = SAArena(
            timeout=1,
            num_goods=3,
            num_rounds=500,
            kth_price=2,
            valuation_type="complement",
            players=[
                agent_submission,
                SCPPAgent("Agent_1"),
                SCPPAgent("Agent_2"),
                SCPPAgent("Agent_3"),
            ]
        )
        start = time.time()
        arena.run()
        end = time.time()
        print(f"{end - start} Seconds Elapsed")
    else:
        arena = SAArena(
            timeout=1,
            num_goods=3,
            num_rounds=100,
            kth_price=2,
            valuation_type="complement",
            players=[
                agent_submission,
                TruthfulAgent("Agent_1"),
                TruthfulAgent("Agent_2"),
            ]
        )
        start = time.time()
        arena.run()
        end = time.time()
        print(f"{end - start} Seconds Elapsed")