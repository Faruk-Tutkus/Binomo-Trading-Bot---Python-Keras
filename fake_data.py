import random
import csv
gün = 6
ay = 4
yıl = 2024
saat = 14
dakika = 32
saniye = 0
def Zaman():
    global gün,ay,yıl,saat,dakika,saniye
    if saniye >= 57:
        dakika += 1
        saniye = 0
    elif dakika > 58:
        saat += 1
        dakika = 0
    elif saat > 22:
        gün += 1
        saat = 0
    elif gün > 28:
        ay += 1
        gün = 0
    elif ay > 10:
        yıl += 1
        ay = 0
    else:
        saniye += 3
    
    ans = ""
    if gün < 10:  
        ans += '0' + str(gün)
    else:
        ans = str(gün)
    if ay < 10:
        ans += '/' + '0' + str(ay)
    else:
        ans += '/' + str(ay)
    if yıl < 10:
        ans += '0' + str(yıl)
    else:
        ans += '/' + str(yıl)
    
    if saat < 10:
        ans += ', ' + '0' + str(saat)
    else:
        ans += ', ' + str(saat)
    if dakika < 10:
        ans += ':' + '0' + str(dakika)
    else:
        ans += ':' + str(dakika)
    if saniye < 10:
        ans += ':' + '0' + str(saniye)
    else:
        ans += ':' + str(saniye)
        
    
    return ans
başlangıç_değeri = 63650
def Değer():
    global başlangıç_değeri
    artış_miktarı = [25,50,100,125,150,175,200,225,250,275]
    miktar = random.randint(1,500)
    art_azalt = random.randint(0,1)
    if art_azalt == 1 and başlangıç_değeri < 70000:
        başlangıç_değeri += miktar
    elif art_azalt == 0 and başlangıç_değeri > 50000:
        başlangıç_değeri -= miktar
    return str(başlangıç_değeri)
data = {}
def main():
    for _ in range(50000):
        a = Zaman()
        b = Değer()
        #print(a + ',' + b)
        data[a] = b
    
    with open('fake_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Value"])
        for key, value in data.items():
            if value.strip() != '':
                writer.writerow([key, value])
if __name__ == '__main__':
    main()