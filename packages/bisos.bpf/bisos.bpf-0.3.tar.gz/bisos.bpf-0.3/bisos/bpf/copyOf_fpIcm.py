# -*- coding: utf-8 -*-

""" #+begin_org
* *[Summary]* :: A =CmndSvc= for
#+end_org """

####+BEGIN: b:prog:file/proclamations :outLevel 1
""" #+begin_org
* *[[elisp:(org-cycle)][| Proclamations |]]* :: Libre-Halaal Software --- Part Of Blee ---  Poly-COMEEGA Format.
** This is Libre-Halaal Software. © Libre-Halaal Foundation. Subject to AGPL.
** It is not part of Emacs. It is part of Blee.
** Best read and edited  with Poly-COMEEGA (Polymode Colaborative Org-Mode Enhance Emacs Generalized Authorship)
#+end_org """
####+END:

####+BEGIN: b:prog:file/particulars :authors ("./inserts/authors-mb.org")
""" #+begin_org
* *[[elisp:(org-cycle)][| Particulars |]]* :: Authors, version
** This File: NOTYET
** Authors: Mohsen BANAN, http://mohsen.banan.1.byname.net/contact
#+end_org """
####+END:

####+BEGIN: b:python:file/particulars-csInfo :status "inUse"
""" #+begin_org
* *[[elisp:(org-cycle)][| Particulars-csInfo |]]*
#+end_org """
import typing
icmInfo: typing.Dict[str, typing.Any] = { 'moduleName': ['niche'], }
icmInfo['version'] = '202207121913'
icmInfo['status']  = 'inUse'
icmInfo['panel'] = 'niche-Panel.org'
icmInfo['groupingType'] = 'IcmGroupingType-pkged'
icmInfo['cmndParts'] = 'IcmCmndParts[common] IcmCmndParts[param]'
####+END:

""" #+begin_org
* /[[elisp:(org-cycle)][| Description |]]/ :: [[file:/bisos/git/auth/bxRepos/blee-binders/bisos-core/COMEEGA/_nodeBase_/fullUsagePanel-en.org][BISOS COMEEGA Panel]]
Module description comes here.
** Relevant Panels:
** Status: In use with blee3
** /[[elisp:(org-cycle)][| Planned Improvements |]]/ :
*** TODO complete fileName in particulars.
#+end_org """

####+BEGIN: b:prog:file/orgTopControls :outLevel 1
""" #+begin_org
* [[elisp:(org-cycle)][| Controls |]] :: [[elisp:(delete-other-windows)][(1)]] | [[elisp:(show-all)][Show-All]]  [[elisp:(org-shifttab)][Overview]]  [[elisp:(progn (org-shifttab) (org-content))][Content]] | [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] | [[elisp:(bx:org:run-me)][Run]] | [[elisp:(bx:org:run-me-eml)][RunEml]] | [[elisp:(progn (save-buffer) (kill-buffer))][S&Q]]  [[elisp:(save-buffer)][Save]]  [[elisp:(kill-buffer)][Quit]] [[elisp:(org-cycle)][| ]]
** /Version Control/ ::  [[elisp:(call-interactively (quote cvs-update))][cvs-update]]  [[elisp:(vc-update)][vc-update]] | [[elisp:(bx:org:agenda:this-file-otherWin)][Agenda-List]]  [[elisp:(bx:org:todo:this-file-otherWin)][ToDo-List]]
#+end_org """
####+END:

####+BEGIN: b:python:file/workbench :outLevel 1
""" #+begin_org
* [[elisp:(org-cycle)][| Workbench |]] :: [[elisp:(python-check (format "/bisos/venv/py3/bisos3/bin/python -m pyclbr %s" (bx:buf-fname))))][pyclbr]] || [[elisp:(python-check (format "/bisos/venv/py3/bisos3/bin/python -m pydoc ./%s" (bx:buf-fname))))][pydoc]] || [[elisp:(python-check (format "/bisos/pipx/bin/pyflakes %s" (bx:buf-fname)))][pyflakes]] | [[elisp:(python-check (format "/bisos/pipx/bin/pychecker %s" (bx:buf-fname))))][pychecker (executes)]] | [[elisp:(python-check (format "/bisos/pipx/bin/pycodestyle %s" (bx:buf-fname))))][pycodestyle]] | [[elisp:(python-check (format "/bisos/pipx/bin/flake8 %s" (bx:buf-fname))))][flake8]] | [[elisp:(python-check (format "/bisos/pipx/bin/pylint %s" (bx:buf-fname))))][pylint]]  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:

####+BEGIN: bx:icm:python:icmItem :itemType "=PyImports= " :itemTitle "*Py Library IMPORTS*"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  =PyImports=  [[elisp:(outline-show-subtree+toggle)][||]] *Py Library IMPORTS*  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/update/sw/icm/py/importUcfIcmBleepG.py"
from unisos import ucf
from unisos import icm

icm.unusedSuppressForEval(ucf.__file__)  # in case icm and ucf are not used

G = icm.IcmGlobalContext()
# G.icmLibsAppend = __file__
# G.icmCmndsLibsAppend = __file__

from blee.icmPlayer import bleep
####+END:

import typing

from bisos import bpf

import os



####+BEGIN: bx:icm:py3:section :title "Common Parameters Specification"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  /Section/    [[elisp:(outline-show-subtree+toggle)][||]] *Common Parameters Specification*  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:

####+BEGIN: bx:icm:python:func :funcName "commonParamsSpecify" :funcType "ParSpec" :retType "" :deco "" :argsList "icmParams"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-ParSpec  [[elisp:(outline-show-subtree+toggle)][||]] /commonParamsSpecify/ retType= argsList=(icmParams)  [[elisp:(org-cycle)][| ]]
#+end_org """
def commonParamsSpecify(
    icmParams,
):
####+END:
    icmParams.parDictAdd(
        parName='fpBase',
        parDescription="File Parameters Directory Base Path.",
        parDataType=None,
        parDefault=None,
        parChoices=list(),
        parScope=icm.ICM_ParamScope.TargetParam,  # type: ignore
        argparseShortOpt=None,
        argparseLongOpt='--fpBase',
    )

####+BEGIN: bx:icm:py3:section :title "CS-Lib Examples"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  /Section/    [[elisp:(outline-show-subtree+toggle)][||]] *CS-Lib Examples*  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:


####+BEGIN: bx:dblock:python:func :funcName "examples_fpBase" :comment "Show/Verify/Update For relevant PBDs" :funcType "examples" :retType "none" :deco "" :argsList "fpBase cls menuLevel='chapter'"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Func-examples :: /examples_fpBase/ =Show/Verify/Update For relevant PBDs= retType=none argsList=(fpBase cls menuLevel='chapter')  [[elisp:(org-cycle)][| ]]
"""
def examples_fpBase(
    fpBase,
    cls,
    menuLevel='chapter',
):
####+END:
    """
** Common examples.
"""
    def cpsInit(): return collections.OrderedDict()
    def menuItem(verbosity): icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity=verbosity) # 'little' or 'none'
    # def execLineEx(cmndStr): icm.ex_gExecMenuItem(execLine=cmndStr)

    if menuLevel == 'chapter':
        icm.cmndExampleMenuChapter('*FILE_Params Access And Management*')
    else:
        icm.cmndExampleMenuChapter('*FILE_Params Access And Management*')

    cmndName = "fpParamsList" ; cmndArgs = "" ;
    cps=cpsInit() ; cps['fpBase'] = fpBase ; cps['cls'] = cls
    menuItem(verbosity='little')

    cmndArgs = "basic setExamples getExamples" ; menuItem(verbosity='little')

    cmndName = "fpParamsSetDefaults" ; cmndArgs = "" ;
    cps=cpsInit() ; cps['fpBase'] = fpBase ; cps['cls'] = cls
    menuItem(verbosity='little')

    cmndName = "fpParamsRead" ; cmndArgs = "" ;
    cps=cpsInit() ; cps['fpBase'] = fpBase ; cps['cls'] = cls
    menuItem(verbosity='little')

    cmndArgs = "basic setExamples getExamples" ; menuItem(verbosity='little')


####+BEGIN: blee:bxPanel:foldingSection :outLevel 0 :sep nil :title "CmndSvcs" :anchor ""  :extraInfo "Command Services Section"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*     [[elisp:(outline-show-subtree+toggle)][| _CmndSvcs_: |]]  Command Services Section  [[elisp:(org-shifttab)][<)]] E|
#+end_org """
####+END:


