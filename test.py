import cv2
import numpy as np
img=cv2.imread('homo.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(img.shape)
h=np.array([[-1.89038795e-01, -1.22980354e+00,  4.57756092e+02],
 [-2.63401695e-02, -2.31312092e+00  ,8.10783550e+02],
 [-5.91585943e-05, -3.11763467e-03 , 1.00000000e+00]])
'''
ps=np.array(
[[28 ,  341],
[773  , 340],
[278  , 183],
[495  , 189]])
pd=np.array(
[[260 ,  352],
[527  , 356],
[278  , 0],
[496  , 0]]
)
'''


ps=np.array( [
[88  , 330],
[711 ,  360],
[231  , 284],
[606 ,  305],
] )



pd=np.array([
[274 ,  588],
[564 ,  575],
[244 ,  35],
[550 ,  37]
])





h, status = cv2.findHomography(ps, pd)
print(h)
birdview=cv2.warpPerspective(img,h, (img.shape[1],img.shape[0] ) )
v=np.array([360, 760,1])
a=np.matmul(h,v)
print(a/a[2])
#print(sum(birdview))

while(1):
        cv2.imshow("pp",birdview)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
