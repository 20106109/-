#coding:utf-8
from main import *
from csv_manager import *
from functools import partial
from register_func_manager import Register
crawler_dict = Register()
crawler_dict_other = Register()#包含爬取时间过长以及selenium相关
@crawler_dict
def sichuan_crawler():
    sichuan_test = sichuan()
    sichuan_test.get_sichuan_administrative_normative_documents('http://sthjt.sc.gov.cn/sthjt/c23101801/xzgfxwj.shtml')
    sichuan_test.get_sichuan_other_documents('http://sthjt.sc.gov.cn/sthjt/c23101802/qtwj.shtml')
@crawler_dict
def shanghai_crawler():
    shanghai_test = shanghai()
    shanghai_test.get_shanghai_other_documents('https://sthj.sh.gov.cn/hbzhywpt2025/index.html')
    shanghai_test.get_shanghai_normative_documents('https://sthj.sh.gov.cn/hbzhywpt2022/index.html')
    shanghai_test.get_shanghai_announcement('https://sthj.sh.gov.cn/hbzhywpt5004/index.html')
    shanghai_test.get_shanghai_local_law('https://sthj.sh.gov.cn/hbzhywpt1013/hbzhywpt1042/index.html')
@crawler_dict
def beijing_crawler():
    beijing_test = beijing()
    beijing_test.get_beijing_local_standards('http://sthjj.beijing.gov.cn/bjhrb/index/xxgk69/zfxxgk43/fdzdgknr2/dfbz/index.html')
    beijing_test.get_beijing_policy('http://sthjj.beijing.gov.cn/bjhrb/index/xxgk69/zfxxgk43/fdzdgknr2/zcfb/325821937/index.html')
    beijing_test.get_beijing_announcement('http://sthjj.beijing.gov.cn/bjhrb/index/xxgk69/zfxxgk43/fdzdgknr2/325924085/index.html')
@crawler_dict
def tianjin_crawler():
    tianjin_test = tianjin()
    tianjin_test.get_tianjin_announcement('https://sthj.tj.gov.cn/ZWXX808/TZGG6419/')
@crawler_dict
def hebei_crawler():
    hebei_test = hebei()
    hebei_test.get_hebei_announcement('http://hbepb.hebei.gov.cn/hbhjt/zwgk/fdzdgknr/tongzhigonggao/')
@crawler_dict
def shanxi_crawler():
    shanxi_test = shanxi()
    shanxi_test.get_shanxi_local_standards('http://sthjt.shanxi.gov.cn/zwgk/hbbz/dfhjbhbz/')
    shanxi_test.get_shanxi_Departmental_normative_documents('http://sthjt.shanxi.gov.cn/zwgk/zcfg/gfxwj_1/dfgfxwj/')
    shanxi_test.get_shanxi_normative_documents('http://sthjt.shanxi.gov.cn/zfxxgk/zdgkjbml/fgwj/gfxwj/')
@crawler_dict
def neimenggu_crawler():
    neimenggu_test = neimenggu()
    neimenggu_test.get_neimenggu_local_law('https://sthjt.nmg.gov.cn/xxgk/zfxxgk/fdzdgknr/?gk=3&cid=16280')
@crawler_dict
def liaoning_crawler():
    liaoning_test = liaoning()
    liaoning_test.get_liaoning_announcement('https://sthj.ln.gov.cn/sthj/index/tzgg/index.shtml')
    liaoning_test.get_liaoning_liaohuanhan('https://sthj.ln.gov.cn/sthj/xxgk/zwxxgk/xxgkml/index.shtml')
    liaoning_test.get_liaoning_liaohuanfa('https://sthj.ln.gov.cn/sthj/xxgk/zwxxgk/xxgkml/index.shtml')
    liaoning_test.get_liaoning_liaohuanban('https://sthj.ln.gov.cn/sthj/xxgk/zwxxgk/xxgkml/index.shtml')
    liaoning_test.get_liaoning_other('https://sthj.ln.gov.cn/sthj/xxgk/zwxxgk/xxgkml/index.shtml')
@crawler_dict
def jilin_crawler():
    jilin_test = jilin()
    jilin_test.get_jilin_announcement('http://sthjt.jl.gov.cn/ywdt/tzgg/')
@crawler_dict
def heilongjiang_crawler():
    heilongjiang_test = heilongjiang()
    heilongjiang_test.get_heilongjiang_administrative_normative_documents('http://sthj.hlj.gov.cn/sthj/c111958/public_zfxxgk.shtml?tab=gkzc')
@crawler_dict
def jiangsu_crawler():
    jiangsu_test = jiangsu()
    jiangsu_test.get_jiangsu_normative_documents('http://sthjt.jiangsu.gov.cn/col/col89427/index.html')
    jiangsu_test.get_jiangsu_law('http://sthjt.jiangsu.gov.cn/col/col83738/index.html')
    jiangsu_test.get_jiangsu_ecological_environment_standards('http://sthjt.jiangsu.gov.cn/col/col83739/index.html')
@crawler_dict
def zhejiang_crawler():
    zhejiang_test = zhejiang()
    zhejiang_test.get_zhejiang_announcement('http://sthjt.zj.gov.cn/col/col1229263559/index.html')
    zhejiang_test.get_zhejiang_local_standards('http://sthjt.zj.gov.cn/col/col1201911/index.html')
    zhejiang_test.get_zhejiang_local_law('http://sthjt.zj.gov.cn/col/col1229564975/index.html')
