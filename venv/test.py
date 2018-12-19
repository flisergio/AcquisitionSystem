import CSVExchanging

for i in range(502, 940):
    try:
        CSVExchanging.saveToDatabase(str(i))
    except:
        print(i)
        continue

