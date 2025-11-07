from agt_server.core.game.AdxOneDayGame import OneDayBidBundle, AdxOneDayGame
from agt_server.core.game.bid_entry import SimpleBidEntry
from agt_server.core.game.market_segment import MarketSegment
from agt_server.core.game.campaign import Campaign
from typing import Dict, Any
from agt_server.server.connect_stencil import connect_agent_to_server
from agt_server.core.agents.lab08.random_agent import RandomAdXAgent
from agt_server.core.agents.lab08.aggressive_bidding_agent import AggressiveBiddingAgent
from agt_server.core.local_arena import LocalArena
from agt_server.core.agents.common.base_agent import BaseAgent

class MyAdXAgent(BaseAgent):
    """
    Your implementation of the AdX One Day agent.
    
    This agent should implement a bidding strategy for the AdX One Day game.
    You will be assigned a campaign with:
    - id: campaign ID
    - market_segment: target demographic (e.g., Female_Old, Male_Young_HighIncome)
    - reach: number of impressions needed to fulfill the campaign
    - budget: total budget available for bidding
    
    Your goal is to bid on market segments to win impressions that match your campaign,
    while staying within your budget and maximizing profit.
    
    Key concepts:
    - Market segments can be 1, 2, or 3 attributes (e.g., Female, Female_Old, Female_Old_HighIncome)
    - You can bid on any segment that matches your campaign (use MarketSegment.is_subset)
    - Second-price sealed-bid auctions determine winners
    - You only get credit for impressions that match your campaign's target segment
    - Profit = (reach_fulfilled / total_reach) * budget - total_spending
    """
    
    def __init__(self, name: str = "MyAdXAgent"):
        super().__init__(name)
        self.game_title = "adx_oneday"
        # TODO: Add any instance variables you need for your strategy
        self.scaling_factor = 1.2
        self.campaign = None

    def reset(self):
        """Reset the agent for a new game."""
        # TODO: Reset any game-specific state variables
        self.campaign = None
        # pass
    
    def setup(self):
        """Initialize the agent for a new game."""
        # TODO: Initialize any strategy-specific variables
        self.scaling_factor = 1.2
        self.campaign = None
        # pass

    def get_action(self, observation: Dict[str, Any]) -> OneDayBidBundle:
        """
        Return a OneDayBidBundle for your assigned campaign.
        
        This is the main method you need to implement. It should:
        1. Extract your campaign from the observation
        2. Create SimpleBidEntry objects for relevant market segments
        3. Set appropriate bids and spending limits
        4. Return a OneDayBidBundle
        
        Args:
            observation: Dictionary containing your campaign information
            
        Returns:
            OneDayBidBundle: Your bidding strategy for this game
        """
        # Convert campaign dictionary to Campaign object if needed
        campaign_data = observation['campaign']
        self.campaign = Campaign.from_dict(campaign_data) if isinstance(campaign_data, dict) else campaign_data
        
        # TODO: Implement your bidding strategy here
        # 
        # Example strategy (you should replace this with your own):
        # 1. Find all market segments that match your campaign
        # 2. Create bid entries for those segments
        # 3. Set bids and spending limits based on your strategy
        # 4. Return the bid bundle
        campaign_data = observation['campaign']
        self.campaign = Campaign.from_dict(campaign_data) if isinstance(campaign_data, dict) else campaign_data
        vpm = self.campaign.budget / self.campaign.reach
        bid_am = vpm * self.scaling_factor
        bid_entries = []
        mse = [seg for seg in MarketSegment.all_segments() if seg.is_subset(self.campaign.market_segment, seg)]
        limit = self.campaign.budget / max(len(mse), 1)
        for seg in mse:
            entry = SimpleBidEntry(
                market_segment=seg,
                bid=bid_am,
                spending_limit=limit,
            )
            bid_entries.append(entry)
        return OneDayBidBundle(campaign_id=self.campaign.id, day_limit=self.campaign.budget, bid_entries=bid_entries)

if __name__ == "__main__":
    server = True
    name = "wdjbhd"  # TODO: Give your agent a unique name
    host = "10.37.40.198"
    port = 8080  
    verbose = False  
    game = "adx_oneday" 
    
    if server:
        async def main():
            agent = MyAdXAgent()
            
            await connect_agent_to_server(agent, game, name, host, port, verbose)
        
        import asyncio
        asyncio.run(main())
    else:
        print("Testing MyAdXAgent locally...")
        print("=" * 50)
        
        agent = MyAdXAgent(name="MyAdXAgent")
        opponent1 = AggressiveBiddingAgent()
        random_agents = [RandomAdXAgent(f"RandomAgent_{i}") for i in range(8)]
        
        agents = [agent, opponent1] + random_agents
        arena = LocalArena(
            game_title="adx_oneday",
            game_class=AdxOneDayGame,
            agents=agents,
            num_agents_per_game=10,
            num_rounds=10,
            timeout=30.0,
            save_results=False,
            verbose=True
        )
        arena.run_tournament()
        
        print("\nLocal test completed!")

agent_submission = MyAdXAgent()