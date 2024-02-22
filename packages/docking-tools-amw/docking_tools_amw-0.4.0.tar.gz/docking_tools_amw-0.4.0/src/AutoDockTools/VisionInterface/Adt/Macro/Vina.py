########################################################################
#
#    Vision Macro - Python source code - file generated by vision
#    Monday 26 July 2010 14:44:06 
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
# $Header: /mnt/raid/services/cvs/python/packages/share1.5/AutoDockTools/VisionInterface/Adt/Macro/Vina.py,v 1.1 2010/07/26 21:47:05 jren Exp $
#
# $Id: Vina.py,v 1.1 2010/07/26 21:47:05 jren Exp $
#

from NetworkEditor.macros import MacroNode
from NetworkEditor.macros import MacroNode
class Vina(MacroNode):

    def __init__(self, constrkw={}, name='Vina', **kw):
        kw['name'] = name
        MacroNode.__init__(*(self,), **kw)

    def beforeAddingToNetwork(self, net):
        MacroNode.beforeAddingToNetwork(self, net)
        from Vision.StandardNodes import stdlib
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
        from Vision.StandardNodes import stdlib
        from WebServices.VisionInterface.WSNodes import wslib
        ## building macro network ##
        Vina_30 = self
        from traceback import print_exc
        from Vision.StandardNodes import stdlib
        from WebServices.VisionInterface.WSNodes import wslib
        masterNet.getEditor().addLibraryInstance(wslib,"WebServices.VisionInterface.WSNodes", "wslib")
        from WebServices.VisionInterface.WSNodes import addOpalServerAsCategory
        try:
            addOpalServerAsCategory("http://kryptonite.nbcr.net/opal2", replace=False)
        except:
            pass
        try:
            ## saving node input Ports ##
            input_Ports_31 = self.macroNetwork.ipNode
            input_Ports_31.configure(*(), **{'paramPanelImmediate': 1, 'expanded': False})
        except:
            print("WARNING: failed to restore MacroInputNode named input Ports in network self.macroNetwork")
            print_exc()
            input_Ports_31=None

        try:
            ## saving node output Ports ##
            output_Ports_32 = self.macroNetwork.opNode
            output_Ports_32.configure(*(), **{'paramPanelImmediate': 1, 'expanded': False})
        except:
            print("WARNING: failed to restore MacroOutputNode named output Ports in network self.macroNetwork")
            print_exc()
            output_Ports_32=None

        try:
            ## saving node AutodockVina_Screening_kryptonite_nbcr_net ##
            from NetworkEditor.items import FunctionNode
            AutodockVina_Screening_kryptonite_nbcr_net_33 = FunctionNode(functionOrString='AutodockVina_Screening_kryptonite_nbcr_net', host="http://kryptonite.nbcr.net/opal2", namedArgs={'num_modes': '', 'energy_range': '', 'seed': '', 'receptor': '', 'size_y': '', 'size_z': '', 'out': '', 'log': '', 'urllib': '', 'exhaustiveness': '', 'localRun': False, 'flex': '', 'center_z': '', 'center_x': '', 'center_y': '', 'userlib': '', 'size_x': '', 'config': '', 'filter': '', 'ligand_db': '', 'cpu': '', 'execPath': ''}, constrkw={'functionOrString': "'AutodockVina_Screening_kryptonite_nbcr_net'", 'host': '"http://kryptonite.nbcr.net/opal2"', 'namedArgs': {'num_modes': '', 'energy_range': '', 'seed': '', 'receptor': '', 'size_y': '', 'size_z': '', 'out': '', 'log': '', 'urllib': '', 'exhaustiveness': '', 'localRun': False, 'flex': '', 'center_z': '', 'center_x': '', 'center_y': '', 'userlib': '', 'size_x': '', 'config': '', 'filter': '', 'ligand_db': '', 'cpu': '', 'execPath': ''}}, name='AutodockVina_Screening_kryptonite_nbcr_net', library=wslib)
            self.macroNetwork.addNode(AutodockVina_Screening_kryptonite_nbcr_net_33,217,185)
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['num_modes'].configure(*(), **{'defaultValue': None})
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['energy_range'].configure(*(), **{'defaultValue': None})
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['seed'].configure(*(), **{'defaultValue': None})
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['receptor'].configure(*(), **{'defaultValue': None})
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['size_y'].configure(*(), **{'defaultValue': None})
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['size_z'].configure(*(), **{'defaultValue': None})
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['out'].configure(*(), **{'defaultValue': None})
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['log'].configure(*(), **{'defaultValue': None})
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['urllib'].configure(*(), **{'defaultValue': None})
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['exhaustiveness'].configure(*(), **{'defaultValue': None})
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['localRun'].configure(*(), **{'defaultValue': None})
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['flex'].configure(*(), **{'defaultValue': None})
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['center_z'].configure(*(), **{'defaultValue': None})
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['center_x'].configure(*(), **{'defaultValue': None})
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['center_y'].configure(*(), **{'defaultValue': None})
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['userlib'].configure(*(), **{'defaultValue': None})
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['size_x'].configure(*(), **{'defaultValue': None})
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['config'].configure(*(), **{'defaultValue': None, 'required': True})
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['filter'].configure(*(), **{'defaultValue': None})
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['ligand_db'].configure(*(), **{'defaultValue': None})
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['cpu'].configure(*(), **{'defaultValue': None})
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['execPath'].configure(*(), **{'defaultValue': None})
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['num_modes'].widget.configure(*(), **{'choices': ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10')})
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['num_modes'].widget.set(r"", run=False)
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['energy_range'].widget.configure(*(), **{'choices': ('1', '2', '3')})
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['energy_range'].widget.set(r"", run=False)
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['seed'].widget.set(r"", run=False)
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['receptor'].rebindWidget()
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['receptor'].widget.set(r"", run=False)
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['receptor'].unbindWidget()
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['size_y'].widget.set(r"", run=False)
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['size_z'].widget.set(r"", run=False)
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['out'].widget.set(r"", run=False)
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['log'].widget.set(r"", run=False)
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['urllib'].rebindWidget()
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['urllib'].widget.set(r"", run=False)
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['urllib'].unbindWidget()
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['exhaustiveness'].widget.configure(*(), **{'choices': ('1', '2', '3', '4', '5', '6', '7', '8')})
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['exhaustiveness'].widget.set(r"", run=False)
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['localRun'].widget.set(0, run=False)
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['flex'].widget.set(r"", run=False)
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['center_z'].widget.set(r"", run=False)
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['center_x'].widget.set(r"", run=False)
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['center_y'].widget.set(r"", run=False)
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['userlib'].widget.set(r"", run=False)
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['size_x'].widget.set(r"", run=False)
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['config'].rebindWidget()
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['config'].widget.set(r"", run=False)
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['config'].unbindWidget()
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['filter'].rebindWidget()
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['filter'].widget.set(r"", run=False)
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['filter'].unbindWidget()
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['ligand_db'].widget.configure(*(), **{'choices': ('sample', 'NCIDS_SC', 'NCI_DS1', 'NCI_DS2', 'human_metabolome', 'chembridge_building_blocks', 'drugbank_nutraceutics', 'drugbank_smallmol', 'asinex', 'fda_approved', 'otava', 'zinc_natural_products')})
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['ligand_db'].widget.set(r"", run=False)
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['cpu'].widget.configure(*(), **{'choices': ('1', '2')})
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['cpu'].widget.set(r"", run=False)
            AutodockVina_Screening_kryptonite_nbcr_net_33.inputPortByName['execPath'].widget.set(r"", run=False)
            AutodockVina_Screening_kryptonite_nbcr_net_33.configure(*(), **{'paramPanelImmediate': 1, 'expanded': False})
        except:
            print("WARNING: failed to restore FunctionNode named AutodockVina_Screening_kryptonite_nbcr_net in network self.macroNetwork")
            print_exc()
            AutodockVina_Screening_kryptonite_nbcr_net_33=None

        try:
            ## saving node PrepareVinaInputs ##
            from Vision.StandardNodes import Generic
            PrepareVinaInputs_34 = Generic(constrkw={}, name='PrepareVinaInputs', library=stdlib)
            self.macroNetwork.addNode(PrepareVinaInputs_34,140,107)
            PrepareVinaInputs_34.addInputPort(*(), **{'singleConnection': True, 'name': 'receptor_obj', 'cast': True, 'datatype': 'receptor_prepared', 'defaultValue': None, 'required': True, 'height': 8, 'width': 12, 'shape': 'triangle', 'color': '#009900', 'originalDatatype': 'None'})
            PrepareVinaInputs_34.addInputPort(*(), **{'singleConnection': True, 'name': 'ligand_obj', 'cast': True, 'datatype': 'LigandDB', 'defaultValue': None, 'required': True, 'height': 8, 'width': 12, 'shape': 'rect', 'color': '#FFCCFF', 'originalDatatype': 'None'})
            PrepareVinaInputs_34.addOutputPort(*(), **{'name': 'receptor_file', 'datatype': 'string', 'height': 8, 'width': 12, 'shape': 'oval', 'color': 'white'})
            PrepareVinaInputs_34.addOutputPort(*(), **{'name': 'ligand_lib', 'datatype': 'string', 'height': 8, 'width': 12, 'shape': 'oval', 'color': 'white'})
            PrepareVinaInputs_34.addOutputPort(*(), **{'name': 'filter_file', 'datatype': 'string', 'height': 8, 'width': 12, 'shape': 'oval', 'color': 'white'})
            code = """def doit(self, receptor_obj, ligand_obj):
        receptor_file = receptor_obj.path
        filter_file = ligand_obj.filter_file
        ligand_lib = ligand_obj.loc

        if receptor_obj.type == "local":
            if not(os.path.exists(receptor_file)):
                print "ERROR: receptor_file " + receptor_file + " does not exist"
                return '''stop'''
        
	pass
        self.outputData(receptor_file=receptor_file, ligand_lib=ligand_lib, filter_file=filter_file)
## to ouput data on port receptor_file use
## self.outputData(receptor_file=data)
## to ouput data on port ligand_lib use
## self.outputData(ligand_lib=data)
## to ouput data on port filter_file use
## self.outputData(filter_file=data)






"""
            PrepareVinaInputs_34.configure(function=code)
            PrepareVinaInputs_34.configure(*(), **{'paramPanelImmediate': 1, 'expanded': False})
        except:
            print("WARNING: failed to restore Generic named PrepareVinaInputs in network self.macroNetwork")
            print_exc()
            PrepareVinaInputs_34=None

        try:
            ## saving node GetMainURLFromList ##
            from WebServices.VisionInterface.WSNodes import GetMainURLFromListNode
            GetMainURLFromList_35 = GetMainURLFromListNode(constrkw={}, name='GetMainURLFromList', library=wslib)
            self.macroNetwork.addNode(GetMainURLFromList_35,217,248)
            GetMainURLFromList_35.inputPortByName['urls'].configure(*(), **{'defaultValue': None})
            GetMainURLFromList_35.configure(*(), **{'paramPanelImmediate': 1, 'expanded': False})
        except:
            print("WARNING: failed to restore GetMainURLFromListNode named GetMainURLFromList in network self.macroNetwork")
            print_exc()
            GetMainURLFromList_35=None

        #self.macroNetwork.run()
        self.macroNetwork.freeze()

        ## saving connections for network Vina ##
        if PrepareVinaInputs_34 is not None and AutodockVina_Screening_kryptonite_nbcr_net_33 is not None:
            try:
                self.macroNetwork.connectNodes(
                    PrepareVinaInputs_34, AutodockVina_Screening_kryptonite_nbcr_net_33, "receptor_file", "receptor", blocking=True
                    , splitratio=[0.48630431331124768, 0.72717758735716731])
            except:
                print("WARNING: failed to restore connection between PrepareVinaInputs_34 and AutodockVina_Screening_kryptonite_nbcr_net_33 in network self.macroNetwork")
        if PrepareVinaInputs_34 is not None and AutodockVina_Screening_kryptonite_nbcr_net_33 is not None:
            try:
                self.macroNetwork.connectNodes(
                    PrepareVinaInputs_34, AutodockVina_Screening_kryptonite_nbcr_net_33, "ligand_lib", "urllib", blocking=True
                    , splitratio=[0.61963739449043087, 0.74955133389937689])
            except:
                print("WARNING: failed to restore connection between PrepareVinaInputs_34 and AutodockVina_Screening_kryptonite_nbcr_net_33 in network self.macroNetwork")
        if PrepareVinaInputs_34 is not None and AutodockVina_Screening_kryptonite_nbcr_net_33 is not None:
            try:
                self.macroNetwork.connectNodes(
                    PrepareVinaInputs_34, AutodockVina_Screening_kryptonite_nbcr_net_33, "filter_file", "filter", blocking=True
                    , splitratio=[0.32670226336274166, 0.25123642944789149])
            except:
                print("WARNING: failed to restore connection between PrepareVinaInputs_34 and AutodockVina_Screening_kryptonite_nbcr_net_33 in network self.macroNetwork")
        if AutodockVina_Screening_kryptonite_nbcr_net_33 is not None and GetMainURLFromList_35 is not None:
            try:
                self.macroNetwork.connectNodes(
                    AutodockVina_Screening_kryptonite_nbcr_net_33, GetMainURLFromList_35, "result", "urls", blocking=True
                    , splitratio=[0.23401196873379349, 0.68593608346615742])
            except:
                print("WARNING: failed to restore connection between AutodockVina_Screening_kryptonite_nbcr_net_33 and GetMainURLFromList_35 in network self.macroNetwork")
        output_Ports_32 = self.macroNetwork.opNode
        if GetMainURLFromList_35 is not None and output_Ports_32 is not None:
            try:
                self.macroNetwork.connectNodes(
                    GetMainURLFromList_35, output_Ports_32, "newurl", "new", blocking=True
                    , splitratio=[0.26588001265563421, 0.34355863787969732])
            except:
                print("WARNING: failed to restore connection between GetMainURLFromList_35 and output_Ports_32 in network self.macroNetwork")
        input_Ports_31 = self.macroNetwork.ipNode
        if input_Ports_31 is not None and PrepareVinaInputs_34 is not None:
            try:
                self.macroNetwork.connectNodes(
                    input_Ports_31, PrepareVinaInputs_34, "new", "receptor_obj", blocking=True
                    , splitratio=[0.59193136382656331, 0.41134942510734418])
            except:
                print("WARNING: failed to restore connection between input_Ports_31 and PrepareVinaInputs_34 in network self.macroNetwork")
        if input_Ports_31 is not None and PrepareVinaInputs_34 is not None:
            try:
                self.macroNetwork.connectNodes(
                    input_Ports_31, PrepareVinaInputs_34, "new", "ligand_obj", blocking=True
                    , splitratio=[0.29092159940560591, 0.60619808825531374])
            except:
                print("WARNING: failed to restore connection between input_Ports_31 and PrepareVinaInputs_34 in network self.macroNetwork")
        if input_Ports_31 is not None and AutodockVina_Screening_kryptonite_nbcr_net_33 is not None:
            try:
                self.macroNetwork.connectNodes(
                    input_Ports_31, AutodockVina_Screening_kryptonite_nbcr_net_33, "new", "config", blocking=True
                    , splitratio=[0.24239548372031838, 0.55842775396640953])
            except:
                print("WARNING: failed to restore connection between input_Ports_31 and AutodockVina_Screening_kryptonite_nbcr_net_33 in network self.macroNetwork")
        self.macroNetwork.runOnNewData.value = True

        ## modifying MacroInputNode dynamic ports
        input_Ports_31 = self.macroNetwork.ipNode
        input_Ports_31.outputPorts[1].configure(name='PrepareVinaInputs_receptor_obj')
        input_Ports_31.outputPorts[2].configure(name='PrepareVinaInputs_ligand_obj')
        input_Ports_31.outputPorts[3].configure(name='AutodockVina_Screening_kryptonite_nbcr_net_config')

        ## modifying MacroOutputNode dynamic ports
        output_Ports_32 = self.macroNetwork.opNode
        output_Ports_32.inputPorts[1].configure(singleConnection='auto')
        output_Ports_32.inputPorts[1].configure(name='GetMainURLFromList_newurl')
        ## configure MacroNode input ports
        Vina_30.inputPorts[0].configure(name='PrepareVinaInputs_receptor_obj')
        Vina_30.inputPorts[0].configure(datatype='receptor_prepared')
        Vina_30.inputPorts[1].configure(name='PrepareVinaInputs_ligand_obj')
        Vina_30.inputPorts[1].configure(datatype='LigandDB')
        Vina_30.inputPorts[2].configure(name='AutodockVina_Screening_kryptonite_nbcr_net_config')
        Vina_30.inputPorts[2].configure(datatype='string')
        ## configure MacroNode output ports
        Vina_30.outputPorts[0].configure(name='GetMainURLFromList_newurl')
        Vina_30.outputPorts[0].configure(datatype='string')

        Vina_30.shrink()

        ## reset modifications ##
        Vina_30.resetTags()
        Vina_30.buildOriginalList()
