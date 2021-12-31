# Target-spotter-Using-PSO-and-OpenCV

it uses an AI based computing technique i.e Particle Swarm Optimization (PSO). This Computing technique, tries to give a possible best solution to a problem, through the position of the particle (can be said as ’eye’ of the algorithm), the technique iteratively tries to find the best particle solution using the past and current data. An image processing technique is used to find the features of the image which is the ORB algorithm, then a machine learning algorithm for matching them, and Operating system related multiprocessing techniques are used for enabling the parallel computing for faster computation. All these techniques are integrated together to get the task done. It provides you a flexibility on the use of computational power based on the parameter values you give, which makes it useful for many applications

pipe_implementation.py - it is a basic program, which starts 2 processes and implements a pipe between them for Interprocess communication 

PSO example.py - Is basic Particle Swarm Optimisation implementation, on an array

PSO_tarInter.py - it's the main program, where PSO with multiprocessing and Inter Process Communication, is used to identify the target in the video footage and also an inerface is implemented

PSO_tarNoIpc.py - it's a similar program but doesn't use Multiporocessing and Interprocess Communication, rather executes it as a single process
