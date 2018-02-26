import pymysql

conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="root", db="test", charset="utf8")
cur = conn.cursor()

# 新建el处理流程表
createtable = "CREATE TABLE ELimgtest(id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,original_el_path  VARCHAR (255),constract_el_path VARCHAR (255),rectangle_el_path VARCHAR (255),dytzqt_el_path VARCHAR (255),tzqt_el_path VARCHAR (255),dytz_el_path VARCHAR (255))AUTO_INCREMENT = 0"
cur.execute(createtable)
