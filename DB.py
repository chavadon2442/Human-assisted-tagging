from PyQt5.QtSql import QSqlDatabase, QSqlQuery,QSqlTableModel
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import os
import sys

class AppDB(QWidget):
    def __init__(self, parent=None):
        super(AppDB, self).__init__(parent)
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("./database/local.db")
        self.db.open()
        self.createDB()  

    def createDB(self):
        query = QSqlQuery() 
        query.exec("CREATE TABLE DETAILS (Tag_No INTEGER PRIMARY KEY, Description TEXT)")
        query.exec("CREATE TABLE Image( Image_Name TEXT NOT NULL, Tag_No INT NOT NULL, PRIMARY KEY(Image_Name,Tag_No), FOREIGN KEY(Tag_No) REFERENCES DETAILS(Tag_No))")

        query.exec("INSERT into DETAILS values(2,'dry_neck_label')")
        query.exec("INSERT into DETAILS values(3,'pale_neck_label_but_not_dry')")
        query.exec("INSERT into DETAILS values(4,'label_has_scratch_but_not_dry')")
        query.exec("INSERT into DETAILS values(5,'dirty_wuth_white_fungus_inside')")
        query.exec("INSERT into DETAILS values(6,'dirty_with_black_fungus_inside')")
        query.exec("INSERT into DETAILS values(7,'shallow_scratches_on_shoulder')")
        query.exec("INSERT into DETAILS values(8,'perfect_bottles')")

        query.exec("INSERT into DETAILS values(9,'no_label')")
        query.exec("INSERT into DETAILS values(10,'dry_label')")
        query.exec("INSERT into DETAILS values(11,'straw')")
        query.exec("INSERT into DETAILS values(12,'cigarettes')")
        query.exec("INSERT into DETAILS values(13,'bottle_caps')")
        query.exec("INSERT into DETAILS values(14,'transparent_plastic_bags')")
        query.exec("INSERT into DETAILS values(15,'tissue_paper')")
        query.exec("INSERT into DETAILS values(16,'toothpick')")
        query.exec("INSERT into DETAILS values(17,'wire')")
        query.exec("INSERT into DETAILS values(18,'other_kind_of_trash')")
        query.exec("INSERT into DETAILS values(19,'medical_zip_lock_bag')")
        query.exec("INSERT into DETAILS values(20,'paper')")
        query.exec("INSERT into DETAILS values(21,'opaque_plastic_bag')")
        query.exec("INSERT into DETAILS values(22,'cap_liner')")
        query.exec("INSERT into DETAILS values(23,'cotton_bud')")
        query.exec("INSERT into DETAILS values(24,'sticks')")
        query.exec("INSERT into DETAILS values(25,'dirty_with_soil_outside')")
        query.exec("INSERT into DETAILS values(26,'dirty_with_soil_inside')")
        query.exec("INSERT into DETAILS values(27,'water_in_bottle')")
        query.exec("INSERT into DETAILS values(28,'dirty_outside')")
        query.exec("INSERT into DETAILS values(29,'closed_cap_bottles')")

        query.exec("INSERT into DETAILS values(30,'broken_side')")
        query.exec("INSERT into DETAILS values(31,'broken_under')")
        query.exec("INSERT into DETAILS values(32,'broken_inside')")
        query.exec("INSERT into DETAILS values(33,'broken_top')")
        query.exec("INSERT into DETAILS values(34,'chipped_finsidh_from_beer_factory')")
        query.exec("INSERT into DETAILS values(35,'shark_mouth')")
        query.exec("INSERT into DETAILS values(36,'scuff')")
        query.exec("INSERT into DETAILS values(37,'deep_scratch')")
        query.exec("INSERT into DETAILS values(38,'rainbow')")
        query.exec("INSERT into DETAILS values(39,'sprayed_or_painted')")
        query.exec("INSERT into DETAILS values(40,'termites')")
        query.exec("INSERT into DETAILS values(41,'wrong_label')")

        ## GET directory from the application 
        # dir = "Bottom_ViewImages"
        # for folder in os.listdir(dir):
        #     description = folder
        #     query.exec("SELECT Tag_No FROM DETAILS WHERE Description = '{}' ".format(description))
        
        #     while query.next():

        #         result = query.value(0).__str__()
        #         print(result)
        #         getdir = dir + '/' + folder 
        #         for files in os.listdir(getdir):
        #            query.exec("INSERT into Image values('{}','{}')".format(files,result))

        ## BASIC GET IMAGE WITH TAGS SEARCH QUERY

        # searchlist = []
        # search_input = input('Do you want to search certain tags for images, Y/N ?')
        # if search_input.lower() == 'y' or search_input.lower() == 'yes':
            
        #     queryy = int(input('Please enter your tag :  '))
        #     query.exec("SELECT Image_name FROM IMAGE where Tag_no == '{}'".format(queryy))
            
        #     while query.next():
        #         result = query.value(0)
        #         searchlist.append(result)
    def query_alltag(self):
        query = QSqlQuery() 
        query.exec("SELECT Tag_No, Description FROM DETAILS")
        query_alltags = []
        while query.next():
            result = query.value(1)
            query_alltags.append(result)
        return query_alltags

    def tag_image(self, img_name, tags):
        query = QSqlQuery() 
        if len(tags) == 1:
            query.exec("SELECT Tag_No FROM DETAILS WHERE Description = '{}' ".format(tags[0]))
            while query.next():
                result = query.value(0).__str__()
            query.exec("INSERT into Image values ('{}','{}')".format(img_name,result))
        if len(tags) > 1:
            for mtags in tags:
                query.exec("SELECT Tag_No FROM DETAILS WHERE Description = '{}' ".format(mtags))
                while query.next():
                    result = query.value(0)
                query.exec("INSERT into Image values ('{}','{}')".format(img_name,result))

        
        
       

            
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())