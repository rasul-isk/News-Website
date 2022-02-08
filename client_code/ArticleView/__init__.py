from ._anvil_designer import ArticleViewTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..ArticleEdit import ArticleEdit

class ArticleView(ArticleViewTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

  def edit_article_button_click(self, **event_args):
    # Create a copy of the existing article from the Data Table 
    article_copy = dict(self.item)
    # Open an alert displaying the 'ArticleEdit' Form
    # set the `self.item` property of the ArticleEdit Form to a copy of the article to be updated
    save_clicked = alert(
      content=ArticleEdit(item=article_copy),
      title="Update Article",
      large=True,
      buttons=[("Save", True), ("Cancel", False)]
    )
    # Update the article if the user clicks save
    if save_clicked:
      anvil.server.call('update_article', self.item, article_copy)

      # Now refresh the page
      self.refresh_data_bindings()

  def delete_article_button_click(self, **event_args):
    # Get the user to confirm if they wish to delete the article
    # If they confirm, raise the 'x-delete-article' event on the parent (which is the articles_panel on our Homepage)
    if confirm("Are you sure you want to delete {}?".format(self.item['title'])):
      self.parent.raise_event('x-delete-article', article=self.item)
