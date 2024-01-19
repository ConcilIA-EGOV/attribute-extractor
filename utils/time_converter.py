import csv
import pandas as pd


def convert_time_to_numeric():
    prev_file = open("database1.csv", "r")
    new_file = open("formated_result.csv", "w")

    csv_reader = csv.DictReader(prev_file)
    csv_writer = csv.writer(new_file)

    csv_writer.writerow(csv_reader.fieldnames)
    for row in csv_reader:
        # Intervalo de extravio
        list_extravio = row['intervalo de extravio'].split(':')
        if (len(list_extravio) == 2):
            extravio = int(list_extravio[0]) + round(int(list_extravio[1])/60, 2)
        else:
            extravio = ':'.join(list_extravio)

        # Intervalo de atraso
        list_atraso = row['intervalo de atraso'].split(':')
        if (len(list_atraso) == 2):
            atraso = int(list_atraso[0]) + round(int(list_atraso[1])/60, 2)
        else:
            atraso = ':'.join(list_atraso)

        row['intervalo de extravio'] = extravio
        row['intervalo de atraso'] = atraso
        csv_writer.writerow(row.values())

    prev_file.close()
    new_file.close()

    # Convertendo para xlsx
    data_frame = pd.read_csv("formated_result.csv")
    data_frame.to_excel("formated_result.xlsx", index=False)

def main():
    convert_time_to_numeric()

if __name__ == "__main__":
    main()