@crawler_dict
def anhui_crawler():
    anhui_test = anhui()
    anhui_test.get_anhui_active_publicity('https://sthjt.ah.gov.cn/public/column/21691?type=4&action=list&nav=3&catId=32709621')
    anhui_test.get_anhui_publicity('https://sthjt.ah.gov.cn/public/column/21691?type=6&action=xinzheng')
@crawler_dict
def fujian_crawler():
    fujian_test = fujian()
    fujian_test.get_fujian_policies_law('http://sthjt.fujian.gov.cn/zwgk/flfg/')
    fujian_test.get_fujian_announcement('http://sthjt.fujian.gov.cn/zwgk/gsgg/')
    fujian_test.get_fujian_normative_documents('http://sthjt.fujian.gov.cn/zwgk/zfxxgkzl/zfxxgkml/gfxwj/')
    fujian_test.get_fujian_policy('http://sthjt.fujian.gov.cn/zwgk/zfxxgkzl/zfxxgkml/mlflfg/')
@crawler_dict
def jiangxi_crawler():
    jiangxi_test = jiangxi()
    jiangxi_test.get_jiangxi_local_standards('http://sthjt.jiangxi.gov.cn/col/col48703/index.html')
    jiangxi_test.get_jiangxi_announcement('http://sthjt.jiangxi.gov.cn/col/col42164/index.html')
    jiangxi_test.get_jiangxi_plan('http://sthjt.jiangxi.gov.cn/col/col42202/index.html')
@crawler_dict
def shandong_crawler():
    shandong_test = shandong()
    shandong_test.get_shandong_policies_law('http://xxgk.sdein.gov.cn/xxgkml/hjbhgfxwj/')
    shandong_test.get_shandong_normative_documents('http://zfc.sdein.gov.cn/gfxwj/xxyxgfxwj/')
@crawler_dict_other
def hunan_crawler():
    hunan_test = hunan()
    hunan_test.get_hunan_announcement('http://sthjt.hunan.gov.cn/sthjt/xxgk/tzgg/index.html')
    hunan_test.get_hunan_local_law('http://sthjt.hunan.gov.cn/sthjt/xxgk/zcfg/dfxfg/index.html')
    hunan_test.get_hunan_normative_documents('http://sthjt.hunan.gov.cn/sthjt/xxgk/zcfg/gfxwj/index.html')
@crawler_dict
def hubei_crawler():
    hubei_test = hubei()
    hubei_test.get_hubei_active_publicity('http://sthjt.hubei.gov.cn/fbjd/zc/zcwj/')
    hubei_test.get_hubei_ecological_environment_standards('http://sthjt.hubei.gov.cn/fbjd/xxgkml/gysyjs/sthj/hjbz/')
    hubei_test.get_hubei_local_law('http://sthjt.hubei.gov.cn/fbjd/xxgkml/gysyjs/sthj/sthjfg/flfg/')
@crawler_dict
def henan_crawler():
    henan_test = henan()
    henan_test.get_henan_announcement('https://sthjt.henan.gov.cn/xxzy/tzgg/')
    henan_test.get_henan_environmental('https://sthjt.henan.gov.cn/xxgk/hbwj/')
@crawler_dict
def guangdong_crawler():
    guangdong_test = guangdong()
    guangdong_test.get_guangdong_normative_documents('http://gdee.gd.gov.cn/hbwj/index.html')
    guangdong_test.get_guangdong_announcement('http://gdee.gd.gov.cn/ggtz3126/index.html')
    guangdong_test.get_guangdong_standards('http://gdee.gd.gov.cn/gkmlpt/index#3155')
@crawler_dict
def guangxi_crawler():
    guangxi_test = guangxi()
    guangxi_test.get_guangxi_local_standards('http://sthjt.gxzf.gov.cn/zfxxgk/zfxxgkgl/fdzdgknr/zcfg/dfsthjbz/')
    guangxi_test.get_guangxi_normative_documents('http://sthjt.gxzf.gov.cn/zfxxgk/zfxxgkgl/fdzdgknr/zcfg/gfxwj/')
@crawler_dict
def hainan_crawler():
    hainan_test = hainan()
    hainan_test.get_hainan_normative_documents('http://hnsthb.hainan.gov.cn/xxgk/0200/0202/zwgk/zcfg/')
    hainan_test.get_hainan_proclamation('http://hnsthb.hainan.gov.cn/xxgk/0400/tzgg_gg/')
    hainan_test.get_hainan_notice('http://hnsthb.hainan.gov.cn/xxgk/0400/tzgg_tz/')
@crawler_dict
def chongqing_crawler():
    chongqing_test = chongqing()
    chongqing_test.get_chongqing_announcement('https://sthjj.cq.gov.cn/zwxx_249/tzgg/')
@crawler_dict_other
def guizhou_crawler():
    guizhou_test = guizhou()
    guizhou_test.get_guizhou_normative_documents('https://sthj.guizhou.gov.cn/zwgk/gzhgfxwjsjk/gfxwjsjk/')
    guizhou_test.get_guizhou_departmental_documents('https://sthj.guizhou.gov.cn/zwgk/zcwj/tjwj/')
    guizhou_test.get_guizhou_law_standards('https://sthj.guizhou.gov.cn/zwgk/zdlyxx/fgybz/flfgjbz/')
