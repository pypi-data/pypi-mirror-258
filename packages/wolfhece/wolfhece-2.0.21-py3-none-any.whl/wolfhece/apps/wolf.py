import wx

from ..PyTranslate import _
from ..PyGui import MapManager

# try:
#     from ..PyTranslate import _
#     from ..PyGui import MapManager
# except:
#     from wolfhece.PyTranslate import _
#     from wolfhece.PyGui import MapManager

def main():
    ex = wx.App()
    mywolf=MapManager()
    ex.MainLoop()

if __name__=='__main__':
    main()