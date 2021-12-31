import numpy as np
import multiprocessing
from time import sleep
from time import time
import cv2
#----gui----
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

root=Tk()
root.title("Particle Swarm Optimization")
root.configure(bg="red")

#frames--------

#title frame
t_frame=LabelFrame(root)
t_frame.grid(row=0,column=0,columnspan=3,padx=3,pady=3)
t_label=Label(t_frame,text="Particle Swarm Optimization",bg="red",fg="white",relief=RIDGE,bd=10,width=25,font=("Calibri",35,"bold"))
t_label.pack()

#main frame
m_frame=LabelFrame(root,bg="red")
m_frame.grid(row=1,column=0,columnspan=3,padx=3,pady=3)

#input fields------
nop_label=Label(m_frame,text="Number of particles",bg="crimson",fg="white",relief=RIDGE,bd=5,width=20,font=("Calibri",20,"bold"),anchor=W)
nop_label.grid(row=0,column=0,padx=10,pady=10)
nof_particles=Entry(m_frame,width=20,bd=7,font=("consolas",15,"bold"))
nof_particles.grid(row=0,column=1,padx=10,pady=10)

noi_label=Label(m_frame,text="Number of iterations",bg="crimson",fg="white",relief=RIDGE,bd=5,width=20,font=("Calibri",20,"bold"),anchor=W)
noi_label.grid(row=1,column=0,padx=10,pady=10)
nof_iterations=Entry(m_frame,width=20,bd=7,font=("consolas",15,"bold"))
nof_iterations.grid(row=1,column=1,padx=10,pady=10)

#image
img_label=Label(m_frame,text="Image:",bg="crimson",fg="white",relief=RIDGE,bd=5,width=20,font=("Calibri",20,"bold"),anchor=W)
img_label.grid(row=2,column=0,padx=10,pady=10)


def ch_img():
    	global frame1
    	global y
    	global ia
    	if y!=0:
    	    	frame1.grid_remove()
    	y=y+1
    	root.filename=filedialog.askopenfilename(initialdir="",title="Choose an image",
                                             filetypes=(("png files","*.png"),("jpg files","*.jpg"),("All files","*.*")))
#    if root.filename:
#       i_button.grid_remove()
    	frame1=Frame(m_frame,bd=4,relief=RIDGE,bg="crimson")
    	frame1.grid(row=2,column=2,padx=10,pady=10)
    	ia=root.filename
    	img_add=Label(frame1,text=root.filename,bg="PaleTurquoise1",fg="black",bd=5,font=("Calibri",15,"bold"),padx=10)
    	img_add.pack()

#----for avoiding overlapping of img address
global y
y=0
#----

i_button=Button(m_frame,text="Choose",bg="white",fg="black",relief=RAISED,width=7,font=("Calibri",13,"bold"),command=ch_img)
i_button.grid(row=2,column=1,padx=10,pady=10)

#video
vid_label=Label(m_frame,text="Video:",bg="crimson",fg="white",relief=RIDGE,bd=5,width=20,font=("Calibri",20,"bold"),anchor=W)
vid_label.grid(row=3,column=0,padx=10,pady=10)

def ch_vid():
    	global frame2
    	global z
    	global va
    	if z!=0:
    	    	frame2.grid_remove()
    	z=z+1
    	root.filename=filedialog.askopenfilename(initialdir="",title="Choose a video",filetypes=(("mkv files","*.mkv"),("mp4 files","*.mp4"),("All files","*.*")))
    	frame2=Frame(m_frame,bd=4,relief=RIDGE,bg="crimson")
    	frame2.grid(row=3,column=2,padx=10,pady=10)
    	va=root.filename
    	vid_add=Label(frame2,text=root.filename,bg="PaleTurquoise1",fg="black",bd=5,font=("Calibri",15,"bold"),padx=10)
    	vid_add.pack()
    
#----for avoiding overlapping of vid address
global z
z=0
#----
    
v_button=Button(m_frame,text="Choose",bg="white",fg="black",relief=RAISED,width=7,font=("Calibri",13,"bold"),command=lambda:ch_vid())
v_button.grid(row=3,column=1,padx=10,pady=10)

