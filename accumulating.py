import pandas as pd

step_counter = 0

def print_step(message):
    global step_counter
    step_counter += 1
    print(f"{step_counter}. {message}")

# Initial idle cash
mastercard_idle_cash = 67500000.00  # $67,500,000.00

class Mastercard:
    def __init__(self, idle_cash):
        self.idle_cash = idle_cash
        self.usdx_balance = idle_cash  # Accumulating balance remains same
        self.usdx_price = 1.00  # Initial token price

    def invest_usdx(self, xft):
        xft.receive_funds(self.usdx_balance)
        print_step("Mastercard invests in USDX")

    def redeem_usdx(self, xft):
        usd_redeemed = xft.process_redemption(self.usdx_balance)
        self.usdx_balance = 0
        print_step(f"Mastercard redeems USDX tokens and receives ${usd_redeemed:,.2f} USD")
        return usd_redeemed

class XFT:
    def __init__(self):
        self.funds = 0
        self.daily_yield_rate = 0.0005  # 0.05% daily yield
        self.usdx_price = 1.00  # Initialize price
        self.token_supply = 67500000.00  # Constant token supply

    def receive_funds(self, amount):
        self.funds += amount
        print_step(f"XFT receives ${amount:,.0f} USD from Mastercard")
        self.mint_tokens(amount)

    def mint_tokens(self, amount):
        tokens = amount  # 1 USDX = $1
        # For accumulating tokens, token quantity remains the same
        print_step(f"XFT sets initial accumulating USDX token price at ${self.usdx_price:.2f}")

    def distribute_yield(self, days=10):
        daily_yield_data = []
        for day in range(1, days + 1):
            # Accumulating token calculations
            yield_amount = self.usdx_price * self.daily_yield_rate
            self.usdx_price *= (1 + self.daily_yield_rate)
            total_value = mastercard.usdx_balance * self.usdx_price
            daily_yield_data.append({
                'Day': day,
                'Token Supply': self.token_supply,
                'Token Price': self.usdx_price,
                'Total Value': total_value,
                'Yield / Token': yield_amount
            })
        return daily_yield_data

    def process_redemption(self, amount):
        usd_value = amount * self.usdx_price
        self.funds -= usd_value
        print_step(f"XFT processes redemption of {amount:.0f} accumulating tokens at ${self.usdx_price:.6f} each")
        return usd_value

# Simulation
mastercard = Mastercard(mastercard_idle_cash)
xft = XFT()

print("\n=== ACCUMULATING DEMO ===\n")

# Investment
mastercard.invest_usdx(xft)



# Yield Accrual and Distribution for 30 days
daily_yield_data = xft.distribute_yield(days=10)

# Redemption
mastercard_redeemed_usd = mastercard.redeem_usdx(xft)

# Summary
total_earned = mastercard_redeemed_usd - mastercard_idle_cash  # Only accumulating tokens
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
    'Yield / Token': '${:<20,.6f}'.format
}))
