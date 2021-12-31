import numpy as np
from time import sleep
from time import time
import cv2

class par:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.px = 0
        self.py = 0
        self.vx = 0
        self.vy = 0
        self.pbest = 0

    def p_update(self, x, y, i):
        self.pbest = i
        self.px = x
        self.py = y
        
def find_obj(tar, obj):
	orb = cv2.ORB_create()
	kp1, des1 = orb.detectAndCompute(obj, None)
	kp2, des2 = orb.detectAndCompute(tar, None)
	index_par = dict(algorithm=0, trees=5)
	search_par = {}
	# flann = cv2.FlannBasedMatcher(index_par,search_par)
	flann = cv2.BFMatcher()
	matches = flann.knnMatch(des1, des2, k=2)
	good = []
	ratio = 0.8
	for m, n in matches:
		if m.distance < ratio * n.distance:
			good.append(m)
	print(len(good))
	#cv2.waitKey(0)
	#sim_img = cv2.drawMatches(obj, kp1, tar, kp2, good, None)
	#cv2.imshow("com img",sim_img)
	#cv2.waitKey(1)
	return len(good)



def pso(video, no_par, target, iterations, wt=0.7, pc=0.9, gc=0.5):
	particle = []
	tar_rows = len(target)
	tar_cols = len(target[0])
	check, frame = video.read()
	rows = len(frame) - tar_rows-10
	cols = len(frame[0]) - tar_cols-10
	print("Target lenght",str(tar_rows)," target Width",str(tar_cols)," Frame lenght", str(len(frame))," frame Width",str(len(frame[0]))," frame Space : ",str(rows), str(cols))
	globaldim = [int(len(frame[0])/2), int(len(frame)/2)]
	for i in range(no_par):
		a = par()
		a.x = np.random.randint(0, cols) + int(tar_cols/2)
		a.y = np.random.randint(0, rows) + int(tar_rows/2)
		# print("Particle Coordinates : ",str(a.x),str(a.y))
		a.vx = np.random.randint(0, int(rows / 2))
		a.vy = np.random.randint(0, int(cols / 2))
		a.px = np.random.randint(0, cols) + int(tar_cols/2)
		a.py = np.random.randint(0, rows) + int(tar_rows/2)
		particle.append(a)
		# print("Initial position of particle",str(i),"is",str([a.x,a.y]),"& velocity is",str([a.vx,a.vy]))
	while True:
		globalbest = 0
		check, frame = video.read()
		if check == False:
			return
		'''for  k in particle:
			k.pbest = 0'''
		it = True
		for j in range(iterations):
			co = []
			#print("In iteration",str(j))
			for k in range(len(particle)):
				i = particle[k]
				# print("Particle Coordinates : ",str(particle[k].x),str(particle[k].y))
				co.append([i.x, i.y])
				syS = int(i.y-(tar_rows/2))
				syE = int(i.y+(tar_rows/2)-1)
				sxS = int(i.x-tar_cols/2)
				sxE = int(i.x+tar_cols/2-1)
				#cv2.imshow("Test", frame[ syS:syE , sxS:sxE ])
				#print(syS,syE,sxS,sxE)
				#cv2.waitKey(0)
				fit_val = find_obj(target, frame[ syS:syE , sxS:sxE ])
				####cv2.imshow("Particle", frame[ syS:syE , sxS:sxE ])
				#cv2.waitKey(1)
				#print(fit_val)
				if it:
					i.pbest = 0
					it = False
				if fit_val > 20:
					i.p_update(i.x, i.y, fit_val)
				if i.pbest > 40:
					globalbest = i.pbest
					globaldim[0] = i.x
					globaldim[1] = i.y
				# print("Global best so far :",tuple(globaldim))
				# print("Co-ordinates of particle",str(k),"are:",str([i.x,i.y]),"& velocity is",str([i.vx,i.vy]))
				i.vx = int(wt * np.random.rand() * i.vx + pc * np.random.rand() * (i.px - i.x) + gc * np.random.rand() * (globaldim[0] - i.x))
				i.vy = int(wt * np.random.rand() * i.vy + pc * np.random.rand() * (i.py - i.y) + gc * np.random.rand() * (globaldim[1] - i.y))
				# print("w * Vx + pc * (Px-Vx) + gc * (Gx-Vx) = ",str(i.vx))
				# print("w * Vy + pc * (Py-Vy) + gc * (Gy-Vy) = ",str(i.vy))
				i.x = i.x + i.vx
				if i.x -(tar_cols/2) -1< 0:
				  i.x = int(tar_cols/2)
				elif i.x >= cols+int(tar_cols/2):
				  i.x = (cols - 1) + int(tar_cols/2)
				# print("X Co-ordinate of particle",k,"X(n) = X(n-1) + Vx =",i.x)
				i.y = i.y + i.vy
				if i.y -(tar_rows/2) -1 < 0:
				  i.y = 0 + int(tar_rows/2)
				elif i.y -(tar_rows/2) >= rows + int(tar_rows/2):
				  i.y = rows - 1 + int(tar_rows/2)
		#print("Global ", str(globaldim[0] -int(tar_cols/2)), str(globaldim[1]-int(tar_rows/2)), str(globaldim[0]+int(tar_cols/2)),str(globaldim[1] +int(tar_rows/2)))
		for c in co:
			cv2.rectangle(frame, (c[0]-20, c[1]-20), (c[0]+20, c[1] +20), (255, 0, 0), 3)
		cv2.rectangle(frame, (globaldim[0] -int(tar_cols/2), globaldim[1]-int(tar_rows/2)), (globaldim[0]+int(tar_cols/2), globaldim[1] +int(tar_rows/2)), (0, 255, 0), 3)
		frame = cv2.resize(frame, None, fx=0.6, fy=0.60)
		cv2.imshow("motion", frame)
		key = cv2.waitKey(1)
		if key == ord('p'):
			cv2.waitKey(0)
		elif key == ord('q'):
			return
	return

no_par = int(input("Enter the no of particles : "))
iterations = int(input("Enter the no of iterations : "))

video = cv2.VideoCapture("Pexels Videos.mp4")#"Pexels Videos 2675512.mp4"
target = cv2.imread("Target car1.png")
#cv2.imshow("test", target)

init = time()
pso(video, no_par, target, iterations)
print("Time taken : ", time()-init)
video.release()
cv2.destroyAllWindows()
