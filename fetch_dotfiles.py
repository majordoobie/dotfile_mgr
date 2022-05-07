import argparse
def main():
    args = _get_args()


def _get_args() -> argparse.Namespace:
    """
    Sets up the arguments to run the bot.
    Returns
    -------
    parser: argparser.ArgumentParser
        Parser object
    """
    parser = argparse.ArgumentParser(
            description="Tool fetches all the configuration files specified "
                        "in the json file. The desination can be left "
            )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--live', help='Run bot with Panther shell', action='store_true', dest='live_mode',
                       default=False)
    group.add_argument('--dev', help='Run in dev shell', action='store_true', dest='dev_mode', default=False)
    return parser


if __name__ == "__main__":
    main()
