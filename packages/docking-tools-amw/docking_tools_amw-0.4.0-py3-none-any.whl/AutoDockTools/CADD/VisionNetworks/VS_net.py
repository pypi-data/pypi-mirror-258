#!/bin/ksh ~/.mgltools/pythonsh
########################################################################
#
#    Vision Network - Python source code - file generated by vision
#    Monday 26 July 2010 15:53:39 
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
# $Header: /mnt/raid/services/cvs/python/packages/share1.5/AutoDockTools/CADD/VisionNetworks/VS_net.py,v 1.1 2010/11/06 00:59:32 sanner Exp $
#
# $Id: VS_net.py,v 1.1 2010/11/06 00:59:32 sanner Exp $
#


if __name__=='__main__':
    from sys import argv
    if '--help' in argv or '-h' in argv or '-w' in argv: # run without Vision
        withoutVision = True
        from Vision.VPE import NoGuiExec
        ed = NoGuiExec()
        from NetworkEditor.net import Network
        import os
        masterNet = Network("process-"+str(os.getpid()))
        ed.addNetwork(masterNet)
    else: # run as a stand alone application while vision is hidden
        withoutVision = False
        from Vision import launchVisionToRunNetworkAsApplication, mainLoopVisionToRunNetworkAsApplication
	if '-noSplash' in argv:
	    splash = False
	else:
	    splash = True
        masterNet = launchVisionToRunNetworkAsApplication(splash=splash)
        import os
        masterNet.filename = os.path.abspath(__file__)
from traceback import print_exc
## loading libraries ##
from AutoDockTools.VisionInterface.Adt import Adt
from WebServices.VisionInterface.WSNodes import wslib
from Vision.StandardNodes import stdlib
try:
    masterNet
except (NameError, AttributeError): # we run the network outside Vision
    from NetworkEditor.net import Network
    masterNet = Network()

masterNet.getEditor().addLibraryInstance(Adt,"AutoDockTools.VisionInterface.Adt", "Adt")

masterNet.getEditor().addLibraryInstance(wslib,"WebServices.VisionInterface.WSNodes", "wslib")

masterNet.getEditor().addLibraryInstance(stdlib,"Vision.StandardNodes", "stdlib")

from WebServices.VisionInterface.WSNodes import addOpalServerAsCategory
try:
    addOpalServerAsCategory("http://ws.nbcr.net/opal2", replace=False)
except:
    pass
try:
    addOpalServerAsCategory("http://kryptonite.nbcr.net/opal2", replace=False)
except:
    pass
try:
    ## saving node iterate ##
    from Vision.StandardNodes import Iterate
    iterate_0 = Iterate(constrkw={}, name='iterate', library=stdlib)
    masterNet.addNode(iterate_0,16,228)
    iterate_0.inputPortByName['stopOnFailure'].widget.set(0, run=False)
    iterate_0.configure(*(), **{'paramPanelImmediate': 1})
except:
    print("WARNING: failed to restore Iterate named iterate in network masterNet")
    print_exc()
    iterate_0=None

