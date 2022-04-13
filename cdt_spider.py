import re
import requests
from lxml import etree
from encapsulation import write_csv, read_conf, get_ele_number


class CdtSpider:
    Cookie = "FSSBBIl1UgzbN7N80S=AmMA4i6RzjkRrd_3ufeSlQfRQhRevsPbmE06ayvNafw1d0Z8uUyGLpxfJn_V2ebb;token=C1hCSkY2yWAEzQ7TZ_qacMPu3A2z8eMGLcs-6SJsZlQGCQDLBMsWGNErug8; FSSBBIl1UgzbN7N80T=3YvgnQKQu_pAA8qIKo67lwh.qa_y7_crUjNjnT5VR2YSpI8r_9cVgrlo3GsrB_vQQWum7udZevXQMVm5n0zROwyQS0tANP60Pm.ESLc9grs6896Muycmt3uZqbhlHOFiREOpyFFciGCYfrhbn_tGJIziPqNnZPjrsYpxvfYNLgLQDawn.2ZY0juLQEWTGzrzzNim.qsWACT4zmz_HBOnt8btdT1Ob5D1ANc47rKOMrvP4_GUjkYtRoI3JJXoio_Byg2MwcR_zzM8E4lFeoxrmtuSMWqwSq7PITW1NxpkOweZXlXOr6OJbtCQRjSMC2kmFkCEUKxNLKDPULG297tAkzC4UE9jf6QXOc.O6rHLZbQm04a"

    url = 'http://www.chinadrugtrials.org.cn/clinicaltrials.searchlistdetail.dhtml'

    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
        'Cookie': Cookie,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '211',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'www.chinadrugtrials.org.cn',
        'Origin': 'http://www.chinadrugtrials.org.cn',
        'Referer': 'http://www.chinadrugtrials.org.cn/clinicaltrials.searchlist.dhtml',
        'Upgrade-Insecure-Requests': '1'
    }

    def turn_page(self):
        # 总页数
        page_all = 820
        for j in range(0, page_all + 1):
            print(f"'*******'当前第{j + 1}页数据+'*******'")
            page = j * 20 + 1
            for index in range(page, page + 20):
                data = {
                    'id': '',
                    'ckm_index': index,
                    'sort': 'desc',
                    'sort2': '',
                    'rule': 'CTR',
                    'secondLevel': '1',
                    'currentpage': page,
                    'keywords': '',
                    'reg_no': '',
                    'indication': '',
                    'case_no': '',
                    'drugs_name': '',
                    'drugs_type': '',
                    'appliers': '',
                    'communities': '',
                    'researchers': '',
                    'agencies': '',
                    'state': ''
                }
                resp = requests.post(self.url, headers=self.headers, data=data).text
                html = etree.HTML(resp)

                # 登记号
                try:
                    ctr_no_text = html.xpath('.//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[1]/td')[0].text
                except:
                    ctr_no_text=''

                # >>>>> get_trial_info
                # 试验状态
                try:
                    status_text = html.xpath('.//div[@id="collapseOne"]//table[@class="searchDetailTable"][1]//tr[1]/td[2]')[0].text
                except:
                    status_text =''
                # 六,试验状态
                try:
                    detail_status_text = html.xpath('.//div[text()="1、试验状态"]/following::text()[1]')[0]
                except:
                    detail_status_text=''
                # 申请人联系人
                try:
                    requestor_text = html.xpath('.//div[@id="collapseOne"]//table[@class="searchDetailTable"][1]/tr[2]/td[1]')[0].text
                except:
                    requestor_text=''
                # 申请人名称
                try:
                    sponsor_text = html.xpath('.//div[@id="collapseOne"]//table[@class="searchDetailTable"][1]/tr[3]/td[1]')[0].text
                except:
                    sponsor_text=''
                # 首次公示信息日期
                try:
                    publication_date_text =html.xpath('.//div[@id="collapseOne"]//table[@class="searchDetailTable"][1]/tr[2]/td[2]')[0].text
                except:
                    publication_date_text=''
                # 相关登记号
                try:
                    related_trial_no_text =html.xpath('.//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]/tr[2]/td')[0].text
                    if related_trial_no_text == None:
                        related_trial_no_text = ''
                except:
                    related_trial_no_text=''
                # 药物名称&曾用名

                try:
                    drug_text = html.xpath('//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[3]/td')[
                        0].text
                    drug_name_text, drug_previous_name_text = drug_text.split('曾用名:')
                except:
                    drug_name_text=''
                    drug_previous_name_text=''
                # 药物类型
                try:
                    drug_type_text = html.xpath('//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[4]/td')[0].text
                except:
                    drug_type_text=''
                # 临床申请受理号
                try:
                    clinical_register_no_text = html.xpath(
                        '//*[@id="collapseTwo"]/div/table[1]//tr[5]/th[contains(text(),"临床申请受理号")]/following::td[1]')[0].text.replace('企业选择不公示', '')
                except IndexError:
                    clinical_register_no_text = ''
                # 适应症
                try:
                    indication_text = html.xpath('//table[@class="searchDetailTable"][1]//tr[6]/td')[0].text
                except:
                    indication_text=''
                # 试验分期 (未处理)
                try:
                    phase_text = html.xpath('//table[@class="searchDetailTable"][3]//tr[1]/td[2]')[0].text
                except:
                    phase_text=''
                # 试验分期
                try:
                    standard_phase_text = html.xpath('//table[@class="searchDetailTable"][3]//tr[1]/td[2]')[0].text
                    standard_phase_text = read_conf('trial_info', 'standard_phase', standard_phase_text)
                    if standard_phase_text.find("其它其他说明:") >= 0:
                        temp_standard_phase = standard_phase_text.replace("IV", "Four").replace("III", "Three").replace("II", "Two").replace("I", "One").replace("1", "One").replace("2", "Two").replace("3", "Three").replace("4", "IV")
                        if re.match(".*One.*Two.*Three", temp_standard_phase):
                            standard_phase_text = "I/II/III"
                        elif re.match(".*One.*Three", temp_standard_phase):
                            standard_phase_text = "I/III"
                        elif re.match(".*One.*Two", temp_standard_phase):
                            standard_phase_text = "I/II"
                        elif re.match(".*Two.*Three", temp_standard_phase):
                            standard_phase_text = "II/III"
                        elif re.match(".*Three.*Four", temp_standard_phase):
                            standard_phase_text = "III/IV"
                        elif re.match(".*One", temp_standard_phase):
                            standard_phase_text = "I"
                        elif re.match(".*Two", temp_standard_phase):
                            standard_phase_text = "II"
                        elif re.match(".*Three", temp_standard_phase):
                            standard_phase_text = "III"
                        elif re.match(".*Four", temp_standard_phase):
                            standard_phase_text = "IV"
                    standard_phase_text = re.sub(re.compile(r"^其它其他说明:.+", re.S), "Other", standard_phase_text)
                except:
                    standard_phase_text=''
                # 试验分类
                try:
                    category_text = html.xpath('//table[@class="searchDetailTable"][3]//tr[1]/td[1]')[0].text
                except:
                    category_text=''
                # 试验范围
                try:
                    scope_text = html.xpath('//table[@class="searchDetailTable"][3]//tr[2]/td[3]')[0].text
                except:
                    scope_text=''
                # 年龄
                try:
                    age_text = html.xpath('//*[@id="collapseTwo"]/div/table[4]//tr[1]/td')[0].text
                except:
                    age_text=''
                # 性别
                try:
                    gender_text = html.xpath('//*[@id="collapseTwo"]/div/table[4]//tr[2]/td')[0].text
                except:
                    gender_text=''
                # 目标入组人数
                try:
                    planned_size_text = html.xpath('.//div[text()="2、试验人数"]/following::table[1]//tr[1]/td')[0].text
                except:
                    planned_size_text=''
                # 已入组人数
                try:
                    actual_size_text = html.xpath('.//div[text()="2、试验人数"]/following::table[1]//tr[2]/td')[0].text
                except:
                    actual_size_text=''
                # 实际入组总人数
                try:
                    final_size_text = html.xpath('.//div[text()="2、试验人数"]/following::table[1]//tr[3]/td')[0].text
                except:
                    final_size_text=''
                # 入选标准
                try:
                    inclusion_criteria_text = html.xpath('.//th[text()="入选标准"]/following::table[1]//text()')
                    inclusion_criteria_text = ''.join(str(i) for i in inclusion_criteria_text)
                except:
                    inclusion_criteria_text=''
                # 排除标准
                try:
                    exclusion_criteria_text = html.xpath('.//th[text()="排除标准"]/following::table[1]//text()')
                    exclusion_criteria_text = ''.join(str(i) for i in exclusion_criteria_text)
                except:
                    exclusion_criteria_text=''
                # 第一例受试者签署知情同意书日期
                try:
                    icf_date_text = html.xpath('.//div[text()="2、试验人数"]/following::table[2]//tr[1]/td')[0].text
                except:
                    icf_date_text=''
                # 第一例受试者入组日期
                try:
                    fpi_Date_text = html.xpath('.//div[text()="2、试验人数"]/following::table[2]//tr[2]/td')[0].text
                except:
                    fpi_Date_text=''
                # 试验完成日期
                try:
                    close_date_text = html.xpath('.//div[text()="2、试验人数"]/following::table[2]//tr[3]/td')[0].text
                except:
                    close_date_text=''
                # 试验目的
                try:
                    purpose_text = html.xpath('.//div[text()="1、试验目的"]/following::text()[1]')[0]
                except:
                    purpose_text=''
                # 试验专业题目
                try:
                    official_name_text = \
                        html.xpath('//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[7]/td')[
                            0].text.replace('\"', '')
                except:
                    official_name_text=''
                # 试验通俗题目
                try:
                    common_name_text =html.xpath('//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[8]/td')[0].text.replace('"', '')
                except:
                    common_name_text=''
                # 试验药
                try:
                    test_drugs_text = html.xpath('//*[@id="collapseTwo"]/div/table[5]//tr[1]//table//text()')
                    test_drugs_text = ''.join(str(i) for i in test_drugs_text)
                    test_drugs_text = test_drugs_text.replace('\r', '').replace('\n', '').replace('\t', '').replace('\"','').replace(' ', '').replace('序号名称用法', '')
                except:
                    test_drugs_text=''
                # 对照药
                try:
                    control_drugs_text = html.xpath('//*[@id="collapseTwo"]/div/table[5]//tr[2]//table//text()')
                    control_drugs_text = ''.join(str(i) for i in control_drugs_text)
                    control_drugs_text = control_drugs_text.replace('\r', '').replace('\n', '').replace('\t', '').replace('\"', '').replace(' ', '').replace('序号名称用法', '')
                except:
                    control_drugs_text=''
                trial = [
                    ctr_no_text, status_text, detail_status_text, requestor_text, sponsor_text,
                    publication_date_text, related_trial_no_text, drug_name_text, drug_previous_name_text,
                    drug_type_text, clinical_register_no_text, indication_text, phase_text, standard_phase_text,
                    category_text, scope_text, age_text, gender_text, planned_size_text, actual_size_text,
                    final_size_text, inclusion_criteria_text, exclusion_criteria_text, icf_date_text, fpi_Date_text,
                    close_date_text, purpose_text, official_name_text, common_name_text, test_drugs_text,
                    control_drugs_text
                ]
                trial_info = []
                trial_all_info = []
                for i in trial:
                    trial = i.replace('\r', '').replace('\n', '').replace('\t', '').replace('\"', '').replace(' ', '')
                    trial_info.append(trial)
                trial_all_info.append(trial_info)
                write_csv('data/trial_info.csv', trial_all_info)

                # >>>>> get_pi_info
                pi_data = []
                # 获取tab数量
                table = html.xpath(
                    './/table//th[@style="text-align: center;" and @rowspan="3"]/parent::tr/parent::table')
                tab_num = get_ele_number(table)
                for i in range(1, tab_num + 1):
                    try:
                        pi_name_text = html.xpath(f'.//table//th[@style="text-align: center;" and @rowspan="3" and text()="{i}"]/parent::tr/parent::table//tr[1]/td[1]')[0].text
                    except:
                        pi_name_text=''
                    try:
                        pi_title_text = html.xpath(f'.//table//th[@style="text-align: center;" and @rowspan="3" and text()="{i}"]/parent::tr/parent::table//tr[1]/td[3]')[0].text
                    except:
                        pi_title_text=''
                    try:
                        pi_phone_text = html.xpath(f'.//table//th[@style="text-align: center;" and @rowspan="3" and text()="{i}"]/parent::tr/parent::table//tr[2]/td[1]')[0].text
                    except:
                        pi_phone_text=''
                    try:
                        pi_mail_text = html.xpath(f'.//table//th[@style="text-align: center;" and @rowspan="3" and text()="{i}"]/parent::tr/parent::table//tr[2]/td[2]')[0].text
                    except:
                        pi_mail_text=''
                    try:
                        pi_postcode_text = html.xpath(f'.//table//th[@style="text-align: center;" and @rowspan="3" and text()="{i}"]/parent::tr/parent::table//tr[3]/td[1]')[0].text
                    except:
                        pi_postcode_text=''
                    try:
                        pi_site_name_text = html.xpath(f'.//table//th[@style="text-align: center;" and @rowspan="3" and text()="{i}"]/parent::tr/parent::table//tr[3]/td[2]')[0].text
                    except:
                        pi_site_name_text=''
                    pi_info = [ctr_no_text, pi_name_text, pi_title_text, pi_phone_text, pi_mail_text,
                               pi_postcode_text, pi_site_name_text]
                    pi_data.append(pi_info)
                write_csv('data/trial_pi_info.csv', pi_data)

                # >>>>> get_site_info
                site_data = []
                # 获取tab数量
                site_table = html.xpath('.//div[@class="sDPTit2" and text()="2、各参加机构信息"]/following::table[1]//tr')
                table_tr_num = get_ele_number(site_table)
                for i in range(2, table_tr_num + 1):
                    try:
                        site_name_text = html.xpath(f'.//div[text()="2、各参加机构信息"]/following::table[1]//tr[{i}]/td[2]')[0].text
                    except:
                        site_name_text=''
                    try:
                        pi_name_text = html.xpath(f'.//div[text()="2、各参加机构信息"]/following::table[1]//tr[{i}]/td[3]')[0].text
                    except:
                        pi_name_text=''
                    try:
                        country_text = html.xpath(f'.//div[text()="2、各参加机构信息"]/following::table[1]//tr[{i}]/td[4]')[0].text
                    except:
                        country_text=''
                    try:
                        province_state_text = html.xpath(f'.//div[text()="2、各参加机构信息"]/following::table[1]//tr[{i}]/td[5]')[0].text
                    except:
                        province_state_text=''
                    try:
                        city_text = html.xpath(f'.//div[text()="2、各参加机构信息"]/following::table[1]//tr[{i}]/td[6]')[0].text
                    except:
                        city_text=''

                    trial_site_info = [ctr_no_text, site_name_text, pi_name_text, country_text, province_state_text,city_text]
                    site_data.append(trial_site_info)
                write_csv('data/trial_site_info.csv', site_data)

                # >>>>> get_ec_info
                ec_data = []
                ec_table = html.xpath(
                    './/div[text()="五、伦理委员会信息"]/following::table[1]//tr')
                table_tr_num = get_ele_number(ec_table)
                for i in range(2, table_tr_num + 1):
                    try:
                        ec_name_text = html.xpath(
                            f'.//div[text()="五、伦理委员会信息"]/following::table[1]//tr[{i}]/td[2]')[0].text
                    except:
                        ec_name_text=''
                    try:
                        ec_conclusion_text = html.xpath(
                            f'.//div[text()="五、伦理委员会信息"]/following::table[1]//tr[{i}]/td[3]')[0].text.replace('\r','').replace('\n', '').replace('\t', '').replace('\"', '')
                    except:
                        ec_conclusion_text=''
                    try:
                        ec_date_text = html.xpath(
                            f'.//div[text()="五、伦理委员会信息"]/following::table[1]//tr[{i}]/td[4]')[0].text
                    except:
                        ec_date_text=''
                    trial_ec_info = [ctr_no_text, ec_name_text, ec_conclusion_text, ec_date_text]
                    ec_data.append(trial_ec_info)
                write_csv('data/trial_ec_info.csv', ec_data)


a = CdtSpider()
a.turn_page()
