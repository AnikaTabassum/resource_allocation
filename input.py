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
		start_activities=[]
		all_activity=[]
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
			for i in range(1,len(x)-2):
				# print(x[i])
				if x[i]=="-":
					cnt+=1
					start_activities.append(x[0])
				pred.append(x[i])

			ac1=Activity(x[0],x[len(x)-2],x[len(x)-1],-1,-1,-1,-1,-1,pred,sucs)
			all_activity.append(ac1)

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
		print(graph)

		activity_dict={}
		for activity in all_activity:
			activity_dict[activity.name]=activity
			print(activity.name)


		while queue:
			s = queue.pop(0) 
			print ("lol ",s, end = " ") 
			# print(graph)
			for neighbour in graph[s]:
				activity_dict[neighbour].es=max(activity_dict[s].ef,activity_dict[neighbour].es)
				activity_dict[neighbour].ef=activity_dict[neighbour].es+activity_dict[neighbour].duration
				print("neighbour ",neighbour, activity_dict[neighbour].es)
				if neighbour not in visited:
					visited.append(neighbour)
					queue.append(neighbour)

		for activity in all_activity:
			activity.es=activity_dict[activity.name].es
			activity.ef=activity_dict[activity.name].ef
		print(all_activity)

		return all_activity

	# def forward_pass_calculation(self, activity_dict):


	def forward_pass(self,all_activity):
		# all_activity
		pred_dict={}
		for activity in all_activity:
			pred_dict[activity.name]=activity.pred
		
		# print(pred_dict)
		start_sucs=[]
		for key in pred_dict:
			if pred_dict[key]==['-'] and key!="start":
				# print("key ", key, pred_dict[key])
				pred_dict[key]="start"
				start_sucs.append(key)
		for activity in all_activity:
			if activity.name=="start":
				activity.sucs=start_sucs

		sucs_dict={}
		cnt=0
		finish_activities=[]
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

			all_activity=inputProcessing().create_finish_node(finish_activities,all_activity)
		
		print(all_activity[len(all_activity)-1].pred)

		
		visited = [] # List to keep track of visited nodes.
		queue = []     #Initialize a queue
		all_activity=inputProcessing().bfs(visited, queue, sucs_dict, 'start', all_activity)

		

		all_activity[len(all_activity)-1].sucs=finish_activities
		for activity in all_activity:
			for val in finish_activities:
				if activity.name==val:
					activity.sucs=['finish']
					all_activity[len(all_activity)-1].es=max(all_activity[len(all_activity)-1].es,activity.ef)
					all_activity[len(all_activity)-1].ef=all_activity[len(all_activity)-1].es

		for activity in all_activity:
			print("activity ", activity.name, activity.sucs, activity.pred, activity.es, activity.ef)
inputProcessing().takeinput()
# inputProcessing().forward_pass()