try:
    ## saving node VirtualScreening ##
    from Adt.Macro.VirtualScreening import VirtualScreening
    VirtualScreening_1 = VirtualScreening(constrkw={}, name='VirtualScreening', library=Adt)
    masterNet.addNode(VirtualScreening_1,216,497)
    VirtualScreening_1.configure(*(), **{'paramPanelImmediate': 1, 'expanded': False})
    PrepareReceptor_4 = VirtualScreening_1.macroNetwork.nodes[2]
    Pdb2pqrWS_7 = PrepareReceptor_4.macroNetwork.nodes[2]
    Pdb2pqrOpalService_ws_nbcr_net_11 = Pdb2pqrWS_7.macroNetwork.nodes[3]
    Pdb2pqrOpalService_ws_nbcr_net_11.inputPortByName['noopt'].widget.set(0, run=False)
    Pdb2pqrOpalService_ws_nbcr_net_11.inputPortByName['phi'].widget.set(0, run=False)
    Pdb2pqrOpalService_ws_nbcr_net_11.inputPortByName['psi'].widget.set(0, run=False)
    Pdb2pqrOpalService_ws_nbcr_net_11.inputPortByName['verbose'].widget.set(1, run=False)
    Pdb2pqrOpalService_ws_nbcr_net_11.inputPortByName['chain'].widget.set(0, run=False)
    Pdb2pqrOpalService_ws_nbcr_net_11.inputPortByName['nodebump'].widget.set(0, run=False)
    Pdb2pqrOpalService_ws_nbcr_net_11.inputPortByName['chi'].widget.set(0, run=False)
    Pdb2pqrOpalService_ws_nbcr_net_11.inputPortByName['ligand'].widget.set(r"", run=False)
    Pdb2pqrOpalService_ws_nbcr_net_11.inputPortByName['hbond'].widget.set(0, run=False)
    Pdb2pqrOpalService_ws_nbcr_net_11.inputPortByName['with_ph'].widget.set(r"", run=False)
    Pdb2pqrOpalService_ws_nbcr_net_11.inputPortByName['forcefield'].widget.configure(*(), **{'choices': ('AMBER', 'CHARMM', 'PARSE', 'TYL06')})
    Pdb2pqrOpalService_ws_nbcr_net_11.inputPortByName['forcefield'].widget.set(r"AMBER", run=False)
    Pdb2pqrOpalService_ws_nbcr_net_11.inputPortByName['clean'].widget.set(0, run=False)
    Pdb2pqrOpalService_ws_nbcr_net_11.inputPortByName['inId'].widget.set(r"", run=False)
    Pdb2pqrOpalService_ws_nbcr_net_11.inputPortByName['apbs_input'].widget.set(0, run=False)
    Pdb2pqrOpalService_ws_nbcr_net_11.inputPortByName['ffout'].widget.configure(*(), **{'choices': ('AMBER', 'CHARMM', 'PARSE', 'TYL06')})
    Pdb2pqrOpalService_ws_nbcr_net_11.inputPortByName['ffout'].widget.set(r"", run=False)
    Pdb2pqrOpalService_ws_nbcr_net_11.inputPortByName['localRun'].widget.set(0, run=False)
    Pdb2pqrOpalService_ws_nbcr_net_11.inputPortByName['rama'].widget.set(0, run=False)
    Pdb2pqrOpalService_ws_nbcr_net_11.inputPortByName['execPath'].widget.set(r"", run=False)
    Pdb2pqrOpalService_ws_nbcr_net_11.inputPortByName['assign_only'].widget.set(0, run=False)
    GetURLFromList_12 = Pdb2pqrWS_7.macroNetwork.nodes[4]
    GetURLFromList_12.inputPortByName['ext'].widget.set(r"pqr", run=False)

    ## saving connections for network Pdb2pqrWS ##
    Pdb2pqrWS_7.macroNetwork.freeze()
    Pdb2pqrWS_7.macroNetwork.unfreeze()

    ## modifying MacroInputNode dynamic ports
    input_Ports_8 = Pdb2pqrWS_7.macroNetwork.ipNode
    input_Ports_8.outputPorts[1].configure(name='CheckFileFormat_value')

    ## modifying MacroOutputNode dynamic ports
    output_Ports_9 = Pdb2pqrWS_7.macroNetwork.opNode
    output_Ports_9.inputPorts[1].configure(singleConnection='auto')
    output_Ports_9.inputPorts[2].configure(singleConnection='auto')
    output_Ports_9.inputPorts[1].configure(name='UpdateReceptor_receptor_obj')
    output_Ports_9.inputPorts[2].configure(name='UpdateReceptor_pdb2pqr_result')
    Pdb2pqrWS_7.inputPorts[0].configure(name='CheckFileFormat_value')
    Pdb2pqrWS_7.inputPorts[0].configure(datatype='receptor')
    ## configure MacroNode input ports
    Pdb2pqrWS_7.outputPorts[0].configure(name='UpdateReceptor_receptor_obj')
    Pdb2pqrWS_7.outputPorts[0].configure(datatype='receptor')
    Pdb2pqrWS_7.outputPorts[1].configure(name='UpdateReceptor_pdb2pqr_result')
    Pdb2pqrWS_7.outputPorts[1].configure(datatype='string')
    ## configure MacroNode output ports
    Pdb2pqrWS_7.shrink()
    PrepareReceptorWS_14 = PrepareReceptor_4.macroNetwork.nodes[3]
    PrepareReceptorOpalService_ws_nbcr_net_18 = PrepareReceptorWS_14.macroNetwork.nodes[3]
    PrepareReceptorOpalService_ws_nbcr_net_18.inputPortByName['o'].widget.set(r"", run=False)
    PrepareReceptorOpalService_ws_nbcr_net_18.inputPortByName['v'].widget.set(0, run=False)
    PrepareReceptorOpalService_ws_nbcr_net_18.inputPortByName['localRun'].widget.set(0, run=False)
    PrepareReceptorOpalService_ws_nbcr_net_18.inputPortByName['execPath'].widget.set(r"", run=False)
    GetURLFromList_19 = PrepareReceptorWS_14.macroNetwork.nodes[4]
    GetURLFromList_19.inputPortByName['ext'].widget.set(r"pdbqt", run=False)
    DownloadToFile_20 = PrepareReceptorWS_14.macroNetwork.nodes[5]
    DownloadToFile_20.inputPortByName['overwrite'].widget.set(1, run=False)

    ## saving connections for network PrepareReceptorWS ##
    PrepareReceptorWS_14.macroNetwork.freeze()
    PrepareReceptorWS_14.macroNetwork.unfreeze()

    ## modifying MacroInputNode dynamic ports
    input_Ports_15 = PrepareReceptorWS_14.macroNetwork.ipNode
    input_Ports_15.outputPorts[1].configure(name='CheckFileFormat_value')
    input_Ports_15.outputPorts[2].configure(name='PrepareReceptorOpalService_ws_nbcr_net_C')

    ## modifying MacroOutputNode dynamic ports
    output_Ports_16 = PrepareReceptorWS_14.macroNetwork.opNode
    output_Ports_16.inputPorts[1].configure(singleConnection='auto')
    output_Ports_16.inputPorts[2].configure(singleConnection='auto')
    output_Ports_16.inputPorts[1].configure(name='UpdateReceptor_receptor_prepared_obj')
    output_Ports_16.inputPorts[2].configure(name='UpdateReceptor_receptor_result')
    PrepareReceptorWS_14.inputPorts[0].configure(name='CheckFileFormat_value')
    PrepareReceptorWS_14.inputPorts[0].configure(datatype='receptor')
    PrepareReceptorWS_14.inputPorts[1].configure(name='PrepareReceptorOpalService_ws_nbcr_net_C')
    PrepareReceptorWS_14.inputPorts[1].configure(datatype='boolean')
    ## configure MacroNode input ports
    PrepareReceptorWS_14.outputPorts[0].configure(name='UpdateReceptor_receptor_prepared_obj')
    PrepareReceptorWS_14.outputPorts[0].configure(datatype='receptor_prepared')
    PrepareReceptorWS_14.outputPorts[1].configure(name='UpdateReceptor_receptor_result')
    PrepareReceptorWS_14.outputPorts[1].configure(datatype='string')
    ## configure MacroNode output ports
    PrepareReceptorWS_14.shrink()

    ## saving connections for network PrepareReceptor ##
    PrepareReceptor_4.macroNetwork.freeze()
    PrepareReceptor_4.macroNetwork.unfreeze()

    ## modifying MacroInputNode dynamic ports
    input_Ports_5 = PrepareReceptor_4.macroNetwork.ipNode
    input_Ports_5.outputPorts[1].configure(name='Pdb2pqrWS_CheckFileFormat_value')
    input_Ports_5.outputPorts[2].configure(name='PrepareReceptorWS_PrepareReceptorOpalService_ws_nbcr_net_C')

    ## modifying MacroOutputNode dynamic ports
    output_Ports_6 = PrepareReceptor_4.macroNetwork.opNode
    output_Ports_6.inputPorts[1].configure(singleConnection='auto')
    output_Ports_6.inputPorts[2].configure(singleConnection='auto')
    output_Ports_6.inputPorts[1].configure(name='PrepareReceptorWS_UpdateReceptor_receptor_prepared_obj')
    output_Ports_6.inputPorts[2].configure(name='PrepareReceptorWS_UpdateReceptor_receptor_result')
    PrepareReceptor_4.inputPorts[0].configure(name='Pdb2pqrWS_CheckFileFormat_value')
    PrepareReceptor_4.inputPorts[0].configure(datatype='receptor')
    PrepareReceptor_4.inputPorts[1].configure(name='PrepareReceptorWS_PrepareReceptorOpalService_ws_nbcr_net_C')
    PrepareReceptor_4.inputPorts[1].configure(datatype='boolean')
    ## configure MacroNode input ports
    PrepareReceptor_4.outputPorts[0].configure(name='PrepareReceptorWS_UpdateReceptor_receptor_prepared_obj')
    PrepareReceptor_4.outputPorts[0].configure(datatype='receptor_prepared')
    PrepareReceptor_4.outputPorts[1].configure(name='PrepareReceptorWS_UpdateReceptor_receptor_result')
    PrepareReceptor_4.outputPorts[1].configure(datatype='string')
    ## configure MacroNode output ports
    PrepareReceptor_4.shrink()
    ComputeGrids_22 = VirtualScreening_1.macroNetwork.nodes[3]
    prepareGPF_kryptonite_nbcr_net_26 = ComputeGrids_22.macroNetwork.nodes[3]
    prepareGPF_kryptonite_nbcr_net_26.inputPortByName['singlelib'].widget.set(r"", run=False)
    prepareGPF_kryptonite_nbcr_net_26.inputPortByName['r_url'].widget.set(r"", run=False)
    prepareGPF_kryptonite_nbcr_net_26.inputPortByName['zpoints'].widget.set(r"", run=False)
    prepareGPF_kryptonite_nbcr_net_26.inputPortByName['filter_file_url'].widget.set(r"", run=False)
    prepareGPF_kryptonite_nbcr_net_26.inputPortByName['lib'].widget.configure(*(), **{'choices': ('sample', 'NCIDS_SC', 'NCI_DS1', 'NCI_DS2', 'oldNCI', 'human_metabolome', 'chembridge_building_blocks', 'drugbank_nutraceutics', 'drugbank_smallmol', 'fda_approved')})
    prepareGPF_kryptonite_nbcr_net_26.inputPortByName['lib'].widget.set(r"", run=False)
    prepareGPF_kryptonite_nbcr_net_26.inputPortByName['ypoints'].widget.set(r"", run=False)
    prepareGPF_kryptonite_nbcr_net_26.inputPortByName['xcenter'].widget.set(r"auto", run=False)
    prepareGPF_kryptonite_nbcr_net_26.inputPortByName['p'].widget.set(r"", run=False)
    prepareGPF_kryptonite_nbcr_net_26.inputPortByName['o'].widget.set(r"", run=False)
    prepareGPF_kryptonite_nbcr_net_26.inputPortByName['zcenter'].widget.set(r"auto", run=False)
    prepareGPF_kryptonite_nbcr_net_26.inputPortByName['v'].widget.set(0, run=False)
    prepareGPF_kryptonite_nbcr_net_26.inputPortByName['userlib'].widget.set(r"", run=False)
    prepareGPF_kryptonite_nbcr_net_26.inputPortByName['xpoints'].widget.set(r"", run=False)
    prepareGPF_kryptonite_nbcr_net_26.inputPortByName['localRun'].widget.set(0, run=False)
    prepareGPF_kryptonite_nbcr_net_26.inputPortByName['ycenter'].widget.set(r"auto", run=False)
    prepareGPF_kryptonite_nbcr_net_26.inputPortByName['execPath'].widget.set(r"", run=False)
    autogrid_kryptonite_nbcr_net_27 = ComputeGrids_22.macroNetwork.nodes[4]
    autogrid_kryptonite_nbcr_net_27.inputPortByName['infile_url'].widget.set(r"", run=False)
    autogrid_kryptonite_nbcr_net_27.inputPortByName['l'].widget.set(r"output.glg", run=False)
    autogrid_kryptonite_nbcr_net_27.inputPortByName['o'].widget.set(0, run=False)
    autogrid_kryptonite_nbcr_net_27.inputPortByName['p'].widget.set(r"", run=False)
    autogrid_kryptonite_nbcr_net_27.inputPortByName['localRun'].widget.set(0, run=False)
    autogrid_kryptonite_nbcr_net_27.inputPortByName['execPath'].widget.set(r"", run=False)
    GetURLFromList_30 = ComputeGrids_22.macroNetwork.nodes[7]
    GetURLFromList_30.inputPortByName['ext'].widget.set(r"gpf", run=False)

    ## saving connections for network ComputeGrids ##
    ComputeGrids_22.macroNetwork.freeze()
    ComputeGrids_22.macroNetwork.unfreeze()

    ## modifying MacroInputNode dynamic ports
    input_Ports_23 = ComputeGrids_22.macroNetwork.ipNode
    input_Ports_23.outputPorts[1].configure(name='GetComputeGridsInputs_ligands')
    input_Ports_23.outputPorts[2].configure(name='GetComputeGridsInputs_receptor_pdbqt')
    input_Ports_23.outputPorts[3].configure(name='GetComputeGridsInputs_gpf_obj')

    ## modifying MacroOutputNode dynamic ports
    output_Ports_24 = ComputeGrids_22.macroNetwork.opNode
    output_Ports_24.inputPorts[1].configure(singleConnection='auto')
    output_Ports_24.inputPorts[2].configure(singleConnection='auto')
    output_Ports_24.inputPorts[1].configure(name='MakeAutogridResultObj_autogrid_result_obj')
    output_Ports_24.inputPorts[2].configure(name='GetMainURLFromList_newurl')
    ComputeGrids_22.inputPorts[0].configure(name='GetComputeGridsInputs_ligands')
    ComputeGrids_22.inputPorts[0].configure(datatype='LigandDB')
    ComputeGrids_22.inputPorts[1].configure(name='GetComputeGridsInputs_receptor_pdbqt')
    ComputeGrids_22.inputPorts[1].configure(datatype='receptor_prepared')
    ComputeGrids_22.inputPorts[2].configure(name='GetComputeGridsInputs_gpf_obj')
    ComputeGrids_22.inputPorts[2].configure(datatype='gpf_template')
    ## configure MacroNode input ports
    ComputeGrids_22.outputPorts[0].configure(name='MakeAutogridResultObj_autogrid_result_obj')
    ComputeGrids_22.outputPorts[0].configure(datatype='autogrid_results')
    ComputeGrids_22.outputPorts[1].configure(name='GetMainURLFromList_newurl')
    ComputeGrids_22.outputPorts[1].configure(datatype='string')
    ## configure MacroNode output ports
    ComputeGrids_22.shrink()
    AutodockVS_31 = VirtualScreening_1.macroNetwork.nodes[4]
    autodock_kryptonite_nbcr_net_35 = AutodockVS_31.macroNetwork.nodes[3]
    autodock_kryptonite_nbcr_net_35.inputPortByName['ga_run'].widget.set(r"", run=False)
    autodock_kryptonite_nbcr_net_35.inputPortByName['lib'].widget.configure(*(), **{'choices': ('sample', 'NCIDS_SC', 'NCI_DS1', 'NCI_DS2', 'human_metabolome', 'chembridge_building_blocks', 'drugbank_nutraceutics', 'drugbank_smallmol', 'fda_approved')})
    autodock_kryptonite_nbcr_net_35.inputPortByName['lib'].widget.set(r"", run=False)
    autodock_kryptonite_nbcr_net_35.inputPortByName['filter_file_url'].widget.set(r"", run=False)
    autodock_kryptonite_nbcr_net_35.inputPortByName['ga_num_evals'].widget.set(r"", run=False)
    autodock_kryptonite_nbcr_net_35.inputPortByName['sched'].widget.configure(*(), **{'choices': ('SGE', 'CSF')})
    autodock_kryptonite_nbcr_net_35.inputPortByName['sched'].widget.set(r"SGE", run=False)
    autodock_kryptonite_nbcr_net_35.inputPortByName['ga_num_generations'].widget.set(r"", run=False)
    autodock_kryptonite_nbcr_net_35.inputPortByName['userlib'].widget.set(r"", run=False)
    autodock_kryptonite_nbcr_net_35.inputPortByName['ga_pop_size'].widget.set(r"", run=False)
    autodock_kryptonite_nbcr_net_35.inputPortByName['localRun'].widget.set(0, run=False)
    autodock_kryptonite_nbcr_net_35.inputPortByName['email'].widget.set(r"", run=False)
    autodock_kryptonite_nbcr_net_35.inputPortByName['execPath'].widget.set(r"", run=False)

    ## saving connections for network AutodockVS ##
    AutodockVS_31.macroNetwork.freeze()
    AutodockVS_31.macroNetwork.unfreeze()

    ## modifying MacroInputNode dynamic ports
    input_Ports_32 = AutodockVS_31.macroNetwork.ipNode
    input_Ports_32.outputPorts[1].configure(name='PrepareADVSInputs_ligands')
    input_Ports_32.outputPorts[2].configure(name='PrepareADVSInputs_autogrid_results')
    input_Ports_32.outputPorts[3].configure(name='PrepareADVSInputs_dpf_template_obj')

    ## modifying MacroOutputNode dynamic ports
    output_Ports_33 = AutodockVS_31.macroNetwork.opNode
    output_Ports_33.inputPorts[1].configure(singleConnection='auto')
    output_Ports_33.inputPorts[1].configure(name='GetMainURLFromList_newurl')
    AutodockVS_31.inputPorts[0].configure(name='PrepareADVSInputs_ligands')
    AutodockVS_31.inputPorts[0].configure(datatype='LigandDB')
    AutodockVS_31.inputPorts[1].configure(name='PrepareADVSInputs_autogrid_results')
    AutodockVS_31.inputPorts[1].configure(datatype='autogrid_results')
    AutodockVS_31.inputPorts[2].configure(name='PrepareADVSInputs_dpf_template_obj')
    AutodockVS_31.inputPorts[2].configure(datatype='dpf_template')
    ## configure MacroNode input ports
    AutodockVS_31.outputPorts[0].configure(name='GetMainURLFromList_newurl')
    AutodockVS_31.outputPorts[0].configure(datatype='string')
    ## configure MacroNode output ports
    AutodockVS_31.shrink()

    ## saving connections for network VirtualScreening ##
    VirtualScreening_1.macroNetwork.freeze()
    VirtualScreening_1.macroNetwork.unfreeze()

    ## modifying MacroInputNode dynamic ports
    input_Ports_2 = VirtualScreening_1.macroNetwork.ipNode
    input_Ports_2.outputPorts[1].configure(name='PrepareReceptor_Pdb2pqrWS_CheckFileFormat_value')
    input_Ports_2.outputPorts[2].configure(name='ComputeGrids_GetComputeGridsInputs_ligands')
    input_Ports_2.outputPorts[3].configure(name='ComputeGrids_GetComputeGridsInputs_gpf_obj')
    input_Ports_2.outputPorts[4].configure(name='AutodockVS_PrepareADVSInputs_dpf_template_obj')
    input_Ports_2.outputPorts[5].configure(name='PrepareReceptor_PrepareReceptorWS_PrepareReceptorOpalService_ws_nbcr_net_C')

    ## modifying MacroOutputNode dynamic ports
    output_Ports_3 = VirtualScreening_1.macroNetwork.opNode
    output_Ports_3.inputPorts[1].configure(singleConnection='auto')
    output_Ports_3.inputPorts[1].configure(name='AutodockVS_GetMainURLFromList_newurl')
    VirtualScreening_1.inputPorts[0].configure(name='PrepareReceptor_Pdb2pqrWS_CheckFileFormat_value')
    VirtualScreening_1.inputPorts[0].configure(datatype='receptor')
    VirtualScreening_1.inputPorts[1].configure(name='ComputeGrids_GetComputeGridsInputs_ligands')
    VirtualScreening_1.inputPorts[1].configure(datatype='LigandDB')
    VirtualScreening_1.inputPorts[2].configure(name='ComputeGrids_GetComputeGridsInputs_gpf_obj')
    VirtualScreening_1.inputPorts[2].configure(datatype='gpf_template')
    VirtualScreening_1.inputPorts[3].configure(name='AutodockVS_PrepareADVSInputs_dpf_template_obj')
    VirtualScreening_1.inputPorts[3].configure(datatype='dpf_template')
    VirtualScreening_1.inputPorts[4].configure(name='PrepareReceptor_PrepareReceptorWS_PrepareReceptorOpalService_ws_nbcr_net_C')
    VirtualScreening_1.inputPorts[4].configure(datatype='boolean')
    ## configure MacroNode input ports
    VirtualScreening_1.outputPorts[0].configure(name='AutodockVS_GetMainURLFromList_newurl')
    VirtualScreening_1.outputPorts[0].configure(datatype='string')
    ## configure MacroNode output ports
    VirtualScreening_1.shrink()
    VirtualScreening_1.configure(*(), **{'paramPanelImmediate': 1, 'expanded': False})
