
INPUT_FILE=$1
OUTPUT_FILE=$2
FP_MODEL=$3
BACKEND=$4
#0: CPU target (by default), 1: OpenCL, 2: OpenCL fp16 (half-float precision), 3: VPU,5: HETERO:FPGA,CPU
TARGET=$5


if [ "$TARGET" == "5" ]; then
    # Environment variables and compilation for edge compute nodes with FPGAs
    source /opt/fpga_support_files/setup_env.sh
    aocl program acl0 /opt/intel/openvino/bitstreams/a10_vision_design_bitstreams/2019R1_PL1_FP11_MobileNet_Clamp.aocx
fi

cd $PBS_O_WORKDIR
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/

 
if [ "$FP_MODEL" == "FP16" ]; then
  FPEXT='-fp16'
fi

    
./monitor \
-m=models/Transportation/object_detection/face/pruned_mobilenet_reduced_ssd_shared_weights/dldt/face-detection-adas-0001${FPEXT}.bin \
-c=models/Transportation/object_detection/face/pruned_mobilenet_reduced_ssd_shared_weights/dldt/face-detection-adas-0001${FPEXT}.xml \
-sm=models/Retail/object_attributes/emotions_recognition/0003/dldt/emotions-recognition-retail-0003${FPEXT}.bin \
-sc=models/Retail/object_attributes/emotions_recognition/0003/dldt/emotions-recognition-retail-0003${FPEXT}.xml \
-i=$INPUT_FILE \
-o=$OUTPUT_FILE \
-b=$BACKENED \
-t=$TARGET
