import random
from collections import defaultdict
dct = defaultdict(int)
def carry_out_experiment():
    ans = 0
    for _ in range(100):
        x = random.choice([1,2])
        if x == 2:
            ans+=1
    return ans
tmp = 0
for i in range(100_000):
    print(i)
    y = carry_out_experiment()
    dct[y]+=1
    tmp+=(50-y)**2
    #print(f"exp.{i+1} res={y} dif={abs(y-50)}")
disp = tmp/(i+1)
print(disp**0.5)
lst = list(dct.items())
lst.sort(key=lambda x:x[0])
for elem in lst:
    print(elem)