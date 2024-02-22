# Released under GPLv3+ License
# Danial Behzadi<dani.behzi@ubuntu.com>, 2020-2024.

"""
main front file for tractor
"""

import fire

from . import actions
from . import bridges
from . import checks
from . import proxy


def main() -> None:
    """
    use fire to manage cli
    """
    fire.Fire(
        {
            "start": actions.start,
            "stop": actions.stop,
            "newid": actions.new_id,
            "restart": actions.restart,
            "set": proxy.proxy_set,
            "unset": proxy.proxy_unset,
            "isset": checks.proxy_set,
            "isrunning": checks.running,
            "isconnected": checks.connected,
            "bridgesfile": bridges.get_file,
            "killtor": actions.kill_tor,
        }
    )


if __name__ == "__main__":
    main()
