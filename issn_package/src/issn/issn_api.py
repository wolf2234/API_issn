import requests
from typing import Union
from time import sleep


def load_data_by_url(url: str, params: dict) -> dict:
    """Функція завантажує дані через мережу.
       Для цього вона робить запит по url адресу.

    :param url: url адрес ресурсу
    :param params: параметри запиту
    :return: словник з даними по ouci
    """

    max_attemp_count = 3
    request_timeout = 1000
    attemp = 0
    data = {}

    while attemp < max_attemp_count:
        try:
            params["format"] = "json"
            response = requests.get(url, params=params)
            data = response.json()
        except requests.exceptions.ConnectionError:
            message = "Error: No internet connection!"
            return {"error_message": message}
        except requests.exceptions.HTTPError:
            message = "Error: URL isn't valid!"
            return {"error_message": message}
        except requests.exceptions.JSONDecodeError as exception_json:
            message = f"error=Invalid JSON; description='{exception_json}';"
            return {"error_message": message}
        except:
            data = None

        if data and (not data.get("error")) and (not data.get("exception")):
            break

        attemp += 1
        sleep(request_timeout)

    if data.get("error") and data.get("exception"):
        message = f"status={data.get('status')}; error={data.get('error')}; description='{data.get('exception')}';"
        return {"error_message": message}
    return data


def get_by_issn(issn: str) -> dict:
    """Функція повертає дані по issn.

    :param issn: ідентифікатор issn
    :return: Словник з даними по issn
    """

    api_url = f"https://portal.issn.org/resource/ISSN/{issn}"
    params = {"issn": issn}

    data = load_data_by_url(url=api_url, params=params)
    result = parse_issn_data(issn, data)

    return result


def parse_issn_data(issn: str, data: dict) -> dict:
    """Функція розпізнає дані по issn.

    :param issn: ідентифікатор issn
    :param data: дані по issn
    :return: Словник з даними по issn
    """

    result = {
        "issn": issn,
        "data": {},
        "unparsed_keys": [],
        "unsuccessful": [],
        "errors": [],
        "stats": {},
    }

    graph = data.get("@graph")
    issn_data = {}
    counter = len(graph) if graph else 0
    unsuccess = 0
    unparsed = 0

    if not graph:
        result["errors"].append(f"ISSN '{issn}' is invalid!!!")
        result["errors"].append(data["error_message"])
        return result

    for item in graph:
        id_attr = item.get("@id")

        if not id_attr:
            continue

        if id_attr.startswith("http://id.loc.gov/vocabulary/countries"):
            country = parse_country(item)
            issn_data["Country"] = country[0]
        elif id_attr.startswith("organization/ISSNCenter"):
            organization = parse_oraganization(item)
            issn_data["Organization"] = organization[0]
        elif id_attr == f"resource/ISSN/{issn}#ReferencePublicationEvent":
            country_code = parse_country_code(item)
            issn_data["CountryCode"] = country_code[0]
        elif id_attr == f"resource/ISSN/{issn}#ISSN":
            resource_issn = parse_issn(issn, item)
            issn_data["ISSN"] = resource_issn[0]
        elif id_attr == f"resource/ISSN/{issn}#ISSN-L":
            resource_issnL = parse_issnL(item)
            issn_data["ISSN-L"] = resource_issnL[0]
        elif id_attr == f"resource/ISSN/{issn}#KeyTitle":
            key_title = parse_key_title(item)
            issn_data["KeyTitle"] = key_title[0]
        elif id_attr == f"resource/ISSN/{issn}#Record":
            record = parse_record(item)
            issn_data.update(record[0])
        elif id_attr == f"resource/ISSN/{issn}":
            another_resource_data = parse_issn_resource(item)
            issn_data["ISSN_resource"] = issn
            issn_data["resource"] = another_resource_data[0]
        elif id_attr.startswith("resource/ISSN-L/"):
            result["unparsed_keys"].append("resource/ISSN-L/{issn-L}")
            unparsed += 1
        elif id_attr.startswith(f"resource/ISSN/{issn}#InterveningPublicationEvent"):
            result["unparsed_keys"].append(
                "resource/ISSN/{issn}#InterveningPublicationEvent"
            )
            unparsed += 1
        elif id_attr.startswith(f"resource/ISSN/{issn}#PublicationPlace"):
            result["unparsed_keys"].append("resource/ISSN/{issn}#PublicationPlace")
            unparsed += 1
        elif id_attr.startswith(f"resource/ISSN/{issn}#ReproductionPlace"):
            result["unparsed_keys"].append("resource/ISSN/{issn}#ReproductionPlace")
            unparsed += 1
        elif id_attr.startswith(f"resource/ISSN/{issn}#Publisher"):
            result["unparsed_keys"].append("resource/ISSN/{issn}#Publisher")
            unparsed += 1
        elif id_attr.startswith(f"resource/ISSN/{issn}#IssuingBody"):
            result["unparsed_keys"].append("resource/ISSN/{issn}#IssuingBody")
            unparsed += 1
        elif id_attr.startswith(f"resource/ISSN/{issn}#ReproductionAgency"):
            result["unparsed_keys"].append("resource/ISSN/{issn}#ReproductionAgency")
            unparsed += 1
        elif id_attr.startswith(f"organization/keepers#"):
            result["unparsed_keys"].append("organization/keepers#{keeperCode}")
            unparsed += 1
        elif id_attr.endswith(f"GeoCoordinates"):
            result["unparsed_keys"].append(
                "resource/ISSN/{issn}#PublicationPlace-{placename}-GeoCoordinates"
            )
            unparsed += 1
        elif id_attr.endswith(f"Geocoordinates"):
            result["unparsed_keys"].append(
                "resource/ISSN/{issn}#ReproductionPlace-{placeName}-Geocoordinates"
            )
            unparsed += 1
        elif id_attr == f"resource/ISSN/{issn}#CODEN":
            result["unparsed_keys"].append("resource/ISSN/{issn}#CODEN")
            unparsed += 1
        elif id_attr == f"resource/ISSN/{issn}#AbbreviatedKeyTitle":
            result["unparsed_keys"].append("resource/ISSN/{issn}#AbbreviatedKeyTitle")
            unparsed += 1
        elif id_attr == f"resource/ISSN/{issn}#LatestPublicationEvent":
            result["unparsed_keys"].append(
                "resource/ISSN/{issn}#LatestPublicationEvent"
            )
            unparsed += 1
        else:
            result["unsuccessful"].append(id_attr)
            unsuccess += 1

    result["data"] = issn_data

    stats = {
        "total_keys": counter,
        "success_keys": (counter - unsuccess),
        "unsuccess_keys": unsuccess,
        "unparsed_keys": unparsed,
    }

    result["stats"] = stats

    return result


