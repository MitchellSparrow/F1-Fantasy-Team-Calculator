
from data import get_f1_data

COMBINED_COST_LIMIT = 99.1

res = get_f1_data(COMBINED_COST_LIMIT)
df = res[0]

print(df.head(30))