####+BEGIN: bx:dblock:python:class :className "FP_Base" :superClass "icm.FILE_TreeObject" :comment "Expected to be subclassed" :classType "basic"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Class-basic :: /FP_Base/ icm.FILE_TreeObject =Expected to be subclassed=  [[elisp:(org-cycle)][| ]]
"""
class FP_Base(icm.FILE_TreeObject):
####+END:
    """ FP_Base is also a FILE_TreeObject.
    """

####+BEGIN: bx:icm:py3:method :methodName "__init__" :deco "deprecated(\"moved to bpf\")"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /__init__/ deco=deprecated("moved to bpf")  [[elisp:(org-cycle)][| ]]
#+end_org """
    @deprecated("moved to bpf")
    def __init__(
####+END:
            self,
            fileSysPath,
    ):
        """Representation of a FILE_TreeObject when _objectType_ is FILE_ParamBase (a node)."""
        super().__init__(fileSysPath,)

####+BEGIN: bx:icm:py3:method :methodName "baseCreate" :deco ""
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /baseCreate/  [[elisp:(org-cycle)][| ]]
"""
    def baseCreate(
####+END:
            self,
    ):
        """  """
        return self.nodeCreate()

####+BEGIN: bx:icm:py3:method :methodName "baseValidityPredicate" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /baseValidityPredicate/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def baseValidityPredicate(
####+END:
                self,
    ):
        """  """
        pass

####+BEGIN: bx:icm:py3:method :methodName "fps_asIcmParamsAdd" :deco "staticmethod"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /fps_asIcmParamsAdd/ deco=staticmethod  [[elisp:(org-cycle)][| ]]
"""
    @staticmethod
    def fps_asIcmParamsAdd(
####+END:
            icmParams,
    ):
        """staticmethod: takes in icmParms and augments it with fileParams. returns icmParams."""
        icmParams.parDictAdd(
            parName='exampleFp',
            parDescription="Name of Bpo of the live AALS Platform",
            parDataType=None,
            parDefault=None,
            parChoices=list(),
            parScope=icm.ICM_ParamScope.TargetParam,  # type: ignore
            argparseShortOpt=None,
            argparseLongOpt='--exampleFp',
        )

        return icmParams

####+BEGIN: bx:icm:py3:method :methodName "fps_namesWithRelPath" :deco "classmethod"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /fps_namesWithRelPath/ deco=classmethod  [[elisp:(org-cycle)][| ]]
"""
    @classmethod
    def fps_namesWithRelPath(
####+END:
            cls,
    ):
        """classmethod: returns a dict with fp names as key and relBasePath as value.
        The names refer to icmParams.parDictAdd(parName) of fps_asIcmParamsAdd
        """
        relBasePath = "."
        return (
            {
                'exampleFP': relBasePath,
            }
        )

####+BEGIN: bx:icm:py3:method :methodName "fps_namesWithAbsPath" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /fps_namesWithAbsPath/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def fps_namesWithAbsPath(
####+END:
            self,
    ):
        """Uses fps_namesWithRelPath to construct absPath for relPath values. Returns a dict."""
        namesWithRelPath = self.__class__.fps_namesWithRelPath()
        namesWithAbsPath = dict()
        for eachName, eachRelPath in namesWithRelPath.items():
            namesWithAbsPath[eachName] = os.path.join(self.fileTreeBaseGet(), eachRelPath)
        return namesWithAbsPath

####+BEGIN: bx:icm:py3:method :methodName "fps_readTree" :deco "deprecated(\"moved to bpf\")"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /fps_readTree/ deco=deprecated("moved to bpf")  [[elisp:(org-cycle)][| ]]
#+end_org """
    @deprecated("moved to bpf")
    def fps_readTree(
####+END:
            self,
    ):
        """Returns a dict of FILE_Param s. Reads in all FPs at self.fps_absBasePath()."""
        cmndOutcome = icm.OpOutcome()
        FP_readTreeAtBaseDir = icm.FP_readTreeAtBaseDir()
        FP_readTreeAtBaseDir.cmndOutcome = cmndOutcome

        FP_readTreeAtBaseDir.cmnd(
            interactive=False,
            FPsDir=self.fileTreeBaseGet(),
        )
        if cmndOutcome.error: return cmndOutcome

        self.fps_dictParams = cmndOutcome.results
        return cmndOutcome

####+BEGIN: bx:icm:py3:method :methodName "fps_setParam" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /fps_setParam/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def fps_setParam(
####+END:
            self,
            paramName,
            paramValue,
    ):
        """Returns a dict of FILE_Param s. Reads in all FPs at self.fps_absBasePath()."""
        namesWithAbsPath = self.fps_namesWithAbsPath()
        fpBase = namesWithAbsPath[paramName]
        icm.FILE_ParamWriteTo(fpBase, paramName, paramValue)

####+BEGIN: bx:icm:py3:method :methodName "fps_getParam" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /fps_getParam/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def fps_getParam(
####+END:
            self,
            paramName,
    ):
        """Returns a dict of FILE_Param s. Reads in all FPs at self.fps_absBasePath()."""
        namesWithAbsPath = self.fps_namesWithAbsPath()
        fpBase = namesWithAbsPath[paramName]
        paramValue = icm.FILE_ParamReadFrom(fpBase, paramName,)
        return paramValue




