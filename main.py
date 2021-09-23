
from data import get_f1_data

COMBINED_COST_LIMIT = 99.1
NUM_RACES = 4

df = get_f1_data(COMBINED_COST_LIMIT)

print(df.head(30))
