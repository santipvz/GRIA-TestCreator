from UTILS import exam
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate exams")
    parser.add_argument("--folder", required=True, help="Folder name")
    parser.add_argument("--numExams", type=int, default=1, help="Number of exams")
    parser.add_argument(
        "--numOfQuestions", type=int, default=30, help="Number of questions per exam"
    )
    args = parser.parse_args()

    exam.examGenerator(args.folder, args.numExams, args.numOfQuestions)
