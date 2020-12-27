########## activity class ##################
class Activity:
	def __init__(self, name, duration, resource, es, ef, ls, lf, freefloat, pred, sucs):
		self.name = name
		self.duration= int(duration)
		self.resource= int(resource)
		self.es=es
		self.ef=ef
		self.ls=ls
		self.lf=lf
		self.freefloat=freefloat
		self.pred=pred
		self.sucs=sucs

class inputProcessing:
	def __init__(self):
		super(inputProcessing, self).__init__()
		# self.arg = arg
		global start_activities
		global all_activity
		global filename
		
	def takeinput(self):
		filename="data.txt"
		start_activities=[] #activities who don't have any predecessors
		all_activity=[] #list of all activity objects
		with open(filename) as f:
			activity_list = f.readlines()
		activity_list = [x.strip() for x in activity_list] 
		# print(activity_list)

		cnt=0
		for activity in activity_list:
			x=activity.split(",")
			# print(x)
			pred=[]
			sucs=[]
			### assuming first column is name, last twos are resource and duration,, al others are dependency list
			for i in range(1,len(x)-2):
				# print(x[i])
				if x[i]=="-":
					cnt+=1
					start_activities.append(x[0])
				pred.append(x[i])

			ac1=Activity(x[0],x[len(x)-2],x[len(x)-1],-1,-1,-1,-1,-1,pred,sucs)
			all_activity.append(ac1)
		## if there are more than 1 start nodes, make a start node on your own
		if cnt>1:
			all_activity=inputProcessing().create_start_node(start_activities, all_activity)
		# print(all_activity[0].name)
		self.forward_pass(all_activity)

	def create_start_node(self, start_activities, all_activity):
		pred=[]
		sucs=start_activities
		ac1=Activity("start",0,0,0,0,0,0,0,pred,sucs)
		# all_activity.append(ac1)
		all_activity.insert(0,ac1)
		## inserting start node at the 0 position
		# print(all_activity[0].sucs)
		return all_activity

	def create_finish_node(self, finish_activities, all_activity):
		pred=finish_activities
		sucs=[]
		ac1=Activity("finish",0,0,-1,-1,-1,-1,-1,finish_activities,sucs)
		all_activity.append(ac1)
		
		return all_activity

	def bfs(self,visited,queue, graph, node, all_activity):
		visited.append(node)
		queue.append(node)
		# print(graph)
		## dictionary for mapping the activity names with the activity objects easily
		activity_dict={}
		for activity in all_activity:
			activity_dict[activity.name]=activity
			# print(activity.name)


		while queue:
			s = queue.pop(0) 
			# print ("lol ",s, end = " ") 
			# print(graph)
			for neighbour in graph[s]:
				#### visiting each neighbour and calculating ES and EF
				activity_dict[neighbour].es=max(activity_dict[s].ef,activity_dict[neighbour].es)
				activity_dict[neighbour].ef=activity_dict[neighbour].es+activity_dict[neighbour].duration
				# print("neighbour ",neighbour, activity_dict[neighbour].es)
				if neighbour not in visited:
					visited.append(neighbour)
					queue.append(neighbour)
		#### we were keeping values in the dict before, nnow keepingthis in the main list
		for activity in all_activity:
			activity.es=activity_dict[activity.name].es
			activity.ef=activity_dict[activity.name].ef
		# print(all_activity)

		return all_activity

	# def forward_pass_calculation(self, activity_dict):


	def forward_pass(self,all_activity):
		# all_activity
		############ mapping activities with predecessors#####################
		pred_dict={}
		for activity in all_activity:
			pred_dict[activity.name]=activity.pred
		

		start_sucs=[] #keeps the valaues  of the successors of start node

		##### inserting start as start node of the nodes, who do not have any predecessors
		for key in pred_dict:
			if pred_dict[key]==['-'] and key!="start":
				# print("key ", key, pred_dict[key])
				pred_dict[key]="start"
				start_sucs.append(key)
		for activity in all_activity:
			if activity.name=="start":
				activity.sucs=start_sucs

		sucs_dict={}### mapping each node with it's successors list
		cnt=0
		finish_activities=[]### the activities who do nont have any successors

		##### checking if a key is in the predecessors list of a node, if true,   
		######### the key is the successor of the predecessors
		for activity in all_activity:
			sucs_list=[]
			for key in pred_dict:
				# print(pred_dict[key])
				if activity.name in pred_dict[key]:
					sucs_list.append(key)
					# sucs_dict[activity.name]=key
			sucs_dict[activity.name]=sucs_list
			activity.sucs=sucs_list
			if sucs_list==[] and activity.name!="start":
				cnt+=1
				finish_activities.append(activity.name)
		if cnt>1:
			### if thereis morethan one finish node, then create a finish node
			all_activity=inputProcessing().create_finish_node(finish_activities,all_activity)
		
		# print(all_activity[len(all_activity)-1].pred)

		
		visited = [] # List to keep track of visited nodes.
		queue = []     #Initialize a queue

		############# calling cfs with start node###############
		all_activity=inputProcessing().bfs(visited, queue, sucs_dict, 'start', all_activity)

		

		### putting the activities who do not have any successor, as successor of finish activities
		all_activity[len(all_activity)-1].pred=finish_activities 
		for activity in all_activity:
			for val in finish_activities:
				if activity.name==val:
					activity.sucs=['finish']
					### calculating value of finish nodes
					all_activity[len(all_activity)-1].es=max(all_activity[len(all_activity)-1].es,activity.ef)
					all_activity[len(all_activity)-1].ef=all_activity[len(all_activity)-1].es


		################ printing all the activities#####################
		for activity in all_activity:
			print("activity ", activity.name, activity.sucs, activity.pred, activity.es, activity.ef)


inputProcessing().takeinput()
# inputProcessing().forward_pass()