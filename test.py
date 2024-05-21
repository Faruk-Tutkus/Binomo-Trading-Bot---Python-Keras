import csv

def update_value(value):
    if str(value).startswith('0') or str(value).startswith('1') or str(value).startswith('2'):
        return '2' + str(value)
    else:
        return '1' + str(value)

def process_csv(input_file, output_file):
    with open(input_file, 'r') as f_in, open(output_file, 'w', newline='') as f_out:
        reader = csv.DictReader(f_in)
        writer = csv.DictWriter(f_out, fieldnames=reader.fieldnames)
        writer.writeheader()

        for row in reader:
            row['Value'] = update_value(row['Value'])
            writer.writerow(row)

if __name__ == "__main__":
    input_file = "data.csv"  # Değiştirmeniz gereken dosya adı
    output_file = "out.csv"  # Değiştirmeniz gereken dosya adı
    process_csv(input_file, output_file)
    print("CSV dosyası başarıyla işlendi.")