except:
    print("WARNING: failed to restore VirtualScreening named VirtualScreening in network masterNet")
    print_exc()
    VirtualScreening_1=None

try:
    ## saving node PublicServerLigandDB ##
    from Adt.Input.PublicServerLigandDB import PublicServerLigandDB
    PublicServerLigandDB_37 = PublicServerLigandDB(constrkw={}, name='PublicServerLigandDB', library=Adt)
    masterNet.addNode(PublicServerLigandDB_37,345,23)
    PublicServerLigandDB_37.inputPortByName['server_lib'].widget.set(r"sample", run=False)
    PublicServerLigandDB_37.configure(*(), **{'paramPanelImmediate': 1})
except:
    print("WARNING: failed to restore PublicServerLigandDB named PublicServerLigandDB in network masterNet")
    print_exc()
    PublicServerLigandDB_37=None

try:
    ## saving node FilterLigandsNode ##
    from Adt.Filter.filterLigands import FilterLigandsNode
    FilterLigandsNode_38 = FilterLigandsNode(constrkw={}, name='FilterLigandsNode', library=Adt)
    masterNet.addNode(FilterLigandsNode_38,345,107)
    FilterLigandsNode_38.inputPortByName['filterMode'].widget.set(r"default", run=False)
    FilterLigandsNode_38.inputPortByName['hbd_min'].widget.set(0, run=False)
    FilterLigandsNode_38.inputPortByName['hbd_max'].widget.set(99, run=False)
    FilterLigandsNode_38.inputPortByName['hba_min'].widget.set(0, run=False)
    FilterLigandsNode_38.inputPortByName['hba_max'].widget.set(99, run=False)
    FilterLigandsNode_38.inputPortByName['mw_min'].widget.set(0, run=False)
    FilterLigandsNode_38.inputPortByName['mw_max'].widget.set(9999, run=False)
    FilterLigandsNode_38.inputPortByName['nat_min'].widget.set(0, run=False)
    FilterLigandsNode_38.inputPortByName['nat_max'].widget.set(999, run=False)
    FilterLigandsNode_38.inputPortByName['torsdof_min'].widget.set(0, run=False)
    FilterLigandsNode_38.inputPortByName['torsdof_max'].widget.set(32, run=False)
    FilterLigandsNode_38.configure(*(), **{'paramPanelImmediate': 1})