"""
*  [[elisp:(org-cycle)][| ]]  /FILE_Param/         :: *FILE_Param: File Parameter (FILE_ParamBase, FILE_Param, FILE_ParamDict)* [[elisp:(org-cycle)][| ]]
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class            ::  FILE_ParamBase    [[elisp:(org-cycle)][| ]]
"""
class FILE_ParamBase(bpf.fto.FILE_TreeObject):
    """Representation of a FILE_TreeObject when _objectType_ is FILE_ParamBase (a node).
    """
    def baseCreate(self):
        """  """
        return self.nodeCreate()

    def baseValidityPredicate(self):
        """  """
        return self.validityPredicate()


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class            ::  FILE_Param    [[elisp:(org-cycle)][| ]]
"""

class FILE_Param(object):
    """Representation of One FILE_Parameter.

    A FILE_Param consists of 3 parts
       1) ParameterName
       2) ParameterValue
       3) ParameterAttributes

    On the file system:
      1- name of directory is ParameterName
      2- content of ParameterName/value is ParameterValue
      3- rest of the files in ParameterName/ are ParameterAttributes.

    The concept of a FILE_Param dates back to [[http://www.qmailwiki.org/Qmail-control-files][Qmail Control Files]] (at least).
    A FILE_Param is broader than that concept in two respects.
     1) A FILE_Param is represented as a directory on the file system. This FILE_Param
        permits the parameter to have attributes beyond just a value. Other attributes
        are themselves in the form of a traditional filename/value.
     2) The scope of usage of a FILE_Param is any parameter not just a control parameter.


    We are deliberately not using a python dictionary to represent a FILE_Param
    instead it is a full fledged python-object.
    """

    def __init__(self,
                 parName=None,
                 parValue=None,
                 storeBase=None,
                 storeRoot=None,
                 storeRel=None,
                 attrRead=None,
                 ):
        '''Constructor'''
        self.__parName = parName
        self.__parValue = parValue
        self.__storeBase = storeBase   # storeBase = storeRoot + storeRel
        self.__storeRoot = storeRoot
        self.__storeRel = storeRel
        self.__attrRead = attrRead


    def __str__(self):
        return  format(
            str(self.parNameGet()) + ": " + str(self.parValueGet())
            )

    def parNameGet(self):
        """  """
        return self.__parName

    def parValueGet(self):
        """        """
        return self.__parValue

    def parValueGetLines(self):
        """        """
        if self.__parValue == None:
            return None
        return self.__parValue.splitlines()

    def parValueSet(self, value):
        """        """
        self.__parValue = value

    def attrReadGet(self):
        """        """
        return self.__attrRead

    def attrReadSet(self, attrRead):
        """        """
        self.__attrRead = attrRead

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def readFrom(self, storeBase=None, parName=None):
        """Read into a FILE_param content of parBase/parName.

        Returns a FILE_param which was contailed in parBase/parName.
        """
        if self.__storeBase == None and storeBase == None:
            return icm.EH_problem_usageError("storeBase")

        if self.__parName == None and parName == None:
            return icm.EH_problem_usageError("parName")

        if storeBase:
            self.__storeBase = storeBase

        if parName:
            self.__parName = parName

        self.__parName = parName

        parNameFullPath = os.path.join(self.__storeBase, parName)

        return self.readFromPath(parNameFullPath)

    # Undecorated because called before initialization
    #@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def readFromPath(self, parNameFullPath):
        """Read into a FILE_param content of parBase/parName.

        Returns a FILE_param which was contailed in parBase/parName.
        """

        if not os.path.isdir(parNameFullPath):
            #return icm.EH_problem_usageError("parName: " + parNameFullPath)
            return None

        fileParam = self

        fileParam.__parName = os.path.basename(parNameFullPath)

        #
        # Now we will fill fileParam based on the directory content
        #
        #if os.path.exists(parNameFullPath):
            #return icm.EH_problem_usageError(f"Missing Path: {parNameFullPath}")

        for item in os.listdir(parNameFullPath):
            if item == "CVS":
                continue
            fileFullPath = os.path.join(parNameFullPath, item)
            if os.path.isfile(fileFullPath):
                if item == 'value':
                    lineString = open(fileFullPath, 'r').read().strip()    # Making sure we get rid of \n on read()
                    self.parValueSet(lineString)
                    continue

                # Rest of the files are expected to be attributes

                #lineString = open(fileFullPath, 'r').read()
                # NOTYET, check for exceptions
                #eval('self.attr' + str(item).title() + 'Set(lineString)')
            #else:
                #icm.EH_problem_usageError("Unexpected Non-File: " + fileFullPath)

        return fileParam


    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def writeTo(self, storeBase=None, parName=None, parValue=None):
        """Write this FILE_Param to storeBase.

        """
        if self.__storeBase == None and storeBase == None:
            return icm.EH_problem_usageError("storeBase")

        if self.__parName == None and parName == None:
            return icm.EH_problem_usageError("parName")

        if self.__parValue == None and parValue == None:
            return icm.EH_problem_usageError("parValue")

        if storeBase:
            self.__storeBase = storeBase

        if parName:
            self.__parName = parName
        else:
            parName = self.__parName

        if parValue:
            self.__parValue = parValue
        else:
            parValue = self.__parValue

        parNameFullPath = os.path.join(self.__storeBase, parName)
        try: os.makedirs( parNameFullPath, 0o777 )
        except OSError: pass

        fileTreeObject = bpf.fto.FILE_TreeObject(parNameFullPath)

        fileTreeObject.leafCreate()

        parValueFullPath = os.path.join(parNameFullPath, 'value')
        with open(parValueFullPath, "w") as valueFile:
             valueFile.write(str(parValue) +'\n')
             icm.LOG_here("FILE_Param.writeTo path={path} value={value}".
                      format(path=parValueFullPath, value=parValue))

        return parNameFullPath


    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def writeToPath(self, parNameFullPath=None, parValue=None):
        """Write this FILE_Param to storeBase.
        """

        return self.writeTo(storeBase=os.path.dirname(parNameFullPath),
                            parName=os.path.basename(parNameFullPath),
                            parValue=parValue)


    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def writeToFromFile(self, storeBase=None, parName=None, parValueFile=None):
        """Write this FILE_Param to storeBase.

        """
        if self.__storeBase == None and storeBase == None:
            return icm.EH_problem_usageError("storeBase")

        if self.__parName == None and parName == None:
            return icm.EH_problem_usageError("parName")

        if parValueFile == None:
             return icm.EH_problem_usageError("parValueFile")

        if storeBase:
            self.__storeBase = storeBase

        if parName:
            self.__parName = parName
        else:
            parName = self.__parName

        # if parValue:
        #     self.__parValue = parValue
        # else:
        #     parValue = self.__parValue

        parNameFullPath = os.path.join(self.__storeBase, parName)
        try: os.makedirs( parNameFullPath, 0o777 )
        except OSError: pass

        fileTreeObject = bpf.fto.FILE_TreeObject(parNameFullPath)

        fileTreeObject.leafCreate()

        parValueFullPath = os.path.join(parNameFullPath, 'value')
        with open(parValueFullPath, "w") as valueFile:
            with open(parValueFile, "r") as inFile:
                for line in inFile:
                    valueFile.write(line)

        return parNameFullPath


    def reCreationString(self):
        """Provide the string needed to recreate this object.

        """
        return

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  FILE_ParamWriteTo    [[elisp:(org-cycle)][| ]]
"""
@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def FILE_ParamWriteTo(parRoot=None,
                      parName=None,
                      parValue=None,
                      ):
    """
    """

    thisFileParam = FILE_Param(parName=parName, parValue=parValue,)

    if thisFileParam == None:
        return icm.EH_critical_usageError('')

    return thisFileParam.writeTo(storeBase=parRoot)

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  FILE_ParamWriteToPath    [[elisp:(org-cycle)][| ]]
"""
@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def FILE_ParamWriteToPath(parNameFullPath=None,
                          parValue=None,
                          ):
    """
    """

    thisFileParam = FILE_Param()

    if thisFileParam == None:
        return icm.EH_critical_usageError('')

    return thisFileParam.writeToPath(parNameFullPath=parNameFullPath,
                                     parValue=parValue)


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  FILE_ParamWriteToFromFile    [[elisp:(org-cycle)][| ]]
"""
@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def FILE_ParamWriteToFromFile(parRoot=None,
                      parName=None,
                      parValueFile=None,
                      ):
    """
    """

    thisFileParam = FILE_Param(parName=parName)

    if thisFileParam == None:
        return icm.EH_critical_usageError('')

    return thisFileParam.writeToFromFile(storeBase=parRoot, parValueFile=parValueFile)


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  FILE_ParamReadFrom    [[elisp:(org-cycle)][| ]]
"""
@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def FILE_ParamReadFrom(parRoot=None,
                      parName=None,
                      parVerTag=None,
                      ):
    blank = FILE_Param()

    if blank == None:
        return icm.EH_critical_usageError('blank')

    filePar = blank.readFrom(storeBase=parRoot, parName=parName)

    if filePar == None:
        #print('Missing: ' + parRoot + parName)
        raise IOError
        #return EH_critical_usageError('blank')
        return None

    return filePar

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  FILE_ParamValueReadFrom    [[elisp:(org-cycle)][| ]]
"""
@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def FILE_ParamValueReadFrom(parRoot=None,
                      parName=None,
                      parVerTag=None,
                      ):
    blank = FILE_Param()

    if blank == None:
        return icm.EH_critical_usageError('blank')

    filePar = blank.readFrom(storeBase=parRoot, parName=parName)

    if filePar == None:
        print(('Missing: ' + parRoot + parName))
        #raise IOError
        #return icm.EH_critical_usageError('blank')
        return None

    return(filePar.parValueGet())


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  FILE_ParamReadFromPath    [[elisp:(org-cycle)][| ]]
"""
@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def FILE_ParamReadFromPath(parRoot=None,
                      parVerTag=None,
                      ):
    blank = FILE_Param()

    if blank == None:
        return icm.EH_critical_usageError('blank')

    filePar = blank.readFromPath(parRoot)

    if filePar == None:
        #print('Missing: ' + parRoot + parName)
        raise IOError
        #return icm.EH_critical_usageError('blank')

    return filePar


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  FILE_ParamValueReadFromPath    [[elisp:(org-cycle)][| ]]
"""
#@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def FILE_ParamValueReadFromPath(parRoot=None,
                      parVerTag=None,
                      ):
    blank = FILE_Param()

    if blank == None:
        return icm.EH_critical_usageError('blank')

    filePar = blank.readFromPath(parRoot)

    if filePar == None:
        print(('Missing: ' + parRoot))
        return icm.EH_critical_usageError('blank')

    return(filePar.parValueGet())


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  FILE_ParamVerWriteTo    [[elisp:(org-cycle)][| ]]
"""
@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def FILE_ParamVerWriteTo(parRoot=None,
                      parName=None,
                      parVerTag=None,
                      parValue=None,
                      ):
    """ Given ticmoBase, Create parName, then assign parValue to parVerTag
    """

    parFullPath = os.path.join(parRoot, parName)
    try: os.makedirs( parFullPath, 0o777 )
    except OSError: pass

    thisFileParam = FILE_Param(parName=parVerTag,
                                    parValue=parValue,
                                    )

    if thisFileParam == None:
        return icm.EH_critical_usageError('')

    return thisFileParam.writeTo(storeBase=parFullPath)


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  FILE_ParamVerReadFrom    [[elisp:(org-cycle)][| ]]
"""
@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def FILE_ParamVerReadFrom(parRoot=None,
                      parName=None,
                      parVerTag=None,
                      ):
    blank = FILE_Param()

    if blank == None:
        try:  icm.EH_critical_usageError('blank')
        except RuntimeError:  return

    parFullPath = os.path.join(parRoot, parName)
    try: os.makedirs( parFullPath, 0o777 )
    except OSError: pass


    filePar = blank.readFrom(storeBase=parFullPath, parName=parVerTag)

    if filePar == None:
        #print('Missing: ' + parRoot + parName)
        return icm.EH_critical_usageError('blank')

    #print(filePar.parValueGet())
    return filePar



