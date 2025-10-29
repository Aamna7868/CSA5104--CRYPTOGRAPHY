import re

def egcd(a,b):
    if b==0:return(a,1,0)
    g,x1,y1=egcd(b,a%b)
    return(g,y1,x1-(a//b)*y1)
def modinv(a,m):
    g,x,_=egcd(a,m)
    return x%m if g==1 else None
def det2(M):
    return (M[0][0]*M[1][1]-M[0][1]*M[1][0])%26
def inv2(M):
    d=det2(M);di=modinv(d,26)
    if di is None:return None
    adj=[[M[1][1]%26,(-M[0][1])%26],[(-M[1][0])%26,M[0][0]%26]]
    return [[(di*adj[i][j])%26 for j in range(2)]for i in range(2)]
def mat_mul(A,B):
    return [[sum(A[i][k]*B[k][j]for k in range(2))%26 for j in range(len(B[0]))]for i in range(2)]

pt=re.sub('[^a-z]','',input("Enter plaintext: ").lower())
ct=re.sub('[^a-z]','',input("Enter ciphertext: ").lower())
P=[[ord(pt[0])-97,ord(pt[2])-97],[ord(pt[1])-97,ord(pt[3])-97]]
C=[[ord(ct[0])-97,ord(ct[2])-97],[ord(ct[1])-97,ord(ct[3])-97]]
P_inv=inv2(P)
if P_inv is None:exit("Plaintext matrix not invertible")
K=mat_mul(C,P_inv)
print("Recovered Key Matrix:")
for r in K:print(r)
