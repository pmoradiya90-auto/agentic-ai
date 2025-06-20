import xmltodict
import json


def convert_xml_to_json(xml_file_path):
    with open(xml_file_path, "r") as f:
        dict_data = xmltodict.parse(f.read())
        json_data = json.dumps(dict_data, indent=4)
        print(json_data)


xml_file_path = "/Users/pramilasingh/workspace/workspace_pradip_new/call_quality/test.xml"
convert_xml_to_json(xml_file_path)