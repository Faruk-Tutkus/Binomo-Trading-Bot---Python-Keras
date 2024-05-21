import csv

def count_values(csv_file):
    value_counts = {}

    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            for value in row:
                if value in value_counts:
                    value_counts[value] += 1
                else:
                    value_counts[value] = 1

    return value_counts

def write_counts_to_csv(value_counts, output_file):
    sorted_counts = sorted(value_counts.items(), key=lambda x: x[1], reverse=True)
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for value, count in sorted_counts:
            writer.writerow([value, count])

csv_file = "data.csv"  # İşlem yapmak istediğiniz CSV dosyasının adını belirtin
output_file = "deger_sayilari.csv"  # Değerlerin sayılarının kaydedileceği yeni CSV dosyasının adını belirtin
value_counts = count_values(csv_file)
write_counts_to_csv(value_counts, output_file)
print(f"Değer sayıları {output_file} dosyasına büyükten küçüğe sıralanarak kaydedildi.")