#clear button------------
def clearall():
    	global frame1
    	global frame2
    	nof_particles.delete(0,END)
    	nof_iterations.delete(0,END)
    	frame1.grid_remove()
    	frame2.grid_remove()
	
c_frame=Frame(root,bd=4,relief=RIDGE,bg="crimson")
c_frame.grid(row=2,column=0)
clear=Button(c_frame,text="Clear",bg="white",fg="black",relief=RAISED,width=8,font=("Calibri",14,"bold"),command=clearall).pack()


#exit button----------
def exitroot():
    	val=messagebox.askquestion("Quit","Confirm?")
    	if val=='yes':
        	root.destroy()

e_frame=Frame(root,bd=4,relief=RIDGE,bg="crimson")
e_frame.grid(row=2,column=2)
xit=Button(e_frame,text="Exit",bg="white",fg="black",relief=RAISED,width=8,font=("Calibri",14,"bold"),command=exitroot).pack()



#-----------

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
	
	#print(len(good))
	
	#cv2.waitKey(0)
	#sim_img = cv2.drawMatches(obj, kp1, tar, kp2, good, None)
	#cv2.imshow("com img",sim_img)
	#key = cv2.waitKey(1)
	#breaking if q is pressed
	#pausing if p is pressed
	#if key == ord('p'):
	#	cv2.waitKey(0)
	#if key == ord('l'):
	#	if len(good) > 40:
	#		cv2.waitKey(0)
	return len(good)

def print_state(conn):
	# Printing
	while True:
		frame = conn.recv()
		if (frame[0][0][0] == '0'):
			return
		frame = cv2.resize(frame, None, fx=0.6, fy=0.60)
		cv2.imshow("motion", frame)
		key = cv2.waitKey(1)
		if key == ord('q'):
			return
		elif key == ord('p'):
			cv2.waitKey(0)


