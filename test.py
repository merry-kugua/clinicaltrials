import re
import requests
from lxml import etree

from encapsulation import read_conf, get_ele_number, write_csv


class CdtSpider:
    def turn_page(self):
        parser = etree.HTMLParser(encoding="utf-8")
        html = etree.parse("data/a.html", parser=parser)
        # 登记号
        ctr_no_text = html.xpath('c')[0].text

        # >>>>> get_trial_info
        # 试验状态
        status_text = html.xpath('.//div[@id="collapseOne"]//table[@class="searchDetailTable"][1]/tr[1]/td[2]')[
            0].text
        # 六,试验状态
        detail_status_text = html.xpath('.//div[text()="1、试验状态"]/following::text()[1]')[0]
        # 申请人联系人
        requestor_text = \
            html.xpath('.//div[@id="collapseOne"]//table[@class="searchDetailTable"][1]/tr[2]/td[1]')[0].text
        # 申请人名称
        sponsor_text = \
            html.xpath('.//div[@id="collapseOne"]//table[@class="searchDetailTable"][1]/tr[3]/td[1]')[0].text
        # 首次公示信息日期
        publication_date_text = \
            html.xpath('.//div[@id="collapseOne"]//table[@class="searchDetailTable"][1]/tr[2]/td[2]')[0].text
        # 相关登记号
        related_trial_no_text = \
            html.xpath('.//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]/tr[2]/td')[0].text
        if related_trial_no_text == None:
            related_trial_no_text = ''
        # 药物名称&曾用名
        drug_text = \
            html.xpath('//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]//tr[3]/td')[0].text
        drug_name_text, drug_previous_name_text = drug_text.split('曾用名:')
        # 药物类型
        drug_type_text = html.xpath('//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]/tr[4]/td')[
            0].text
        # 临床申请受理号
        clinical_register_no_text = html.xpath(
            '//*[@id="collapseTwo"]/div/table[1]/tr[5]/th[contains(text(),"临床申请受理号")]/following::td[1]')[
            0].text.replace('企业选择不公示', '')
        # 适应症
        indication_text = html.xpath('//table[@class="searchDetailTable"][1]/tr[6]/td')[0].text
        # 试验分期 (未处理)
        phase_text = html.xpath('//table[@class="searchDetailTable"][3]/tr[1]/td[2]')[0].text
        # 试验分期
        standard_phase_text = html.xpath('//table[@class="searchDetailTable"][3]/tr[1]/td[2]')[0].text
        standard_phase_text = read_conf('trial_info', 'standard_phase', standard_phase_text)
        if standard_phase_text.find("其它其他说明:") >= 0:
            temp_standard_phase = standard_phase_text.replace("IV", "Four").replace("III", "Three"). \
                replace("II", "Two").replace("I", "One").replace("1", "One").replace("2", "Two") \
                .replace("3", "Three").replace("4", "IV")
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
        # 试验分类
        category_text = html.xpath('//table[@class="searchDetailTable"][3]//tr[1]/td[1]')[0].text
        # 试验范围
        scope_text = html.xpath('//table[@class="searchDetailTable"][3]/tr[2]/td[3]')[0].text
        # 年龄
        age_text = html.xpath('//*[@id="collapseTwo"]/div/table[4]/tr[1]/td')[0].text
        # 性别
        gender_text = html.xpath('//*[@id="collapseTwo"]/div/table[4]/tr[2]/td')[0].text
        # 目标入组人数
        planned_size_text = html.xpath('.//div[text()="2、试验人数"]/following::table[1]/tr[1]/td')[0].text
        # 已入组人数
        actual_size_text = html.xpath('.//div[text()="2、试验人数"]/following::table[1]/tr[2]/td')[0].text
        # 实际入组总人数
        final_size_text = html.xpath('.//div[text()="2、试验人数"]/following::table[1]/tr[3]/td')[0].text
        # 入选标准
        inclusion_criteria_text = html.xpath('.//th[text()="入选标准"]/following::table[1]//text()')
        inclusion_criteria_text = ''.join(str(i) for i in inclusion_criteria_text)
        # 排除标准
        exclusion_criteria_text = html.xpath('.//th[text()="排除标准"]/following::table[1]//text()')
        exclusion_criteria_text = ''.join(str(i) for i in exclusion_criteria_text)
        # 第一例受试者签署知情同意书日期
        icf_date_text = html.xpath('.//div[text()="2、试验人数"]/following::table[2]/tr[1]/td')[0].text
        # 第一例受试者入组日期
        fpi_Date_text = html.xpath('.//div[text()="2、试验人数"]/following::table[2]/tr[2]/td')[0].text
        # 试验完成日期
        close_date_text = html.xpath('.//div[text()="2、试验人数"]/following::table[2]/tr[3]/td')[0].text
        # 试验目的
        purpose_text = html.xpath('.//div[text()="1、试验目的"]/following::text()[1]')[0]
        # 试验专业题目
        official_name_text = \
            html.xpath('//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]/tr[7]/td')\
            [0].text.replace('\"', '')
        # 试验通俗题目
        common_name_text = \
            html.xpath('//div[@id="collapseTwo"]//table[@class="searchDetailTable"][1]/tr[8]/td')\
            [0].text.replace('"', '')
        # 试验药
        test_drugs_text=html.xpath('//*[@id="collapseTwo"]/div/table[5]//tr[1]//table//text()')
        test_drugs_text = ''.join(str(i) for i in test_drugs_text)
        test_drugs_text=test_drugs_text.replace('\r', '').replace('\n', '').replace('\t', '')\
            .replace('\"', '').replace(' ', '').replace('序号名称用法','')

        # 对照药
        control_drugs_text = html.xpath('//*[@id="collapseTwo"]/div/table[5]//tr[2]//table//text()')
        control_drugs_text = ''.join(str(i) for i in control_drugs_text)
        control_drugs_text = control_drugs_text.replace('\r', '').replace('\n', '').replace('\t', '')\
            .replace('\"', '').replace(' ','').replace('序号名称用法', '')

        trial = [
            ctr_no_text, status_text, detail_status_text, requestor_text, sponsor_text,
            publication_date_text, related_trial_no_text, drug_name_text, drug_previous_name_text, drug_type_text,
            clinical_register_no_text, indication_text, phase_text, standard_phase_text, category_text,
            scope_text, age_text, gender_text, planned_size_text, actual_size_text,
            final_size_text, inclusion_criteria_text, exclusion_criteria_text, icf_date_text, fpi_Date_text,
            close_date_text, purpose_text, official_name_text, common_name_text,control_drugs_text,test_drugs_text
        ]
        trial_info = []
        trial_all_info = []
        for i in trial:
            trial = i.replace('\r', '').replace('\n', '').replace('\t', '').replace('\"', '')\
                .replace(' ', '').replace(u'\xa0', '')
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
            pi_name_text = html.xpath(
                f'.//table//th[@style="text-align: center;" and @rowspan="3" and text()="{i}"]/parent::tr/parent::table//tr[1]/td[1]')[
                0].text
            pi_title_text = html.xpath(
                f'.//table//th[@style="text-align: center;" and @rowspan="3" and text()="{i}"]/parent::tr/parent::table//tr[1]/td[3]')[
                0].text
            pi_phone_text = html.xpath(
                f'.//table//th[@style="text-align: center;" and @rowspan="3" and text()="{i}"]/parent::tr/parent::table//tr[2]/td[1]')[
                0].text
            pi_mail_text = html.xpath(
                f'.//table//th[@style="text-align: center;" and @rowspan="3" and text()="{i}"]/parent::tr/parent::table//tr[2]/td[2]')[
                0].text
            pi_postcode_text = html.xpath(
                f'.//table//th[@style="text-align: center;" and @rowspan="3" and text()="{i}"]/parent::tr/parent::table//tr[3]/td[1]')[
                0].text
            pi_site_name_text = html.xpath(
                f'.//table//th[@style="text-align: center;" and @rowspan="3" and text()="{i}"]/parent::tr/parent::table//tr[3]/td[2]')[
                0].text

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
            site_name_text = html.xpath(
                f'.//div[text()="2、各参加机构信息"]/following::table[1]//tr[{i}]/td[2]')[0].text
            pi_name_text = html.xpath(
                f'.//div[text()="2、各参加机构信息"]/following::table[1]//tr[{i}]/td[3]')[0].text
            country_text = html.xpath(
                f'.//div[text()="2、各参加机构信息"]/following::table[1]//tr[{i}]/td[4]')[0].text
            province_state_text = html.xpath(
                f'.//div[text()="2、各参加机构信息"]/following::table[1]//tr[{i}]/td[5]')[0].text
            city_text = html.xpath(
                f'.//div[text()="2、各参加机构信息"]/following::table[1]//tr[{i}]/td[6]')[0].text
            trial_site_info = [ctr_no_text, site_name_text, pi_name_text, country_text, province_state_text,
                               city_text]
            site_data.append(trial_site_info)
        write_csv('data/trial_site_info.csv', site_data)

        # >>>>> get_ec_info
        ec_data = []
        ec_table = html.xpath(
            './/div[text()="五、伦理委员会信息"]/following::table[1]//tr')
        table_tr_num = get_ele_number(ec_table)
        for i in range(2, table_tr_num + 1):
            ec_name_text = html.xpath(
                f'.//div[text()="五、伦理委员会信息"]/following::table[1]//tr[{i}]/td[2]')[0].text
            ec_conclusion_text = html.xpath(
                f'.//div[text()="五、伦理委员会信息"]/following::table[1]//tr[{i}]/td[3]')[0].text.replace('\r', '').replace(
                '\n', '').replace('\t', '').replace('\"', '')
            ec_date_text = html.xpath(
                f'.//div[text()="五、伦理委员会信息"]/following::table[1]//tr[{i}]/td[4]')[0].text
            trial_ec_info = [ctr_no_text, ec_name_text, ec_conclusion_text, ec_date_text]
            ec_data.append(trial_ec_info)
        write_csv('data/trial_ec_info.csv', ec_data)


a = CdtSpider()
a.turn_page()
