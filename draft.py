import pandas as pd

# Load precomputed average rookie winshares
avg_rookie_ws = pd.read_csv('avg_rookie_winshare.csv', index_col=0).WS
# Sort for trade value
trade_val = pd.Series(index=avg_rookie_ws.index, data=avg_rookie_ws.sort_values(ascending=False).values)

def trade_eval(give_picks, receive_picks):
    give_val = trade_val.loc[give_picks].sum()
    receive_val = trade_val.loc[receive_picks].sum()

    success = receive_val > give_val
    if success:
        print("\nTrade result: Success! This trade receives more value than it gives away.\n")
        # Print additional metrics/reasoning here
    else:
        print("\nTrade result: Don't do it! This trade gives away more value than it receives.\n")
        # Print additional metrics/reasoning here

    print(f'Give val: {give_val}')
    print(f'Receive val: {receive_val}')


# Get the draft picks to give/receive from the user
# You can assume that this input will be entered as expected
# DO NOT CHANGE THESE PROMPTS
print("\nSelect the picks to be traded away and the picks to be received in return.")
print("For each entry, provide 1 or more pick numbers from 1-60 as a comma-separated list.")
print("As an example, to trade the 1st, 3rd, and 25th pick you would enter: 1, 3, 25.\n")
give_str = input("Picks to give away: ")
receive_str = input("Picks to receive: ")

# Convert user input to an array of ints
give_picks = list(map(int, give_str.split(',')))
receive_picks = list(map(int, receive_str.split(',')))

trade_eval(give_picks, receive_picks)

