from libs.logging import turn_on_debug, print_log
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

        total_keys += book['statistic'].get('total_keys', 0)
        num_success_keys += book['statistic'].get('success_keys', 0)
        num_unsuccess_keys += book['statistic'].get('unsuccess_keys', 0)
        num_unparsed_keys += book['statistic'].get('unparsed_keys', 0)

        for key in book['unsuccessful']:
            unsuccess_keys.append(key)

        for key in book['unparsed_b']:
            unsuccess_b_keys.append(key)

        for key in book['unparsed_keys']:
            unparsed_keys[key] = 1 if (key not in unparsed_keys) \
                                    else (unparsed_keys[key] + 1)

        # if total_issns >= 100:
        #     break

    print_log(f"=== Total of ISSN: {total_issns} ===")
    print_log(f"=== Total of keys: {total_keys} ===")
    print_log(f"=== Successful processed keys: {num_success_keys} ===")
    print_log(f"=== Unsuccessful processed keys: {num_unsuccess_keys} ===")
    print_log(f"=== Unparsed keys: {num_unparsed_keys} ===")
    print_log("====================")

    print_log(f"=== List of Unparsed keys: {sum(unparsed_keys.values())} ===")
    for key, value in unparsed_keys.items():
        print_log(f"=== key: {key} | value: {value} ===")

    print_log("====================")

    print_log(f"=== List of Unparsed keys 'b': {len(unsuccess_b_keys)} ===")
    # for key in unsuccess_b_keys:
    #     print_log(f"=== key: {key} ===")

    print_log("====================")

    print_log(f"=== List of Unsuccessful parsed keys {len(unsuccess_keys)} ===")
    # for key in unsuccess_keys:
    #     print_log(f"=== key: {key} ===")

    print_log("====================")


if __name__ == '__main__':
    turn_on_debug(True)
    process_data_by_issn()