except:
    print("WARNING: failed to restore FilterLigandsNode named FilterLigandsNode in network masterNet")
    print_exc()
    FilterLigandsNode_38=None

try:
    ## saving node PreserveCharges? ##
    from Vision.StandardNodes import CheckButtonNE
    PreserveCharges__39 = CheckButtonNE(constrkw={}, name='PreserveCharges?', library=stdlib)
    masterNet.addNode(PreserveCharges__39,617,20)
    PreserveCharges__39.inputPortByName['button'].widget.set(1, run=False)
    PreserveCharges__39.configure(*(), **{'paramPanelImmediate': 1})
except:
    print("WARNING: failed to restore CheckButtonNE named PreserveCharges? in network masterNet")
    print_exc()
    PreserveCharges__39=None

try:
    ## saving node DownloadSaveDir ##
    from WebServices.VisionInterface.WSNodes import DownloadSaveDirNode
    DownloadSaveDir_40 = DownloadSaveDirNode(constrkw={}, name='DownloadSaveDir', library=wslib)
    masterNet.addNode(DownloadSaveDir_40,170,558)
    DownloadSaveDir_40.inputPortByName['url'].configure(*(), **{'defaultValue': None})
    DownloadSaveDir_40.inputPortByName['url'].rebindWidget()
    DownloadSaveDir_40.inputPortByName['url'].widget.set(r"", run=False)
    DownloadSaveDir_40.inputPortByName['url'].unbindWidget()
    DownloadSaveDir_40.configure(*(), **{'paramPanelImmediate': 1})