@crawler_dict
def yunnan_crawler():
    yunan_test = yunnan()
    yunan_test.get_yunnan_publicity('https://sthjt.yn.gov.cn/xxgk/index.aspx')
@crawler_dict
def shan_xi_crawler():
    shan_xi_test = shan_xi()
    shan_xi_test.get_shan_xi_normative_documents('http://sthjt.shaanxi.gov.cn/html/hbt/zfxxgk/guifanxingwenjian/index.html')
    shan_xi_test.get_shan_xi_standards('http://sthjt.shaanxi.gov.cn/html/hbt/standard/fgbzxq/index.html')
@crawler_dict
def ningxia_crawler():
    ningxia_test = ningxia()
    ningxia_test.get_ningxia_publicity('https://sthjt.nx.gov.cn/zfxxgk/fdzdgknr/lzyj/')
    ningxia_test.get_ningxia_announcement('https://sthjt.nx.gov.cn/xwzx/gsgg/')
    ningxia_test.get_ningxia_standards('https://sthjt.nx.gov.cn/zwgk/fgbz/bzgf_63327/')

@crawler_dict
def xinjiang_crawler():
    xinjiang_test = xinjiang()
    xinjiang_test.get_xinjiang_notice('http://sthjt.xinjiang.gov.cn/xjepd/gwbgtz/common_list.shtml')
    xinjiang_test.get_xinjiang_proclamation('http://sthjt.xinjiang.gov.cn/xjepd/gwbggg/common_list.shtml')
    xinjiang_test.get_xinjiang_publicity('http://www.xjbt.gov.cn/xxgk/zdgk/tzgg/')
@crawler_dict
def shengtaihuanjingbu_crawler():
    shengtaihuanjingbu_test = shengtaihuanjingbu()
    shengtaihuanjingbu_test.get_shengtaihuanjingbu_policy('https://www.mee.gov.cn/zcwj/')
    shengtaihuanjingbu_test.get_shengtaihuanjingbu_law('https://www.mee.gov.cn/xxgk2018/')
    shengtaihuanjingbu_test.get_shengtaihuanjingbu_administrative_normative_documents('https://www.mee.gov.cn/xxgk2018/')
    shengtaihuanjingbu_test.get_shengtaihuanjingbu_ecological_environment_standards('https://www.mee.gov.cn/ywgz/fgbz/bz/bzfb/')
@crawler_dict_other
def zhongguorenminzhengfu_crawler():
    zhongguorenminzhengfu_test = zhongguorenminzhengfu()
    zhongguorenminzhengfu_test.get_zhongguorenminzhengfu_policy('https://sousuo.www.gov.cn/zcwjk/policyDocumentLibrary?q=&t=zhengcelibrary_bm&orpro=')
    zhongguorenminzhengfu_test.get_zhongguorenminzhengfu_publicity('https://www.gov.cn/zhengce/xxgk/')
@crawler_dict
def jiaotongyunshubu_crawler():
    jiaotongyunshubu_test = jiaotongyunshubu()
    jiaotongyunshubu_test.get_jiaotongyunshubu_publicity('https://xxgk.mot.gov.cn/2020/jigou/?gk=5')
@crawler_dict
def ziranziyuanbu_crawler():
    ziranziyuanbu_test = ziranziyuanbu()
    ziranziyuanbu_test.get_ziranziyuanbu_standards('https://www.mnr.gov.cn/gk/bzgf/')
    ziranziyuanbu_test.get_ziranziyuanbu_publicity('http://f.mnr.gov.cn/')
    ziranziyuanbu_test.get_ziranziyuanbu_announcement('https://www.mnr.gov.cn/gk/tzgg/')
@crawler_dict
def fazhangaigewei_crawler():
    fazhangaigewei_test = fazhangaigewei()
    fazhangaigewei_test.get_fazhangaigewei_order('https://www.ndrc.gov.cn/xxgk/zcfb/fzggwl/')
    fazhangaigewei_test.get_fazhangaigewei_normative_documents('https://www.ndrc.gov.cn/xxgk/zcfb/ghxwj/')
    fazhangaigewei_test.get_fazhangaigewei_proclamation('https://www.ndrc.gov.cn/xxgk/zcfb/gg/')
    fazhangaigewei_test.get_fazhangaigewei_notice('https://www.ndrc.gov.cn/xxgk/zcfb/tz/')
# print(crawler_dict.items())

