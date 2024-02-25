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
                    doc_data = xmltodict.parse(raw_doc_data,
                                               process_namespaces=True,
                                               namespaces=namespaces,
                                               namespace_separator='_',
                                               attr_prefix='_',
                                               cdata_key='__value')
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
                self.logger.error("error for %s - %s " % (appNum, e))

        db.get_db_dirty().delete_items('gb', st13_ok)

    def process(self):
        pass