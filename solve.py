import pandas
import csv
import json

result_json_payload = []
res_frame = []
result_csv_file = 'Sample/result.csv'
result_json_file = 'Sample/result.json'

data_filenames = ['Sample/uid_to_xyz_00.csv', 'Sample/uid_to_xyz_00.csv', 'Sample/uid_to_xyz_01.csv',
                  'Sample/uid_to_xyz_02.csv', 'Sample/uid_to_xyz_03.csv', 'Sample/uid_to_xyz_04.csv',
                  'Sample/uid_to_xyz_05.csv']


# range_file = 'Sample/range_data.csv'

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
    # range_frame = pandas.read_csv(range_file)
    # change to datetime from str
    dataframe['time'] = pandas.to_datetime(dataframe['time'])
    # type_range = range_frame.loc[(range_frame['uid'] == dataframe.head(1)['uid'].to_list()[0])]
    # change datetime to date and groupby date to find mean x y z values
    samp = dataframe.groupby(pandas.Grouper(key='time', axis=0, freq='D')).mean().dropna()
    # create time field and store dataframe's index there
    samp['time'] = samp.index.astype(str)
    lister = list(samp.columns)
    # rearrange columns as required
    time_and_mean = samp[[lister[-1]] + lister[1:4]]
    # drop mean index
    time_and_mean = time_and_mean.reset_index(drop=True)
    # appending different file dataframes into single frame
    res_frame.append(time_and_mean)

# concat all files data to final dataframe and unique date
final_csv_frame = pandas.concat(res_frame)
final_csv_frame = final_csv_frame.groupby('time').mean().reset_index(level=-1)

# result payload generate
print("building json data")
for row in final_csv_frame.iterrows():
    single_payload = {
        "date": row[1].time,
        "mean": {
            "x_axis": "{:.2f}".format(row[1].x_axis),
            "y_axis": "{:.2f}".format(row[1].y_axis),
            "z_axis": "{:.2f}".format(row[1].z_axis)
        }
    }
    result_json_payload.append(single_payload)

# generating csv result file
print(f"creating csv result at {result_csv_file}")
final_csv_frame.to_csv(result_csv_file, encoding='utf-8')

# generating json result file
print(f"creating csv result at {result_json_file}")
with open(result_json_file, 'w') as out_file:
    json.dump(result_json_payload, out_file, sort_keys=True, indent=4, ensure_ascii=False)

print("results created")
