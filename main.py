from front_end import MyApp
from obd_data import Data
import obd
import os

p = Data()
p.connect()
# os.system("sleep 10")

p.main()
MyApp(p).build()

if __name__ == '__main__':
    MyApp(p).run()