def parse_issn_resource(item: dict) -> tuple:
    errors = {"parse_issn_resource": []}

    if "url" not in item:
        errors["parse_issn_resource"].append(f"attribute 'url' doesnt exist in {item}")

    if "name" not in item:
        errors["parse_issn_resource"].append(
            f"attribute 'name' doesn't exist in {item}"
        )

    if "otherPhysicalFormat" not in item:
        errors["parse_issn_resource"].append(
            f"attribute 'otherPhysicalFormat' doesn't exist in {item}"
        )

    if "title" not in item:
        errors["parse_issn_resource"].append(
            f"attribute 'title' doesn't exist in {item}"
        )

    if "isFormatOf" not in item:
        errors["parse_issn_resource"].append(
            f"attribute 'isFormatOf' doesn't exist in {item}"
        )

    if "isPartOf" not in item:
        errors["parse_issn_resource"].append(
            f"attribute 'isPartOf' doesn't exist in {item}"
        )

    if "identifiedBy" not in item:
        errors["parse_issn_resource"].append(
            f"attribute 'identifiedBy' doesn't exist in {item}"
        )

    if "mainTitle" not in item:
        errors["parse_issn_resource"].append(
            f"attribute 'mainTitle' doesn't exist in {item}"
        )

    resource = {
        "Format": parse_format(item)[0],
        "URL": item.get("url"),
        "Name": item.get("name"),
        "Title": item.get("title"),
        "identifiedBy": item.get("identifiedBy"),
        "mainTitle": item.get("mainTitle"),
        "otherPhysicalFormat": item.get("otherPhysicalFormat"),
        "isFormatOf": item.get("isFormatOf"),
        "isPartOf": item.get("isPartOf"),
    }
    return (resource, errors)