"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class            ::  FILE_ParamDict    [[elisp:(org-cycle)][| ]]
"""

class FILE_ParamDict(object):
    """Maintain a list of FILE_Params.

    NOTYET, nesting of dictionaries.
    """

    def __init__(self):
        self.__fileParamDict = dict()

    def parDictAdd(self, fileParam=None):
        """        """
        self.__fileParamDict.update({fileParam.parNameGet():fileParam})

    def parDictGet(self):
        """        """
        return self.__fileParamDict

    def parNameFind(self, parName=None):
        """        """
        return self.__fileParamDict[parName]

    def readFrom(self, path=None):
        """Read each file's content into a FLAT dictionary item with the filename as key.

        Returns a Dictionary of paramName:FILE_Param.
        """

        absolutePath = os.path.abspath(path)

        if not os.path.isdir(absolutePath):
            return None

        for item in os.listdir(absolutePath):
            fileFullPath = os.path.join(absolutePath, item)
            if os.path.isdir(fileFullPath):

                blank = FILE_Param()

                itemParam = blank.readFrom(storeBase=absolutePath, parName=item)

                self.parDictAdd(itemParam)

        return self.__fileParamDict



"""
*  [[elisp:(org-cycle)][| ]]  /FILE_paramDictRead/ :: *FILE_paramDictRead:* (CMND) [[elisp:(org-cycle)][| ]]
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  FILE_paramDictRead    [[elisp:(org-cycle)][| ]]
"""
@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def FILE_paramDictRead(interactive=icm.Interactivity.Both,
                      inPathList=None):
    """ Old Style CMND
    """
    try: icm.callableEntryEnhancer(type='cmnd')
    except StopIteration:  return(icm.ReturnCode.ExtractionSuccess)

    G = icm.IcmGlobalContext()
    G.curFuncNameSet(ucf.FUNC_currentGet().__name__)

    if icm.Interactivity().interactiveInvokation(interactive):
        icmRunArgs = G.icmRunArgsGet()
        #if cmndArgsLengthValidate(cmndArgs=icmRunArgs.cmndArgs, expected=0, comparison=int__gt):
            #return(ReturnCode.UsageError)

        inPathList = []
        for thisPath in icm.icmRunArgs.cmndArgs:
            inPathList.append(thisPath)
    else:
        if inPathList == None:
            return icm.EH_critical_usageError('inPathList is None and is Non-Interactive')

    for thisPath in inPathList:
        blankDict = FILE_ParamDict()
        thisParamDict = blankDict.readFrom(path=thisPath)
        icm.TM_here('path=' + thisPath)

        if thisParamDict == None:
            continue

        for parName, filePar  in thisParamDict.items():
            print(('parName=' + parName))
            if filePar == None:
                continue
            thisValue=filePar.parValueGetLines()
            if thisValue == None:
                icm.TM_here("Skipping: " + filePar.parNameGet())
                continue
            print((
                filePar.parNameGet() +
                '=' +
                thisValue[0]))
    return


####+BEGIN: bx:icm:python:cmnd:classHead :modPrefix "" :cmndName "FP_readTreeAtBaseDir" :comment "" :parsMand "FPsDir" :parsOpt "" :argsMin "0" :argsMax "0" :asFunc "" :interactiveP ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc    [[elisp:(outline-show-subtree+toggle)][||]] /FP_readTreeAtBaseDir/ parsMand=FPsDir parsOpt= argsMin=0 argsMax=0 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
#+end_org """
class FP_readTreeAtBaseDir(icm.Cmnd):
    cmndParamsMandatory = [ 'FPsDir', ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 0,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
        interactive=False,        # Can also be called non-interactively
        FPsDir=None,         # or Cmnd-Input
    ) -> icm.OpOutcome:
        cmndOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=cmndOutcome):
                return cmndOutcome

        callParamsDict = {'FPsDir': FPsDir, }
        if not icm.cmndCallParamsValidate(callParamsDict, interactive, outcome=cmndOutcome):
            return cmndOutcome
        FPsDir = callParamsDict['FPsDir']

####+END:
        #G = IcmGlobalContext()

        # return FP_readTreeAtBaseDir_f(
        #     interactive=interactive,
        #     outcome = cmndOutcome,
        #     FPsDir=FPsDir,
        # )

        blankParDictObj  = FILE_ParamDict()
        thisParamDict = blankParDictObj.readFrom(path=FPsDir)
        icm.TM_here(f"path={FPsDir}")

        if thisParamDict == None:
            return icm.eh_problem_usageError(
                cmndOutcome,
                "thisParamDict == None",
            )

        if interactive:
            icm.ANN_write(FPsDir)
            FILE_paramDictPrint(thisParamDict)

        return cmndOutcome.set(
            opError=icm.OpError.Success,
            opResults=thisParamDict,
        )

    def cmndDocStr(self): return """
** Reads and recurses through all FPs.  [[elisp:(org-cycle)][| ]]
*** When interactive, also prints out parValues as read.
"""


def cmndCallParamsValidate(
        callParamDict,
        interactive,
        outcome=None,

):
    """Expected to be used in all CMNDs.

MB-2022 --- This is setting the variable not validating it.
    Perhaps the function should have been cmndCallParamsSet.

Usage Pattern:

    if not icm.cmndCallParamValidate(FPsDir, interactive, outcome=cmndOutcome):
       return cmndOutcome
"""
    #G = IcmGlobalContext()
    #if type(callParamOrList) is not list: callParamOrList = [ callParamOrList ]

    if not outcome:
        outcome = icm.OpOutcome()

    for key  in callParamDict:
        # print(f"111 {key}")
        # interactive could be true in two situations:
        # 1) When a cs is executed on cmnd-line.
        # 2) When a cs is invoked with interactive as true.
        # When (2) callParamDict[key] is expcted to be true by having been specified at invokation.
        #
        if not callParamDict[key]:
            # MB-2022 The logic here seems wrong. When non-interactive, only mandattories
            # should be verified.
            # if not interactive:
            #     return eh_problem_usageError(
            #         outcome,
            #         "Missing Non-Interactive Arg {}".format(key),
            #     )
            if interactive:
                exec("callParamDict[key] = IcmGlobalContext().usageParams." + key)
            # print(f"222 {callParamDict[key]}")


    return True



def FILE_paramDictPrint(fileParamDict):
    """ Returns a Dictionary of paramName:FILE_Param.        """
    for parName, filePar  in fileParamDict.items():
        #print('parName=' + parName)
        if filePar == None:
            continue
        thisValue=filePar.parValueGetLines()
        if thisValue == None:
            icm.TM_here("Skipping: " + filePar.parNameGet())
            continue
        if thisValue:
            print((
                filePar.parNameGet() +
                '=' +
                thisValue[0]))
        else: # Empty list
            print((
                filePar.parNameGet() +
                '='))



