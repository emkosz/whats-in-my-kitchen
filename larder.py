import sys
import os
# Title: What's in my kitchen?
# Autor: Emma Koszinowski
# Date: 04/13/2015

# A program that keeps a check on the food stuffs in the users kitchen. 
# The program stores a list of food stuff in a file between runs that makes it possible to print 
# a list of what's available and/or what is running out. It's also possible to search for specific articles.

# I made this program during an academic introduction course to programming at The Royal institute of Technology 
# in Stockholm. 


# -----------------------------------------
# ----- A class that describes eatables. -----
# Attributes:
#     name - the name of the food.
#     description - description of the food
#     amount - how much of the food that's left.
#     runningOut - describes if the food is running out.
#
class Article:
   # Creates a new article with the attributes name, description, amount
   def __init__(self, name, description, amount):
      self.name = name
      self.description = description
      self.amount = amount 
      self.isRunningOut = False
       
# ---- A class that describes a larder. ----- 
# Attributes:
#     articles -  a list that contains all of the food stuff in the file 
#     filename - the file is saved as an attribute to be used in methods and functions where needed   
#      
class Larder:
   # Creates a catalog of food stuff from the articles in the file.
   def __init__(self, filename):
      self.articles = []
      file = open(filename, 'rU')
      self.filename = filename
      for line in file:
         part = line.strip().split(', ')
         if (len(part) >=3):
            article = Article(part[0], part[1], part[2])
            if (len(part)) == 4:
               article.isRunningOut = True
         self.articles.append(article)  
      file.close()
      
   # Saves the catalog of food stuff to the file   
   def save_articles(self):
      #calls the attribute self.filename
      file = open(self.filename, 'w')
      for article in self.articles:
         file.write(article.name + ', ' +  article.description + ', ' + article.amount)
         if article.isRunningOut:
            file.write(', running out')
         file.write("\n")
      file.close()   
      
   # Returns the food stuff if it excists in the larder, otherwise None
   def find_article(self, name):
      article_list = list()
      for article in self.articles:
         if are_similar(name, article.name):
            article_list.append(article)
      return article_list
      
# ----- Help functions ----

# Returns True if s1 and s2 are similar
def are_similar(s1, s2):
   return s1.strip().casefold() in s2.strip().casefold() or s2.strip().casefold() in s1.strip().casefold()
            
   
# Returns an index of the list of articles
def choose_article_index(int1, myLarder):
   while True:
      article_list = myLarder.articles
      if len(article_list) == 0:
         print("That won't work! Your kitchen is completly empty! \nYou should go shopping and add some food to your kitchen!")
         return None
      else:
         try:
            list_articles(myLarder)
            question = int(input(int1))            
         except ValueError:
            print("Please type a number!")
            continue
         if question >=len(myLarder.articles):
            print("\nHey, you don't have that many eatables.")
         elif question < 0:
            print("Please type a number larger than 0.")
            continue
         else:
            return question
            


           
# ---- Functions for the text interface -----

# Prints the menu
def print_menu():
   print("Here's what you can do:")
   print("\t", 'L    List avaliable eatables in your kitchen')
   print("\t", 'R    List eatables that are running out')
   print("\t", 'S    Search for specific food')
   print("\t", 'A    Add new food')
   print("\t", 'D    Delete food')
   print("\t", 'C    Change the amount of the food') 
   print("\t", 'M    Mark specific food as running out.')  
   print("\t", 'Q    Quit the program')
   print("\t", "?    or 'help', will let you see the menu again")
   
   
# Lets the user choose what to do.
# Transforms lower-case to upper-case letters
def choose():
   while True:
      choice = input("\nWhat would you like to do? ")
      if len(choice) <= 0:
         print("Type one of the letters from the menu!")
         print_menu()
         continue
      else:
         return choice[0].upper()
   
# A function to search for a specific article.
def search_article(myLarder):
   searchedArticle = input('What food are you looking for? ')
   article_list = myLarder.find_article(searchedArticle)
   if len(article_list)== 0:
      print("\n\tNope, you don't have", searchedArticle)
   else:
      for article in article_list:
         print("\n\tYou've got", article.amount, article.description, article.name)
   
