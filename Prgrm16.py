import re,random,math
ct=re.sub('[^A-Z ]','',input("Ciphertext: ").upper())
n=int(input("Top how many? "))
F="ETAOINSHRDLCUMWFGYPBVKJXQZ";D={"TH":5,"HE":4,"IN":3,"ER":3,"AN":2,"RE":2}
def dec(k,s):return''.join(chr(ord('A')+k[ord(c)-65]) if 'A'<=c<='Z' else c for c in s)
def score(p):
    s=p.upper();return sum(D.get(s[i:i+2],0) for i in range(len(s)-1))+5*sum(s.count(w) for w in (" THE "," AND "," TO "," OF "))
def freq_key():
    cnt={c:0 for c in F}
    for ch in ct:
        if 'A'<=ch<='Z':cnt[ch]+=1
    ords=sorted(F,key=lambda x:-cnt[x]);k=[0]*26
    for i,c in enumerate(ords):k[ord(c)-65]=ord(F[i])-65
    return k
def neigh(k):
    a,b=random.sample(range(26),2);k2=k[:];k2[a],k2[b]=k2[b],k2[a];return k2
def hill(s):
    k=s[:];best=k[:];cur=score(dec(k,ct));bestsc=cur
    for _ in range(1000):
        kn=neigh(k);sc=score(dec(kn,ct))
        if sc>cur or random.random()<math.exp((sc-cur)/1.0):k,cur=kn,sc
        if cur>bestsc:best,bestsc=k[:],cur
    return best,bestsc
starts=[freq_key()]+[random.sample(range(26),26) for _ in range(6)]
res=[]
for s in starts:
    k,sc=hill(s);res.append((sc,dec(k,ct)))
res=sorted(res,reverse=True)[:n]
for i,(sc,pt) in enumerate(res,1):print(f"\n#{i} score={sc}\n{pt}")
