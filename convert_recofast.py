import ROOT
import os.path
import pandas as pd
import tables
import root_numpy

def import_subrun(run_path):
	"""
		This function imports a subrun-root file, reads in the tree and converts it to a pandas dataframe.

		Input Parameters:   -) run_path: string containing the path to the data of the run

		Output Parameters:   -) pd_df: tree of the subrun saved as a pandas dataframe
	"""

	### Open ROOT Tree
	subrun = ROOT.TFile.Open(run_path)
	subrun_tree = subrun.Get("analysistree/anatree")
	subrun_DataSet = root_numpy.tree2array(subrun_tree)
#	print(subrun_DataSet[0][55])
	pd_df = pd.DataFrame(subrun_DataSet, columns = [
		'Run','Subrun','EventNumberInRun','EventTimeSeconds','EventTimeNanoseconds',
		'IsData', 'NumberOfHits', 'Hit_TPC', 'Hit_View','Hit_Channel','Hit_PeakTime',
		'Hit_ChargeSummedADC','Hit_ChargeIntegral','Hit_PeakHeight','Hit_StartTime',
		'Hit_EndTime', 'Hit_Width', 'Hit_GoodnessOfFit', 'Hit_FitParameter_Amplitude',
		'Hit_FitParameter_Offset', 'Hit_FitParameter_Tau1', 'Hit_FitParameter_Tau2',
		'Hit_Multiplicity',
		'Hit_TrackID', 'Hit_ClusterID', 'NumberOfClusters', 'ClusterID',
		'Cluster_NumberOfHits', 'Cluster_View', 'Cluster_ChargeIntegral',
		'Cluster_ChargeIntegralAveragePerHit', 'Cluster_StartChannel',
		'Cluster_StartTick', 'Cluster_EndChannel', 'Cluster_EndTick',
		'Cluster_StartCharge', 'Cluster_StartAngle', 'Cluster_EndCharge',
		'Cluster_EndAngle', 'NumberOfTracks', 'TrackID',
		'Track_NumberOfHits', 'Track_Length_Trajectory', 'Track_Length_StraightLine',
		'Track_StartPoint_X', 'Track_StartPoint_Y',
		'Track_StartPoint_Z', 'Track_StartPoint_DistanceToBoundary',
		'Track_EndPoint_X', 'Track_EndPoint_Y',
		'Track_EndPoint_Z', 'Track_EndPoint_DistanceToBoundary',
		'Track_StartDirection_Theta', 'Track_StartDirection_Phi',
		'Track_StartDirection_X', 'Track_StartDirection_Y',
		'Track_StartDirection_Z', 'Track_EndDirection_Theta',
		'Track_EndDirection_Phi', 'Track_EndDirection_X',
		'Track_EndDirection_Y', 'Track_EndDirection_Z',
		'Track_Momentum', 'Track_Momentum_Range', 'Track_Momentum_mschi',
		'Track_Momentum_mscmic', 'Track_Momentum_mscfwd',
		'Track_Momentum_mscbwd', 'Track_Momentum_mscllfdw',
		'Track_Momentum_mscllbwd',
		'Track_PitchInViews', 'Track_NumberOfHitsPerView',
		'Track_Hit_X','Track_Hit_Y','Track_Hit_Z',
		'Track_Hit_LocalTrack_Direction_X', 'Track_Hit_LocalTrack_Direction_Y',
		'Track_Hit_LocalTrack_Direction_Z', 'Track_Hit_LocalTrack_Direction_Theta',
		'Track_Hit_LocalTrack_Direction_Phi',
		'Track_Hit_ds_LocalTrackDirection', 'Track_Hit_ds_3DPosition',
		'Track_Hit_TPC','Track_Hit_View','Track_Hit_Channel',
		'Track_Hit_PeakTime', 'Track_Hit_ChargeSummedADC',
		'Track_Hit_ChargeIntegral', 'Track_Hit_Amplitude',
		'Track_Hit_StartTime', 'Track_Hit_EndTime',
		'Track_Hit_Width', 'Track_Hit_GoodnessOfFit',
		'Track_Hit_Multiplicity'])

	# Split global hit buffer into hits by track

	subrun_track_hit_x = []
	subrun_track_hit_y = []
	subrun_track_hit_z = []

	for e in range(len(pd_df['NumberOfTracks'])):
		hit_index = 0
		event_track_hit_x = []
		event_track_hit_y = []
		event_track_hit_z = []
		for t in range(pd_df['NumberOfTracks'][e]):
			track_hit_x = []
			track_hit_y = []
			track_hit_z = []
			nhits = pd_df['Track_NumberOfHits'][e][t]
			for i in range(hit_index, hit_index+nhits):
				track_hit_x.append(pd_df['Track_Hit_X'][e][i])
				track_hit_y.append(pd_df['Track_Hit_Y'][e][i])
				track_hit_z.append(pd_df['Track_Hit_Z'][e][i])
			hit_index += nhits
			event_track_hit_x.append(track_hit_x)
			event_track_hit_y.append(track_hit_y)
			event_track_hit_z.append(track_hit_z)
		subrun_track_hit_x.append(event_track_hit_x)
		subrun_track_hit_y.append(event_track_hit_y)
		subrun_track_hit_z.append(event_track_hit_z)

	print pd_df.shape
	print len(subrun_track_hit_x)

	pd_df.drop('Track_Hit_X', axis=1, inplace=True)
	pd_df.drop('Track_Hit_Y', axis=1, inplace=True)
	pd_df.drop('Track_Hit_Z', axis=1, inplace=True)
	pd_df.assign(Track_Hit_X=pd.Series(subrun_track_hit_x, index=pd_df.index))
	pd_df.assign(Track_Hit_Y=pd.Series(subrun_track_hit_y, index=pd_df.index))
	pd_df.assign(Track_Hit_Z=pd.Series(subrun_track_hit_z, index=pd_df.index))

	print run_path, "has been imported"
	return pd_df

start = 0
end = 1
for i in range(start,end):
		path_to_file = "/eos/experiment/wa105/offline/LArSoft/MC/MC5/Parser/recofast/%i-RecoFast-Parser.root" %i
		if( os.path.isfile(path_to_file)):
			table = import_subrun(path_to_file)
			table.to_hdf("./recofast_hdf5/%i-RecoFast-Parser.hdf5" % i, key = "table", mode = 'w')
print("All done")
