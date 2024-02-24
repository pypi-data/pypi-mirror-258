from GOESVisualizer import GSVis

GSobj = GSVis('west', 2021, 7, 20, 12, -125, -117, 35, 45, gamma = 2.5)
#
#GSobj = GSVis('east', 2021, 7, 26, 18, -110, -60, 30, 50, gamma = 3)
# only plot
GSobj.loop(21,4)
GSobj.savepics()
GSobj.animate()
# or only save
#GSobj.plotGS(True,'sample.png')
