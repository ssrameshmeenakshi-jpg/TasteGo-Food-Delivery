def coundig(num):
    count=0
    while num>0:
        num=num//10
        count+=1
    return count
num=int(input("Enter a positive integer:"))
print("Number of digits:",coundig(num))