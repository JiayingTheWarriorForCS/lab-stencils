def calculate_marginal_value(goods, selected_good, valuation_function, bids, prices):
    """
    Calculates the marginal value of a given good for a bidder in a simultaneous sealed bid auction.

    TODO: Fill in marginal value as described in the pseudocode in the assignment.
    """
    bu = set()
    for good in goods:
        if good == selected_good:
            continue
        bid = bids[good]
        price = prices[good]
        if bid >= price:
            bu.add(good)
    val_with = valuation_function(bu | {selected_good})
    val_without = valuation_function(bu)
    marginal_value = val_with - val_without
    return marginal_value
    # raise NotImplementedError
