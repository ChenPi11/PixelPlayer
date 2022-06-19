import glob,os
orsiz=1*1000*1000#1MB
print("REMIX")
f=open(open("NAME").read(),"wb")
lst=[]
for i in glob.glob(".\\*.dat"):
    try:
        lst.append(int(os.path.splitext(os.path.basename(i))[0]))
    except Exception as e:
        print(e)
lst.sort()
for i in lst:
    i=str(i)+".dat"
    print("MIX:",i)
    fw=open(i,"rb")
    while True:
        data=fw.read(orsiz)
        if not data:
            break
        f.write(data)
        f.flush()
    fw.close()
f.close()
print("DONE",f.name)