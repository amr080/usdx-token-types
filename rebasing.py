import pandas as pd

step_counter = 0

def print_step(message):
    global step_counter
    step_counter += 1
    print(f"{step_counter}. {message}")

# Initial idle cash
visa_idle_cash = 67500000.00  # $67,500,000.00

class Visa:
    def __init__(self, idle_cash):
        self.idle_cash = idle_cash
        self.usdx_balance = 0  # Rebasing balance

    def subscribe_usdx(self, xft):
        xft.receive_funds(self.idle_cash)
        print_step("Visa subscribes to USDX")

    def redeem_usdx(self, xft):
        usd_redeemed = xft.process_redemption(self.usdx_balance)
        self.usdx_balance = 0
        print_step(f"Visa redeems USDX tokens and receives ${usd_redeemed:,.2f} USD")
        return usd_redeemed

class XFT:
    def __init__(self):
        self.funds = 0
        self.daily_yield_rate = 0.0005  # 0.05% daily yield

    def receive_funds(self, amount):
        self.funds += amount
        print_step(f"XFT receives ${amount:,.0f} USD from Visa")
        self.mint_tokens(amount)

    def mint_tokens(self, amount):
        tokens = amount  # 1 USDX = $1
        visa.usdx_balance += tokens
        print_step(f"XFT mints {int(tokens):,} rebasing USDX tokens to Visa")

    def calculate_yield(self, balance):
        return balance * self.daily_yield_rate

    def distribute_yield(self, days=10):
        daily_yield_data = []
        for day in range(1, days + 1):
            yield_amount = self.calculate_yield(visa.usdx_balance)
            visa.usdx_balance += yield_amount  # Rebasing: increase token balance
            daily_yield_data.append({
                'Day': day,
                'Token Supply': visa.usdx_balance,
                'Token Price': 1.00,  # Constant for rebasing
                'Total Value': visa.usdx_balance * 1.00,  # Token Price * Token Supply
                'Tokens Earned': yield_amount
            })
        return daily_yield_data

    def process_redemption(self, amount):
        usd_value = amount  # Rebasing tokens have a fixed price of $1
        self.funds -= usd_value
        print_step(f"XFT processes redemption of {amount:,.2f} rebasing tokens at $1.00 each")
        return usd_value

# Simulation
visa = Visa(visa_idle_cash)
xft = XFT()

print("\n=== REBASING DEMO ===\n")


# Subscription
visa.subscribe_usdx(xft)

# Yield Accrual and Distribution for 30 days
daily_yield_data = xft.distribute_yield(days=10)

# Redemption
visa_redeemed_usd = visa.redeem_usdx(xft)

# Summary
total_earned = visa_redeemed_usd - visa_idle_cash  # Only rebasing tokens
print_step(f"Total USD earned after 10 days: ${total_earned:,.2f}")

# Displaying the 30-day yield data in a formatted table
df_yield = pd.DataFrame(daily_yield_data)
pd.set_option('display.colheader_justify', 'left')  # Left-align column headers

# Print formatted table
print("\n\n10-Day Yield Data:")
print(df_yield.to_string(index=False, formatters={
    'Day': '{:<5}'.format,
    'Token Supply': '{:<20,.2f}'.format,
    'Token Price': '${:<20,.6f}'.format,
    'Total Value': '${:<20,.2f}'.format,
    'Tokens Earned': '{:<20,.6f}'.format,
}))