"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  FILE_paramDictReadDeep    [[elisp:(org-cycle)][| ]]
"""
@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def FILE_paramDictReadDeep(interactive=icm.Interactivity.Both,
                      inPathList=None):
    """
    """
    try: icm.callableEntryEnhancer(type='cmnd')
    except StopIteration:  return(icm.ReturnCode.ExtractionSuccess)

    G = icm.IcmGlobalContext()
    G.curFuncNameSet(ucf.FUNC_currentGet().__name__)

    if icm.Interactivity().interactiveInvokation(interactive):
        icmRunArgs = G.icmRunArgsGet()
        #if cmndArgsLengthValidate(cmndArgs=icmRunArgs.cmndArgs, expected=0, comparison=int__gt):
            #return(ReturnCode.UsageError)

        inPathList = []
        for thisPath in icm.icmRunArgs.cmndArgs:
            inPathList.append(thisPath)
    else:
        if inPathList == None:
            return icm.EH_critical_usageError('inPathList is None and is Non-Interactive')

    fileParamsDict = {}

    for thisPath in inPathList:
        #absolutePath = os.path.abspath(thisPath)

        if not os.path.isdir(thisPath):
            return icm.EH_critical_usageError('Missing Directory: {thisPath}'.format(thisPath=thisPath))

        for root, dirs, files in os.walk(thisPath):
            #print("root={root}".format(root=root))
            #print ("dirs={dirs}".format(dirs=dirs))
            #print ("files={files}".format(files=files))

            thisFileParamValueFile = os.path.join(root, "value")
            if os.path.isfile(thisFileParamValueFile):
                try:
                    fileParam = FILE_ParamReadFromPath(parRoot=root)
                except IOError:
                    icm.EH_problem_info("Missing " + root)
                    continue

                fileParamsDict.update({root:fileParam.parValueGet()})
                if interactive:
                    print((root + "=" + fileParam.parValueGet()))

    return fileParamsDict


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  FILE_parametersReadDeep_PlaceHolder    [[elisp:(org-cycle)][| ]]
"""

def FILE_parametersReadDeep_PlaceHolder(path=None):
    """Read each file's content into a DEEP dictionary item with the filename as key.

    Not Fully Implemeted YET.
    """
    retVal = None

    absolutePath = os.path.abspath(path)

    if not os.path.isdir(absolutePath):
        return retVal

    fileParamsDict = dict()

    for root, dirs, files in os.walk(absolutePath):
        # Each time that we see a dir we will create a new subDict
        print(root)
        print(dirs)
        print(files)

    return fileParamsDict


####+BEGIN: bx:icm:python:section :title "ICM_Param: ICM Parameter (ICM_Param, ICM_ParamDict)"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *ICM_Param: ICM Parameter (ICM_Param, ICM_ParamDict)*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:

ICM_ParamScope = ucf.enum('TargetParam', 'IcmGeneralParam', 'CmndSpecificParam')

####+BEGIN: bx:dblock:python:class :className "ICM_Param" :superClass "" :comment "" :classType "basic"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-basic    :: /ICM_Param/ object  [[elisp:(org-cycle)][| ]]
"""
class ICM_Param(object):
####+END:
     """Representation of an Interactively Invokable Module Parameter (ICM_Param).

     An ICM Parameter is a superset of an argsparse parameter which also includes:
        - CMND relevance (Mandatory and Optional)
        - Maping onto FILE_Params


     ICM_Param is initially used to setup ArgParse and other user-interface parameter aspects.
     """

     def __init__(self,
                  parName=None,
                  parDescription=None,
                  parDataType=None,
                  parDefault=None,
                  parChoices=None,
                  parScope=None,
                  parMetavar=None,
                  parAction='store',                    # Same as argparse's action
                  parNargs=None,                        # Same as argparse's nargs
                  parCmndApplicability=None,             # List of CMNDs to which this ICM is applicable
                  argparseShortOpt=None,
                  argparseLongOpt=None,
                 ):
         '''Constructor'''
         self.__parName = parName
         self.__parValue = None
         self.__parCmndApplicability = parCmndApplicability
         self.__parDescription = parDescription
         self.__parDataType = parDataType
         self.__parDefault = parDefault
         self.__parChoices = parChoices
         self.__parMetavar = parMetavar
         self.parActionSet(parAction)
         self.parNargsSet(parNargs)
         self.__argparseShortOpt =  argparseShortOpt
         self.__argparseLongOpt =  argparseLongOpt

     def __str__(self):
         return  ("""\
parName: {parName}
value: {value}
description: {description}""".
                  format(
                      parName=self.parNameGet(),
                      value=self.parValueGet(),
                      description=self.parDescriptionGet()
                  )
             )

     def parNameGet(self):
         """  """
         return self.__parName

     def parNameSet(self, parName):
         """        """
         self.__parName = parName

     def parValueGet(self):
         """        """
         return self.__parValue

     def parValueSet(self, value):
         """        """
         self.__parValue = value

     def parDescriptionGet(self):
         """        """
         return self.__parDescription

     def parDescriptionSet(self, parDescription):
         """        """
         self.__parDescription = parDescription

     def parDataTypeGet(self):
         """        """
         return self.__parDataType

     def parDataTypeSet(self, parDataType):
         """        """
         self.__parDataType = parDataType

     def parDefaultGet(self):
         """        """
         return self.__parDefault

     def parDefaultSet(self, parDefault):
         """        """
         self.__parDefault = parDefault

     def parChoicesGet(self):
         """        """
         return self.__parChoices

     def parChoicesSet(self, parChoices):
         """        """
         self.__parChoices = parChoices

     def parActionGet(self):
         """        """
         return self.__parAction

     def parActionSet(self, parAction):
         """        """
         self.__parAction = parAction

     def parNargsGet(self):
         """        """
         return self.__parNargs

     def parNargsSet(self, parNargs):
         """        """
         self.__parNargs = parNargs

     def argsparseShortOptGet(self):
         """        """
         return self.__argparseShortOpt

     def argsparseShortOptSet(self, argsparseShortOpt):
         """        """
         self.__argparseShortOpt = argsparseShortOpt

     def argsparseLongOptGet(self):
         """        """
         return self.__argparseLongOpt

     def argsparseLongOptSet(self, argsparseLongOpt):
         """        """
         self.__argparseLongOpt = argsparseLongOpt

     def readFrom(self, parRoot=None, parName=None):
         """Read into a FILE_param content of parBase/parName.

         Returns a FILE_param which was contailed in parBase/parName.
         """

         absoluteParRoot = os.path.abspath(parRoot)

         if not os.path.isdir(absoluteParRoot):
             return None

         absoluteParBase = os.path.join(absoluteParRoot, parName)

         if not os.path.isdir(absoluteParBase):
             return None

         fileParam = self

         self.__parName = parName

         #
         # Now we will fill fileParam based on the directory content
         #
         for item in os.listdir(absoluteParBase):
             fileFullPath = os.path.join(absoluteParBase, item)
             if os.path.isfile(fileFullPath):

                 if item == 'value':
                     lineString = open(fileFullPath, 'r').read()
                     self.parValueSet(lineString)
                     continue

                 # Rest of the files are expected to be attributes

                 lineString = open(fileFullPath, 'r').read()
                 # NOTYET, check for exceptions
                 eval('self.attr' + str(item).title() + 'Set(lineString)')

         return fileParam

     @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
     def writeAsFileParam(
             self,
             parRoot=None,
     ):
         """Writing a FILE_param content of self.

         Returns a FILE_param which was contailed in parBase/parName.
         """

         absoluteParRoot = os.path.abspath(parRoot)

         if not os.path.isdir(absoluteParRoot):
            try: os.makedirs( absoluteParRoot, 0o775 )
            except OSError: pass

         #print absoluteParRoot

         #print
         #print self.parValueGet()

         parValue = self.parValueGet()
         if not parValue:
             parValue = "unSet"

         FILE_ParamWriteTo(
             parRoot=absoluteParRoot,
             parName=self.parNameGet(),
             parValue=parValue,
         )

         varValueFullPath = os.path.join(
             absoluteParRoot,
             self.parNameGet(),
             'description'
         )

         bpf.fto.FV_writeToFilePathAndCreate(
             filePath=varValueFullPath,
             varValue=self.parDescriptionGet(),
         )

         varValueBaseDir = os.path.join(
             absoluteParRoot,
             self.parNameGet(),
             'enums'
         )

         for thisChoice in self.parChoicesGet():
             bpf.fto.FV_writeToBaseDirAndCreate(
                 baseDir=varValueBaseDir,
                 varName=thisChoice,
                 varValue="",
             )

####+BEGIN: bx:icm:py3:func :funcName "readTreeAtBaseDir_wOp" :funcType "wOp" :retType "OpOutcome" :deco "icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)" :argsList ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-wOp      [[elisp:(outline-show-subtree+toggle)][||]] /readTreeAtBaseDir_wOp/ deco=icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)  [[elisp:(org-cycle)][| ]]
#+end_org """
@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def readTreeAtBaseDir_wOp(
####+END:
        fpsDir: typing.AnyStr,
        outcome: typing.Optional[bpf.op.Outcome] = None,
) -> bpf.op.Outcome:
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ] A Wrapped Operation with results
    #+end_org """

    if not outcome:
        outcome = bpf.op.Outcome()

    blankParDictObj  = FILE_ParamDict()
    thisParamDict = blankParDictObj.readFrom(path=fpsDir)
    icm.TM_here(f"path={fpsDir}")

    if thisParamDict == None:
        return icm.eh_problem_usageError(
            outcome,
            "thisParamDict == None",
        )

    # icm.ANN_write(fpsDir)
    # FILE_paramDictPrint(thisParamDict)

    return outcome.set(
        opError=icm.OpError.Success,
        opResults=thisParamDict,
    )