def pso(frameRcv, printSend, no_par, target, iterations, wt=0.4, pc=0.6, gc=0.5):
	particle = []
	ogc = gc #storing original value
	tar_rows = len(target)
	tar_cols = len(target[0])
	frame = frameRcv.recv()
	rows = len(frame) - tar_rows-10
	cols = len(frame[0]) - tar_cols-10
	#print("Target lenght",str(tar_rows)," target Width",str(tar_cols)," Frame lenght", str(len(frame))," frame Width",str(len(frame[0]))," frame Space : ",str(rows), str(cols))
	globaldim = [int(len(frame[0])/2), int(len(frame)/2)]
	for i in range(no_par):
		a = par()
		a.x = np.random.randint(0, cols) + int(tar_cols/2)
		a.y = np.random.randint(0, rows) + int(tar_rows/2)
		# print("Particle Coordinates : ",str(a.x),str(a.y))
		a.vx = np.random.randint(0, int(rows / 2))
		a.vy = np.random.randint(0, int(cols / 2))
		a.px = np.random.randint(0, len(frame[0]))
		a.py = np.random.randint(0, len(frame))
		particle.append(a)
	tar_found = False
	tar_lost = 0
		# print("Initial position of particle",str(i),"is",str([a.x,a.y]),"& velocity is",str([a.vx,a.vy]))
	while True:
		globalbest = 0
		frame = frameRcv.recv()
		if (frame[0][0][0] == '0'):
			printSend.send([[['0']]])
			return
		'''for  k in particle:
			k.pbest = 0'''
		it = True
		if not tar_found:
			for a in particle:
				# a.x = np.random.randint(0, cols) + int(tar_cols/2)
				# a.y = np.random.randint(0, rows) + int(tar_rows/2)
				# print("Particle Coordinates : ",str(a.x),str(a.y))
				a.vy = np.random.randint(0, int(rows / 2))
				a.vx = np.random.randint(0, int(cols / 2))
				a.px = np.random.randint(0, cols) + int(tar_cols/2)
				a.py = np.random.randint(0, rows) + int(tar_rows/2)
		for j in range(iterations):
			co = []
			if tar_found:
				print("#######")
			else:
				print("--------")
			for k in range(len(particle)):
				i = particle[k]
				co.append([i.x, i.y])
				syS = int(i.y-(tar_rows/2))
				syE = int(i.y+(tar_rows/2)-1)
				sxS = int(i.x-tar_cols/2)
				sxE = int(i.x+tar_cols/2-1)
				fit_val = find_obj(target, frame[ syS:syE , sxS:sxE ])
				if j == 0:
					i.pbest = 0
					it = False
				print(fit_val)
				print(i.pbest)
				if fit_val > i.pbest:
					i.p_update(i.x, i.y, fit_val)
				if i.pbest > 40 and i.pbest > globalbest:
					globalbest = i.pbest
					globaldim[0] = i.px
					globaldim[1] = i.py
					tar_found = True
					tar_lost = 0
					gc = ogc
				else:
					tar_lost += 1
					if tar_lost >= 3*no_par:
						gc = 0
						tar_found = False
				print("Tar lost : ", tar_lost)
				i.vx = int(wt * np.random.rand() * i.vx + pc * np.random.rand() * (i.px - i.x) + gc * np.random.rand() * (globaldim[0] - i.x))
				i.vy = int(wt * np.random.rand() * i.vy + pc * np.random.rand() * (i.py - i.y) + gc * np.random.rand() * (globaldim[1] - i.y))
				i.x = i.x + i.vx
				if i.x -(tar_cols/2) -1< 0:
				  i.x = int(tar_cols/2)
				elif i.x >= cols+int(tar_cols/2):
				  i.x = (cols - 1) + int(tar_cols/2)
				i.y = i.y + i.vy
				if i.y -(tar_rows/2) -1 < 0:
				  i.y = 0 + int(tar_rows/2)
				elif i.y -(tar_rows/2) >= rows + int(tar_rows/2):
				  i.y = rows - 1 + int(tar_rows/2)
		for c in co:
			cv2.rectangle(frame, (c[0]-20, c[1]-20), (c[0]+20, c[1] +20), (255, 0, 0), 3)
		if tar_found:
			cv2.rectangle(frame, (globaldim[0] -int(tar_cols/2), globaldim[1]-int(tar_rows/2)), (globaldim[0]+int(tar_cols/2), globaldim[1] +int(tar_rows/2)), (0, 255, 0), 3)
		printSend.send(frame)
	frameRcv.close()
	printSend.close()
	return

#submit button----------------
def proceed():
	global ia
	global va
	no_par=int(nof_particles.get())
	iterations=int(nof_iterations.get())
	root.destroy()
	video = cv2.VideoCapture(va)
	target = cv2.imread(ia)
	#cv2.imshow("test", target)

	printSend, printRcv = multiprocessing.Pipe()  # sends result frames from the pso process to the princing process
	frameSend, frameRcv = multiprocessing.Pipe()  # sends frames of videos from main process to pso implementation process


	p1 = multiprocessing.Process(target=pso, args=(frameRcv,printSend, no_par,target, iterations))
	p2 = multiprocessing.Process(target=print_state, args=(printRcv,))
	p1.start()
	sleep(0.5)
	p2.start()
	
	init = time()
	while (True):
		check, frame = video.read()
		if(check == False):
			frameSend.send([[['0']]])
			break
		frameSend.send(frame)
		# print("frame s")
		key = cv2.waitKey(1)
		#breaking if q is pressed
		if key == ord('q'):
			printSend.send([[['0']]])
			frameSend.send([[['0']]])
			break
		#pausing if p is pressed
		elif key == ord('p'):
			cv2.waitKey(0)
	end = time()
	p1.join()
	p2.join()
	print("Time taken : ", str(end-init));
	video.release()
	cv2.destroyAllWindows()
s_frame=Frame(root,bd=4,relief=RIDGE,bg="crimson")
s_frame.grid(row=2,column=1)
submit=Button(s_frame,text="Submit",bg="white",fg="black",relief=RAISED,width=8,font=("Calibri",14,"bold"),command=proceed).pack()


root.mainloop()

