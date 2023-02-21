import argparse
from dotenv import dotenv_values
import os
import video_compessor

#global vars
REQUIRED_VARIABLES = ["WEBHOOK_URL", "INTERVAL", "INPUT_DIRECTORY", "OUTPUT_DIRECTORY", "DELETE_FLAG"]

DEFAULT_OUTPUT_DIRECTORY = os.path.join(os.path.expanduser('~'), "Videos", "Compressed")
DEFAULT_INPUT_DIRECTORY = os.path.join(os.path.expanduser('~'), "Videos", "NvidiaHighlights")

def run_cli(cli_args):
    print("Running in cli mode")

    payload = {"WEBHOOK_URL": cli_args.webhook_url,
               "INTERVAL": cli_args.interval,
               "INPUT_DIRECTORY": cli_args.input_dir,
               "OUTPUT_DIRECTORY": cli_args.output_dir,
               "DELETE_FLAG": cli_args.delete_flag
              }
    video_compessor.start(payload)

def run_env():
    print("Running in env mode")
    env_variables = dotenv_values()

    if not len(env_variables):
        print("Couldnt find .env file.. exiting")
        exit(1)
    
    for env in REQUIRED_VARIABLES:
        if env not in env_variables:
            print("Couldnt find {} variable.. exiting".format(env))
            exit(1)
    
    video_compessor.start(env_variables)

if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Mode to use', required=True, dest='mode')

    cli_parser = subparsers.add_parser("cli", help="Use cli mode")
    env_parser = subparsers.add_parser("env", help="Use env mode")

    cli_parser.add_argument('--webhook_url', type=str, required=True, help="The discord webhook url to post files to")
    cli_parser.add_argument('--input_dir', type=str, default=DEFAULT_INPUT_DIRECTORY, help="The directory where original videos reside")
    cli_parser.add_argument('--output_dir', type=str, default=DEFAULT_OUTPUT_DIRECTORY, help="The directory where compressed videos are stored")
    cli_parser.add_argument('--interval', type=int, default=5, help="The interval in which videos are compressed in (M)")
    cli_parser.add_argument('--delete_flag', type=bool, default=False, help="Delete original files after compressing?")

    args = parser.parse_args()
    
    if args.mode == "env":
        run_env()
    else:
        run_cli(args)


    