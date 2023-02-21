DOWNLOAD_URL="https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z"
FILE_NAME="ffmpeg.gz"
FOLDER_NAME="ffmpeg/bin"

extract_ffmpeg () {
  echo "Attempting to extract ffmpeg"
  dir_name="$(pwd)/$FOLDER_NAME"

  if [ -d $FOLDER_NAME ]
  then 
    rm -rf $FOLDER_NAME
  fi

  mkdir -p $FOLDER_NAME
  res=$(7z e $FILE_NAME -o"$dir_name" *.exe -r)
  
  if [ $? -eq 0 ]
  then
    echo "Successfully extracted ffmpeg"
    rm $FILE_NAME
  else
    echo "Error while extracting ffmpeg"
    rm $FILE_NAME
    exit 1
  fi
}


download_ffmpeg() {
    echo "Attempting to download ffmpeg"
    res=$(curl -s -w "%{response_code}" $DOWNLOAD_URL -o $FILE_NAME -L)

    if [ $res -eq 200 ] 
    then
        echo "Successfully downloaded ffmpeg"
    else
        echo "Error: couldn't download ffmpeg"
        exit 1
    fi
}

install_and_run() {
  var=$(pip install -r video_compressor/requirements.txt -q)

}

download_ffmpeg
extract_ffmpeg

exit 0