############################################################
# sichuan_test = sichuan()
# partial(sichuan_test.get_sichuan_administrative_normative_documents,'http://sthjt.sc.gov.cn/sthjt/c23101801/xzgfxwj.shtml')
# partial(sichuan_test.get_sichuan_other_documents,'http://sthjt.sc.gov.cn/sthjt/c23101802/qtwj.shtml')
# shanghai_test = shanghai()
# partial(shanghai_test.get_shanghai_other_documents,'https://sthj.sh.gov.cn/hbzhywpt2025/index.html')
# partial(shanghai_test.get_shanghai_normative_documents,'https://sthj.sh.gov.cn/hbzhywpt2022/index.html')
# partial(shanghai_test.get_shanghai_announcement,'https://sthj.sh.gov.cn/hbzhywpt5004/index.html')
# partial(shanghai_test.get_shanghai_local_law,'https://sthj.sh.gov.cn/hbzhywpt1013/hbzhywpt1042/index.html')
# beijing_test = beijing()
# partial(beijing_test.get_beijing_local_standards,'http://sthjj.beijing.gov.cn/bjhrb/index/xxgk69/zfxxgk43/fdzdgknr2/dfbz/index.html')
# partial(beijing_test.get_beijing_policy,'http://sthjj.beijing.gov.cn/bjhrb/index/xxgk69/zfxxgk43/fdzdgknr2/zcfb/325821937/index.html')
# partial(beijing_test.get_beijing_announcement,'http://sthjj.beijing.gov.cn/bjhrb/index/xxgk69/zfxxgk43/fdzdgknr2/325924085/index.html')
# tianjin_test = tianjin()
# partial(tianjin_test.get_tianjin_announcement,'https://sthj.tj.gov.cn/ZWXX808/TZGG6419/')
# hebei_test = hebei()
# partial(hebei_test.get_hebei_announcement,'http://hbepb.hebei.gov.cn/hbhjt/zwgk/fdzdgknr/tongzhigonggao/')
# shanxi_test = shanxi()
# partial(shanxi_test.get_shanxi_local_standards,'http://sthjt.shanxi.gov.cn/zwgk/hbbz/dfhjbhbz/')
# partial(shanxi_test.get_shanxi_Departmental_normative_documents,'http://sthjt.shanxi.gov.cn/zwgk/zcfg/gfxwj_1/dfgfxwj/')
# partial(shanxi_test.get_shanxi_normative_documents,'http://sthjt.shanxi.gov.cn/zfxxgk/zdgkjbml/fgwj/gfxwj/')
# neimenggu_test = neimenggu()
# partial(neimenggu_test.get_neimenggu_local_law,'https://sthjt.nmg.gov.cn/xxgk/zfxxgk/fdzdgknr/?gk=3&cid=16280')
# liaoning_test = liaoning()
# partial(liaoning_test.get_liaoning_announcement,'https://sthj.ln.gov.cn/sthj/index/tzgg/index.shtml')
# partial(liaoning_test.get_liaoning_liaohuanhan,'https://sthj.ln.gov.cn/sthj/xxgk/zwxxgk/xxgkml/index.shtml')
# partial(liaoning_test.get_liaoning_liaohuanfa,'https://sthj.ln.gov.cn/sthj/xxgk/zwxxgk/xxgkml/index.shtml')
# partial(liaoning_test.get_liaoning_liaohuanban,'https://sthj.ln.gov.cn/sthj/xxgk/zwxxgk/xxgkml/index.shtml')
# partial(liaoning_test.get_liaoning_other,'https://sthj.ln.gov.cn/sthj/xxgk/zwxxgk/xxgkml/index.shtml')
# jilin_test = jilin()
# partial(jilin_test.get_jilin_announcement,'http://sthjt.jl.gov.cn/ywdt/tzgg/')
# heilongjiang_test = heilongjiang()
# partial(heilongjiang_test.get_heilongjiang_administrative_normative_documents,'http://sthj.hlj.gov.cn/sthj/c111958/public_zfxxgk.shtml?tab=gkzc')
# jiangsu_test = jiangsu()
# partial(jiangsu_test.get_jiangsu_normative_documents,'http://sthjt.jiangsu.gov.cn/col/col89427/index.html')
# partial(jiangsu_test.get_jiangsu_law,'http://sthjt.jiangsu.gov.cn/col/col83738/index.html')
# partial(jiangsu_test.get_jiangsu_ecological_environment_standards,'http://sthjt.jiangsu.gov.cn/col/col83739/index.html')
# zhejiang_test = zhejiang()
# partial(zhejiang_test.get_zhejiang_announcement,'http://sthjt.zj.gov.cn/col/col1229263559/index.html')
# partial(zhejiang_test.get_zhejiang_local_standards,'http://sthjt.zj.gov.cn/col/col1201911/index.html')
# partial(zhejiang_test.get_zhejiang_local_law,'http://sthjt.zj.gov.cn/col/col1229564975/index.html')
# anhui_test = anhui()
# partial(anhui_test.get_anhui_active_publicity,'https://sthjt.ah.gov.cn/public/column/21691?type=4&action=list&nav=3&catId=32709621')
# partial(anhui_test.get_anhui_publicity,'https://sthjt.ah.gov.cn/public/column/21691?type=6&action=xinzheng')
# fujian_test = fujian()
# partial(fujian_test.get_fujian_policies_law,'http://sthjt.fujian.gov.cn/zwgk/flfg/')
# partial(fujian_test.get_fujian_announcement,'http://sthjt.fujian.gov.cn/zwgk/gsgg/')
# partial(fujian_test.get_fujian_normative_documents,'http://sthjt.fujian.gov.cn/zwgk/zfxxgkzl/zfxxgkml/gfxwj/')
# partial(fujian_test.get_fujian_policy,'http://sthjt.fujian.gov.cn/zwgk/zfxxgkzl/zfxxgkml/mlflfg/')
# jiangxi_test = jiangxi()
# partial(jiangxi_test.get_jiangxi_local_standards,'http://sthjt.jiangxi.gov.cn/col/col48703/index.html')
# partial(jiangxi_test.get_jiangxi_announcement,'http://sthjt.jiangxi.gov.cn/col/col42164/index.html')
# partial(jiangxi_test.get_jiangxi_plan,'http://sthjt.jiangxi.gov.cn/col/col42202/index.html')
# shandong_test = shandong()
# partial(shandong_test.get_shandong_policies_law,'http://xxgk.sdein.gov.cn/xxgkml/hjbhgfxwj/')
# partial(shandong_test.get_shandong_normative_documents,'http://zfc.sdein.gov.cn/gfxwj/xxyxgfxwj/')
# hunan_test = hunan()
# partial(hunan_test.get_hunan_announcement,'http://sthjt.hunan.gov.cn/sthjt/xxgk/tzgg/index.html')
# partial(hunan_test.get_hunan_local_law,'http://sthjt.hunan.gov.cn/sthjt/xxgk/zcfg/dfxfg/index.html')
# partial(hunan_test.get_hunan_normative_documents,'http://sthjt.hunan.gov.cn/sthjt/xxgk/zcfg/gfxwj/index.html')
# hubei_test = hubei()
# partial(hubei_test.get_hubei_active_publicity,'http://sthjt.hubei.gov.cn/fbjd/zc/zcwj/')
# partial(hubei_test.get_hubei_ecological_environment_standards,'http://sthjt.hubei.gov.cn/fbjd/xxgkml/gysyjs/sthj/hjbz/')
# partial(hubei_test.get_hubei_local_law,'http://sthjt.hubei.gov.cn/fbjd/xxgkml/gysyjs/sthj/sthjfg/flfg/')
# henan_test = henan()
# partial(henan_test.get_henan_announcement,'https://sthjt.henan.gov.cn/xxzy/tzgg/')
# partial(henan_test.get_henan_environmental,'https://sthjt.henan.gov.cn/xxgk/hbwj/')
# guangdong_test = guangdong()
# partial(guangdong_test.get_guangdong_normative_documents,'http://gdee.gd.gov.cn/hbwj/index.html')
# partial(guangdong_test.get_guangdong_announcement,'http://gdee.gd.gov.cn/ggtz3126/index.html')
# partial(guangdong_test.get_guangdong_standards,'http://gdee.gd.gov.cn/gkmlpt/index#3155')
# guangxi_test = guangxi()
# partial(guangxi_test.get_guangxi_local_standards,'http://sthjt.gxzf.gov.cn/zfxxgk/zfxxgkgl/fdzdgknr/zcfg/dfsthjbz/')
# partial(guangxi_test.get_guangxi_normative_documents,'http://sthjt.gxzf.gov.cn/zfxxgk/zfxxgkgl/fdzdgknr/zcfg/gfxwj/')
# hainan_test = hainan()
# partial(hainan_test.get_hainan_normative_documents,'http://hnsthb.hainan.gov.cn/xxgk/0200/0202/zwgk/zcfg/')
# partial(hainan_test.get_hainan_proclamation,'http://hnsthb.hainan.gov.cn/xxgk/0400/tzgg_gg/')
# partial(hainan_test.get_hainan_notice,'http://hnsthb.hainan.gov.cn/xxgk/0400/tzgg_tz/')
# chongqing_test = chongqing()
# partial(chongqing_test.get_chongqing_announcement,'https://sthjj.cq.gov.cn/zwxx_249/tzgg/')
# guizhou_test = guizhou()
# partial(guizhou_test.get_guizhou_normative_documents,'https://sthj.guizhou.gov.cn/zwgk/gzhgfxwjsjk/gfxwjsjk/')
# partial(guizhou_test.get_guizhou_departmental_documents,'https://sthj.guizhou.gov.cn/zwgk/zcwj/tjwj/')
# partial(guizhou_test.get_guizhou_law_standards,'https://sthj.guizhou.gov.cn/zwgk/zdlyxx/fgybz/flfgjbz/')
# yunan_test = yunnan()
# partial(yunan_test.get_yunnan_publicity,'https://sthjt.yn.gov.cn/xxgk/index.aspx')
# shan_xi_test = shan_xi()
# partial(shan_xi_test.get_shan_xi_normative_documents,'http://sthjt.shaanxi.gov.cn/html/hbt/zfxxgk/guifanxingwenjian/index.html')
# partial(shan_xi_test.get_shan_xi_standards,'http://sthjt.shaanxi.gov.cn/html/hbt/standard/fgbzxq/index.html')
# ningxia_test = ningxia()
# partial(ningxia_test.get_ningxia_publicity,'https://sthjt.nx.gov.cn/zfxxgk/fdzdgknr/lzyj/')
# partial(ningxia_test.get_ningxia_announcement,'https://sthjt.nx.gov.cn/xwzx/gsgg/')
# partial(ningxia_test.get_ningxia_standards,'https://sthjt.nx.gov.cn/zwgk/fgbz/bzgf_63327/')
#
# xinjiang_test = xinjiang()
# partial(xinjiang_test.get_xinjiang_notice,'http://sthjt.xinjiang.gov.cn/xjepd/gwbgtz/common_list.shtml')
# partial(xinjiang_test.get_xinjiang_proclamation,'http://sthjt.xinjiang.gov.cn/xjepd/gwbggg/common_list.shtml')
# partial(xinjiang_test.get_xinjiang_publicity,'http://www.xjbt.gov.cn/xxgk/zdgk/tzgg/')
# shengtaihuanjingbu_test = shengtaihuanjingbu()
# partial(shengtaihuanjingbu_test.get_shengtaihuanjingbu_policy,'https://www.mee.gov.cn/zcwj/')
# partial(shengtaihuanjingbu_test.get_shengtaihuanjingbu_law,'https://www.mee.gov.cn/xxgk2018/')
# partial(shengtaihuanjingbu_test.get_shengtaihuanjingbu_administrative_normative_documents,'https://www.mee.gov.cn/xxgk2018/')
# partial(shengtaihuanjingbu_test.get_shengtaihuanjingbu_ecological_environment_standards,'https://www.mee.gov.cn/ywgz/fgbz/bz/bzfb/')
# zhongguorenminzhengfu_test = zhongguorenminzhengfu()
# partial(zhongguorenminzhengfu_test.get_zhongguorenminzhengfu_policy,'https://sousuo.www.gov.cn/zcwjk/policyDocumentLibrary?q=&t=zhengcelibrary_bm&orpro=')
# partial(zhongguorenminzhengfu_test.get_zhongguorenminzhengfu_publicity,'https://www.gov.cn/zhengce/xxgk/')
# jiaotongyunshubu_test = jiaotongyunshubu()
# partial(jiaotongyunshubu_test.get_jiaotongyunshubu_publicity,'https://xxgk.mot.gov.cn/2020/jigou/?gk=5')
# ziranziyuanbu_test = ziranziyuanbu()
# partial(ziranziyuanbu_test.get_ziranziyuanbu_standards,'https://www.mnr.gov.cn/gk/bzgf/')
# partial(ziranziyuanbu_test.get_ziranziyuanbu_publicity,'http://f.mnr.gov.cn/')
# partial(ziranziyuanbu_test.get_ziranziyuanbu_announcement,'https://www.mnr.gov.cn/gk/tzgg/')
# fazhangaigewei_test = fazhangaigewei()
# partial(fazhangaigewei_test.get_fazhangaigewei_order('https://www.ndrc.gov.cn/xxgk/zcfb/fzggwl/'))
# partial(fazhangaigewei_test.get_fazhangaigewei_normative_documents,'https://www.ndrc.gov.cn/xxgk/zcfb/ghxwj/')
# partial(fazhangaigewei_test.get_fazhangaigewei_proclamation,'https://www.ndrc.gov.cn/xxgk/zcfb/gg/')
# partial(fazhangaigewei_test.get_fazhangaigewei_notice,'https://www.ndrc.gov.cn/xxgk/zcfb/tz/')
#########################################################

