#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CNCRS XML标签类定义
"""

from common import dictcm
from common.xmlcm import XmlTag


class CNCRSBaseTag(XmlTag):
    """
    CNCRS标签基类
    """

    def __init__(self, tag, **kwargs):
        """
        标签初始化
        @return: 无
        """
        # 为空的话,初始化
        if not kwargs:
            kwargs = {}
        # 标签默认前缀,如果指定的话,保留指定值
        if "prefix" not in kwargs or not kwargs["prefix"]:
            kwargs["prefix"] = "cncrs"

        super(CNCRSBaseTag, self).__init__(tag, **kwargs)

    def add_sub_tag_by_kv(self, k, v, prefix=None):
        """
        给当前标签添加子标签
        :param sub_tag: 子标签对象
        :return: 无
        """
        # 添加子标签
        tag = CNCRSBaseTag(k, value=v, prefix=prefix)
        self.add_sub_tag(tag)

    def add_sub_tags(self, keys, data_map, ignore_empty=True, prefix=None):
        """
        按照关键词一览和数据字典批量添加子标签
        :param keys:关键词列表
        :param data_map:数据字典
        :param ignore_empty:忽略空值
        :param prefix:子标签的前缀
        :return:无
        """
        for k in keys:
            v = dictcm.get(data_map, k)
            # 如果忽略空白,且值为空,则不添加子标签
            if ignore_empty and v is None:
                continue
            self.add_sub_tag_by_kv(k, v, prefix)


class CNCRSRootTag(CNCRSBaseTag):
    """
    CNCRS根节点标签
    """

    def __init__(self):
        """
        标签初始化
        @return: 无
        """
        init_param = {
            'attr': {'version': "1.0"},
            'xmlns': {
                'stc': "http://aeoi.chinatax.gov.cn/crs/stctypes/v1",
                'cncrs': "http://aeoi.chinatax.gov.cn/crs/cncrs/v1"
            }
        }
        super(CNCRSRootTag, self).__init__("CNCRS", **init_param)


class MessageHeaderTag(CNCRSBaseTag):
    """
    MessageHeader标签
    """

    def __init__(self, **kwargs):
        """
        标签初始化
        @return: 无
        """
        super(MessageHeaderTag, self).__init__("MessageHeader", **kwargs)
        # 用字典初始化子标签
        attr_keys = [
            "ReportingID",  # 系统用户账号
            "FIID",  # 金融机构注册码（固定长度14位）
            "ReportingType",  # 报送类型：固定为CRS
            "MessageRefId",  # 报告唯一编码，与报告文件名相同。
            "ReportingPeriod",  # 所报送数据所属公立年度，每个报告应仅包含一个年度的数据。
            "MessageTypeIndic",  # 报告类型（固定长度6位）
            "Tmstp"  # 报告生成时间戳（可以和文件名不一致）
        ]
        self.add_sub_tags(attr_keys, kwargs)


class ReportingGroupTag(CNCRSBaseTag):
    """
    ReportingGroup标签
    """

    def __init__(self, **kwargs):
        """
        标签初始化
        @return: 无
        """
        super(ReportingGroupTag, self).__init__("ReportingGroup", **kwargs)


class AccountReportTag(CNCRSBaseTag):
    """
    AccountReport标签
    """

    def __init__(self, **kwargs):
        """
        标签初始化
        @return: 无
        """
        super(AccountReportTag, self).__init__("AccountReport", **kwargs)


class AccountHolderTag(CNCRSBaseTag):
    """
    AccountHolder标签
    """

    def __init__(self, **kwargs):
        """
        标签初始化
        @return: 无
        """
        super(AccountHolderTag, self).__init__("AccountHolder", **kwargs)


class IndividualTag(CNCRSBaseTag):
    """
    Individual标签
    """

    def __init__(self, **kwargs):
        """
        标签初始化
        @return: 无
        """
        super(IndividualTag, self).__init__("Individual", **kwargs)


class OrganisationTag(CNCRSBaseTag):
    """
    Organisation标签
    """

    def __init__(self, **kwargs):
        """
        标签初始化
        @return: 无
        """
        super(OrganisationTag, self).__init__("Organisation", **kwargs)


class ControllingPersonTag(CNCRSBaseTag):
    """
    ControllingPerson标签
    """

    def __init__(self, **kwargs):
        """
        标签初始化
        @return: 无
        """
        super(ControllingPersonTag, self).__init__("ControllingPerson", **kwargs)


class DocSpecTag(CNCRSBaseTag):
    """
    DocSpec标签
    """

    def __init__(self, **kwargs):
        """
        标签初始化
        @return: 无
        """
        super(DocSpecTag, self).__init__("DocSpec", **kwargs)
        # 用字典初始化子标签
        tag_keys = [
            "DocRefId",  # 账户记录编号，不得重复（固定长度29位）
            "CorrDocRefId",  # 被修改或被删除的账户记录编号（固定长度29位）
            "DocTypeIndic"  # 账户报告的类型（固定长度2位）
        ]
        self.add_sub_tags(tag_keys, kwargs, prefix="stc")


class MoneyAmountTag(CNCRSBaseTag):
    """
    货币金额标签
    """

    def __init__(self, tag, curr_code, amount):
        """
        标签初始化
        @:param curr_code:货币代码
        @:param amount:金额
        @return: 无
        """
        init_param = {
            'attr': {'currCode': curr_code},
            'value': '%.2f' % amount
        }
        super(MoneyAmountTag, self).__init__(tag, **init_param)


class PaymentTag(CNCRSBaseTag):
    """
    Payment标签
    """

    def __init__(self, payment_type, curr_code, amount):
        """
        标签初始化
        @return: 无
        """
        super(PaymentTag, self).__init__("Payment")
        # 收入类型
        self.add_sub_tag_by_kv("PaymentType", payment_type)
        # 收入金额数量
        amount_tag = MoneyAmountTag("PaymentAmnt", curr_code, amount)
        self.add_sub_tag(amount_tag)


class NameTag(CNCRSBaseTag):
    """
    Name标签
    """

    def __init__(self, **kwargs):
        """
        标签初始化
        @:param curr_code:货币代码
        @:param amount:金额
        @return: 无
        """
        init_param = {
            'attr': {'nameType': dictcm.get(kwargs, "nameType")},
            'prefix': "stc"
        }
        super(NameTag, self).__init__("Name", **init_param)
        # 用字典初始化子标签
        tag_keys = [
            "FirstName",  # 英文(拼音)姓
            "LastName",  # 英文(拼音)名
            "NameCN"  # 中文姓名
        ]
        self.add_sub_tags(tag_keys, kwargs, prefix="stc")


class OrganisationNameTag(CNCRSBaseTag):
    """
    机构Name标签
    """

    def __init__(self, **kwargs):
        """
        标签初始化
        @:param curr_code:货币代码
        @:param amount:金额
        @return: 无
        """
        init_param = {
            'attr': {'nameType': dictcm.get(kwargs, "nameType")},
            'prefix': "stc"
        }
        super(OrganisationNameTag, self).__init__("Name", **init_param)
        # 用字典初始化子标签
        tag_keys = [
            "OrganisationNameEN",  # 机构英文名
            "OrganisationNameCN"  # 机构中文名
        ]
        self.add_sub_tags(tag_keys, kwargs, prefix="stc")


class AddressTag(CNCRSBaseTag):
    """
    Address标签
    """

    def __init__(self, address_type, country_code, city_en, address_free_en, address_free_cn):
        """
        标签初始化
        @:param curr_code:货币代码
        @:param amount:金额
        @return: 无
        """
        init_param = {
            'attr': {'legalAddressType': address_type},
            'prefix' : "stc"
        }
        super(AddressTag, self).__init__("Address", **init_param)
        # 国家代码
        self.add_sub_tag_by_kv("CountryCode", country_code, prefix="stc")
        # 英文地址
        adr_en = CNCRSBaseTag("AddressEN", prefix="stc")
        # 英文固定地址
        adr_fix_en = CNCRSBaseTag("AddressFixEN", prefix="stc")
        adr_fix_en.add_sub_tag(CNCRSBaseTag("CityEN", value=city_en, prefix="stc"))
        adr_en.add_sub_tag(adr_fix_en)
        adr_en.add_sub_tag(CNCRSBaseTag("AddressFreeEN", value=address_free_en, prefix="stc"))
        self.add_sub_tag(adr_en)

        # 中文文地址
        adr_cn = CNCRSBaseTag("AddressCN", prefix="stc")
        adr_cn.add_sub_tag(CNCRSBaseTag("AddressFreeCN", value=address_free_cn, prefix="stc"))
        self.add_sub_tag(adr_cn)


class TINTag(CNCRSBaseTag):
    """
    纳税人识别号标签
    """

    def __init__(self, country_code, tin_code):
        """
        标签初始化
        @:param country_code:国家代码
        @:param tin_code:识别号
        @return: 无
        """
        init_param = {
            'attr': {
                'issuedBy': country_code,
                'inType': "TIN"
            },
            'value': tin_code,
            'prefix': "stc"
        }
        super(TINTag, self).__init__("TIN", **init_param)


class BirthInfoTag(CNCRSBaseTag):
    """
    BirthInfo标签
    """

    def __init__(self, birth_date, country_code):
        """
        标签初始化
        @:param birth_date:生日日期(YYYY-MM-DD)
        @:param country_code:出生国代码
        @return: 无
        """
        super(BirthInfoTag, self).__init__("BirthInfo", prefix="stc")
        # 生日
        self.add_sub_tag_by_kv("BirthDate", birth_date, prefix="stc")
        # 国家
        country = CNCRSBaseTag("CountryInfo", prefix="stc")
        country.add_sub_tag(CNCRSBaseTag("CountryCode", value=country_code, prefix="stc"))
        self.add_sub_tag(country)