except:
    print("WARNING: failed to restore DownloadSaveDirNode named DownloadSaveDir in network masterNet")
    print_exc()
    DownloadSaveDir_40=None

try:
    ## saving node GetStructuresFromDir ##
    from Adt.Input.GetStructuresFromDir import GetStructuresFromDir
    GetStructuresFromDir_41 = GetStructuresFromDir(constrkw={}, name='GetStructuresFromDir', library=Adt)
    masterNet.addNode(GetStructuresFromDir_41,16,22)
    GetStructuresFromDir_41.inputPortByName['directory'].widget.set(r"VS", run=False)
    GetStructuresFromDir_41.configure(*(), **{'paramPanelImmediate': 1})
except:
    print("WARNING: failed to restore GetStructuresFromDir named GetStructuresFromDir in network masterNet")
    print_exc()
    GetStructuresFromDir_41=None

try:
    ## saving node InputValidation ##
    from Adt.Mapper.InputValidation import InputValidation
    InputValidation_42 = InputValidation(constrkw={}, name='InputValidation', library=Adt)
    masterNet.addNode(InputValidation_42,86,318)
    InputValidation_42.configure(*(), **{'paramPanelImmediate': 1, 'expanded': False})
except:
    print("WARNING: failed to restore InputValidation named InputValidation in network masterNet")
    print_exc()
    InputValidation_42=None

