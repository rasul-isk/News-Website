import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

@anvil.server.callable
def add_article(article_dict):
  # Get the logged in user
  current_user = anvil.users.get_user()

  # Check that someone is logged in
  if current_user is not None:
    app_tables.articles.add_row(
	  created=datetime.now(),
	  # Store the logged in user in the 'user' column
	  user=current_user,
	  **article_dict
	)
  
@anvil.server.callable
def get_articles():
  # Get the logged in user
  current_user = anvil.users.get_user()

  # Check that someone is logged in
  if current_user is not None:
    # Get a list of articles that belong to the logged-in user,
    # sorted by 'created' column, in descending order
    return app_tables.articles.search(
      tables.order_by("created", ascending=False),
      user=current_user
    )

@anvil.server.callable
def update_article(article, article_dict):
  if verify_user_permission(article):
    # Set the 'updated' property to datetime.now()
    article_dict['updated'] = datetime.now()
    article.update(**article_dict)
  else:
    # Raise an exception if the article doesn't exist in the Data Table
    # or the user doesn't own the article being updated
    raise Exception("Article does not exist or does not belong to this user")
    
@anvil.server.callable
def delete_article(article):
  if verify_user_permission(article):
    # Delete the article
    article.delete()
  else:
    # Raise an exception if the article doesn't exist in the Data Table
    # or the user doesn't own the article being deleted
    raise Exception("Article does not exist or does not belong to this user")
    
    
def verify_user_permission(article):
  current_user = anvil.users.get_user()
  # Check that someone is logged in
  if current_user is not None:
    # Check if the article to be updated does exist in the Data Table
    # Check that the article belongs to the logged in user
    if app_tables.articles.has_row(article) and article['user'] == current_user:
      return True