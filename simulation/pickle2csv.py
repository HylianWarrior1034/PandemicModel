import pickle
import pandas as pd

input = 'Anytown_Jan06_fullweek_dict.pkl'
output = 'pickletocsv.csv'

data_dict= pickle.load(open(input, 'rb'), encoding='latin1')

data_list = list(data_dict.keys())

emblist = [data_dict[i] for i in data_list]

df = pd.DataFrame(emblist)
df.insert(0, 'data', emblist)
df.to_csv(output, header=False, index=False)