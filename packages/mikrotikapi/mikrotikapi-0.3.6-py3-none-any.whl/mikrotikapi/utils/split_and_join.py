from pydantic import IPvAnyNetwork, IPvAnyAddress


def split_values(v) -> list:
    if isinstance(v, str):
        return v.split(",")
    else:
        return v


def join_values(v: list) -> str:
    return ",".join(v) if v else ""


def split_network_values(v) -> list:
    if isinstance(v, str):
        addresses = v.split(",")
        return [IPvAnyNetwork(address) for address in addresses]
    else:
        return v


def join_network_values(v) -> str:
    return ",".join(str(address) for address in v) if v else ""


def split_ip_values(v) -> list:
    if isinstance(v, str):
        addresses = v.split(",")
        return [IPvAnyAddress(address) for address in addresses]
    else:
        return v


def join_ip_values(v) -> str:
    return ",".join(str(address) for address in v) if v else ""


def split_ip_network_values(v) -> list:
    if isinstance(v, str):
        values = v.split(",")
        result = []
        for value in values:
            try:
                result.append(IPvAnyAddress(value))
            except ValueError:
                try:
                    result.append(IPvAnyNetwork(value))
                except ValueError:
                    pass
        return result
    else:
        return v


def join_ip_network_values(v: list) -> str:
    return ",".join(str(value) for value in v) if v else ""
