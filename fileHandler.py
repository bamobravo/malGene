import csv
def read2Matrix(filename):
    data=[];
    label=[];
    with open(filename,'r') as csvFile:
        reader = csv.reader(csvFile);
        for row in reader:
            if row[0]=='':
                continue;
            data.append([float(x) for x in row[1:]])
            label.append(row[0]);
    return label,data

def showUsage():
    """this function will print the usage information of the """
    output ="usage:\n this program take maximum of two argument,the first is the rate(high,low,intermediate)\n and the second is the metric type to be used "
    print(output)
    exit()
