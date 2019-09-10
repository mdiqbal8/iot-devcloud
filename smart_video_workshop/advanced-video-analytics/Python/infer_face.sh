cd $PBS_O_WORKDIR
mkdir -p $1
python3 interactive_face_detection.py   -m models/Transportation/object_detection/face/pruned_mobilenet_reduced_ssd_shared_weights/dldt/face-detection-adas-0001-fp16.xml \
                            -i $2 \
                            -o $1 \
                            -d MYRIAD \
                            -l ~/inference_engine_samples_build/intel64/Release/lib/libcpu_extension.so 
