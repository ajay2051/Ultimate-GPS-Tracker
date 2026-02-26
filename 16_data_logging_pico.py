sensor_data_1 = ["25.5, 26.0, 24.8"]
sensor_data_2 = ["35.5, 23.0, 26.8"]
sensor_data_3 = ["35.5, 23.0, 24.8"]

all_data = [sensor_data_1, sensor_data_2, sensor_data_3]

with open('log.txt', 'w') as file:
    for data in all_data:
        line = ','.join(data)
        print(data)
        print(line)
        file.write(line + '\n')

with open('log.txt', 'r') as file:
    for line in file:
        values = line.strip().split(',')
    content = file.read()
    print(content)
    print(values)