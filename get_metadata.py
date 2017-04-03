from ghost import Ghost
import json

links = json.load(open("links.json"))
ids = [link.split("/")[-1].split("-")[0].split("_")[-1] for link in links]
ghost = Ghost()
session = ghost.start()
total_metadata = {}
for id in ids[:5000]:
    try:
        session.open('http://www.ultimateplans.com/Index.aspx')
        session.set_field_value("#m_ctlViewSearch_m_txtPlanNoData", id)
        session.click("#m_ctlViewSearch_m_hlinkSearch", expect_loading=True)
        href = session.evaluate("document.getElementById('m_ctlViewHomePlans_m_rptrHomePlans__ctl0_m_tblHomePlans').tBodies[0].rows[0].cells[0].children[0]")[0]['href']
        session.evaluate(href, expect_loading=True)
        fp_data = {}
        if session.evaluate("document.getElementById('m_ctlViewPlanDetails_m_lblMasterSuiteData').textContent")[0] == "Main":
            fp_data['master_suite'] = 1
        else:
            fp_data['master_suite'] = 0
        fp_data['footage'] = int(session.evaluate("document.getElementById('m_ctlViewPlanDetails_m_lblmFloorData').textContent")[0])
        fp_data['bedrooms'] = int(session.evaluate("document.getElementById('m_ctlViewPlanDetails_m_lblBedroomData').textContent")[0])
        fp_data['full_bath'] = int(session.evaluate("document.getElementById('m_ctlViewPlanDetails_m_lblBathData').textContent")[0])
        fp_data['half_bath'] = int(session.evaluate("document.getElementById('m_ctlViewPlanDetails_m_lblHalfBathData').textContent")[0])
        if session.evaluate("document.getElementById('m_ctlViewPlanDetails_m_lblLaundryData').textContent")[0] == "Main":
            fp_data['laundry'] = 1
        else:
            fp_data['laundry'] = 0
        fp_data['garage_bays'] = int(session.evaluate("document.getElementById('m_ctlViewPlanDetails_m_lblGarageData').textContent")[0])
        fp_data['width'] = int(session.evaluate("document.getElementById('m_ctlViewPlanDetails_m_lblWidthData').textContent")[0].split("'")[0])
        fp_data['length'] = int(session.evaluate("document.getElementById('m_ctlViewPlanDetails_m_lblDepthData').textContent")[0].split("'")[0])
        total_metadata[id] = fp_data
    except:
        print "Couldnt get data for plan %s" % id
json.dump(total_metadata, open("plan_metadata.json", "w+"))
