########################################################################
#
#    Vision Macro - Python source code - file generated by vision
#    Thursday 05 May 2011 15:54:07 
#    
#       The Scripps Research Institute (TSRI)
#       Molecular Graphics Lab
#       La Jolla, CA 92037, USA
#
# Copyright: Daniel Stoffler, Michel Sanner and TSRI
#   
# revision: Guillaume Vareille
#  
#########################################################################
#
# $Header: /mnt/raid/services/cvs/python/packages/share1.5/AutoDockTools/VisionInterface/Adt/Macro/PrepareSingleLigand.py,v 1.2 2011/05/05 23:05:56 jren Exp $
#
# $Id: PrepareSingleLigand.py,v 1.2 2011/05/05 23:05:56 jren Exp $
#

from NetworkEditor.macros import MacroNode
from NetworkEditor.macros import MacroNode
class PrepareSingleLigand(MacroNode):
    '''
        Runs web service for prepare single ligand
        
        Input 1: Unprepared ligand file
        Input 2: Directory to download output to

        Output 1: Path to downloaded prepared receptor file
        Output 2: URL to prepared receptor 
    '''

    def __init__(self, constrkw={}, name='PrepareSingleLigand', **kw):
        kw['name'] = name
        MacroNode.__init__(*(self,), **kw)

    def beforeAddingToNetwork(self, net):
        MacroNode.beforeAddingToNetwork(self, net)
        from WebServices.VisionInterface.WSNodes import wslib
        net.getEditor().addLibraryInstance(wslib,"WebServices.VisionInterface.WSNodes", "wslib")
        from WebServices.VisionInterface.WSNodes import addOpalServerAsCategory
        try:
            addOpalServerAsCategory("http://kryptonite.nbcr.net/opal2", replace=False)
        except:
            pass

    def afterAddingToNetwork(self):
        masterNet = self.macroNetwork
        from NetworkEditor.macros import MacroNode
        MacroNode.afterAddingToNetwork(self)
        from WebServices.VisionInterface.WSNodes import wslib
        ## building macro network ##
        PrepareSingleLigand_18 = self
        from traceback import print_exc
        from WebServices.VisionInterface.WSNodes import wslib
        masterNet.getEditor().addLibraryInstance(wslib,"WebServices.VisionInterface.WSNodes", "wslib")
        from WebServices.VisionInterface.WSNodes import addOpalServerAsCategory
        try:
            addOpalServerAsCategory("http://kryptonite.nbcr.net/opal2", replace=False)
        except:
            pass
        try:
            ## saving node input Ports ##
            input_Ports_19 = self.macroNetwork.ipNode
            input_Ports_19.configure(*(), **{'paramPanelImmediate': 1, 'expanded': False})
        except:
            print("WARNING: failed to restore MacroInputNode named input Ports in network self.macroNetwork")
            print_exc()
            input_Ports_19=None

        try:
            ## saving node output Ports ##
            output_Ports_20 = self.macroNetwork.opNode
            output_Ports_20.configure(*(), **{'paramPanelImmediate': 1, 'expanded': False})
        except:
            print("WARNING: failed to restore MacroOutputNode named output Ports in network self.macroNetwork")
            print_exc()
            output_Ports_20=None

        try:
            ## saving node PrepareLigandSingle_kryptonite_nbcr_net ##
            from NetworkEditor.items import FunctionNode
            PrepareLigandSingle_kryptonite_nbcr_net_21 = FunctionNode(functionOrString='PrepareLigandSingle_kryptonite_nbcr_net', host="http://kryptonite.nbcr.net/opal2", namedArgs={'A': '', 'C': False, 'B': '', 'ligand': '', 'g': False, 'F': False, 'I': '', 'M': False, 'p': '', 'R': '', 'U': '', 'v': False, 'Z': False, 'localRun': False, 'execPath': '', 'd': ''}, constrkw={'functionOrString': "'PrepareLigandSingle_kryptonite_nbcr_net'", 'host': '"http://kryptonite.nbcr.net/opal2"', 'namedArgs': {'A': '', 'C': False, 'B': '', 'ligand': '', 'g': False, 'F': False, 'I': '', 'M': False, 'p': '', 'R': '', 'U': '', 'v': False, 'Z': False, 'localRun': False, 'execPath': '', 'd': ''}}, name='PrepareLigandSingle_kryptonite_nbcr_net', library=wslib)
            self.macroNetwork.addNode(PrepareLigandSingle_kryptonite_nbcr_net_21,217,92)
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['A'].configure(*(), **{'defaultValue': None})
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['C'].configure(*(), **{'defaultValue': None})
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['B'].configure(*(), **{'defaultValue': None})
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['ligand'].configure(*(), **{'defaultValue': None, 'required': True})
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['g'].configure(*(), **{'defaultValue': None})
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['F'].configure(*(), **{'defaultValue': None})
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['I'].configure(*(), **{'defaultValue': None})
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['M'].configure(*(), **{'defaultValue': None})
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['p'].configure(*(), **{'defaultValue': None})
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['R'].configure(*(), **{'defaultValue': None})
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['U'].configure(*(), **{'defaultValue': None})
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['v'].configure(*(), **{'defaultValue': None})
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['Z'].configure(*(), **{'defaultValue': None})
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['localRun'].configure(*(), **{'defaultValue': None})
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['execPath'].configure(*(), **{'defaultValue': None})
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['d'].configure(*(), **{'defaultValue': None})
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['A'].widget.configure(*(), **{'choices': ('bonds_hydrogens', 'bonds', 'hydrogens')})
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['A'].widget.set(r"", run=False)
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['C'].widget.set(0, run=False)
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['B'].widget.set(r"", run=False)
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['ligand'].rebindWidget()
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['ligand'].widget.set(r"", run=False)
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['ligand'].unbindWidget()
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['g'].widget.set(0, run=False)
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['F'].widget.set(0, run=False)
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['I'].widget.set(r"", run=False)
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['M'].widget.set(0, run=False)
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['p'].widget.set(r"", run=False)
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['R'].widget.set(r"", run=False)
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['U'].widget.configure(*(), **{'choices': ('nphs_lps', 'nphs', 'lps')})
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['U'].widget.set(r"", run=False)
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['v'].widget.set(0, run=False)
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['Z'].widget.set(0, run=False)
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['localRun'].widget.set(0, run=False)
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['execPath'].widget.set(r"", run=False)
            PrepareLigandSingle_kryptonite_nbcr_net_21.inputPortByName['d'].widget.set(r"", run=False)
            PrepareLigandSingle_kryptonite_nbcr_net_21.configure(*(), **{'paramPanelImmediate': 1, 'expanded': False})
        except:
            print("WARNING: failed to restore FunctionNode named PrepareLigandSingle_kryptonite_nbcr_net in network self.macroNetwork")
            print_exc()
            PrepareLigandSingle_kryptonite_nbcr_net_21=None

        try:
            ## saving node GetURLFromList ##
            from WebServices.VisionInterface.WSNodes import GetURLFromListNode
            GetURLFromList_22 = GetURLFromListNode(constrkw={}, name='GetURLFromList', library=wslib)
            self.macroNetwork.addNode(GetURLFromList_22,217,171)
            GetURLFromList_22.inputPortByName['urllist'].configure(*(), **{'defaultValue': None})
            GetURLFromList_22.inputPortByName['ext'].configure(*(), **{'defaultValue': None})
            GetURLFromList_22.inputPortByName['ext'].widget.set(r"pdbqt", run=False)
            GetURLFromList_22.configure(*(), **{'paramPanelImmediate': 1})
        except:
            print("WARNING: failed to restore GetURLFromListNode named GetURLFromList in network self.macroNetwork")
            print_exc()
            GetURLFromList_22=None

        #self.macroNetwork.run()
        self.macroNetwork.freeze()

        ## saving connections for network PrepareSingleLigand ##
        if PrepareLigandSingle_kryptonite_nbcr_net_21 is not None and GetURLFromList_22 is not None:
            try:
                self.macroNetwork.connectNodes(
                    PrepareLigandSingle_kryptonite_nbcr_net_21, GetURLFromList_22, "result", "urllist", blocking=True
                    , splitratio=[0.32868238447942777, 0.66102005033481848])
            except:
                print("WARNING: failed to restore connection between PrepareLigandSingle_kryptonite_nbcr_net_21 and GetURLFromList_22 in network self.macroNetwork")
        output_Ports_20 = self.macroNetwork.opNode
        if GetURLFromList_22 is not None and output_Ports_20 is not None:
            try:
                self.macroNetwork.connectNodes(
                    GetURLFromList_22, output_Ports_20, "url", "new", blocking=True
                    , splitratio=[0.24357139972148803, 0.60352121442381113])
            except:
                print("WARNING: failed to restore connection between GetURLFromList_22 and output_Ports_20 in network self.macroNetwork")
        input_Ports_19 = self.macroNetwork.ipNode
        if input_Ports_19 is not None and PrepareLigandSingle_kryptonite_nbcr_net_21 is not None:
            try:
                self.macroNetwork.connectNodes(
                    input_Ports_19, PrepareLigandSingle_kryptonite_nbcr_net_21, "new", "ligand", blocking=True
                    , splitratio=[0.58130558930809739, 0.62673128127582967])
            except:
                print("WARNING: failed to restore connection between input_Ports_19 and PrepareLigandSingle_kryptonite_nbcr_net_21 in network self.macroNetwork")
        self.macroNetwork.runOnNewData.value = True

        ## modifying MacroInputNode dynamic ports
        input_Ports_19 = self.macroNetwork.ipNode
        input_Ports_19.outputPorts[1].configure(name='PrepareLigandSingle_kryptonite_nbcr_net_ligand')

        ## modifying MacroOutputNode dynamic ports
        output_Ports_20 = self.macroNetwork.opNode
        output_Ports_20.inputPorts[1].configure(singleConnection='auto')
        output_Ports_20.inputPorts[1].configure(name='GetURLFromList_url')
        ## configure MacroNode input ports
        PrepareSingleLigand_18.inputPorts[0].configure(name='PrepareLigandSingle_kryptonite_nbcr_net_ligand')
        PrepareSingleLigand_18.inputPorts[0].configure(datatype='string')
        ## configure MacroNode output ports
        PrepareSingleLigand_18.outputPorts[0].configure(name='GetURLFromList_url')
        PrepareSingleLigand_18.outputPorts[0].configure(datatype='string')

        PrepareSingleLigand_18.shrink()

        ## reset modifications ##
        PrepareSingleLigand_18.resetTags()
        PrepareSingleLigand_18.buildOriginalList()
