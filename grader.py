

## Imports
import numpy
import os

class Profile:
    def __init__(self, user):
        self.user_id = user
        self.user_filename = self.find_file_for(user)
        ## Dict of form {course name: syllabus filename}
        self.current_courses = {}
        ## Dict of form {course name: syllabus filename} TODO
        #self.past_courses = {}

    ## Finds a file based on user name
    def find_file_for(a_user):
        

######
##  ##
######
class Course:
    ## Initilizes a course based off passed file
    def __init__(self, filename):
        ## Filename of relevent syllabus, just '.txt' for now
        self.syllabus = filename
        self.course_name = ""
        ## List of categories
        self.categories = []
        ## Dict of form {category:weight}
        self.weights = {}
        ## Dict of form {category: {assignment name:grade}}
        self.assignment_grades = {}
        ## Dict of form {category: avg grade}
        self.averages = {}
        self.populate_from_syllabus()

    ## Use passed file to populate all fields of a course
    def populate_from_syllabus(self):
        infile = open(self.syllabus, "r")
        for line in infile:
            if line[0] == "-":
                self.course_name = line[1:].rstrip("\n")
                continue
            category, weight = line.rstrip("\n").split(":")
            self.categories.append(category)
            self.weights[category] = float(weight)
            self.assignment_grades[category] = {}
            self.averages[category] = 0
        infile.close()

    ##
    def populate_user_data(self, filename):
        if os.stat(filename).st_size == 0:
            print "-----------------------"
            print "--No user data exists--"
            print "-----------------------"
        else:
            infile = open(filename, "r")
            current_catagory = ""
            for line in infile:
                line = line.rstrip("\n")
                if line in self.categories:
                    current_catagory = line
                    continue
                assignment, grade = line.split(":")
                self.assignment_grades[current_catagory][assignment] = float(grade)
            infile.close()

    ##
    def update_avg(self):
        for key in self.assignment_grades.keys():
            temp_sum = 0
            if (len(self.assignment_grades[key]) != 0):
                for name in self.assignment_grades[key].keys():
                    temp_sum += self.assignment_grades[key][name]
                temp_sum = temp_sum/len(self.assignment_grades[key])
                self.averages[key] = temp_sum
    ##
    def find_current_grade(self):
        self.update_avg()
        final_grade = 0
        used_weights = 0
        for category in self.categories:
            ## Don't include an empty category
            if (len(self.assignment_grades[category]) != 0):
                used_weights += self.weights[category]
                final_grade += self.averages[category] * self.weights[category]
        final_grade = (final_grade / used_weights)*100
        return final_grade

    ##
    def find_max_grade(self):
        return -1.0

    ##
    def find_min_grade(self):
        return -1.0

    ##
    def print_course(self):
        print "Syllabus file: {}".format(self.syllabus)
        print "Course name: {}".format(self.course_name)
        print "---------------------"
        print "Category's w/ weights"
        for key in self.weights.keys():
            print "{} : {:3.2f}".format(key, self.weights[key])
        print "------------------------"
        self.update_avg()
        print "Category score averages:"
        for key in self.averages.keys():
            print "{} : {:3.2f}".format(key, self.averages[key])
        print "-----------------------------"
        print "Stored assignments w/ grades:"
        for key in self.assignment_grades.keys():
            for name in self.assignment_grades[key].keys():
                print "{} : {:3.2f}".format(name, self.assignment_grades[key][name])
        print "-------------"
        print "Current grade: {:3.2f}".format(self.find_current_grade())
        print "Maximum possible grade: {:3.2f}".format(self.find_max_grade())
        print "Minimum possible grade: {:3.2f}".format(self.find_min_grade())

##
def add_grades(some_course, datafilename):
    output = open(datafilename, "a")
    for category in some_course.categories:
        choice = raw_input("Do you have any {} grades to add? ".format(category))
        while choice != "no":
            choice = raw_input("Do you have more {} grades to add? ".format(category))
            if (choice.lower() == "yes"):
                assign_name = raw_input("What is the name of the assignment? ")
                score = raw_input("What did you get on it?(Proper format: 95/100 ==> .95) ")
                output.write("{}\n".format(category))
                output.write("{}:{:1.2f}\n".format(assign_name, float(score)))
            elif(choice.lower() == "no"):
                continue
    some_course.populate_user_data(datafilename)
    output.close()

def main():
    file_name = raw_input("Select syllabus file to load: ")
    test_course = Course(file_name)
    file_name = raw_input("Select data file to load: ")
    test_course.populate_user_data(file_name)
    choice = raw_input("Do you need to add any grades? ")
    if (choice.lower() == "yes"):
        add_grades(test_course, file_name)
    test_course.print_course()

if __name__ == '__main__':
    main()