#masterNet.run()
masterNet.freeze()

## saving connections for network vs-obj6 ##
if PublicServerLigandDB_37 is not None and FilterLigandsNode_38 is not None:
    try:
        masterNet.connectNodes(
            PublicServerLigandDB_37, FilterLigandsNode_38, "ligDB", "ligands", blocking=True
            , splitratio=[0.33190502385589948, 0.21642002589850867])
    except:
        print("WARNING: failed to restore connection between PublicServerLigandDB_37 and FilterLigandsNode_38 in network masterNet")
if FilterLigandsNode_38 is not None and VirtualScreening_1 is not None:
    try:
        masterNet.connectNodes(
            FilterLigandsNode_38, VirtualScreening_1, "ligands", "ComputeGrids_GetComputeGridsInputs_ligands", blocking=True
            , splitratio=[0.37455111543238506, 0.32420948165762498])
    except:
        print("WARNING: failed to restore connection between FilterLigandsNode_38 and VirtualScreening_1 in network masterNet")
if PreserveCharges__39 is not None and VirtualScreening_1 is not None:
    try:
        masterNet.connectNodes(
            PreserveCharges__39, VirtualScreening_1, "value_bool", "PrepareReceptor_PrepareReceptorWS_PrepareReceptorOpalService_ws_nbcr_net_C", blocking=True
            , splitratio=[0.26471965480569831, 0.73857142767746442])
    except:
        print("WARNING: failed to restore connection between PreserveCharges__39 and VirtualScreening_1 in network masterNet")
