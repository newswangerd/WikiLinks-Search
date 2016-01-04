'''

Purpose: Uses Dijkstra's algorithm to find the shortest path between two 
articles on wikipedia.

By: David Newswanger and Robert Hosking

'''

import Queue
import time

class GraphSearch:
	
	def __init__(self, con):
		'''
			Pre: SQLITE connection object to our database.
		'''
		
		self.conn = con
		self.visited = {}
		self.Q = Queue.Queue()
		self.path = []
		
	def dijkstra(self, start, end):
		
		"""
		Uses breath first search to find the shortest path from start_id
		to end_id
		
		Updates a global dictionary that contains all searched pages to 
		prevent loopback and also serve as the lookup to return the
		actual path
		
		Uses a Queue to implement breath first search
		
		This function uses a "look ahead" search. It checks to see if
		the end_id is in the list of all links of the current article 
		(start_id).
		
		If not then it adds all links to articles on that page to a queue
		and updates start_id to the next value from the queue.
		
		Using lookahead rather than direct comparison we save lots of time.
		
		pre: an id to an article on the database to start the search
			an id to an article on the database to look for
			
		post: void function: purpose is to populate the visited class
			dictionary
		"""
		
		self.visited.clear()
		self.Q.queue.clear()
		self.path = []
		if start == end:
			self.visited.update({end:start})
		links = self.conn.get_links(start)
		while end not in links:
			for link in links:
				if link not in self.visited:
					self.Q.put(link)
					
					#dict visited has form {link:parrent}
					#this form is used to easially find the parrent of any link branch and also check if the page has already been indexed
					self.visited.update({link:start}) 
			start = self.Q.get()
			links = self.conn.get_links(start)
		self.visited.update({end:start})

	def get_path(self, start, end):
		"""
		Calls Dijkstra and operates on the dictionary updated by that 
		funciton to find the parrents of the resulting branch that led 
		to the endpoint
		
		pre: a start and end id to pass to dijkstra()
		post: a list containing the shortest human readable path from 
			the start to the end article
		"""		

		self.dijkstra(start, end)
		while start != end: # base case for backtracking
			# This uses the dictionary to continue to look at the parrent 
			#of each article starting at "end" and stopping at "start"
			# This causes the path to the start node to be added to the list 
			self.path.append(self.conn.get_name(end)) # add the parrent of "end" to the path list 
			end = self.visited[end] # update "end" to the value of end's parrent

		self.path.append(self.conn.get_name(start)) # finally we add the start page b/c the above does not include the start
		
		self.path.reverse() #reverse list to show forward path instead of backtracking path
		return self.path