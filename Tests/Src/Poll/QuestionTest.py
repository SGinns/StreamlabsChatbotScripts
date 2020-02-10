import unittest
import sys
import os
import Question

class QuestionTest(unittest.TestCase):

    def ReadQuestionReadsExistingFilesWithOneWordNames(self):
        import Question
        testFile = open("test.txt","w+")
        fileData = ["A cool question right?", "yes, YES BUT IN CAPS"]
        testFile.writelines(fileData)

        self.assertEqual(Question.ReadQuestion("test", 30), ["A cool question right?", ["yes", "YES BUT IN CAPS"]])

