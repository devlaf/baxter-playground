import sys
import baxter_libs
import baxter_libs.robot_utils
import functional_tests.head
import functional_tests.arms
import functional_tests.grippers
import functional_tests.sonars
from baxter_libs.baxter import Baxter

def main():
    baxter_libs.robot_utils.startup()
    
    #functional_tests.head.test_head_utils()
    functional_tests.sonars.test_sonars()
    
    baxter_libs.robot_utils.shutdown()
    return 0

if __name__ == '__main__':
    sys.exit(main())

