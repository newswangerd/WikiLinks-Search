'''

Purpose: Provides an easy to use interface between our database and application

By: David Newswanger and Robert Hosking

'''
import sqlite3

class DB_Connection:
    def __init__(self, path):
        '''
            Pre: a path to a valide SQLITE database file
            Post: none.
            
            Initializes the connection the the databse
        '''
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
    
    def disconnect(self):
        '''
            Disconnects from the database 
        '''
        self.cursor.close()
        self.conn.close()
    
    def get_links(self, title_id):
        '''
            Pre: a valid id for an article in the database
            Post: returns a list of article ids that are on the current page
            
            Used to get a list of all of the links that on on a given page in our database
        '''
        self.cursor.execute("SELECT link_id FROM links WHERE title_id = ?", (title_id,))
        
        results = []
        for link_id in self.cursor:
            if link_id[0] != 0:
                results.append(link_id[0])
        
        return results
    
    def get_id(self, name):
        '''
            Pre: name of a title in the database
            Post: returns the id of the entry or false if it doesn't exist
        '''
        
        # Checks the articles table
        self.cursor.execute("SELECT id FROM articles WHERE title = ?",(name,))
        id = self.cursor.fetchone()
        if id != None:
            return  id[0]
        
        # Checks the redirects table
        self.cursor.execute("SELECT article_id FROM redirect WHERE title = ?", (name,))
        id = self.cursor.fetchone()
        if id != None:
            return id[0]
        else: return False
    
    def get_name(self, id):
        '''
            Pre: Id of article in database
            Post: Name of article or false if article doesn't exist
        '''
        self.cursor.execute("SELECT title FROM articles WHERE id = ?", (id,))
        name = self.cursor.fetchone()
        if name != None:
            return name[0]
        else: return False
    
    def search_titles(self, title):
        '''
            Pre: string representing title of article in database
            Post: list of titles whose first letters match the name of the title
        '''
        self.cursor.execute("SELECT title FROM articles WHERE title LIKE ?", (title + "%",))
        
        results = []
        for title in self.cursor:
            results.append(title[0])
        return results
    
    def get_redirects(self, name):
        '''
            Pre: id of page in databse:
            Post: returns list of pages that redirect to the page passed to the function
        '''
        id = self.get_id(name)
        self.cursor.execute("SELECT title FROM redirect WHERE article_id = ?", (id,))
        
        results = []
        for title in self.cursor:
            results.append(title[0])
        return results
      


#conn = DB_Connection('/home/robert/Desktop/wiki_links.db')   

'''
tests

conn = DB_Connection('/home/david/Desktop/SQLiteStudio/wiki_links.db')
print conn.get_links(1)
print conn.get_links(275)
print conn.get_id('AccessibleComputing')
print conn.get_id('!WOWOW!')
print conn.get_id('adkfljasldkjflas  laksdjf alskddkj falskdkdjj flaskdkdjf lasldkk jf')
print conn.get_name(1400766)
print conn.search_titles("Adolf")[1]
'''