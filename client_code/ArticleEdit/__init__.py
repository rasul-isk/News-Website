from ._anvil_designer import ArticleEditTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

categories = [
    (cat['name'], cat) for cat in app_tables.categories.search()
    ]

class ArticleEdit(ArticleEditTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    self.category_box.items = categories
    

  def image_uploader_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    # Add the image to self.item
    self.item['image'] = file
