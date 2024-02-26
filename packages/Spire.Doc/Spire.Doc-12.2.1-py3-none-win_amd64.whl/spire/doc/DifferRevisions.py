from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class DifferRevisions(SpireObject):
    """
    Class for different revisions.
    """
    def Dispose(self):
        """
        Dispose the object.
        """
        GetDllLibDoc().DifferRevisions_Dispose.argtypes=[c_void_p]
        CallCFunction(GetDllLibDoc().DifferRevisions_Dispose,self.Ptr)

#    @property
#
#    def DeleteRevisions(self)->'List1':
#        """
#    <summary>
#        Gets the delete revisions.
#    </summary>
#        """
#        GetDllLibDoc().DifferRevisions_get_DeleteRevisions.argtypes=[c_void_p]
#        GetDllLibDoc().DifferRevisions_get_DeleteRevisions.restype=c_void_p
#        intPtr = GetDllLibDoc().DifferRevisions_get_DeleteRevisions(self.Ptr)
#        ret = None if intPtr==None else List1(intPtr)
#        return ret
#


#    @property
#
#    def InsertRevisions(self)->'List1':
#        """
#    <summary>
#        Gets the insert revisions.
#    </summary>
#        """
#        GetDllLibDoc().DifferRevisions_get_InsertRevisions.argtypes=[c_void_p]
#        GetDllLibDoc().DifferRevisions_get_InsertRevisions.restype=c_void_p
#        intPtr = GetDllLibDoc().DifferRevisions_get_InsertRevisions(self.Ptr)
#        ret = None if intPtr==None else List1(intPtr)
#        return ret
#