# Prints a list of name, descriptions and amount of the food stuff   
def list_articles(myLarder):
   articlesToPrint = myLarder.articles
   if len(articlesToPrint) == 0:
      print("There are no eatables in your kitchen! \nYou should go shopping and add some food to your kitchen!")
      print_menu()
   else:
      print("\nHere is a list of eatables avaliable in your kitchen: ")
      for article in articlesToPrint:
         print('Nr:', articlesToPrint.index(article),'You have', article.amount, article.description, article.name)

# A function to list the articles that are running out.  
def articles_running_out(myLarder):
   articlesThatAreRunningOut = myLarder.articles
   if len(articlesThatAreRunningOut) == 0:
      print("There are no eatables in your kitchen! \nYou should go shopping and add some food to your kitchen!")
      print_menu()
   else:
      print ("\nHere's a list of the eatables that are running out: ")
      for article in articlesThatAreRunningOut:
         if article.isRunningOut == True:
            print(article.description, article.name, "(only", article.amount, "remains)")
         elif article.isRunningOut == None:
            print("All the eatables are refilled, nothing is running out.")
                           
         
# Add food stuff to the larder     
def add_new_article(myLarder):
   newArticleName = input("What food did you add to your kitchen? ")
   newArticleDescription = input("Type a description: ")
   newArticleAmount = input("How much of did you add? ")
   # create a new article
   newArticle = Article(newArticleName, newArticleDescription, newArticleAmount)
   # add the new article to the list 
   myLarder.articles.append(newArticle)
   # save the list with the added new article to the list
   myLarder.save_articles()
         
  
# Delete eatables from the larder
def delete_article(myLarder):
   while True:
      articleToDelete = choose_article_index("\nType the number of the food you want to delete. Nr: ", myLarder)
      if articleToDelete == None:
         print_menu()
         break
      else:
         myLarder.articles.pop(articleToDelete)
         myLarder.save_articles()
         break
         
# Change the amount of food stuff
def change_amount(myLarder):
   while True:
      articleToChange = choose_article_index("\nWhat eatable did you refill or use? Nr: ", myLarder)
      if articleToChange == None:
         print_menu()
         break
      else:
         article = myLarder.articles[articleToChange]
         changedAmount = input("Write the new amount: ")
         article.amount = changedAmount
         #article.isRunningOut = False
         running_out = input("Is this food running out? Yes or No: ")
         if running_out == "Yes":
            article.isRunningOut = True
         elif running_out == "No": 
            article.isRunningOut = False
         myLarder.save_articles()
         break

# Let the user specify if food stuff are running out
def change_running_out_value(myLarder):
   while True:
      articleRunningOut = choose_article_index("\nWhat food is running out? Nr: ", myLarder)
      if articleRunningOut == None:
         print_menu()
         break
      else:
         article = myLarder.articles[articleRunningOut]
         article.isRunningOut = True
         myLarder.save_articles()
         break

# Function to quit the program
def quit_program():
   sys.exit("Goodbye, hope to see you soon")
   
# ----------- Mainprogram --------------
print("""

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Hi! Welcome to the program: What's in my kitchen?

This program will help you keep a check on the food in your kitchen! 
When you start the program for the first time the list of itmes will 
be empty. You can easily add food to match the food and amout of the 
items in your kitchen. This makes it possible for you to recieve a list
of avaliable food and also to search for eatables. If food is running out 
in your kitchen you can mark that food as "running out". This will make it 
possible for you to receive a list of eatables that are running out. Very 
handy when it's time to go shopping. 

Enjoy :-)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

""")

# opens the file if it exist, creates the file if it doesn't exist
FILENAME = 'articles.txt'
if os.path.isfile(FILENAME):
   larder = Larder(FILENAME)
else:
   FILENAME = open('articles.txt', 'w')
   larder = Larder(FIlENAME)

print_menu()

choice = choose();
while choice != '123':
   if choice == 'S':
      search_article(larder)
   elif choice == 'L':
      list_articles(larder)
   elif choice == 'R':
      articles_running_out(larder)
   elif choice == 'H':
      print_menu()
   elif choice == '?':
      print_menu()
   elif choice == 'Q':
      quit_program()
   elif choice == 'A':
      add_new_article(larder)
   elif choice == 'D':
      delete_article(larder)
   elif choice == 'C':
      change_amount(larder)
   elif choice == 'M':
      change_running_out_value(larder)
   else:
      print("Sorry, that option doesn't exist.")
      print_menu()
   choice = choose()


