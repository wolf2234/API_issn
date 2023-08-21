from issn_api import get_by_issn, get_issns_from_file


def process_data_by_issn():
    total_issns = 0
    total_keys = 0

    unparsed_keys = {}
    unsuccess_b_keys = list()
    unsuccess_keys = list()

    num_success_keys = 0
    num_unsuccess_keys = 0
    num_unparsed_keys = 0

    for issn in get_issns_from_file():  # читае все иссн из файл
        total_issns += 1

        book = get_by_issn(issn)

        total_keys += book["statistic"].get("total_keys", 0)
        num_success_keys += book["statistic"].get("success_keys", 0)
        num_unsuccess_keys += book["statistic"].get("unsuccess_keys", 0)
        num_unparsed_keys += book["statistic"].get("unparsed_keys", 0)

        for key in book["unsuccessful"]:
            unsuccess_keys.append(key)

        for key in book["unparsed_b"]:
            unsuccess_b_keys.append(key)

        for key in book["unparsed_keys"]:
            unparsed_keys[key] = (
                1 if (key not in unparsed_keys) else (unparsed_keys[key] + 1)
            )

    data = {
            "total_issn": total_issns,
            "total_keys": total_keys,
            "successful_processed_keys": num_success_keys,
            "unsuccessful_processed_keys": num_unsuccess_keys,
            "unparsed_keys": num_unparsed_keys,
            "list_unparsed_keys": sum(unparsed_keys.values()),
            "list_unparsed_keys_b": len(unsuccess_b_keys),
            "list_unsuccessful_parsed_keys": len(unsuccess_keys),
            }

    return data


if __name__ == "__main__":
    process_data_by_issn()