if VirtualScreening_1 is not None and DownloadSaveDir_40 is not None:
    try:
        masterNet.connectNodes(
            VirtualScreening_1, DownloadSaveDir_40, "AutodockVS_GetMainURLFromList_newurl", "url", blocking=True
            , splitratio=[0.74808619960402778, 0.23329088335740467])
    except:
        print("WARNING: failed to restore connection between VirtualScreening_1 and DownloadSaveDir_40 in network masterNet")
if GetStructuresFromDir_41 is not None and iterate_0 is not None:
    try:
        masterNet.connectNodes(
            GetStructuresFromDir_41, iterate_0, "structure_list_obj", "listToLoopOver", blocking=True
            , splitratio=[0.64404900652669483, 0.66433287135542574])
    except:
        print("WARNING: failed to restore connection between GetStructuresFromDir_41 and iterate_0 in network masterNet")
if iterate_0 is not None and VirtualScreening_1 is not None:
    try:
        masterNet.connectNodes(
            iterate_0, VirtualScreening_1, "oneItem", "PrepareReceptor_Pdb2pqrWS_CheckFileFormat_value", blocking=True
            , splitratio=[0.24975750410316327, 0.47366759074690934])
    except:
        print("WARNING: failed to restore connection between iterate_0 and VirtualScreening_1 in network masterNet")
