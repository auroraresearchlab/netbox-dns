from netaddr import IPNetwork, AddrFormatError
from dns import name as dns_name


def arpa_to_prefix(arpa_name):
    name = arpa_name.rstrip(".")

    if name.endswith(".in-addr.arpa"):
        address = ".".join(reversed(name.replace(".in-addr.arpa", "").split(".")))
        mask = len(address.split(".")) * 8

        try:
            return IPNetwork(f"{address}/{mask}")
        except AddrFormatError:
            return None

    elif name.endswith("ip6.arpa"):
        address = "".join(reversed(name.replace(".ip6.arpa", "").split(".")))
        mask = len(address)
        address = address + "0" * (32 - mask)

        try:
            return IPNetwork(
                f"{':'.join([(address[i:i+4]) for i in range(0, 32, 4)])}/{mask*4}"
            )
        except AddrFormatError:
            return None

    else:
        return None


def name_to_unicode(name):
    try:
        return dns_name.from_text(name, origin=None).to_unicode()
    except dns_name.IDNAException:
        return name