####+BEGIN: bx:icm:py3:func :funcName "parsGetAsDictValue_wOp" :funcType "wOp" :retType "OpOutcome" :deco "default" :argsList "typed"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-wOp      [[elisp:(outline-show-subtree+toggle)][||]] /parsGetAsDictValue_wOp/ deco=default  [[elisp:(org-cycle)][| ]]
#+end_org """
@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def parsGetAsDictValue_wOp(
####+END:
        parNamesList: typing.Optional[list],
        fpsDir: typing.AnyStr,
        outcome: typing.Optional[bpf.op.Outcome] = None,
) -> bpf.op.Outcome:
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ] A Wrapped Operation with results being a dictionary of values.
    if not ~parNamesList~, get all the values.
*** TODO --- NOTYET This needs to be moved to
    #+end_org """

    outcome = readTreeAtBaseDir_wOp(fpsDir, outcome=outcome)

    results = outcome.results

    opResults = dict()
    #opErrors = ""

    if parNamesList:
        for each in parNamesList:
            # NOTYET, If no results[each], we need to record it in opErrors
            if each in results.keys():
                opResults[each] = results[each].parValueGet()
            else:
                opResults[each] = "UnFound"


            #print(f"{each} {eachFpValue}")

    else:
        for eachFpName in results:
            opResults[eachFpName] = results[eachFpName].parValueGet()
            #print(f"{eachFpName} {eachFpValue}")

    return outcome.set(
        opError=icm.OpError.Success,
        opResults=opResults,
    )


####+BEGIN: blee:bxPanel:foldingSection :outLevel 0 :sep nil :title "CmndSvcs" :anchor ""  :extraInfo "Command Services Section"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*     [[elisp:(outline-show-subtree+toggle)][| _CmndSvcs_: |]]  Command Services Section  [[elisp:(org-shifttab)][<)]] E|
#+end_org """
####+END:


"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *File Parameters Get/Set -- Commands*
"""

####+BEGIN: bx:icm:python:cmnd:classHead :cmndName "fpParamsList" :parsMand "fpBase cls" :parsOpt "" :argsMin "0" :argsMax "3" :asFunc "" :interactiveP ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc    [[elisp:(outline-show-subtree+toggle)][||]] <<fpParamsList>> parsMand=fpBase cls parsOpt= argsMin=0 argsMax=3 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
#+end_org """
class fpParamsList(icm.Cmnd):
    cmndParamsMandatory = [ 'fpBase', 'cls', ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 3,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
        interactive=False,        # Can also be called non-interactively
        fpBase=None,         # or Cmnd-Input
        cls=None,         # or Cmnd-Input
        argsList=[],         # or Args-Input
    ) -> icm.OpOutcome:
        cmndOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=cmndOutcome):
                return cmndOutcome
            effectiveArgsList = G.icmRunArgsGet().cmndArgs  # type: ignore
        else:
            effectiveArgsList = argsList

        callParamsDict = {'fpBase': fpBase, 'cls': cls, }
        if not icm.cmndCallParamsValidate(callParamsDict, interactive, outcome=cmndOutcome):
            return cmndOutcome
        fpBase = callParamsDict['fpBase']
        cls = callParamsDict['cls']

        cmndArgsSpecDict = self.cmndArgsSpec()
        if not self.cmndArgsValidate(effectiveArgsList, cmndArgsSpecDict, outcome=cmndOutcome):
            return cmndOutcome
####+END:
        # global fpBaseInst; fpBaseInst = typing.cast(getattr(__main__, cls), None)
        # exec(
        #     "fpBaseInst = __main__.{cls}('{fpBase}',)".format(cls=cls, fpBase=fpBase,),
        #     globals(),
        # )
        # fps_namesWithAbsPath = fpBaseInst.fps_namesWithAbsPath()

        fpBaseInst = pattern.sameInstance(getattr(__main__, cls), fpBase)
        fps_namesWithAbsPath = fpBaseInst.fps_namesWithAbsPath()

        if interactive:
            formatTypes = self.cmndArgsGet("0&2", cmndArgsSpecDict, effectiveArgsList)
        else:
            formatTypes = effectiveArgsList

        if formatTypes:
            if formatTypes[0] == "all":
                    cmndArgsSpec = cmndArgsSpecDict.argPositionFind("0&2")
                    argChoices = cmndArgsSpec.argChoicesGet()
                    argChoices.pop(0)
                    formatTypes = argChoices

        for each in formatTypes:    # type: ignore
            if each == 'basic':
                FP_listIcmParams(fps_namesWithAbsPath,)
            elif each == 'getExamples':
                print("Get Examples Come Here")
            elif each == 'setExamples':
                print("Set Examples Come Here")
            else:
                icm.EH_problem_usageError(f"Unknown {each}")

        return cmndOutcome

####+BEGIN: bx:icm:python:method :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList ""
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-anyOrNone :: /cmndArgsSpec/ retType=bool argsList=nil deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self):
####+END:
        """
***** Cmnd Args Specification
"""
        cmndArgsSpecDict = icm.CmndArgsSpecDict()
        cmndArgsSpecDict.argsDictAdd(
            argPosition="0&2",
            argName="formatTypes",
            argDefault="all",
            argChoices=['all', 'basic', 'setExamples', 'getExamples'],
            argDescription="Action to be specified by rest"
        )

        return cmndArgsSpecDict

####+BEGIN: bx:icm:python:method :methodName "cmndDocStr" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList ""
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-anyOrNone :: /cmndDocStr/ retType=bool argsList=nil deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndDocStr(self):
####+END:
        return """
***** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Returns the full path of the Sr baseDir.
"""


####+BEGIN: bx:icm:python:cmnd:classHead :cmndName "fpParamsSet" :parsMand "fpBase cls" :parsOpt "" :argsMin "0" :argsMax "0" :asFunc "" :interactiveP ""
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  ICM-Cmnd   :: /fpParamsSet/ parsMand=fpBase cls parsOpt= argsMin=0 argsMax=0 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class fpParamsSet(icm.Cmnd):
    cmndParamsMandatory = [ 'fpBase', 'cls', ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 0,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
        interactive=False,        # Can also be called non-interactively
        fpBase=None,         # or Cmnd-Input
        cls=None,         # or Cmnd-Input
    ):
        cmndOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=cmndOutcome):
                return cmndOutcome

        callParamsDict = {'fpBase': fpBase, 'cls': cls, }
        if not icm.cmndCallParamsValidate(callParamsDict, interactive, outcome=cmndOutcome):
            return cmndOutcome
        fpBase = callParamsDict['fpBase']
        cls = callParamsDict['cls']

