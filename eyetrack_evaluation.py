"""
计算准确度和精确度
"""

import json
import numpy as np
import os
import csv

folder_path = "/home/wangweida/Documents/test_result"
file_path = "D:/Log/Eye/02_01_18_56_B.txt"

mapper = {
    0: "0-1",
    1: "26-30",
    2: "26-30",
    3: "26-30",
    4: "26-30",
    5: "21-25",
    6: "21-25",
    7: "21-25",
    8: "11-20",
    9: "11-20",
    10: "21-25",
    11: "11-20",
    12: "11-20",
    13: "2-10",
    14: "2-10",
}


def eucl_dist(pt1, pt2):
    return np.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)


def radian_to_degree(radian):
    return radian * 180 / np.pi


def evaluate_file(file_path):
    # load json file
    with open(file_path, "r") as f:
        print(f"processing file: {file_path}")
        data = json.load(f)
        # parse data structure
        ipd = data["ipd"]
        userName = data.get("userName", "unknown")
        points = data["points"]
        result = []
        result2 = {}
        count = {}
        for one_set in points:  # one test image
            testName = one_set["testName"]
            target_idx = one_set["index"]
            target_point = one_set["gazePoint"]
            target_point_x = one_set["gazePoint"]["x"]
            target_point_y = one_set["gazePoint"]["y"]
            target_point_z = one_set["gazePoint"]["z"]
            assert target_point_z != 0, "target point z should not be zero"
            target_vector = np.array([target_point_x, target_point_y, target_point_z])
            predict_points = one_set["eyePos"]
            pt_list = []
            for one_point in predict_points:
                valid = one_point["valid"]
                timestamp = one_point["timestamp"]
                if valid:
                    predict_point_x = one_point["eyePoint"]["x"]
                    predict_point_y = one_point["eyePoint"]["y"]
                    predict_point_z = one_point["eyePoint"]["z"]
                    pt_list.append([predict_point_x, predict_point_y, predict_point_z])
            pt_np = np.array(pt_list)

            # center crop n elements
            length = len(pt_np)
            pt_np = pt_np[length // 2 - 50 : length // 2 + 50]
            # calculate the angle between target_vector and vector in each row of pt_np
            angle_list = []
            for vector in pt_np:
                # angle = np.arccos(np.dot(vector, target_vector) / (np.linalg.norm(vector) * np.linalg.norm(target_vector)))
                dist = eucl_dist(vector, target_vector)
                angle = np.arctan(dist / vector[2])
                angle_list.append(angle)

            angle_np = np.array(angle_list)
            angle_mean = np.mean(angle_np)
            angle_std = np.std(angle_np)
            accuracy = radian_to_degree(angle_mean)
            precision = radian_to_degree(angle_std)
            # print("userName:{}, testImageName:{}, target_point_idx: {}, target_point_pos: {}, accuracy: {}, precision: {}".format(
            #     userName, testName, target_idx, target_point, accuracy, precision))
            result.append(
                [userName, testName, target_idx, target_point, accuracy, precision]
            )
            if mapper[target_idx] not in result2:
                result2[mapper[target_idx]] = np.array([accuracy, precision])
                count[mapper[target_idx]] = 1
            else:
                result2[mapper[target_idx]] += np.array([accuracy, precision])
                count[mapper[target_idx]] += 1

        # save result to csv
        save_path = file_path[:-4] + ".csv"
        with open(save_path, "w", newline="") as f:
            writer = csv.writer(f)
            # write header
            writer.writerow(
                [
                    "userName",
                    "testImageName",
                    "target_point_idx",
                    "target_point_pos",
                    "accuracy",
                    "precision",
                ]
            )
            for data in result:
                writer.writerow(data)

            # add a blank line
            writer.writerow([])

            # write result2
            writer.writerow(["angle range", "accuracy", "precision"])
            for key in sorted(result2.keys(), key=lambda key: int(key.split("-")[0])):
                result2[key] /= count[key]
                writer.writerow([key, result2[key][0], result2[key][1]])
            f.close()
            print("save file: {}".format(save_path))
        # print(f"==>> result2: {result2}")
        # print(f"==>> count: {count}")
        return result2


def evaluate_folder(folder_path):
    save_path = os.path.join(folder_path, "total_result.csv")
    with open(save_path, "w", newline="") as f:
        writer = csv.writer(f)
        total_result = {}
        total_count = {}
        for file in os.listdir(folder_path):
            if file.endswith(".txt"):
                file_path = os.path.join(folder_path, file)
                result = evaluate_file(file_path)
                for key in result:
                    if key not in total_result:
                        total_result[key] = result[key]
                        total_count[key] = 1
                    else:
                        total_result[key] += result[key]
                        total_count[key] += 1

        writer.writerow(["angle range", "accuracy", "precision"])
        for key in sorted(total_result.keys(), key=lambda key: int(key.split("-")[0])):
            total_result[key] /= total_count[key]
            writer.writerow([key, total_result[key][0], total_result[key][1]])


if __name__ == "__main__":
    evaluate_file(file_path)
    # evaluate_folder(folder_path)
