import pandas as pd

# 表头
ec_title = ['ctr_no', 'ec_name', 'ec_conclusion', 'ec_date']

site_title = ['ctr_no', 'site_name', 'pi_name', 'country', 'province_state', 'city']

pi_title = ['ctr_no', 'pi_name', 'pi_title', 'pi_phone', 'pi_mail', 'pi_postcode', 'pi_site_name']

trial_title = ["ctr_no", "status", "requestor", "publication_date", "sponsor", "related_trial_no", "indication",
               "standard_phase","purpose", "drug_name", "age", "planned_size", "actual_size", "final_size",
               "inclusion_criteria", "exclusion_criteria","icf_date", "fpi_date", "close_date"]


def wri_tit(csv_name, tit_list):
    df = pd.read_csv(csv_name, header=None, names=tit_list)
    df.to_csv(csv_name, index=False)


# 写入表头
wri_tit('trial_info.csv', trial_title)
wri_tit('trial_pi_info.csv', pi_title)
wri_tit('trial_site_info.csv', site_title)
wri_tit('trial_ec_info.csv', ec_title)