def start_crawling():
    # sichuan_test = sichuan()
    # sichuan_test.get_sichuan_administrative_normative_documents('http://sthjt.sc.gov.cn/sthjt/c23101801/xzgfxwj.shtml')
    # sichuan_test.get_sichuan_other_documents('http://sthjt.sc.gov.cn/sthjt/c23101802/qtwj.shtml')
    # shanghai_test = shanghai()
    # shanghai_test.get_shanghai_other_documents('https://sthj.sh.gov.cn/hbzhywpt2025/index.html')
    # shanghai_test.get_shanghai_normative_documents('https://sthj.sh.gov.cn/hbzhywpt2022/index.html')
    # shanghai_test.get_shanghai_announcement('https://sthj.sh.gov.cn/hbzhywpt5004/index.html')
    # shanghai_test.get_shanghai_local_law('https://sthj.sh.gov.cn/hbzhywpt1013/hbzhywpt1042/index.html')
    # beijing_test = beijing()
    # beijing_test.get_beijing_local_standards('http://sthjj.beijing.gov.cn/bjhrb/index/xxgk69/zfxxgk43/fdzdgknr2/dfbz/index.html')
    # beijing_test.get_beijing_policy('http://sthjj.beijing.gov.cn/bjhrb/index/xxgk69/zfxxgk43/fdzdgknr2/zcfb/325821937/index.html')
    # beijing_test.get_beijing_announcement('http://sthjj.beijing.gov.cn/bjhrb/index/xxgk69/zfxxgk43/fdzdgknr2/325924085/index.html')
    # tianjin_test = tianjin()
    # tianjin_test.get_tianjin_announcement('https://sthj.tj.gov.cn/ZWXX808/TZGG6419/')
    # hebei_test = hebei()
    # hebei_test.get_hebei_announcement('http://hbepb.hebei.gov.cn/hbhjt/zwgk/fdzdgknr/tongzhigonggao/')
    # shanxi_test = shanxi()
    # shanxi_test.get_shanxi_local_standards('http://sthjt.shanxi.gov.cn/zwgk/hbbz/dfhjbhbz/')
    # shanxi_test.get_shanxi_Departmental_normative_documents('http://sthjt.shanxi.gov.cn/zwgk/zcfg/gfxwj_1/dfgfxwj/')
    # shanxi_test.get_shanxi_normative_documents('http://sthjt.shanxi.gov.cn/zfxxgk/zdgkjbml/fgwj/gfxwj/')
    # neimenggu_test = neimenggu()
    # neimenggu_test.get_neimenggu_local_law('https://sthjt.nmg.gov.cn/xxgk/zfxxgk/fdzdgknr/?gk=3&cid=16280')
    # liaoning_test = liaoning()
    # liaoning_test.get_liaoning_announcement('https://sthj.ln.gov.cn/sthj/index/tzgg/index.shtml')
    # liaoning_test.get_liaoning_liaohuanhan('https://sthj.ln.gov.cn/sthj/xxgk/zwxxgk/xxgkml/index.shtml')
    # liaoning_test.get_liaoning_liaohuanfa('https://sthj.ln.gov.cn/sthj/xxgk/zwxxgk/xxgkml/index.shtml')
    # liaoning_test.get_liaoning_liaohuanban('https://sthj.ln.gov.cn/sthj/xxgk/zwxxgk/xxgkml/index.shtml')
    # liaoning_test.get_liaoning_other('https://sthj.ln.gov.cn/sthj/xxgk/zwxxgk/xxgkml/index.shtml')
    # jilin_test = jilin()
    # jilin_test.get_jilin_announcement('http://sthjt.jl.gov.cn/ywdt/tzgg/')
    # heilongjiang_test = heilongjiang()
    # heilongjiang_test.get_heilongjiang_administrative_normative_documents('http://sthj.hlj.gov.cn/sthj/c111958/public_zfxxgk.shtml?tab=gkzc')
    # jiangsu_test = jiangsu()
    # jiangsu_test.get_jiangsu_normative_documents('http://sthjt.jiangsu.gov.cn/col/col89427/index.html')
    # jiangsu_test.get_jiangsu_law('http://sthjt.jiangsu.gov.cn/col/col83738/index.html')
    # jiangsu_test.get_jiangsu_ecological_environment_standards('http://sthjt.jiangsu.gov.cn/col/col83739/index.html')
    # zhejiang_test = zhejiang()
    # zhejiang_test.get_zhejiang_announcement('http://sthjt.zj.gov.cn/col/col1229263559/index.html')
    # zhejiang_test.get_zhejiang_local_standards('http://sthjt.zj.gov.cn/col/col1201911/index.html')
    # zhejiang_test.get_zhejiang_local_law('http://sthjt.zj.gov.cn/col/col1229564975/index.html')
    # anhui_test = anhui()
    # anhui_test.get_anhui_active_publicity('https://sthjt.ah.gov.cn/public/column/21691?type=4&action=list&nav=3&catId=32709621')
    # anhui_test.get_anhui_publicity('https://sthjt.ah.gov.cn/public/column/21691?type=6&action=xinzheng')
    # fujian_test = fujian()
    # fujian_test.get_fujian_policies_law('http://sthjt.fujian.gov.cn/zwgk/flfg/')
    # fujian_test.get_fujian_announcement('http://sthjt.fujian.gov.cn/zwgk/gsgg/')
    # fujian_test.get_fujian_normative_documents('http://sthjt.fujian.gov.cn/zwgk/zfxxgkzl/zfxxgkml/gfxwj/')
    # fujian_test.get_fujian_policy('http://sthjt.fujian.gov.cn/zwgk/zfxxgkzl/zfxxgkml/mlflfg/')
    # jiangxi_test = jiangxi()
    # jiangxi_test.get_jiangxi_local_standards('http://sthjt.jiangxi.gov.cn/col/col48703/index.html')
    # jiangxi_test.get_jiangxi_announcement('http://sthjt.jiangxi.gov.cn/col/col42164/index.html')
    # jiangxi_test.get_jiangxi_plan('http://sthjt.jiangxi.gov.cn/col/col42202/index.html')
    # shandong_test = shandong()
    # shandong_test.get_shandong_policies_law('http://xxgk.sdein.gov.cn/xxgkml/hjbhgfxwj/')
    # shandong_test.get_shandong_normative_documents('http://zfc.sdein.gov.cn/gfxwj/xxyxgfxwj/')
    # hunan_test = hunan()
    # hunan_test.get_hunan_announcement('http://sthjt.hunan.gov.cn/sthjt/xxgk/tzgg/index.html')
    # hunan_test.get_hunan_local_law('http://sthjt.hunan.gov.cn/sthjt/xxgk/zcfg/dfxfg/index.html')
    # hunan_test.get_hunan_normative_documents('http://sthjt.hunan.gov.cn/sthjt/xxgk/zcfg/gfxwj/index.html')
    # hubei_test = hubei()
    # hubei_test.get_hubei_active_publicity('http://sthjt.hubei.gov.cn/fbjd/zc/zcwj/')
    # hubei_test.get_hubei_ecological_environment_standards('http://sthjt.hubei.gov.cn/fbjd/xxgkml/gysyjs/sthj/hjbz/')
    # hubei_test.get_hubei_local_law('http://sthjt.hubei.gov.cn/fbjd/xxgkml/gysyjs/sthj/sthjfg/flfg/')
    # henan_test = henan()
    # henan_test.get_henan_announcement('https://sthjt.henan.gov.cn/xxzy/tzgg/')
    # henan_test.get_henan_environmental('https://sthjt.henan.gov.cn/xxgk/hbwj/')
    # guangdong_test = guangdong()
    # guangdong_test.get_guangdong_normative_documents('http://gdee.gd.gov.cn/hbwj/index.html')
    # guangdong_test.get_guangdong_announcement('http://gdee.gd.gov.cn/ggtz3126/index.html')
    # guangdong_test.get_guangdong_standards('http://gdee.gd.gov.cn/gkmlpt/index#3155')
    # guangxi_test = guangxi()
    # guangxi_test.get_guangxi_local_standards('http://sthjt.gxzf.gov.cn/zfxxgk/zfxxgkgl/fdzdgknr/zcfg/dfsthjbz/')
    # guangxi_test.get_guangxi_normative_documents('http://sthjt.gxzf.gov.cn/zfxxgk/zfxxgkgl/fdzdgknr/zcfg/gfxwj/')
    # hainan_test = hainan()
    # hainan_test.get_hainan_normative_documents('http://hnsthb.hainan.gov.cn/xxgk/0200/0202/zwgk/zcfg/')
    # hainan_test.get_hainan_proclamation('http://hnsthb.hainan.gov.cn/xxgk/0400/tzgg_gg/')
    # hainan_test.get_hainan_notice('http://hnsthb.hainan.gov.cn/xxgk/0400/tzgg_tz/')
    # chongqing_test = chongqing()
    # chongqing_test.get_chongqing_announcement('https://sthjj.cq.gov.cn/zwxx_249/tzgg/')
    # guizhou_test = guizhou()
    # guizhou_test.get_guizhou_normative_documents('https://sthj.guizhou.gov.cn/zwgk/gzhgfxwjsjk/gfxwjsjk/')
    # guizhou_test.get_guizhou_departmental_documents('https://sthj.guizhou.gov.cn/zwgk/zcwj/tjwj/')
    # guizhou_test.get_guizhou_law_standards('https://sthj.guizhou.gov.cn/zwgk/zdlyxx/fgybz/flfgjbz/')
    # yunan_test = yunnan()
    # yunan_test.get_yunnan_publicity('https://sthjt.yn.gov.cn/xxgk/index.aspx')
    # shan_xi_test = shan_xi()
    # shan_xi_test.get_shan_xi_normative_documents('http://sthjt.shaanxi.gov.cn/html/hbt/zfxxgk/guifanxingwenjian/index.html')
    # shan_xi_test.get_shan_xi_standards('http://sthjt.shaanxi.gov.cn/html/hbt/standard/fgbzxq/index.html')
    # ningxia_test = ningxia()
    # ningxia_test.get_ningxia_publicity('https://sthjt.nx.gov.cn/zfxxgk/fdzdgknr/lzyj/')
    # ningxia_test.get_ningxia_announcement('https://sthjt.nx.gov.cn/xwzx/gsgg/')
    # ningxia_test.get_ningxia_standards('https://sthjt.nx.gov.cn/zwgk/fgbz/bzgf_63327/')

    # xinjiang_test = xinjiang()
    # xinjiang_test.get_xinjiang_notice('http://sthjt.xinjiang.gov.cn/xjepd/gwbgtz/common_list.shtml')
    # xinjiang_test.get_xinjiang_proclamation('http://sthjt.xinjiang.gov.cn/xjepd/gwbggg/common_list.shtml')
    # xinjiang_test.get_xinjiang_publicity('http://www.xjbt.gov.cn/xxgk/zdgk/tzgg/')
    # shengtaihuanjingbu_test = shengtaihuanjingbu()
    # shengtaihuanjingbu_test.get_shengtaihuanjingbu_policy('https://www.mee.gov.cn/zcwj/')
    # shengtaihuanjingbu_test.get_shengtaihuanjingbu_law('https://www.mee.gov.cn/xxgk2018/')
    # shengtaihuanjingbu_test.get_shengtaihuanjingbu_administrative_normative_documents('https://www.mee.gov.cn/xxgk2018/')
    # shengtaihuanjingbu_test.get_shengtaihuanjingbu_ecological_environment_standards('https://www.mee.gov.cn/ywgz/fgbz/bz/bzfb/')
    # zhongguorenminzhengfu_test = zhongguorenminzhengfu()
    # zhongguorenminzhengfu_test.get_zhongguorenminzhengfu_policy('https://sousuo.www.gov.cn/zcwjk/policyDocumentLibrary?q=&t=zhengcelibrary_bm&orpro=')
    # zhongguorenminzhengfu_test.get_zhongguorenminzhengfu_publicity('https://www.gov.cn/zhengce/xxgk/')
    # jiaotongyunshubu_test = jiaotongyunshubu()
    # jiaotongyunshubu_test.get_jiaotongyunshubu_publicity('https://xxgk.mot.gov.cn/2020/jigou/?gk=5')
    # ziranziyuanbu_test = ziranziyuanbu()
    # ziranziyuanbu_test.get_ziranziyuanbu_standards('https://www.mnr.gov.cn/gk/bzgf/')
    # ziranziyuanbu_test.get_ziranziyuanbu_publicity('http://f.mnr.gov.cn/')
    # ziranziyuanbu_test.get_ziranziyuanbu_announcement('https://www.mnr.gov.cn/gk/tzgg/')
    # fazhangaigewei_test = fazhangaigewei()
    # fazhangaigewei_test.get_fazhangaigewei_order('https://www.ndrc.gov.cn/xxgk/zcfb/fzggwl/')
    # fazhangaigewei_test.get_fazhangaigewei_normative_documents('https://www.ndrc.gov.cn/xxgk/zcfb/ghxwj/')
    # fazhangaigewei_test.get_fazhangaigewei_proclamation('https://www.ndrc.gov.cn/xxgk/zcfb/gg/')
    # fazhangaigewei_test.get_fazhangaigewei_notice('https://www.ndrc.gov.cn/xxgk/zcfb/tz/')
    start()
    dboperation()

if __name__=='__main__':
    start_crawling()
    # dboperation()
    pass










