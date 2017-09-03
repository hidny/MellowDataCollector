import cx_Freeze


cx_Freeze.setup(
	name="Mellow_Data_Collector",
	version = "2.7",
	options={"build_exe": {"packages":["pygame"],
				"include_files":["Image/",
				"MellowLogo.png", "versNumber.png"]}},
	description = "Program for manually gathering data about how to do the first position mellow bid",
	executables = [cx_Freeze.Executable("mellowGUI.py", base ="Win32GUI")]
	)

#python setup.py build

#Bug fix: had to take away all prints in serverListener functions to make it work.
# I don't know why that was a problem
#https://stackoverflow.com/questions/3029816/how-do-i-get-a-thread-safe-print-in-python-2-6

#If it doesn't work, you might have to restart and try again according to youtuber.
#This didn't happen to me yet.

#NOTE:
#You could delete scipy to make more room
#You could delete numpy to make more room