#include <string>
#include <iostream>
#include <sstream>
#include <fstream>
#include <time.h>
#include <omp.h>
#include <stdlib.h>
#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/imgproc_c.h>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/video/video.hpp>
#include <vector>
#include <algorithm>
#include <assert.h>

using namespace std;
using namespace cv;

void placeBoxes(Mat &frame, vector<string> obj, bool is_async_mode = true)
{
	string id = obj[0];			  // frame id
	int xmin = std::stoi(obj[1]); // xmin
	int ymin = std::stoi(obj[2]); // ymin
	int xmax = std::stoi(obj[3]); // xmax
	int ymax = std::stoi(obj[4]); // ymax
	string det_label = obj[5];	//label
	string render_time = obj[6];  // probability
	string det_time = obj[7];	 //inference engine detection time
	Scalar color(255, 255, 255);
	Scalar color1(0, 0, 255);
	String warning = "HUMAN IN ASSEMBLY AREA: PAUSE THE MACHINE!";
	String inf_time_message, render_time_message, det_label_message;
	inf_time_message = "Inference time:" + det_time + " ms";
	render_time_message = "OpenCV rendering time:" + render_time + "ms";
	det_label_message = "Worker Safe :" + det_label;
	if (det_label == "False")
	{
		putText(frame, warning, Point(20, 80), CV_FONT_HERSHEY_COMPLEX, 0.8, color1, 2);
	}

	rectangle(frame, Point(xmin, ymin), Point(xmax, ymax), color1, 2);
	putText(frame, det_label_message, Point(20, 35), CV_FONT_HERSHEY_COMPLEX, 0.6, color, 1);
	putText(frame, inf_time_message, Point(20, 15), CV_FONT_HERSHEY_COMPLEX, 0.6, color, 1);
	return;
}

int main(int argc, char **argv)

{
	assert(argc >= 3);
	double t = omp_get_wtime();
	string job_id = getenv("PBS_JOBID");
	string input_stream = argv[1];
	string input_data = string(argv[2]) + "/output_" + job_id + ".txt";
	string progress_data = string(argv[2]) + "/v_progress_" + job_id + ".txt";
	string output_result = string(argv[2]) + "/output_" + job_id + ".mp4";
	int skip_frame = stoi(argv[3]);
	float resl = stof(argv[4]);

	//Start VideoCapture
	Mat frame;
	VideoCapture cap(input_stream);
	if (!cap.isOpened())
	{
		cout << "Error opening video stream or file" << endl;
		return -1;
	}
	//Open the input data file and read the first line to str
	ifstream input(input_data);
	ofstream progress;
	string str;
	getline(input, str, input.widen('\n'));
	vector<string> object(8, "0");
	int width = 0;
	int height = 0;
	int length = 0;
	int id = 0;
	int seq_num = 0;
	int next_id = 0;
	//Open the output file to write processed video to it
	VideoWriter outVideo;
	if (cap.isOpened())
	{
		width = int(cap.get(CAP_PROP_FRAME_WIDTH));
		height = int(cap.get(CAP_PROP_FRAME_HEIGHT));
		length = int(cap.get(CAP_PROP_FRAME_COUNT));
		outVideo.open(output_result, 0x21, 50.0 / skip_frame, Size(width * resl, height * resl), true);
	}
	//Start while loop to process input stream and write the output frame to output_results
	while (cap.isOpened())
	{
		cap >> frame;
		if (frame.empty())
			break;
		while (!str.empty() && seq_num == id && id == next_id)
		{
			int len = 0;
			int j = 0;
			while (len < str.size())
			{
				object[j].clear();
				while (len < str.size() && str[len] != ' ' && str[len] != '\n')
				{
					object[j].push_back(str[len]);
					len++;
				}
				j++;
				len++;
			}
			next_id = std::stoi(object[0]);
			if (id == next_id)
			{
				placeBoxes(frame, object);
				getline(input, str, input.widen('\n'));
			}
			else
			{
				id = next_id;
				break;
			}
		}
		seq_num++;
		if (seq_num % 10 == 0)
		{
			double fps_t = omp_get_wtime() - t;
			progress.open(progress_data);
			string cur_progress = to_string(int(100 * seq_num / length)) + '\n';
			string remaining_time = to_string(int((fps_t / seq_num) * (length - seq_num))) + '\n';
			string estimated_time = to_string(int((fps_t / seq_num) * length)) + '\n';
			progress << cur_progress;
			progress << remaining_time;
			progress << estimated_time;
			progress.flush();
			progress.close();
		}
		if (id % skip_frame == 0)
		{
			resize(frame, frame, Size(width * resl, height * resl), 0, 0, CV_INTER_LINEAR);
			outVideo.write(frame);
		}
	}
	cap.release();
	destroyAllWindows();

	t = omp_get_wtime() - t;
	cout << "Video post-processing time: " << t << " seconds" << endl;
}