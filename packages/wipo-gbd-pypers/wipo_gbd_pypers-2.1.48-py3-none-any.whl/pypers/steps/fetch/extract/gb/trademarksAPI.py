import os

import requests
import xmltodict
import json
from pypers.core.interfaces import db
from pypers.steps.base.extract import ExtractBase


class TrademarksAPI(ExtractBase):
    """
    Extract GBTM archive
    """
    spec = {
        "version": "2.0",
        "descr": [
            "Returns the directory with the extraction"
        ],
        "args":
        {
            "outputs": [
                {
                    "name": "del_list",
                    "descr": "del file that contains a list of application"
                             " numbers to be deleted"
                }
            ],
        }
    }

    def collect_files(self, file):
        f_name, ext = os.path.splitext(os.path.basename(file))
        self.add_xml_file(f_name, file)

    def unpack_archive(self, archive, dest):
        return archive

    def add_xml_file(self, filename, fullpath):
        xml_dir = os.path.join(self.extraction_dir, 'xml')
        if not os.path.exists(xml_dir):
            os.makedirs(xml_dir)
        with open(fullpath, 'r') as f:
            st13s = json.loads(f.read())
        mapping = {
            'applicants': 'applicant',
            'representatives': 'representative'
        }
        namespaces = {
            'http://gb.tmview.europa.eu/trademark/data': None,
            'http://gb.tmview.europa.eu/trademark/applicant': None,
            'http://gb.tmview.europa.eu/trademark/representative': None
        }
        st13_ok = []
        for appNum in st13s:
            url = 'https://soap.ipo.gov.uk/trademark/data/%s' % appNum

            try:
                with requests.session() as session:
                    raw_doc_data = session.get(url, timeout=0.5).content
                    raw_doc_data = '<Transaction xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://gb.tmview.europa.eu/trademark/data"><TransactionHeader><SenderDetails><RequestProducerDateTime>2024-02-21T14:30:46.2804623Z</RequestProducerDateTime></SenderDetails></TransactionHeader><TradeMarkTransactionBody><TransactionContentDetails><TransactionIdentifier>20240221143046</TransactionIdentifier><TransactionCode>GB-TM-Search Trade Mark</TransactionCode><TransactionData><TradeMarkDetails><TradeMark><RegistrationOfficeCode>GB</RegistrationOfficeCode><ApplicationNumber>UK00003289573</ApplicationNumber><ApplicationDate>2018-02-12</ApplicationDate><RegistrationNumber>UK00003289573</RegistrationNumber><RegistrationDate>2018-07-13</RegistrationDate><ApplicationReference>THR.049-TTT</ApplicationReference><ApplicationLanguageCode>en</ApplicationLanguageCode><ExpiryDate>2028-02-12</ExpiryDate><MarkCurrentStatusCode>Registered</MarkCurrentStatusCode><MarkCurrentStatusDate>2018-02-12</MarkCurrentStatusDate><KindMark>Individual</KindMark><MarkFeature>Word</MarkFeature><TotalMarkSeries>0</TotalMarkSeries><TradeDistinctivenessIndicator>false</TradeDistinctivenessIndicator><OppositionPeriodStartDate>2018-05-04</OppositionPeriodStartDate><OppositionPeriodEndDate>2018-07-04</OppositionPeriodEndDate><WordMarkSpecification><MarkVerbalElementText languageCode="en">THE TWISTED TAILOR</MarkVerbalElementText></WordMarkSpecification><GoodsServicesDetails><GoodsServices><ClassDescriptionDetails><ClassDescription><ClassNumber>14</ClassNumber><GoodsServicesDescription languageCode="en">Jewellery; cuff links; horological and chronometric instruments; parts and fittings for the aforesaid goods.   Goods made of precious metals and their alloys, or coated therewith, namely, rings, necklaces, tie clips, collar bars and collar tips being jewelry, cuff links, bracelets, earrings, lapel pins, brooches, key rings.</GoodsServicesDescription></ClassDescription><ClassDescription><ClassNumber>18</ClassNumber><GoodsServicesDescription languageCode="en">Trunks, travelling bags, wallets (pocket-), purses, cases, namely, attaché cases, business cases, carrying cases, cases for keys, catalogue cases, music cases, leather cases, overnight cases, pullman cases, travel cases, business and calling card cases, cosmetic cases sold empty, vanity cases sold empty, backpacks, briefcases; umbrellas.</GoodsServicesDescription></ClassDescription><ClassDescription><ClassNumber>25</ClassNumber><GoodsServicesDescription languageCode="en">Clothing, footwear, headgear; neckties; belts (clothing).    Suits, formal jackets, formal trousers, shirts, coats, outerwear, namely, overcoats, jackets, raincoats, heavy coats, jeans, t-shirts, polo shirts, casual jackets, casual trousers, shorts, knitwear, namely, v-neck sweaters, round neck sweaters, roll neck sweaters, cardigans, swimwear, namely, shorts and trunks,  hats, caps.</GoodsServicesDescription></ClassDescription></ClassDescriptionDetails></GoodsServices></GoodsServicesDetails><ApplicantDetails><ApplicantKey><URI>http://www.ipo.gov.uk/trademark/applicant/507772</URI></ApplicantKey></ApplicantDetails><RepresentativeDetails><RepresentativeKey><URI>http://www.ipo.gov.uk/trademark/representative/9865</URI></RepresentativeKey></RepresentativeDetails></TradeMark></TradeMarkDetails></TransactionData></TransactionContentDetails></TradeMarkTransactionBody></Transaction>'
                    doc_data = xmltodict.parse(raw_doc_data,
                                               process_namespaces=True,
                                               namespaces=namespaces,
                                               namespace_separator='_',
                                               attr_prefix='_',
                                               cdata_key='__value')
                    raw_addr = [
                        '<Transaction xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://gb.tmview.europa.eu/trademark/applicant"><TransactionHeader><SenderDetails><RequestProducerDateTime>2024-02-21T14:31:19.8740194Z</RequestProducerDateTime></SenderDetails></TransactionHeader><TradeMarkTransactionBody><TransactionContentDetails><TransactionIdentifier>20240221143119</TransactionIdentifier><TransactionCode>GB-TM-Search Applicant</TransactionCode><TransactionData><ApplicantDetails><Applicant><ApplicantIdentifier>507772</ApplicantIdentifier><ApplicantIncorporationCountryCode>GB</ApplicantIncorporationCountryCode><ApplicantAddressBook><FormattedNameAddress><Name><FreeFormatName><FreeFormatNameDetails><FreeFormatNameLine>Utopia Holdings Limited</FreeFormatNameLine></FreeFormatNameDetails></FreeFormatName></Name><Address><AddressCountryCode>GB</AddressCountryCode><FreeFormatAddress><FreeFormatAddressLine>Finsgate</FreeFormatAddressLine><FreeFormatAddressLine>5-7 Cranwood Street</FreeFormatAddressLine><FreeFormatAddressLine>LONDON</FreeFormatAddressLine><FreeFormatAddressLine>EC1V 9EE</FreeFormatAddressLine></FreeFormatAddress></Address></FormattedNameAddress></ApplicantAddressBook></Applicant></ApplicantDetails></TransactionData></TransactionContentDetails></TradeMarkTransactionBody></Transaction>',
                        '<Transaction xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://gb.tmview.europa.eu/trademark/representative"><TransactionHeader><SenderDetails><RequestProducerDateTime>2024-02-21T14:31:32.6069379Z</RequestProducerDateTime></SenderDetails></TransactionHeader><TradeMarkTransactionBody><TransactionContentDetails><TransactionIdentifier>20240221143132</TransactionIdentifier><TransactionCode>GB-TM-Search Representative</TransactionCode><TransactionData><RepresentativeDetails><Representative><RepresentativeIdentifier>9865</RepresentativeIdentifier><RepresentativeAddressBook><FormattedNameAddress><Name><FreeFormatName><FreeFormatNameDetails><FreeFormatNameLine>Squire Patton Boggs (UK) LLP</FreeFormatNameLine></FreeFormatNameDetails></FreeFormatName></Name><Address><AddressCountryCode>GB</AddressCountryCode><FreeFormatAddress><FreeFormatAddressLine>60 London Wall</FreeFormatAddressLine><FreeFormatAddressLine>London</FreeFormatAddressLine><FreeFormatAddressLine>EC2M 5TQ</FreeFormatAddressLine></FreeFormatAddress></Address></FormattedNameAddress></RepresentativeAddressBook></Representative></RepresentativeDetails></TransactionData></TransactionContentDetails></TradeMarkTransactionBody></Transaction>'
                    ]
                    counter = 0
                    for type in ['applicants', 'representatives']:
                        address_path = doc_data.get('Transaction', {}).get('TradeMarkTransactionBody', {}).get(
                            'TransactionContentDetails', {}).get('TransactionData', {}).get('TradeMarkDetails', {}).get(
                            'TradeMark', {}).get('%sDetails' % mapping[type].capitalize(), {})
                        if not address_path:
                            continue
                        if not isinstance(address_path, list):
                            address_path = [address_path]
                        to_replace = doc_data.get('Transaction', {}).get('TradeMarkTransactionBody', {}).get(
                            'TransactionContentDetails', {}).get('TransactionData', {}).get('TradeMarkDetails', {}).get(
                            'TradeMark', {})
                        to_replace['%sDetails' % mapping[type].capitalize()] = []
                        for addr in address_path:
                            url = addr.get('%sKey' % mapping[type].capitalize(), {}).get('URI', None)
                            address_data = session.get(url, timeout=0.5).content
                            address_data = raw_addr[counter]
                            counter += 1
                            address_data = xmltodict.parse(address_data,
                                                           process_namespaces=True,
                                                           namespaces=namespaces,
                                                           namespace_separator='_',
                                                           attr_prefix='_',
                                                           cdata_key='__value')
                            address_data = address_data.get('Transaction', {}).get('TradeMarkTransactionBody', {}).get(
                                'TransactionContentDetails', {}).get('TransactionData', {}).get(
                                '%sDetails' % mapping[type].capitalize(), {}).get(mapping[type].capitalize(), {})
                            to_replace['%sDetails' % mapping[type].capitalize()].append(address_data)
                    doc_data = doc_data.get('Transaction', {}).get('TradeMarkTransactionBody', {}).get(
                        'TransactionContentDetails', {}).get('TransactionData', {}).get('TradeMarkDetails', {})
                    appxml_file = os.path.join(xml_dir, '%s.json' % appNum)
                    with open(appxml_file, 'w') as f:
                        f.write(json.dumps(doc_data))

                    self.manifest['data_files'].setdefault(appNum, {})
                    self.manifest['data_files'][appNum]['ori'] = os.path.relpath(
                        appxml_file, self.extraction_dir)
                    st13_ok.append(appNum)
            except Exception as e:
                self.logger.error("error for %s - %s " % (fullpath, e))

            db.get_db_dirty().delete_items('gb', st13_ok)

    def process(self):
        pass