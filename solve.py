import pandas
import csv
import json
from collections import ChainMap

result_json_payload = ""
result_json_final_payload = []
res_frame = []
result_csv_file = 'Sample/result.csv'
result_json_file = 'Sample/result.json'
time = None
old_time = None

data_filenames = ['Sample/uid_to_xyz_00.csv',
                  'Sample/uid_to_xyz_01.csv',
                  'Sample/uid_to_xyz_02.csv', 'Sample/uid_to_xyz_03.csv', 'Sample/uid_to_xyz_04.csv',
                  'Sample/uid_to_xyz_05.csv'
                  ]

range_file = 'Sample/range_data.csv'
range_frame = pandas.read_csv(range_file)
range_frame_times = range_frame['start_time'].to_numpy()
range_frame = range_frame.rename(columns={"start_time": "time"})

# range_frame['date'] = pandas.to_datetime(range_frame['start_time']).dt.date.astype(str)

# pandas.DataFrame(list()).to_csv(res_file, header=['time', 'x_axis', 'y_axis', 'z_axis'], index=False)

headerList = ['time', 'x_axis', 'y_axis', 'z_axis']

# open CSV file and assign header
with open(result_csv_file, 'w') as file:
    dw = csv.DictWriter(file, delimiter=',',
                        fieldnames=headerList)
    dw.writeheader()

for filename in data_filenames:
    print(f"processing file: {filename}")
    dataframe = pandas.read_csv(filename)

    dataframe = dataframe.loc[dataframe['time'].isin(range_frame_times)]
    dataframe = dataframe.set_index('time').join(range_frame[["time", "aid"]].set_index('time'), on='time', how='left')
    dataframe.index = pandas.to_datetime(dataframe.index).date.astype(str)
    dataframe['time'] = dataframe.index
    dataframe = dataframe.groupby(['time', 'aid']).mean()

    # # change to datetime from str
    # dataframe['time'] = pandas.to_datetime(dataframe['time'])
    # # type_range = range_frame.loc[(range_frame['uid'] == dataframe.head(1)['uid'].to_list()[0])]
    # # change datetime to date and groupby date to find mean x y z values
    # samp = dataframe.groupby(pandas.Grouper(key='time', axis=0, freq='D')).mean().dropna()
    # # create time field and store dataframe's index there
    # samp['time'] = samp.index.astype(str)
    # lister = list(samp.columns)
    # # rearrange columns as required
    # time_and_mean = samp[[lister[-1]] + lister[1:4]]
    # # drop mean index
    # time_and_mean = time_and_mean.reset_index(drop=True)
    # # appending different file dataframes into single frame
    res_frame.append(dataframe)

# concat all files data to final dataframe and unique date
final_csv_frame = pandas.concat(res_frame)
# print(final_csv_frame)
# exit()
# final_csv_frame = final_csv_frame.groupby('time').mean().reset_index(level=-1)

# result payload generate
print("building json data")

loop_count = len(final_csv_frame) - 1
for index, row in enumerate(final_csv_frame.iterrows()):
    time = row[0][0]
    single_payload = {
        str(row[0][1]): {
            "mean": {
                "x_axis": "{:.2f}".format(row[1].x_axis),
                "y_axis": "{:.2f}".format(row[1].y_axis),
                "z_axis": "{:.2f}".format(row[1].z_axis)
            }
        }
    }

    result_json_payload = result_json_payload + str(single_payload)[1:-1] + ","

    if (time != old_time and old_time is not None) or index == loop_count:

        datar = str(
            f"{{" + f"'date': '{time}'," + str(result_json_payload).replace('[', '').replace(']', '}') + "}").replace(
            "'", '"')
        datar = datar[0:len(datar) - 2] + datar[-1]
        result_json_final_payload.append(json.loads(datar))


    else:
        print("old")
        old_time = time

    # print(single_payload)

# generating csv result file
# print(f"creating csv result at {result_csv_file}")
# final_csv_frame.to_csv(result_csv_file, encoding='utf-8')

# generating json result file
print(f"creating csv result at {result_json_file}")
with open(result_json_file, 'w') as out_file:
    json.dump(result_json_final_payload, out_file, sort_keys=True, indent=4, ensure_ascii=False)

print("results created")
