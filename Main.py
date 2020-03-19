import data_scheduler.lib_data_merger as mice_data

if __name__=='__main__':
    mice_data_dir = r'C:\Users\lkokot\Desktop\ETHZ_STAT_MSC\sem_2\stats_lab\analysis\CSV data files for analysis'
    md = mice_data.MiceDataMerger(mice_data_dir)
    data = md.fetch_mouse_signal(165, 'eth', 'running')
    print(data.get_pandas()[:35])
    sliced_data = data.sliced_data(12)
    print(len(sliced_data))