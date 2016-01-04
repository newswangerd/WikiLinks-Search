'''

Purpose: Allows for the user to input the names of two articles on Wikipedia.
The program will then attempt to find the shortest number of link that you
need to click to get from the first article to the last one, and then display
the names of the links in the order that they have to be clicked.

By: David Newswanger and Robert Hosking

'''
from itter_search import GraphSearch
from db_lib_sqlite import DB_Connection
from sqlite3 import OperationalError
import os

def main():
    db = os.path.join(os.path.dirname(__file__), 'wiki_links.db')
    conn = DB_Connection(db)
    
    # if the solution above doesn't work, you can hard code the location of the DB here.
    # conn = DB_Connection('path_to_database_here')
    
    try:
        print "What article would you like to start on?"
        start, start_id = get_title(conn)
    except OperationalError:
        exit("It looks like there was a problem connecting to the database. \nPlease make sure that you have a valid database named wiki_links.db in the same directory as this file.")
        
    
    print ""
    print "What article would you like to end on?"
    end, end_id = get_title(conn)
    
    print ""
    print "You are searching for the shortest path between: %s and %s." % (start, end)
    
    search = GraphSearch(conn)
    path = search.get_path(start_id, end_id)
    
    print ""
    print "--------------------- RESULTS ---------------------"
    print ""
    
    # Prints the results onto the screen along with the other names that the article could
    # potentially be listed under.
    counter = 1
    for article in path:
        redirects = ""
        for x in conn.get_redirects(article):
            redirects += x + ", "
        redirects = redirects[:-2]
        
        print str(counter) + ": " + article + " --- Other Possible titles: (" + redirects + ")\n"
        counter += 1
    
    

def get_title(conn):
    '''
        Prompts the user to chose an article in the database
    
        Pre: SQLITE connection object to the database for this project
        Post: Returns the title and title id for the article that the user has chosen.
    '''
    
    # Asks the user for a title and searches for it in the database. If nothing is
    # found, asks the user for another title.
    while(True):
        title = raw_input("Title: ")
        start_list = conn.search_titles(title)
        if len(start_list) == 0: print "It looks like that title doesn't exist."
        else: break
    
    # Prints out a list of all of the titles found as a result of the search
    for (x, val) in enumerate(start_list):
        print str(x + 1) + ": " + val
    
    # Asks the user to pick one of the titles on the list. If they put in an invalid number,
    # prompts them to put in a new one.
    title = ""
    while(True):
        try:
            selected = int(raw_input("Choose the number of the article you want to search for: "))
            try:
                title = start_list[selected - 1]
                title_id = conn.get_id(title)
                break
            except IndexError: print "Make sure the number you enter is in the list." 
        except ValueError: print "Please enter a number."
    
    return (title, title_id)
    
main()