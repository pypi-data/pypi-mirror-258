from src.commands.base import CurlsCommand
from src.commands.result import command_result
from src.data.queries import api as aq


class APIAddCommand(CurlsCommand):

    @classmethod
    def run(cls, args):
        curl_id = args[2] if len(args) < 4 else args[3]
        curr_api = aq.get_current()
        added = aq.add_to_api(curr_api, curl_id)
        if not added:
            return command_result(False, output=f"curl not found: '{curl_id}'.")
        return command_result(True, None, None)