def parse_oraganization(item: dict) -> Union[tuple, None]:
    errors = {"parse_oraganization": []}

    if item.get("@type") != "http://schema.org/Organization":
        errors["parse_oraganization"].append(
            f"attribute '@type' != 'http://schema.org/Organization', {item}"
        )
        return (None, errors)

    code = item.get("@id").split("#")[1]
    return (code, errors)


def parse_country(item: dict) -> Union[tuple, None]:
    errors = {"parse_country": []}

    if "label" not in item:
        errors["parse_country"].append(f"attribute 'label' doesn't exist in {item}")

    return (item.get("label"), errors)


def parse_country_code(item: dict) -> Union[tuple, None]:
    errors = {"parse_country_code": []}

    if item.get("@type") != "http://schema.org/PublicationEvent":
        errors["parse_country_code"].append(
            f"attribute '@type' != 'http://schema.org/PublicationEvent', {item}"
        )

    if "location" not in item:
        errors["parse_country_code"].append(
            f"attribute 'location' doesn't exist in {item}"
        )
        return (None, errors)

    location = item.get("location").split("/")
    code = location[len(location) - 1]
    return (code, errors)


def parse_status(item: dict) -> Union[tuple, None]:
    errors = {"parse_status": []}

    if "status" not in item:
        errors["parse_status"].append(f"attribute 'status' doesn't exist in {item}")
        return (None, errors)

    status = item.get("status").split("#")[1]
    return (status, errors)


def parse_format(item: dict) -> Union[tuple, None]:
    errors = {"parse_format": []}

    if "format" not in item:
        errors["parse_format"].append(f"attribute 'format' doesn't exist in {item}")
        return (None, errors)

    format_issn = item.get("format")

    if type(format_issn) == list:
        formats = []
        for value in format_issn:
            format = value.split("#")[1]
            formats.append(format)
        return (formats, errors)
    else:
        format = item.get("format").split("#")[1]
        return (format, errors)


def parse_key_title(item: dict) -> Union[dict, tuple]:
    errors = {"parse_key_title": []}
    data = parse_item(item)

    if "value" not in item:
        errors["parse_key_title"].append(f"attribute 'value' doesn't exist, {item}")

    return (data, errors)


def parse_issn(issn: str, item: dict) -> Union[dict, tuple]:
    errors = {"parse_issn": []}

    parsed_issn = item.get("value")
    data = parse_item(item)

    if item.get("@type") != "http://id.loc.gov/ontologies/bibframe/Issn":
        errors["parse_issn"].append(
            f"attribute '@type' != 'http://id.loc.gov/ontologies/bibframe/Issn', {item}"
        )

    if issn != parsed_issn:
        errors["parse_issn"].append(f"ISSN is not valid! {parsed_issn}")
        raise ValueError
    return (data, errors)


def parse_issnL(item: dict) -> Union[dict, tuple]:
    errors = {"parse_issnL": []}
    data = parse_item(item)

    if item.get("@type") != "http://id.loc.gov/ontologies/bibframe/IssnL":
        errors["parse_issnL"].append(
            f"attribute '@type' != 'http://id.loc.gov/ontologies/bibframe/IssnL', {item}"
        )
    return (data, errors)


def parse_record(item: dict) -> Union[dict, tuple]:
    errors = {"parse_record": []}
    data = parse_item(item)
    record = {}

    if item.get("@type") != "http://schema.org/CreativeWork":
        errors["parse_record"].append(
            f"attribute '@type' != 'http://schema.org/CreativeWork', {item}"
        )

    if "modified" not in item:
        errors["parse_record"].append(f"attribute 'modified' doesnt exist in {item}")

    for key in parse_item(item):
        if (key != "status") and (key != "modified"):
            del data[key]

    if len(data) == 1:
        return (data, errors)
    else:
        record["Record"] = data
        return (record, errors)


def parse_item(item: dict) -> Union[dict, str]:
    data = {key: item[key] for key in item if "@" not in key}

    if len(data) > 1:
        for key in data:
            if key == "status":
                data[key] = parse_status(item)[0]
        return data
    else:
        for key in data:
            if key == "status":
                data[key] = parse_status(item)[0]
                return data[key]
            else:
                return data[key]


def get_list_messages(error):
    for key in error:
        if error[key]:
            return error
    return {}


