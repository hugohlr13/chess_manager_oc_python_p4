"""Module to launch chess application"""

from controllers.base import ApplicationController

def main():
    """Launch chess application"""
    app = ApplicationController()
    app.start()

if __name__ == "__main__":
    main()