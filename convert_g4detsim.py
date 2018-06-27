import ROOT
import os.path
import pandas as pd
import tables
import root_numpy

def import_subrun(run_path):
	"""
		This function imports a subrun-root file, reads in the tree and converts it to a pandas dataframe.

		Input Parameters:	-) run_path: string containing the path to the data of the run

		Output Parameters:   -) pd_df: tree of the subrun saved as a pandas dataframe
	"""

	### Open ROOT Tree
	subrun = ROOT.TFile.Open(run_path)
	subrun_tree = subrun.Get("analysistree/anatree")
	subrun_DataSet = root_numpy.tree2array(subrun_tree)
	pd_df = pd.DataFrame(subrun_DataSet, columns = [
		'Run','Subrun','EventNumberInRun','EventTimeSeconds','EventTimeNanoseconds', 'IsData',
		'RawWaveform_NumberOfChannels', 'RawWaveform_NumberOfTicks', 'RawWaveform_Channel',
		'RawWaveform_NumberOfTicksInAllChannels', 'RawWaveform_ADC',
		'MCTruth_GEANT4_NumberOfDetectedPhotons', 'MCTruth_GEANT4_DetectedPhoton_Channel',
		'MCTruth_GEANT4_DetectedPhoton_Time', 'MCTruth_GEANT4_NumberOfParticles',
		'MCTruth_GEANT4_NumberOfPrimaries', 'MCTruth_GEANT4_ParticleID', 'MCTruth_GEANT4_PDGCode',
		'MCTruth_GEANT4_Status', 'MCTruth_GEANT4_IsInTPCAV', 'MCTruth_GEANT4_NumberOfDaughterParticles',
		'MCTruth_GEANT4_MotherParticle', 'MCTruth_GEANT4_Mass',
		'MCTruth_GEANT4_StartPoint_X', 'MCTruth_GEANT4_StartPoint_Y', 'MCTruth_GEANT4_StartPoint_Z',
		'MCTruth_GEANT4_StartTime', 'MCTruth_GEANT4_StartEnergy', 'MCTruth_GEANT4_StartMomentum',
		'MCTruth_GEANT4_StartMomentum_X', 'MCTruth_GEANT4_StartMomentum_Y', 'MCTruth_GEANT4_StartMomentum_Z',
		'MCTruth_GEANT4_StartDirection_Theta', 'MCTruth_GEANT4_StartDirection_Phi',
		'MCTruth_GEANT4_InTPCAV_NumberOfParticles', 'MCTruth_GEANT4_InTPCAV_ParticleID',
		'MCTruth_GEANT4_InTPCAV_PDGCode', 'MCTruth_GEANT4_InTPCAV_Pathlength',
		'MCTruth_GEANT4_InTPCAV_StartPoint_X', 'MCTruth_GEANT4_InTPCAV_StartPoint_Y', 'MCTruth_GEANT4_InTPCAV_StartPoint_Z',
		'MCTruth_GEANT4_InTPCAV_StartTime', 'MCTruth_GEANT4_InTPCAV_StartEnergy',
		'MCTruth_GEANT4_InTPCAV_StartMomentum', 'MCTruth_GEANT4_InTPCAV_StartMomentum_X',
		'MCTruth_GEANT4_InTPCAV_StartMomentum_Y', 'MCTruth_GEANT4_InTPCAV_StartMomentum_Z',
		'MCTruth_GEANT4_InTPCAV_StartDirection_Theta', 'MCTruth_GEANT4_InTPCAV_StartDirection_Phi',
		'MCTruth_GEANT4_InTPCAV_EndPoint_X', 'MCTruth_GEANT4_InTPCAV_EndPoint_Y', 'MCTruth_GEANT4_InTPCAV_EndPoint_Z',
		'MCTruth_GEANT4_InTPCAV_EndTime', 'MCTruth_GEANT4_InTPCAV_EndEnergy', 'MCTruth_GEANT4_InTPCAV_EndMomentum',
		'MCTruth_GEANT4_InTPCAV_EndMomentum_X', 'MCTruth_GEANT4_InTPCAV_EndMomentum_Y', 'MCTruth_GEANT4_InTPCAV_EndMomentum_Z',
		'MCTruth_GEANT4_InTPCAV_EndDirection_Theta', 'MCTruth_GEANT4_InTPCAV_EndDirection_Phi',
		'MCTruth_GEANT4_NumberOfTrajectoryStepsPerParticle', 'MCTruth_GEANT4_TotalNumberOfTrajectoryStepsForAllParticles',
		'MCTruth_GEANT4_TrajectoryStep_ParticleID', 'MCTruth_GEANT4_TrajectoryStep_PDGCode',
		'MCTruth_GEANT4_TrajectoryStep_Point_X', 'MCTruth_GEANT4_TrajectoryStep_Point_Y', 'MCTruth_GEANT4_TrajectoryStep_Point_Z',
		'MCTruth_GEANT4_TrajectoryStep_Time', 'MCTruth_GEANT4_TrajectoryStep_Energy',
		'MCTruth_GEANT4_TrajectoryStep_Momentum', 'MCTruth_GEANT4_TrajectoryStep_Momentum_X',
		'MCTruth_GEANT4_TrajectoryStep_Momentum_Y', 'MCTruth_GEANT4_TrajectoryStep_Momentum_Z',
		'MCTruth_GEANT4_TrajectoryStep_Direction_Theta',
		'MCTruth_GEANT4_TrajectoryStep_Direction_Phi',])
	print run_path, "has been imported"
	return pd_df

start = 0
end = 10
for i in range(start,end):
		path_to_file = "/eos/experiment/wa105/offline/LArSoft/MC/MC5/Parser/g4detsim/%i-G4Detsim-Parser.root" %i
		if( os.path.isfile(path_to_file)):
			table = import_subrun(path_to_file)
			table.to_hdf("./g4detsim_hdf5/%i-G4Detsim-Parser.hdf5" % i, key = "table", mode = 'w', complevel=5)
print("All done")
