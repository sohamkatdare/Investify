def calculate_capital_gains_tax(selling_price, cost_basis, holding_period, taxable_income):
    capital_gain = selling_price - cost_basis
    
    if holding_period < 1:  # Short-term capital gains
        tax_rate = get_short_term_tax_rate(taxable_income)
    else:  # Long-term capital gains
        tax_rate = get_long_term_tax_rate(taxable_income)
    
    tax_owed = capital_gain * tax_rate
    
    return tax_owed


def get_short_term_tax_rate(taxable_income):
    # Define your short-term tax rate brackets and rates here
    # Example: (taxable_income, tax_rate)
    brackets = [
        (9875, 0.1),
        (40125, 0.12),
        (85525, 0.22),
        (163300, 0.24),
        (207350, 0.32),
        (518400, 0.35),
        (float('inf'), 0.37)
    ]
    
    return get_tax_rate(taxable_income, brackets)


def get_long_term_tax_rate(taxable_income):
    # Define your long-term tax rate brackets and rates here
    # Example: (taxable_income, tax_rate)
    brackets = [
        (40100, 0),
        (445850, 0.15),
        (501600, 0.2),
        (float('inf'), 0.23)
    ]
    
    return get_tax_rate(taxable_income, brackets)


def get_tax_rate(taxable_income, brackets):
    for limit, rate in brackets:
        if taxable_income <= limit:
            return rate
    
    return 0  # Default rate if taxable_income exceeds the highest limit
selling_price = 5000  # Example selling price
cost_basis = 3000  # Example cost basis
holding_period = 2  # Example holding period in years
taxable_income = 50000  # Example taxable income

tax_paid = calculate_capital_gains_tax(selling_price, cost_basis, holding_period, taxable_income)
print("Tax paid on capital gains:", tax_paid)