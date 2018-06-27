import ROOT
import os.path
import pandas as pd
import tables
import root_numpy

def import_subrun(run_path):
    """
        This function imports a subrun-root file, reads in the tree and converts it to a pandas dataframe.

        Input Parameters:    -) run_path: string containing the path to the data of the run

        Output Parameters:   -) pd_df: tree of the subrun saved as a pandas dataframe
    """

    ### Open ROOT Tree
    subrun = ROOT.TFile.Open(run_path)
    subrun_tree = subrun.Get("analysistree/anatree")
    subrun_DataSet = root_numpy.tree2array(subrun_tree)
#    print(subrun_DataSet[0][55])
    pd_df = pd.DataFrame(subrun_DataSet, columns = ['Run','Subrun','EventNumberInRun','EventTimeSeconds','EventTimeNanoseconds', 'IsData',
													'RecoWaveforms_NumberOfChannels', 'RecoWaveform_Channel', 'RecoWaveform_NTicks',
													'RecoWaveform_NumberOfTicksInAllChannels', 'RecoWaveform_Tick', 'RecoWaveform_ADC',
													'NumberOfHits', 'Hit_TPC', 'Hit_View','Hit_Channel','Hit_PeakTime',
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
													'Track_Chi2PerNDF', 'Track_NDF',
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
                                                    'Track_Momentum_mscbwd', 'Track_Momentum_mscllfdw', 'Track_Momentum_mscllbwd',
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
    print run_path, "has been imported"
    return pd_df

start = 0
end = 10
for i in range(start,end):
        path_to_file = "/eos/experiment/wa105/offline/LArSoft/MC/MC5/Parser/recofull/%i-RecoFull-Parser.root" %i
        if( os.path.isfile(path_to_file)):
            table = import_subrun(path_to_file)
            table.to_hdf("./recofull_hdf5/%i-RecoFull-Parser.hdf5" % i, key = "table", mode = 'w')
print("All done")
