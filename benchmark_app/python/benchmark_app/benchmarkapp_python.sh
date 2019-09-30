set -x
INPUT_FILE=$1
FP_MODEL=$2
DEVICE=$3
API=$4

cd $PBS_O_WORKDIR
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:~/benchmark_app/python/benchmark_app

if [ "$FP_MODEL" == "FP16" ]; then
  FPEXT='-fp16'
fi

echo $INPUT_FILE

! python3 benchmark_app.py \
-m ~/benchmark_app/models/Retail/object_attributes/emotions_recognition/0003/dldt/emotions-recognition-retail-0003${FPEXT}.xml \
-i $INPUT_FILE \
-d $DEVICE \
-api $API
#./benchmark_app \
#-m ~/benchmark_app/models/Retail/object_attributes/emotions_recognition/0003/dldt/emotions-recognition-retail-0003${FPEXT}.xml \
#-i $INPUT_FILE \
#-d $DEVICE \
#-api $API
