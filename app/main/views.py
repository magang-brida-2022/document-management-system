from . import main

@main.get('/')
def index():
  return 'ini index'