####+END:
        fpBaseInst = pattern.sameInstance(getattr(__main__, cls), fpBase)
        fps_namesWithAbsPath = fpBaseInst.fps_namesWithAbsPath()  # type: ignore

        FP_writeWithIcmParams(fps_namesWithAbsPath,)

        return cmndOutcome

####+BEGIN: bx:icm:python:method :methodName "cmndDocStr" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList ""
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-anyOrNone :: /cmndDocStr/ retType=bool argsList=nil deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndDocStr(self):
####+END:
        return """
***** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Returns the full path of the Sr baseDir.
"""


####+BEGIN: bx:icm:python:cmnd:classHead :cmndName "fpParamSetWithNameValue" :parsMand "fpBase cls" :parsOpt "" :argsMin "2" :argsMax "2" :asFunc "" :interactiveP ""
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  ICM-Cmnd   :: /fpParamSetWithNameValue/ parsMand=fpBase cls parsOpt= argsMin=2 argsMax=2 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class fpParamSetWithNameValue(icm.Cmnd):
    cmndParamsMandatory = [ 'fpBase', 'cls', ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 2, 'Max': 2,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
        interactive=False,        # Can also be called non-interactively
        fpBase=None,         # or Cmnd-Input
        cls=None,         # or Cmnd-Input
        argsList=[],         # or Args-Input
    ):
        cmndOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=cmndOutcome):
                return cmndOutcome
            effectiveArgsList = G.icmRunArgsGet().cmndArgs  # type: ignore
        else:
            effectiveArgsList = argsList

        callParamsDict = {'fpBase': fpBase, 'cls': cls, }
        if not icm.cmndCallParamsValidate(callParamsDict, interactive, outcome=cmndOutcome):
            return cmndOutcome
        fpBase = callParamsDict['fpBase']
        cls = callParamsDict['cls']

        cmndArgsSpecDict = self.cmndArgsSpec()
        if not self.cmndArgsValidate(effectiveArgsList, cmndArgsSpecDict, outcome=cmndOutcome):
            return cmndOutcome
####+END:
        paramName = self.cmndArgsGet("0", cmndArgsSpecDict, effectiveArgsList)
        paramValue = self.cmndArgsGet("1", cmndArgsSpecDict, effectiveArgsList)

        print(f"{paramName} {paramValue}")

        fpBaseInst = pattern.sameInstance(getattr(__main__, cls), fpBase)

        fpBaseInst.fps_setParam(paramName, paramValue)

        return cmndOutcome


####+BEGIN: bx:icm:python:method :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList ""
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-anyOrNone :: /cmndArgsSpec/ retType=bool argsList=nil deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self):
####+END:
        """
***** Cmnd Args Specification
"""
        cmndArgsSpecDict = icm.CmndArgsSpecDict()
        cmndArgsSpecDict.argsDictAdd(
            argPosition="0",
            argName="paramName",
            argDefault="OopsName",
            argChoices=[],
            argDescription="Action to be specified by rest"
        )
        cmndArgsSpecDict.argsDictAdd(
            argPosition="1",
            argName="paramValue",
            argDefault="OopsValue",
            argChoices=[],
            argDescription="Action to be specified by rest"
        )

        return cmndArgsSpecDict


####+BEGIN: bx:icm:python:method :methodName "cmndDocStr" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList ""
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-anyOrNone :: /cmndDocStr/ retType=bool argsList=nil deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndDocStr(self):
####+END:
        return """
***** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Returns the full path of the Sr baseDir.
"""


####+BEGIN: bx:icm:python:cmnd:classHead :cmndName "fpParamGetWithName" :parsMand "fpBase cls" :parsOpt "" :argsMin "1" :argsMax "1" :asFunc "" :interactiveP ""
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  ICM-Cmnd   :: /fpParamGetWithName/ parsMand=fpBase cls parsOpt= argsMin=1 argsMax=1 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class fpParamGetWithName(icm.Cmnd):
    cmndParamsMandatory = [ 'fpBase', 'cls', ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 1, 'Max': 1,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
        interactive=False,        # Can also be called non-interactively
        fpBase=None,         # or Cmnd-Input
        cls=None,         # or Cmnd-Input
        argsList=[],         # or Args-Input
    ):
        cmndOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=cmndOutcome):
                return cmndOutcome
            effectiveArgsList = G.icmRunArgsGet().cmndArgs  # type: ignore
        else:
            effectiveArgsList = argsList

        callParamsDict = {'fpBase': fpBase, 'cls': cls, }
        if not icm.cmndCallParamsValidate(callParamsDict, interactive, outcome=cmndOutcome):
            return cmndOutcome
        fpBase = callParamsDict['fpBase']
        cls = callParamsDict['cls']

        cmndArgsSpecDict = self.cmndArgsSpec()
        if not self.cmndArgsValidate(effectiveArgsList, cmndArgsSpecDict, outcome=cmndOutcome):
            return cmndOutcome
####+END:
        paramName = self.cmndArgsGet("0", cmndArgsSpecDict, effectiveArgsList)

        fpBaseInst = pattern.sameInstance(getattr(__main__, cls), fpBase)

        paramValue = fpBaseInst.fps_getParam(paramName,)

        print(f"{paramValue.parValueGet()}")

        return cmndOutcome


####+BEGIN: bx:icm:python:method :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList ""
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-anyOrNone :: /cmndArgsSpec/ retType=bool argsList=nil deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self):
####+END:
        """
***** Cmnd Args Specification
"""
        cmndArgsSpecDict = icm.CmndArgsSpecDict()
        cmndArgsSpecDict.argsDictAdd(
            argPosition="0",
            argName="paramName",
            argDefault="OopsName",
            argChoices=[],
            argDescription="Action to be specified by rest"
        )

        return cmndArgsSpecDict


####+BEGIN: bx:icm:python:method :methodName "cmndDocStr" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList ""
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-anyOrNone :: /cmndDocStr/ retType=bool argsList=nil deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndDocStr(self):
####+END:
        return """
***** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Returns the full path of the Sr baseDir.
"""




####+BEGIN: bx:icm:python:cmnd:classHead :cmndName "fpParamsSetDefaults" :parsMand "fpBase cls" :parsOpt "" :argsMin "0" :argsMax "0" :asFunc "" :interactiveP ""
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  ICM-Cmnd   :: /fpParamsSetDefaults/ parsMand=fpBase cls parsOpt= argsMin=0 argsMax=0 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class fpParamsSetDefaults(icm.Cmnd):
    cmndParamsMandatory = [ 'fpBase', 'cls', ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 0,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
        interactive=False,        # Can also be called non-interactively
        fpBase=None,         # or Cmnd-Input
        cls=None,         # or Cmnd-Input
    ):
        cmndOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=cmndOutcome):
                return cmndOutcome

        callParamsDict = {'fpBase': fpBase, 'cls': cls, }
        if not icm.cmndCallParamsValidate(callParamsDict, interactive, outcome=cmndOutcome):
            return cmndOutcome
        fpBase = callParamsDict['fpBase']
        cls = callParamsDict['cls']

####+END:
        fpBaseInst = pattern.sameInstance(getattr(__main__, cls), fpBase)
        fps_namesWithAbsPath = fpBaseInst.fps_namesWithAbsPath()  # type: ignore

        FP_writeDefaultsWithIcmParams(fps_namesWithAbsPath,)

        return cmndOutcome

####+BEGIN: bx:icm:python:method :methodName "cmndDocStr" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList ""
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-anyOrNone :: /cmndDocStr/ retType=bool argsList=nil deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndDocStr(self):
####+END:
        return """
***** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Returns the full path of the Sr baseDir.
"""



