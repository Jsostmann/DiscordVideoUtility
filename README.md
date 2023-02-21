<p align="center">
  <a href="https://docsify.js.org">
    <img width="250px" height="250px" alt="docsify" src="./logo.png">
  </a>
</p>
<h1 align="center">DiscordVideoUtility</h1>

<p align="center">Utility to compress NvidiaGameHighlight videos with the option to upload videos to discord channel via webhook</p>

## Installation

Install using the `install.sh` script

```shell
sh install.sh
```
or 
```shell
chmod +x install.sh
./install.sh
```


## Usage: `python main.py {cli,env}`

### `cli` command

Use `cli` to operate in cli mode

```shell
python main.py cli --webhook_url WEBHOOK_URL [--input_dir INPUT_DIR] [--output_dir OUTPUT_DIR] [--interval INTERVAL] [--delete_flag DELETE_FLAG]
```

- `--webhook_url` option:
  - Shorthand: `-w`
  - Type: `String`
  - Required: `True`
  - Description: The URL of your discord channel.
- `--input_dir` option:
  - Shorthand: `-i`
  - Type: `String`
  - Default: `~\Users\<USER_NAME>\Videos\NvidiaHighlights\`
  - Required: `False`
  - Description: Input Directory for videos to be compressed.
- `--output_dir` option:
  - Shorthand: `-o`
  - Type: `String`
  - Default: `~\Users\<USER_NAME>\Videos\Compressed\`
  - Required: `False`
  - Description: Output Directory where compressed videos will be placed.
- `--interval` option:
  - Shorthand: `-in`
  - Type: `int`
  - Default: `3`
  - Required: `False`
  - Description: Time Interval which vidoes will be compressed on.
- `--delete_flag` option:
  - Shorthand: `-d`
  - Type: `boolean`
  - Default: `False`
  - Required: `False`
  - Description: Flag that indicates whether or not to delete files in `input_dir` after compressing.
### `env` command

Use `env` to operate in env mode.

```shell
python main.py env
```

Same as `cli` mode, but the options will be pulled from a `.env` file.

*must have `.env` file present*


Example `.env file`
```env
WEBHOOK_URL=https://discord.com/api/webhooks/dummy_webhook
INTERVAL=5
INPUT_DIRECTORY=C:\Users\Test User\Videos\NvidiaHighlights
OUTPUT_DIRECTORY=C:\Users\Test User\Videos\Compressed
DELETE_FLAG=True
```

- `WEBHOOK_URL` option:
  - Type: `String`
  - Required: `True`
  - Description: The URL of your discord channel.
- `INPUT_DIRECTORY` option:
  - Type: `String`
  - Default: `~\Users\<USER_NAME>\Videos\NvidiaHighlights\`
  - Required: `False`
  - Description: Input Directory for videos to be compressed.
- `OUTPUT_DIRECTORY` option:
  - Type: `String`
  - Default: `~\Users\<USER_NAME>\Videos\Compressed\`
  - Required: `False`
  - Description: Output Directory where compressed videos will be placed.
- `INTERVAL` option:
  - Type: `int`
  - Default: `3`
  - Required: `False`
  - Description: Time Interval which vidoes will be compressed on.
- `DELETE_FLAG` option:
  - Type: `boolean`
  - Default: `False`
  - Required: `False`
  - Description: Flag that indicates whether or not to delete files in `input_dir` after compressing.

## License
[MIT](LICENSE)