if iterate_0 is not None and InputValidation_42 is not None:
    try:
        masterNet.connectNodes(
            iterate_0, InputValidation_42, "oneItem", "recpetor_obj", blocking=True
            , splitratio=[0.58378184959869772, 0.29053011237456339])
    except:
        print("WARNING: failed to restore connection between iterate_0 and InputValidation_42 in network masterNet")
if InputValidation_42 is not None and VirtualScreening_1 is not None:
    try:
        masterNet.connectNodes(
            InputValidation_42, VirtualScreening_1, "GPF_template", "ComputeGrids_GetComputeGridsInputs_gpf_obj", blocking=True
            , splitratio=[0.63709387814855534, 0.40809312341502446])
    except:
        print("WARNING: failed to restore connection between InputValidation_42 and VirtualScreening_1 in network masterNet")
if InputValidation_42 is not None and VirtualScreening_1 is not None:
    try:
        masterNet.connectNodes(
            InputValidation_42, VirtualScreening_1, "DPF_template", "AutodockVS_PrepareADVSInputs_dpf_template_obj", blocking=True
            , splitratio=[0.50008775545983264, 0.21584255901641733])
    except:
        print("WARNING: failed to restore connection between InputValidation_42 and VirtualScreening_1 in network masterNet")
if InputValidation_42 is not None and DownloadSaveDir_40 is not None:
    try:
        masterNet.connectNodes(
            InputValidation_42, DownloadSaveDir_40, "result_dir", "path", blocking=True
            , splitratio=[0.32102505593374198, 0.64313754588560501])
    except:
        print("WARNING: failed to restore connection between InputValidation_42 and DownloadSaveDir_40 in network masterNet")
masterNet.runOnNewData.value = False

if __name__=='__main__':
    from sys import argv
    lNodePortValues = []
    if (len(argv) > 1) and argv[1].startswith('-'):
        lArgIndex = 2
    else:
        lArgIndex = 1
    while lArgIndex < len(argv) and argv[lArgIndex][-3:]!='.py':
        lNodePortValues.append(argv[lArgIndex])
        lArgIndex += 1
    masterNet.setNodePortValues(lNodePortValues)
    if '--help' in argv or '-h' in argv: # show help
        masterNet.helpForNetworkAsApplication()
    elif '-w' in argv: # run without Vision and exit
         # create communicator
        from NetworkEditor.net import Communicator
        masterNet.communicator = Communicator(masterNet)
        print('Communicator listening on port:', masterNet.communicator.port)

        import socket
        f = open(argv[0]+'.sock', 'w')
        f.write("%s %i"%(socket.gethostbyname(socket.gethostname()),
                         masterNet.communicator.port))
        f.close()

        masterNet.run()

    else: # stand alone application while vision is hidden
        if '-e' in argv: # run and exit
            masterNet.run()
        elif '-r' in argv or len(masterNet.userPanels) == 0: # no user panel => run
            masterNet.run()
            mainLoopVisionToRunNetworkAsApplication(masterNet.editor)
        else: # user panel
            mainLoopVisionToRunNetworkAsApplication(masterNet.editor)