####+BEGINNOT: bx:icm:python:cmnd:classHead :cmndName "fpParamsRead" :parsMand "fpBase cls" :parsOpt "" :argsMin "0" :argsMax "999" :asFunc "" :interactiveP ""
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  ICM-Cmnd   :: /fpParamsRead/ parsMand=fpBase cls parsOpt= argsMin=0 argsMax=999 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class fpParamsRead(icm.Cmnd):
    cmndParamsMandatory = [ 'fpBase', 'cls', ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 999,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
        interactive=False,        # Can also be called non-interactively
        fpBase=None,         # or Cmnd-Input
        cls=None,         # or Cmnd-Input
        argsList=[],         # or Args-Input
    ):
        cmndOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=cmndOutcome):
                return cmndOutcome
            effectiveArgsList = G.icmRunArgsGet().cmndArgs  # type: ignore
        else:
            effectiveArgsList = argsList

        callParamsDict = {'fpBase': fpBase, 'cls': cls, }
        if not icm.cmndCallParamsValidate(callParamsDict, interactive, outcome=cmndOutcome):
            return cmndOutcome
        fpBase = callParamsDict['fpBase']
        cls = callParamsDict['cls']

        cmndArgsSpecDict = self.cmndArgsSpec(fpBase, cls,)
        if not self.cmndArgsValidate(effectiveArgsList, cmndArgsSpecDict, outcome=cmndOutcome):
            return cmndOutcome
####+END:
        fpBaseInst = pattern.sameInstance(getattr(__main__, cls), fpBase)
        fpBaseDir = fpBaseInst.fileTreeBaseGet()  # type: ignore

        if interactive:
            formatTypes = self.cmndArgsGet("0&999", cmndArgsSpecDict, effectiveArgsList)
        else:
            formatTypes = effectiveArgsList

        for each in formatTypes:   # type: ignore
            if each == 'all':
                icm.LOG_here(f"""format={each} -- fpBaseDir={fpBaseDir}""")
                FP_readTreeAtBaseDir_CmndOutput(
                    interactive=interactive,
                    fpBaseDir=fpBaseDir,
                    cmndOutcome=cmndOutcome,
                )
            # elif each == 'obj':
            #     cmndOutcome= fpBaseDir.fps_readTree()
            #     if cmndOutcome.error: return cmndOutcome

            #     thisParamDict = fpBaseDir.fps_dictParams
            #     if interactive:
            #         icm.ANN_write(fpBaseDir.fps_absBasePath())
            #         icm.FILE_paramDictPrint(thisParamDict)

            else:
                icm.LOG_here(f"""format={each} -- fpBaseDir={fpBaseDir}""")

                # Read the wholething in:
                # FP_readTreeAtBaseDir_CmndOutput(
                #     interactive=False,
                #     fpBaseDir=fpBaseDir,
                #     cmndOutcome=cmndOutcome,
                # )
                #
                # print(cmndOutcome.results)
                #fpsDict = cmndOutcome.results
                #fp = fpsDict[each]
                #print(fp.parValueGet())

                # Or read one by one.
                fp = icm.FILE_ParamReadFrom(
                    parRoot=fpBaseDir,
                    parName=each,
                )
                print(fp.parValueGet())   # type: ignore

        return cmndOutcome

####+BEGIN: bx:icm:python:method :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList "fpBase cls"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-anyOrNone :: /cmndArgsSpec/ retType=bool argsList=(fpBase cls) deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(
        self,
        fpBase,
        cls,
    ):
####+END:
        """
***** Cmnd Args Specification
"""
        cmndArgsSpecDict = icm.CmndArgsSpecDict()
        argChoices = ['all', ]


        fpBaseInst = pattern.sameInstance(getattr(__main__, cls), fpBase)

        for each in fpBaseInst.fps_namesWithRelPath():  # type: ignore
            argChoices.append(each)

        cmndArgsSpecDict.argsDictAdd(
            argPosition="0&999",
            argName="formatTypes",
            argDefault="all",
            argChoices=argChoices,
            argDescription="One, many or all"
        )

        return cmndArgsSpecDict

####+BEGIN: bx:icm:python:method :methodName "cmndDocStr" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList ""
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-anyOrNone :: /cmndDocStr/ retType=bool argsList=nil deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndDocStr(self):
####+END:
        return """
***** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Returns the full path of the Sr baseDir.
"""


####+BEGIN: bx:icm:python:func :funcName "FP_readTreeAtBaseDir_CmndOutput" :funcType "anyOrNone" :retType "bool" :deco "" :argsList "interactive fpBaseDir cmndOutcome"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Func-anyOrNone :: /FP_readTreeAtBaseDir_CmndOutput/ retType=bool argsList=(interactive fpBaseDir cmndOutcome)  [[elisp:(org-cycle)][| ]]
"""
def FP_readTreeAtBaseDir_CmndOutput(
    interactive,
    fpBaseDir,
    cmndOutcome,
):
####+END:
    """Invokes FP_readTreeAtBaseDir.cmnd as interactive-output only."""
    #
    # Interactive-Output + Chained-Outcome Command Invokation
    #
    FP_readTreeAtBaseDir = icm.FP_readTreeAtBaseDir()
    FP_readTreeAtBaseDir.cmndLineInputOverRide = True
    FP_readTreeAtBaseDir.cmndOutcome = cmndOutcome

    return FP_readTreeAtBaseDir.cmnd(
        interactive=interactive,
        FPsDir=fpBaseDir,
    )


####+BEGIN: bx:icm:python:func :funcName "FP_writeDefaultsWithIcmParams" :funcType "succFail" :retType "bool" :deco "" :argsList "icmParamsAndDests"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Func-succFail :: /FP_writeDefaultsWithIcmParams/ retType=bool argsList=(icmParamsAndDests)  [[elisp:(org-cycle)][| ]]
"""
def FP_writeDefaultsWithIcmParams(
    icmParamsAndDests,
):
####+END:
    G = icm.IcmGlobalContext()
    icmParams = G.icmParamDictGet()

    # Write relevant cmndParams as fileParams
    for eachParam, eachDest  in icmParamsAndDests.items():
        thisIcmParam = icmParams.parNameFind(eachParam)   # type: ignore
        thisIcmParam.parValueSet(thisIcmParam.parDefaultGet())
        thisIcmParam.writeAsFileParam(parRoot=eachDest,)

####+BEGIN: bx:icm:python:func :funcName "FP_writeWithIcmParams" :funcType "succFail" :retType "bool" :deco "" :argsList "icmParamsAndDests"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Func-succFail :: /FP_writeWithIcmParams/ retType=bool argsList=(icmParamsAndDests)  [[elisp:(org-cycle)][| ]]
"""
def FP_writeWithIcmParams(
    icmParamsAndDests,
):
####+END:
    G = icm.IcmGlobalContext()
    icmRunArgs = G.icmRunArgsGet() ; icm.unusedSuppressForEval(icmRunArgs)
    icmParams = G.icmParamDictGet()

    cmndParamsDict = dict()

    # Read from cmndLine into callParamsDict
    for eachKey in icmParamsAndDests:
        cmndParamsDict[eachKey] = None
        try:
            exec("cmndParamsDict[eachKey] = icmRunArgs." + eachKey)
        except AttributeError:
            continue

    # Write relevant cmndParams as fileParams
    for eachParam, eachDest  in icmParamsAndDests.items():
        if cmndParamsDict[eachParam]:
            thisIcmParam = icmParams.parNameFind(eachParam)   # type: ignore
            thisIcmParam.parValueSet(cmndParamsDict[eachParam])
            thisIcmParam.writeAsFileParam(parRoot=eachDest,)


####+BEGIN: bx:icm:python:func :funcName "FP_listIcmParams" :funcType "succFail" :retType "bool" :deco "" :argsList "icmParamsAndDests"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Func-succFail :: /FP_listIcmParams/ retType=bool argsList=(icmParamsAndDests)  [[elisp:(org-cycle)][| ]]
"""
def FP_listIcmParams(
    icmParamsAndDests,
):
####+END:
    G = icm.IcmGlobalContext()
    icmRunArgs = G.icmRunArgsGet() ; icm.unusedSuppressForEval(icmRunArgs)
    icmParams = G.icmParamDictGet()

    # List relevant cmndParams as fileParams
    for eachParam, eachDest  in icmParamsAndDests.items():
        thisIcmParam = icmParams.parNameFind(eachParam)   # type: ignore
        print(thisIcmParam)
        print(eachDest)




####+BEGIN: b:prog:file/endOfFile :extraParams nil
""" #+begin_org
* *[[elisp:(org-cycle)][| END-OF-FILE |]]* :: emacs and org variables and control parameters
#+end_org """
### local variables:
### no-byte-compile: t
### end:
####+END:
